from contextlib import contextmanager
import matplotlib.pyplot as mp
import cPickle as pkl
from copy import copy
from formlayout import fedit
from pdb import set_trace
import os.path

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
            if self.options == 'a' and os.path.isfile(self.file) or \
               self.options == 'r':
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
                print tab + '\033[1m' + k + '\033[0m'
                self.dict[k]._ls(self.dict[k].list(),
                                 tab=tab+'    ')
            else:
                print tab + k

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
        fig = self.get_plot(name)
        m.canvas.figure = fig
        del temp_fig
        fig.show()

    def dump(self):
        if self.file != None:
            with open(self.file, 'w') as f:
                pkl.dump(self, f)

    def load(self):
        inter = mp.isinteractive()
        if inter: mp.ioff()
        fig_list = mp.get_fignums()
        if self.file != None:
            with open(self.file, 'r') as f:
                ps = pkl.load(f)
            self.dict = ps.dict
        for p in mp.get_fignums():
            if p not in fig_list:
                mp.close(p)
        if inter: mp.ion()
        
    @contextmanager
    def new_plot(self, name):
        f = mp.figure()
        yield f
        self.dict[name] = f# mp.figure(mp.get_fignums()[-1])

