import matplotlib.pyplot as plt
import csv
import numpy as np
import math
import glob
from pathlib import Path
import openpyxl

xlsxfile = '../HealthyMDSAnnotations.xlsx'
book = openpyxl.load_workbook(xlsxfile)
sheet = book.active

cellsexp3 = sheet['H2':'H121']
E3 = np.empty((120, 1), str)
for c3 in range(0, 120):
        E3[c3] = cellsexp3[c3][0].value

cellsexppat3 = sheet['I2':'I121']
Epat3 = []
for cpat3 in range(0, 120):
        a = cellsexppat3[cpat3][0].value
        Epat3.append(a)

Paths = glob.glob('../TreeDataForPlotting/*.csv')

for ipath in range(0, len(Paths)):

    with open(Paths[ipath]) as csvfile: x = list(csv.reader(csvfile))

    x = x[1:]
    a = np.zeros((len(x), 3), float)
    for ishape in range(0, len(x)):
        a[ishape,:] = x[ishape][1:]

    a = np.matrix(a)

    M = np.zeros((len(a), 1), float)
    for imother in range(0, len(a)):
        if imother == 0:
            M[imother] = 0
        else:
            M[imother] = math.floor(a[imother,0]/2)

    T = np.zeros((len(a), 1), float)
    for itotal in range(0, len(a)):
        if itotal == 0:
            T[itotal] = a[itotal,1]
        else:
            ind = np.where(M[itotal] == a[:, 0])
            if ind[0].size == 0:
                T[itotal] == 0
            else:
                time_mother = T[np.where(M[itotal] == a[:, 0]), 0]
                T[itotal] = time_mother[0] + a[itotal, 1]

    length = [32, 16, 8, 4, 2, 1]

    plt.figure()

    Pos = np.zeros((int(max(a[:,0])), 3), float)
    ax = plt.subplot(111)

    for icell in range(0, len(a)):
        if int(a[icell, 0]) == 1:
            ax.plot([0, 0], [0, -T[0]], 'k-', lw=4)
            Pos[icell, :] = [0, -T[0], a[icell,0]]
            if x[icell][3] == '2':
                ax.plot([0], [-T[0]-5], marker="$x$", color='k')
            elif x[icell][3] == '3':
                ax.plot([0], [-T[0]-5], marker="$?$", color='k')
        else:
            if T[icell] != 0:
                ind = np.where(M[icell] == Pos[:, 2])
                ax.plot([float(Pos[ind, 0]-length[int(np.floor(np.log2(a[icell, 0])))-1]/2),
                         float(Pos[ind, 0]+length[int(np.floor(np.log2(a[icell, 0])))-1]/2)],
                        [float(Pos[ind, 1]), float(Pos[ind, 1])], 'k-', lw=4)
                if int(a[icell, 0]) % 2 == 0:
                    ax.plot([float(Pos[ind, 0]-length[int(np.floor(np.log2(a[icell,0])))-1]/2),
                            float(Pos[ind, 0]-length[int(np.floor(np.log2(a[icell,0])))-1]/2)],
                            [float(Pos[ind,1]), float(-T[icell])], 'k-', lw=4)
                    Pos[icell, :] = [float(Pos[ind, 0]-length[int(np.floor(np.log2(a[icell, 0])))-1]/2), float(-T[icell]), a[icell, 0]]
                    if x[icell][3] == '2':
                        ax.plot([float(Pos[ind, 0]-length[int(np.floor(np.log2(a[icell,0])))-1]/2)],
                                [float(-T[icell]) - 5], marker="$x$", color='k')
                    elif x[icell][3] == '3':
                        ax.plot([float(Pos[ind, 0]-length[int(np.floor(np.log2(a[icell,0])))-1]/2)],
                                [float(-T[icell]) - 5], marker="$?$", color='k')
                else:
                    ax.plot([float(Pos[ind, 0]+length[int(np.floor(np.log2(a[icell, 0])))-1]/2),
                            float(Pos[ind, 0]+length[int(np.floor(np.log2(a[icell, 0])))-1]/2)],
                            [float(Pos[ind, 1]), float(-T[icell])], 'k-', lw=4)
                    Pos[icell, :] = [float(Pos[ind, 0]+length[int(np.floor(np.log2(a[icell, 0])))-1]/2), float(-T[icell]), a[icell,0]]
                    if x[icell][3] == '2':
                        ax.plot([float(Pos[ind, 0]+length[int(np.floor(np.log2(a[icell, 0])))-1]/2)],
                                [float(-T[icell])-5], marker="$x$", color='k')
                    elif x[icell][3] == '3':
                        ax.plot([float(Pos[ind, 0]+length[int(np.floor(np.log2(a[icell, 0])))-1]/2)],
                                [float(-T[icell])-5], marker="$?$", color='k')

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    #plt.ylabel('time (h)')
    plt.ylim([-180, 0])
    ax.set_yticklabels([])
    ax.tick_params(axis='y', colors='white')
    #ax.set_yticklabels([str(int(abs(x))) for x in ax.get_yticks()])

    namecsv = Path(Paths[ipath]).name
    name = namecsv[:-4]

    exp = name[1]
    pos = name[4:7]

    Exp = 'E%d' % int(exp)
    pat = np.zeros((1, 1), str)
    pat = eval('E%d[%d]' % (int(exp), int(pos)))

    if exp == '3':
        patnum = eval('Epat3[%d]' % int(pos))
        title = '%s %s %s' % (name, pat[0], patnum)
    elif exp == '6':
        patnum = eval('Epat6[%d]' % int(pos))
        title = '%s %s %s' % (name, pat[0], patnum)
    else:
        title = '%s %s' % (name, pat[0])

    #plt.title(title)

    #cur_axes = plt.gca()
    #cur_axes.axes.get_xaxis().set_visible(False)
    #cur_axes.axes.get_yaxis().set_visible(False)
    plotpath = '%s.pdf' % name
    plt.savefig(plotpath)
    #plt.show()