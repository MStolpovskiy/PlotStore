from contextlib import contextmanager
from pdb import set_trace

class PlotStore(object):
    def __init__(self, file_name, options):
        self.options = options
        self.file_name = file_name
        self.dict = {'imports': ''}
        if 'r' in self.options:
            self.read()

    def write_imports(self, line=None):
        self.dict['imports'] += line + '\n'

    def write(self):
        import cPickle as pkl
        with open(self.file_name, self.options) as f:
            pkl.dump(self.dict, f)
        
    def read(self):
        import cPickle as pkl
        with open(self.file_name, 'r') as f:
            self.dict = pkl.load(f)

    def ls(self):
        keys = list(self.dict.keys())
        keys.remove('imports')
        return keys

    def draw(self, name):
        exec self.dict['imports']
        if name in self.dict:
            var_list = self.dict[name][0]
            var = {}
            if type(var_list) is not tuple or \
               type(var_list) is tuple and \
               type(var_list[0]) is not tuple:
                var_list = (var_list)
            for v in var_list:
                    var[v[0]] = v[1]
            
            for line in self.dict[name][1]:
                for var_name in var.keys():
                    line = line.replace(var_name, "var['" + var_name + "']")
                exec line.strip()
        else:
            print ("No name ", name, "in the dictionary!")

    @contextmanager
    def new_plot(self, name, *var):
        from inspect import (currentframe, getlineno, findsource, getargs)
        frame = currentframe(2)
        line_start = getlineno(frame)
        yield
        line_finish = getlineno(frame)
        lines, first_line = findsource(frame)
        lines = lines[line_start : line_finish]
        self.dict[name] = (var, lines)
#        print 'code'
#        print frame.f_code
#        print 'getargs'
#        print getargs(frame.f_code)
       
