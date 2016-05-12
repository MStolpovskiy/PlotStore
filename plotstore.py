from contextlib import contextmanager
from pdb import set_trace
import cPickle as pkl
from inspect import (currentframe, getlineno, findsource, getargs)
from pdb import set_trace

class PlotStore(object):
    def __init__(self, file_name, mode):
        '''
        Handles Pickle files with instructions to plot figures.
        -----------------------
        file_name - str,
            Stores name of the Pickle file where the plots
            will be written (or from where they will be read).
        mode - str
            if mode == 'r', read the file. 
            mode == 'w'Otherwise it would
            rewrite existing file.
        -----------------------
        Example:
        
        from myplotlib import PlotStore
        import matplotlib.pyplot as mp
        
        # write some plots to a file
        psw = PlotStore('test.pkl', 'w')
        psw.write_imports('import matplotlib.pyplot as mp')
        
        mp.figure()
        var1 = [1, 2, 3]
        var2 = [1, 3, 2]
        with psw.new_plot('plot1', (var1, var2)):
            mp.plot(var1)
            mp.plot(var2)
        
        mp.figure()
        with psw.new_plot('plot2', (var1)):
            mp.plot(var1)
            
        psw.write()
        del psw
        
        # Read plots from the file
        psr = PlotStore('test.pkl', 'r')
        
        for name in psr.ls(output='list'):
            print name
            mp.figure()
            psr.draw(name)
        
        mp.show()
        
        '''
        if mode not in 'rwa':
            raise ValueError("PlotStore: wrong file option. Must be r, w or a.")
        self.mode = mode
        self.file_name = file_name
        self.dict = {'imports': ''}
        if 'r' in self.mode:
            self.read()

    def write_imports(self, line=None):
        '''
        Write all necessary imports to plot your figure.
        Example:

        ps = PlotStore('test.pkl', 'w')
        ps.write_imports('import matplotlib.pyplot as mp')
        ps.write_imports('import numpy as np')
        '''
        if not line in self.dict['imports']:
            self.dict['imports'] += line + '\n'

    def write(self):
        '''
        Save plots to the file
        '''
        with open(self.file_name, self.mode) as f:
            pkl.dump(self.dict, f)
        
    def read(self):
        '''
        Read plots from the file.
        '''
        with open(self.file_name, self.mode) as f:
            self.dict = pkl.load(f)

    def ls(self, output='print'):
        '''
        List plots, stored in the file
        output - str, ('print' or 'list'). Default - 'print'
            output == 'print' : print the list of plots
            output == 'list' : output python list with names of plots
        '''
        keys = list(self.dict.keys())
        keys.remove('imports')
        keys.sort()
        if output == 'list':
            return keys
        elif output == 'print':
            for k in keys:
                print k

    def draw(self, name):
        '''
        Draw stored plot by name
        '''
        exec self.dict['imports']
        set_trace()
        if name in self.dict:
            var = self.dict[name][0]

            code = ''.join(self.dict[name][1])
            key = ''
            l = 0
            for var_name in var.keys():
                if var_name in code:
                    if len(var_name) > l:
                        l = len(var_name)
                        key = var_name
            code = code.replace(key, "var['" + key + "']")
            exec code.strip()
        else:
            print ("No name ", name, "in the dictionary!")

    @contextmanager
    def new_plot(self, name, var):
        '''
        Add a new plot to the file. See example with 'PlotStore?'
        '''
        frame = currentframe(2)
        line_start = getlineno(frame)
        yield
        line_finish = getlineno(frame)
        lines, first_line = findsource(frame)
        lines = lines[line_start : line_finish]
        def retrieve_name(v):
            callers_local_vars = currentframe(2).f_back.f_locals.items()
            return [v_name for v_name, v_val in callers_local_vars if v_val is v][0]
        var_dict = {}
        for v in var:
            var_dict[retrieve_name(v)] = v
        self.dict[name] = (var_dict, lines)
       
