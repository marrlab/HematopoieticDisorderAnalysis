import matplotlib.pyplot as plt
import csv
import numpy as np
import math
import glob
from pathlib import Path
import openpyxl
import statistics
from scipy import stats
import scikit_posthocs as sp

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

Paths = glob.glob('../TreeDataForPlotting/E3*.csv')

Fate0Tree = np.zeros((len(Paths), 2), float)
Fate1Tree = np.zeros((len(Paths), 2), float)
Fate2Tree = np.zeros((len(Paths), 2), float)
LostTree = np.zeros((len(Paths), 2), float)

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

    Fate0 = np.zeros((len(a), 1), float)
    Fate1 = np.zeros((len(a), 1), float)
    Fate2 = np.zeros((len(a), 1), float)
    Lost = np.zeros((len(a), 1), float)
    for icell in range(0, len(a)):
        if x[icell][3] == '0': # no final fate
            Fate0[icell] = 1
        elif x[icell][3] == '1': # division
            Fate1[icell] = 1
        elif  x[icell][3] == '2': # death
            Fate2[icell] = 1

        if x[icell][3] == '3':
            Lost[icell] == 1

    namecsv = Path(Paths[ipath]).name
    name = namecsv[:-4]
    pos = int(name[4:7])

    Fate0Tree[ipath] = [sum(Fate0),pos]
    Fate1Tree[ipath] = [sum(Fate1),pos]
    Fate2Tree[ipath] = [sum(Fate2),pos]
    LostTree[ipath] = [sum(Lost),pos]


Fate0H500 = np.empty((0, 1))
Fate1H500 = np.empty((0, 1))
Fate2H500 = np.empty((0, 1))
Fate0H522 = np.empty((0, 1))
Fate1H522 = np.empty((0, 1))
Fate2H522 = np.empty((0, 1))
Fate0M354 = np.empty((0, 1))
Fate1M354 = np.empty((0, 1))
Fate2M354 = np.empty((0, 1))

for jpath in range(0, len(Paths)):
    if Fate0Tree[jpath,1] <= 30:
        Fate0H500 = np.append(Fate0H500, Fate0Tree[jpath, 0])
        Fate1H500 = np.append(Fate1H500, Fate1Tree[jpath, 0])
        Fate2H500 = np.append(Fate2H500, Fate2Tree[jpath, 0])
    elif Fate0Tree[jpath,1] > 90:
        Fate0H522 = np.append(Fate0H522, Fate0Tree[jpath, 0])
        Fate1H522 = np.append(Fate1H522, Fate1Tree[jpath, 0])
        Fate2H522 = np.append(Fate2H522, Fate2Tree[jpath, 0])
    else:
        Fate0M354 = np.append(Fate0M354, Fate0Tree[jpath, 0])
        Fate1M354 = np.append(Fate1M354, Fate1Tree[jpath, 0])
        Fate2M354 = np.append(Fate2M354, Fate2Tree[jpath, 0])

CellDeathH500 = np.divide(Fate2H500,Fate1H500+Fate2H500+Fate0H500)
CellDeathH522 = np.divide(Fate2H522,Fate1H522+Fate2H522+Fate0H522)
CellDeathM354 = np.divide(Fate2M354,Fate1M354+Fate2M354+Fate0M354)
#CellDeathH500 = np.divide(Fate2H500,Fate1H500+Fate2H500)
#CellDeathH522 = np.divide(Fate2H522,Fate1H522+Fate2H522)
#CellDeathM354 = np.divide(Fate2M354,Fate1M354+Fate2M354)

CellDeathH500 = CellDeathH500[np.nonzero(CellDeathH500)]*100
CellDeathH522 = CellDeathH522[np.nonzero(CellDeathH522)]*100
CellDeathM354 = CellDeathM354[np.nonzero(CellDeathM354)]*100

mH500 = np.median(CellDeathH500)
mH522 = np.median(CellDeathH522)
mM354 = np.median(CellDeathM354)

KW_M354_H522_H550 = stats.kruskal(CellDeathH500, CellDeathH522, CellDeathM354)

C = [CellDeathH500, CellDeathH522, CellDeathM354]

DT_bonferroni_C = sp.posthoc_dunn(C, p_adjust = 'bonferroni')

plt.figure()
ax = plt.subplot(111)
df = [CellDeathM354, CellDeathH500, CellDeathH522]
x = np.random.normal(1, 0.04, size=len(CellDeathM354))
plt.plot(x, CellDeathM354, '.', color=(255/255, 102/255, 102/255), markeredgecolor='k', zorder=10)
x = np.random.normal(2, 0.04, size=len(CellDeathH500))
plt.plot(x, CellDeathH500, '.', color=(153/255, 204/255, 255/255), markeredgecolor='k', zorder=10)
x = np.random.normal(3, 0.04, size=len(CellDeathH522))
plt.plot(x, CellDeathH522, '.', color=(153/255, 204/255, 255/255), markeredgecolor='k', zorder=10)
box = plt.boxplot(df, patch_artist=True, showfliers=False)
colors = [[255/255, 255/255, 255/255], [255/255, 255/255, 255/255], [255/255, 255/255, 255/255]]
for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)
for median in box['medians']:
    median.set(color='black')
plt.axes().set_xticklabels(['M354', 'H500', 'H522'])
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.ylabel('cell death per tree [%]')
#plt.ylim([0.2, 1.1])
#plotpath = 'CellDeath.svg'
#plt.savefig(plotpath)
plotpath = 'CellDeath.pdf'
plt.savefig(plotpath)
