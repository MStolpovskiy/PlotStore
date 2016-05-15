from contextlib import contextmanager
import matplotlib.pyplot as mp
import cPickle as pkl
from copy import copy
from pdb import set_trace

class PlotStore(object):
    def __init__(self, name=None, options_or_parent_dir=None):
        '''
A directory with plot-objects or other directories.
        '''
        self.dict = {}
        if name is None:
            raise ValueError('None name')
        if options_or_parent_dir is None:
            raise ValueError('None options_or_parent_dir')

        if isinstance(options_or_parent_dir, str):
            self.path = 'Main'
            self.file = name
            self.options = options_or_parent_dir
        elif isinstance(options_or_parent_dir, PlotStore):
            self.parent_dir = options_or_parent_dir
            self._create_path(name)
            self.options = None
        else:
            raise ValueError('Wrong options')
            
        if self.options is not None and self.options not in 'raw':
            raise ValueError('Wrong options')
        if self.options is not None and self.options in 'ra':
            self.load()

    def _create_path(self, name):
        name = name.replace('/', '')
        self.path = self.parent_dir.path + '/' + name

    @property
    def pwd(self):
        return self.path

    def list(self):
        return self.dict.keys()
    
    @property
    def ls(self):
        self._ls(self.dict.keys())

    def _ls(self, keys, tab=''):
        keys.sort()
        for k in keys:
            if isinstance(self.dict[k], PlotStore):
                print tab + '\033[1m' + k
                self.dict[k]._ls(self.dict[k].list(),
                                 tab=tab+'    ')
            else:
                print tab + '\033[0m' + k

    def mkdir(self, name):
        d = PlotStore(name, self)
        self.dict[name] = d

    def cd(self, path):
        path = path.split('/')
        d = copy(self)
        for p in path:
            d = d._cd(p)
        return d
    
    def _cd(self, path):
        if path == '..':
            if self.parent_dir is None:
                raise ValueError('Cannot go up on the dir tree')
            return self.parent_dir
        else:
            return self.dict[path]
    
    def get_plot(self, name):
        if isinstance(self.dict[name], mp.Figure):
            return self.dict[name]
        return None
    
    def draw(self, name):
        temp_fig = mp.figure()
        m = mp.get_current_fig_manager()
        m.canvas.figure = self.get_plot(name)
        del temp_fig
        mp.show()

    def dump(self):
        if self.file != None:
            options = 'w' if self.options == None else self.options
            with open(self.file, options) as f:
                pkl.dump(self, f)

    def load(self):
        if self.file != None:
            options = 'r' if self.options == None else self.options
            with open(self.file, options) as f:
                ps = load(f)
            self.dict = ps.dict
        
    @contextmanager
    def new_plot(self, name):
        f = mp.figure()
        yield f
        self.dict[name] = f# mp.figure(mp.get_fignums()[-1])

