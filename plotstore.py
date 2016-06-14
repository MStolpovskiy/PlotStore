from contextlib import contextmanager
import matplotlib.pyplot as mp
import cPickle as pkl
from copy import copy
import os.path
from .plot import Plot
import re

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
        for p in path:
            self._cd(p)
    
    def _cd(self, path):
        if path == '~':
            if self.path == 'Main':
                return
            while self.parent_dir is not None:
                self._cd('..')
        elif path == '..':
            if self.parent_dir is None:
                raise ValueError('Cannot go up on the dir tree')
            self.path = '/'.join(self.path.split('/')[:-1])
            if 'parent_dir' in self.parent_dir.__dict__.keys():
                pd = self.parent_dir.parent_dir
            else:
                pd = None
            self.dict = self.parent_dir.dict
            self.parent_dir = pd
        else:
            if path in self.dict.keys() and \
               isinstance(self.dict[path], PlotStore):
                self.parent_dir = copy(self)
                self.path += '/' + path
                self.dict = self.dict[path].dict
            else:
                raise ValueError('Wrong path')
    
    def get_plot(self, name):
        if type(name) in [list, tuple]:
            return [self.get_plot(n) for n in name]
        if isinstance(self.dict[name], Plot):
            return self.dict[name]
        return None

    def list(self, name=None):
        if name is None:
            name = '.*'
        else:
            name = name.replace('*', '.*')
            name = name.replace('?', '.')
        return [n for n in self.dict.keys() \
                if isinstance(self.dict[n], Plot) and \
                   re.match(name, n)]
    
    def draw(self, name):
        p = self.get_plot(name)
        p.draw()

    def dump(self):
        if self.options == 'r':
            raise ValueError("Option 'r' is for read-only")
        path = self.pwd
        if path != 'Main':
            self.cd('~')
        if self.file != None:
            with open(self.file, 'w') as f:
                pkl.dump(self, f)
        if path != 'Main':
            path = '/'.join(path.split('/')[1:])
            self.cd(path)

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
        axes = []
        for ax in f.axes:
            axes.append(ax)
        self.dict[name] = Plot(name, axes)

    def mv(self, what, where):
        if isinstance(self.dict[where], PlotStore):
            keys = self.list(what)
            for k in keys:
                self.dict[where].dict[k] = self.dict[k]
                self.dict.pop(k)
