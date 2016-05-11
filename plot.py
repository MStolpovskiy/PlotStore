from inspect import currentframe, getlineno, getsourcelines, getsourcefile

class Plot(object):
    def __init__(self, pkl, name):
        self.name = name
        self.dims = 0
        self.var = []
        self.line = ''
        self.pkl = pkl
        self.line_start = 0
        self.line_finish = -1
        self.frame = currentframe(1)
        
    def __enter__(self):
        self.line_start = getlineno(self.frame) + 1
        return self

    def __exit__(self, type, value, traceback):
        self.line_finish = getlineno(self.frame)
        if self.line_finish >= self.line_start:
            with open(getsourcefile(self.frame), 'r') as source_file:
                lineno = 1
                for line in source_file:
                    if lineno >= self.line_start and \
                       lineno <= self.line_finish and \
                       '#!' in line:
                        self.line += line
                    lineno += 1

        self.pkl.dict[self.name] = (self.dims, self.line, self.var)

    def uploadVar(self, var):
        self.dims += 1
        self.var.append(var)

    def v(self, i_var):
        if i_var >= self.dims:
            raise Exception("Wrong index!!!")
        else:
            return self.var[i_var]
