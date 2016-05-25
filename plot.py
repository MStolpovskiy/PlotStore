import matplotlib.pyplot as mp

class Plot(object):
    def __init__(self, name,
                 axes):
        self.name = name
        self.axes = axes

    def draw(self):
        fig = mp.figure()
        for iax, ax in enumerate(self.axes):
            a = fig.add_subplot(iax + 1, len(self.axes), 1)
            a.set_position(ax['position'])
            lines = ax['lines']
            for l in lines:
                a.plot(l[0], l[1], c=l[2], ls=l[3], alpha=l[4],
                       label=l[5], marker=l[6], lw=l[7], markersize=l[8])
            leg = ax['legend']
            if leg is not None:
                a.legend(title=leg[0], frameon=leg[1])
