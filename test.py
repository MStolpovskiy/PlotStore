import matplotlib.pyplot as mp
from myplotlib import PlotStore

ps = PlotStore('test.pkl', 'w')

with ps.new_plot('plot1'):
    mp.plot([1, 2, 1.5], 'r', ls='--', lw=5, marker='o',
            alpha=0.5, label='bla-bla')
    mp.legend()

ps.dump()

del ps

ps = PlotStore('test.pkl', 'a')

ps.ls
ps.draw('plot1')

with ps.new_plot('plot2'):
    mp.errorbar([1, 2, 3], [3, 2, 1], [0.1, 0.2, 0.3], [0.3, 0.2, 0.1],
                ecolor='r', elinewidth=4, capsize=10, 
                c='b', ls='-.', lw=2, marker='*',
                alpha=1.0, label='bla-bla')
    mp.legend()
ps.mkdir('dir1')
ps.mv('plot*', 'dir1')
    
ps.dump()

del ps

ps = PlotStore('test.pkl', 'a')
ps.cd('dir1')
for k in ps.list():
    ps.draw(k)
mp.show()
