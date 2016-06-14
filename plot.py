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
            a.set_position(ax.get_position())
            lines = ax.get_lines()
            cont = ax.containers
            for l in lines:
#                dobreak = False
#                for c in cont:
#                    if l in c:
#                        dobreak = True
#                        break
#                if dobreak: break
                a.plot(l.get_xdata(), l.get_ydata(),
                       c=l.get_c(), ls=l.get_ls(), alpha=l.get_alpha(),
                       label=l.get_label(), marker=l.get_marker(),
                       lw=l.get_lw(), markersize=l.get_markersize())
            for c in cont:
                a.containers.append(c)
            leg = ax.get_legend()
            if leg is not None:
                t = leg.get_title().get_text()
                t = t if t != 'None' else ''
                a.legend(title=t,
                         frameon=leg.get_frame_on())
