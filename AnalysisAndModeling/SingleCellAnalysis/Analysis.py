import matplotlib.pyplot as plt
import csv
import numpy as np
import math
import glob
from pathlib import Path
import openpyxl
from scipy import stats
import seaborn as sns
import scikit_posthocs as sp
import jenkspy
import numpy.matlib
import statistics

#############
#AnalysisExp3
#############

#read in data
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

TFirstDivH550 = np.zeros((1, 4), float)
TFirstDivM354 = np.zeros((1, 4), float)
TFirstDivH522 = np.zeros((1, 4), float)

pow = np.zeros((1, 10), float)
countpow = 0
for ipow in range(0, 10):
    pow[0, countpow] = pow[0, countpow-1] + 2**ipow
    countpow = countpow + 1

#restructure data into useful format / per patient
for ipath in range(0, len(Paths)):

    print(ipath)

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
            M[imother] = math.floor(a[imother, 0]/2)

    #time to divisions (0th, 1st, 2nd, 3rd,...)
    namecsv = Path(Paths[ipath]).name
    name = namecsv[:-4]

    pos = name[4:7]
    div = np.zeros((int(sum(a[:, 2] == 1)), 4), float)

    countdivcell = 0

    for icell in range(0, len(a)):
        if a[icell, 2] == 1: #take all cells into account which actually divide
            countdiv = 0
            for idiv in range(0, len(np.transpose(pow))): #for each cell, determine its generation
                if pow[0, idiv] >= a[icell, 0] and countdiv == 0:
                    div[countdivcell] = [icell, a[icell, 0], idiv, a[icell, 1]]
                    countdiv = 1
                    countdivcell = countdivcell + 1

    #chategorize particular tree/cells/divisions with correct patient ID
    if 1 <= int(pos) <= 30:
        TFirstDivH550 = np.concatenate((TFirstDivH550, div), axis=0)
    elif 31 <= int(pos) <= 60:
        TFirstDivM354 = np.concatenate((TFirstDivM354, div), axis=0)
    elif 91 <= int(pos) <= 120:
        TFirstDivH522 = np.concatenate((TFirstDivH522, div), axis=0)

maxdiv = max(np.concatenate((TFirstDivH550[:, 2], TFirstDivM354[:, 2], TFirstDivH522[:, 2]), axis=0))

#cell cylce durations per patient
#M354
plt.figure()
ax = plt.subplot(111)
numcellsM3540 = np.where(TFirstDivM354[:, 2] == 0)
numcellsM3540 = numcellsM3540[0][1:]
numcellsM3541 = np.where(TFirstDivM354[:, 2] == 1)
numcellsM3542 = np.where(TFirstDivM354[:, 2] == 2)
numcellsM3543 = np.where(TFirstDivM354[:, 2] == 3)
numcellsM3544 = np.where(TFirstDivM354[:, 2] == 4)

#H522
plt.figure()
ax = plt.subplot(111)
numcellsH5220 = np.where(TFirstDivH522[:, 2] == 0)
numcellsH5220 = numcellsH5220[0][1:]
numcellsH5221 = np.where(TFirstDivH522[:, 2] == 1)
numcellsH5222 = np.where(TFirstDivH522[:, 2] == 2)
numcellsH5223 = np.where(TFirstDivH522[:, 2] == 3)
numcellsH5224 = np.where(TFirstDivH522[:, 2] == 4)

#H550
plt.figure()
ax = plt.subplot(111)
numcellsH5500 = np.where(TFirstDivH550[:, 2] == 0)
numcellsH5500 = numcellsH5500[0][1:]
numcellsH5501 = np.where(TFirstDivH550[:, 2] == 1)
numcellsH5502 = np.where(TFirstDivH550[:, 2] == 2)
numcellsH5503 = np.where(TFirstDivH550[:, 2] == 3)
numcellsH5504 = np.where(TFirstDivH550[:, 2] == 4)

#all together - division times Exp3
plt.figure()
ax = plt.subplot(111)

plt.scatter(np.full((1, len(np.transpose(numcellsM3540))), 0.8), TFirstDivM354[numcellsM3540, 3], color=(255/255, 255/255, 255/255), edgecolors='k')
plt.scatter(np.full((1, len(np.transpose(numcellsM3541))), 1.8), TFirstDivM354[numcellsM3541, 3], color=(255/255, 204/255, 204/255), edgecolors='k')
plt.scatter(np.full((1, len(np.transpose(numcellsM3542))), 2.8), TFirstDivM354[numcellsM3542, 3], color=(255/255, 102/255, 102/255), edgecolors='k')
plt.scatter(np.full((1, len(np.transpose(numcellsM3543))), 3.8), TFirstDivM354[numcellsM3543, 3], color=(255/255, 51/255, 51/255), edgecolors='k')
plt.scatter(np.full((1, len(np.transpose(numcellsM3544))), 4.8), TFirstDivM354[numcellsM3544, 3], color=(153/255, 0/255, 0/255), edgecolors='k')

plt.scatter(np.full((1, len(np.transpose(numcellsH5500))), 1), TFirstDivH550[numcellsH5500, 3], color=(255/255, 255/255, 255/255), edgecolors='k')
plt.scatter(np.full((1, len(np.transpose(numcellsH5501))), 2), TFirstDivH550[numcellsH5501, 3], color=(204/255, 229/255, 255/255), edgecolors='k')
plt.scatter(np.full((1, len(np.transpose(numcellsH5502))), 3), TFirstDivH550[numcellsH5502, 3], color=(153/255, 204/255, 255/255), edgecolors='k')
plt.scatter(np.full((1, len(np.transpose(numcellsH5503))), 4), TFirstDivH550[numcellsH5503, 3], color=(51/255, 153/255, 255/255), edgecolors='k')
plt.scatter(np.full((1, len(np.transpose(numcellsH5504))), 5), TFirstDivH550[numcellsH5504, 3], color=(0/255, 76/255, 153/255), edgecolors='k')

plt.scatter(np.full((1, len(np.transpose(numcellsH5220))), 1.2), TFirstDivH522[numcellsH5220, 3], color=(255/255, 255/255, 255/255), edgecolors='k')
plt.scatter(np.full((1, len(np.transpose(numcellsH5221))), 2.2), TFirstDivH522[numcellsH5221, 3], color=(204/255, 229/255, 255/255), edgecolors='k')
plt.scatter(np.full((1, len(np.transpose(numcellsH5222))), 3.2), TFirstDivH522[numcellsH5222, 3], color=(153/255, 204/255, 255/255), edgecolors='k')
plt.scatter(np.full((1, len(np.transpose(numcellsH5223))), 4.2), TFirstDivH522[numcellsH5223, 3], color=(51/255, 153/255, 255/255), edgecolors='k')
plt.scatter(np.full((1, len(np.transpose(numcellsH5224))), 5.2), TFirstDivH522[numcellsH5224, 3], color=(0/255, 76/255, 153/255), edgecolors='k')

plt.xticks([1, 2, 3, 4, 5])
plt.axes().set_xticklabels(['0th', '1st', '2nd', '3rd', '4th'])
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.ylabel('time (h)')
plt.xlabel('division')
plt.xlim([0, 6])
plt.ylim([0, 160])
plotpath = 'DivisionsExp3All.pdf'
plt.savefig(plotpath)

#Kruskal-Wallis tests
KW_M354_H522_H550_TtoDiv1 = stats.kruskal(TFirstDivM354[numcellsM3540, 3], TFirstDivH550[numcellsH5500, 3], TFirstDivH522[numcellsH5220, 3])
KW_M354_H522_H550_Div1 = stats.kruskal(np.transpose(TFirstDivM354[numcellsM3541, 3]), np.transpose(TFirstDivH550[numcellsH5501, 3]), np.transpose(TFirstDivH522[numcellsH5221, 3]))
KW_M354_H522_H550_Div2 = stats.kruskal(np.transpose(TFirstDivM354[numcellsM3542, 3]), np.transpose(TFirstDivH550[numcellsH5502, 3]), np.transpose(TFirstDivH522[numcellsH5222, 3]))
KW_M354_H522_H550_Div3 = stats.kruskal(np.transpose(TFirstDivM354[numcellsM3543, 3]), np.transpose(TFirstDivH550[numcellsH5503, 3]), np.transpose(TFirstDivH522[numcellsH5223, 3]))
KW_M354_H522_H550_Div4 = stats.kruskal(np.transpose(TFirstDivM354[numcellsM3544, 3]), np.transpose(TFirstDivH550[numcellsH5504, 3]), np.transpose(TFirstDivH522[numcellsH5224, 3]))

#post-hoc tests - Dunn's test - for tests failing KW
div2=  [TFirstDivM354[numcellsM3542, 3][0,:], TFirstDivH550[numcellsH5502, 3][0,:], TFirstDivH522[numcellsH5222, 3][0,:]]
div3=  [TFirstDivM354[numcellsM3543, 3][0,:], TFirstDivH550[numcellsH5503, 3][0,:], TFirstDivH522[numcellsH5223, 3][0,:]]
div4=  [TFirstDivM354[numcellsM3544, 3][0,:], TFirstDivH550[numcellsH5504, 3][0,:], TFirstDivH522[numcellsH5224, 3][0,:]]
DT_bonferroni_Div2 = sp.posthoc_dunn(div2, p_adjust = 'bonferroni')
DT_bonferroni_Div3 = sp.posthoc_dunn(div3, p_adjust = 'bonferroni')
DT_bonferroni_Div4 = sp.posthoc_dunn(div4, p_adjust = 'bonferroni')

#sister cells per patient - divsion specific
#M354
sister1 = np.zeros((1, 4), float)
sister2 = np.zeros((1, 4), float)

plt.figure()
ax = plt.subplot(111)
for icell in range(1, len(TFirstDivM354)):
    #even numbered cells
    if TFirstDivM354[icell, 2] != 0: #need sister pairs - get rid of 0th division/first cell
        if icell == len(TFirstDivM354) - 1: #if last cell
            if TFirstDivM354[icell, 1] % 2 != 0 and TFirstDivM354[icell - 1, 1] == TFirstDivM354[icell, 1] - 1:
                sister2 = np.concatenate((sister2, TFirstDivM354[icell, :].reshape(1, 4)), axis=0)
        elif icell == 1: #if first cell
            if TFirstDivM354[icell, 1] % 2 == 0 and TFirstDivM354[icell+1, 1] == TFirstDivM354[icell, 1]+1: #assure that sister cell also divides
                sister1 = np.concatenate((sister1, TFirstDivM354[icell, :].reshape(1, 4)), axis=0)
        else:
            if TFirstDivM354[icell, 1] % 2 == 0 and TFirstDivM354[icell+1, 1] == TFirstDivM354[icell, 1]+1: #assure that sister cell also divides
                sister1 = np.concatenate((sister1, TFirstDivM354[icell, :].reshape(1, 4)), axis=0)
            elif TFirstDivM354[icell, 1] % 2 != 0 and TFirstDivM354[icell-1, 1] == TFirstDivM354[icell, 1]-1:
                sister2 = np.concatenate((sister2, TFirstDivM354[icell, :].reshape(1, 4)), axis=0)

numcellsM3541sister1 = np.where(sister1[:, 2] == 1)
numcellsM3542sister1 = np.where(sister1[:, 2] == 2)
numcellsM3543sister1 = np.where(sister1[:, 2] == 3)
numcellsM3544sister1 = np.where(sister1[:, 2] == 4)

numcellsM3541sister2 = np.where(sister2[:, 2] == 1)
numcellsM3542sister2 = np.where(sister2[:, 2] == 2)
numcellsM3543sister2 = np.where(sister2[:, 2] == 3)
numcellsM3544sister2 = np.where(sister2[:, 2] == 4)

plt.scatter(sister1[numcellsM3541sister1, 3], sister2[numcellsM3541sister2, 3], color=(255/255, 204/255, 204/255), edgecolors='k', label='1st division')
plt.scatter(sister1[numcellsM3542sister1, 3], sister2[numcellsM3542sister2, 3], color=(255/255, 102/255, 102/255), edgecolors='k', label='2nd division')
plt.scatter(sister1[numcellsM3543sister1, 3], sister2[numcellsM3543sister2, 3], color=(255/255, 51/255, 51/255), edgecolors='k', label='3rd division')
plt.scatter(sister1[numcellsM3544sister1, 3], sister2[numcellsM3544sister2, 3], color=(153/255, 0/255, 0/255), edgecolors='k', label='4th division')
ax.legend()
plt.legend(frameon=False)
plt.plot([0, 60], [0, 60], 'k-', lw=2)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.ylabel('sister 2 - time (h)')
plt.xlabel('sister 1 - time (h)')
plt.xlim([0, 60])
plt.ylim([0, 60])
title = 'M354'
plt.title(title)
plotpath = 'SistersDiv_M354.pdf'
plt.savefig(plotpath)

#H522
sister1 = np.zeros((1, 4), float)
sister2 = np.zeros((1, 4), float)

plt.figure()
ax = plt.subplot(111)
for icell in range(1, len(TFirstDivH522)):
    #even numbered cells
    if TFirstDivH522[icell, 2] != 0: #need sister pairs - get rid of 0th division/first cell
        if icell == len(TFirstDivH522) - 1: #if last cell
            if TFirstDivH522[icell, 1] % 2 != 0 and TFirstDivH522[icell - 1, 1] == TFirstDivH522[icell, 1] - 1:
                sister2 = np.concatenate((sister2, TFirstDivH522[icell, :].reshape(1, 4)), axis=0)
        elif icell == 1: #if first cell
            if TFirstDivH522[icell, 1] % 2 == 0 and TFirstDivH522[icell+1, 1] == TFirstDivH522[icell, 1]+1: #assure that sister cell also divides
                sister1 = np.concatenate((sister1, TFirstDivH522[icell, :].reshape(1, 4)), axis=0)
        else:
            if TFirstDivH522[icell, 1] % 2 == 0 and TFirstDivH522[icell+1, 1] == TFirstDivH522[icell, 1]+1: #assure that sister cell also divides
                sister1 = np.concatenate((sister1, TFirstDivH522[icell, :].reshape(1, 4)), axis=0)
            elif TFirstDivH522[icell, 1] % 2 != 0 and TFirstDivH522[icell-1, 1] == TFirstDivH522[icell, 1]-1:
                sister2 = np.concatenate((sister2, TFirstDivH522[icell, :].reshape(1, 4)), axis=0)

numcellsH5221sister1 = np.where(sister1[:, 2] == 1)
numcellsH5222sister1 = np.where(sister1[:, 2] == 2)
numcellsH5223sister1 = np.where(sister1[:, 2] == 3)
numcellsH5224sister1 = np.where(sister1[:, 2] == 4)

numcellsH5221sister2 = np.where(sister2[:, 2] == 1)
numcellsH5222sister2 = np.where(sister2[:, 2] == 2)
numcellsH5223sister2 = np.where(sister2[:, 2] == 3)
numcellsH5224sister2 = np.where(sister2[:, 2] == 4)

plt.scatter(sister1[numcellsH5221sister1, 3], sister2[numcellsH5221sister2, 3], color=(204/255, 229/255, 255/255), edgecolors='k', label='1st division')
plt.scatter(sister1[numcellsH5222sister1, 3], sister2[numcellsH5222sister2, 3], color=(153/255, 204/255, 255/255), edgecolors='k', label='2nd division')
plt.scatter(sister1[numcellsH5223sister1, 3], sister2[numcellsH5223sister2, 3], color=(51/255, 153/255, 255/255), edgecolors='k', label='3rd division')
plt.scatter(sister1[numcellsH5224sister1, 3], sister2[numcellsH5224sister2, 3], color=(0/255, 76/255, 153/255), edgecolors='k',label='4th division')
ax.legend()
plt.legend(frameon=False)
plt.plot([0, 60], [0, 60], 'k-', lw=2)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.ylabel('sister 2 - time (h)')
plt.xlabel('sister 1 - time (h)')
plt.xlim([0, 60])
plt.ylim([0, 60])
title = 'H522'
plt.title(title)
plotpath = 'SistersDiv_H522.pdf'
plt.savefig(plotpath)

#H550
sister1 = np.zeros((1, 4), float)
sister2 = np.zeros((1, 4), float)

plt.figure()
ax = plt.subplot(111)
for icell in range(1, len(TFirstDivH550)):
    #even numbered cells
    if TFirstDivH550[icell, 2] != 0: #need sister pairs - get rid of 0th division/first cell
        if icell == len(TFirstDivH550) - 1: #if last cell
            if TFirstDivH550[icell, 1] % 2 != 0 and TFirstDivH550[icell - 1, 1] == TFirstDivH550[icell, 1] - 1:
                sister2 = np.concatenate((sister2, TFirstDivH550[icell, :].reshape(1, 4)), axis=0)
        elif icell == 1: #if first cell
            if TFirstDivH550[icell, 1] % 2 == 0 and TFirstDivH550[icell+1, 1] == TFirstDivH550[icell, 1]+1: #assure that sister cell also divides
                sister1 = np.concatenate((sister1, TFirstDivH550[icell, :].reshape(1, 4)), axis=0)
        else:
            if TFirstDivH550[icell, 1] % 2 == 0 and TFirstDivH550[icell+1, 1] == TFirstDivH550[icell, 1]+1: #assure that sister cell also divides
                sister1 = np.concatenate((sister1, TFirstDivH550[icell, :].reshape(1, 4)), axis=0)
            elif TFirstDivH550[icell, 1] % 2 != 0 and TFirstDivH550[icell-1, 1] == TFirstDivH550[icell, 1]-1:
                sister2 = np.concatenate((sister2, TFirstDivH550[icell, :].reshape(1, 4)), axis=0)

numcellsH5501sister1 = np.where(sister1[:, 2] == 1)
numcellsH5502sister1 = np.where(sister1[:, 2] == 2)
numcellsH5503sister1 = np.where(sister1[:, 2] == 3)
numcellsH5504sister1 = np.where(sister1[:, 2] == 4)

numcellsH5501sister2 = np.where(sister2[:, 2] == 1)
numcellsH5502sister2 = np.where(sister2[:, 2] == 2)
numcellsH5503sister2 = np.where(sister2[:, 2] == 3)
numcellsH5504sister2 = np.where(sister2[:, 2] == 4)

plt.scatter(sister1[numcellsH5501sister1, 3], sister2[numcellsH5501sister2, 3], color=(204/255, 229/255, 255/255), edgecolors='k', label='1st division')
plt.scatter(sister1[numcellsH5502sister1, 3], sister2[numcellsH5502sister2, 3], color=(153/255, 204/255, 255/255), edgecolors='k', label='2nd division')
plt.scatter(sister1[numcellsH5503sister1, 3], sister2[numcellsH5503sister2, 3], color=(51/255, 153/255, 255/255), edgecolors='k', label='3rd division')
plt.scatter(sister1[numcellsH5504sister1, 3], sister2[numcellsH5504sister2, 3], color=(0/255, 76/255, 153/255), edgecolors='k', label='4th division')
ax.legend()
plt.legend(frameon=False)
plt.plot([0, 60], [0, 60], 'k-', lw=2)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.ylabel('sister 2 - time (h)')
plt.xlabel('sister 1 - time (h)')
plt.xlim([0, 60])
plt.ylim([0, 60])
title = 'H550'
plt.title(title)
plotpath = 'SistersDiv_H500.pdf'
plt.savefig(plotpath)

#Pearson correlation - random sister swapping for statistical robustness
#M354
nsamples = 100
sister1 = np.zeros((1, 4), float)
sister2 = np.zeros((1, 4), float)

for icell in range(1, len(TFirstDivM354)):
    #even numbered cells
    if TFirstDivM354[icell, 2] != 0: #need sister pairs - get rid of 0th division/first cell
        if icell == len(TFirstDivM354) - 1: #if last cell
            if TFirstDivM354[icell, 1] % 2 != 0 and TFirstDivM354[icell - 1, 1] == TFirstDivM354[icell, 1] - 1:
                sister2 = np.concatenate((sister2, TFirstDivM354[icell, :].reshape(1, 4)), axis=0)
        elif icell == 1: #if first cell
            if TFirstDivM354[icell, 1] % 2 == 0 and TFirstDivM354[icell+1, 1] == TFirstDivM354[icell, 1]+1: #assure that sister cell also divides
                sister1 = np.concatenate((sister1, TFirstDivM354[icell, :].reshape(1, 4)), axis=0)
        else:
            if TFirstDivM354[icell, 1] % 2 == 0 and TFirstDivM354[icell+1, 1] == TFirstDivM354[icell, 1]+1: #assure that sister cell also divides
                sister1 = np.concatenate((sister1, TFirstDivM354[icell, :].reshape(1, 4)), axis=0)
            elif TFirstDivM354[icell, 1] % 2 != 0 and TFirstDivM354[icell-1, 1] == TFirstDivM354[icell, 1]-1:
                sister2 = np.concatenate((sister2, TFirstDivM354[icell, :].reshape(1, 4)), axis=0)

sister1 = sister1[1:, :]
sister2 = sister2[1:, :]

randsister1 = np.zeros((len(sister1), 4), float)
randsister2 = np.zeros((len(sister2), 4), float)
PearsonCoeffM354 = np.zeros((nsamples, 1), float)

for iPearson in range(0, nsamples):

    rand = np.random.binomial(1, 0.5, len(sister1))
    rand0 = np.where(rand == 0)
    rand1 = np.where(rand == 1)
    randsister1 = np.concatenate((sister1[rand0[0], :], sister2[rand1[0], :]), axis=0)
    randsister2 = np.concatenate((sister2[rand0[0], :], sister1[rand1[0], :]), axis=0)

    P = stats.pearsonr(randsister1[:, 3], randsister2[:, 3])
    PearsonCoeffM354[iPearson] = P[0]

meanPearsonCoeffM354 = np.mean(PearsonCoeffM354)
medPearsonCoeffM354 = np.median(PearsonCoeffM354)
stdPearsonCoeffM354 = np.std(PearsonCoeffM354)

#H522
nsamples = 100
sister1 = np.zeros((1, 4), float)
sister2 = np.zeros((1, 4), float)

for icell in range(1, len(TFirstDivH522)):
    #even numbered cells
    if TFirstDivH522[icell, 2] != 0: #need sister pairs - get rid of 0th division/first cell
        if icell == len(TFirstDivH522) - 1: #if last cell
            if TFirstDivH522[icell, 1] % 2 != 0 and TFirstDivH522[icell - 1, 1] == TFirstDivH522[icell, 1] - 1:
                sister2 = np.concatenate((sister2, TFirstDivH522[icell, :].reshape(1, 4)), axis=0)
        elif icell == 1: #if first cell
            if TFirstDivH522[icell, 1] % 2 == 0 and TFirstDivH522[icell+1, 1] == TFirstDivH522[icell, 1]+1: #assure that sister cell also divides
                sister1 = np.concatenate((sister1, TFirstDivH522[icell, :].reshape(1, 4)), axis=0)
        else:
            if TFirstDivH522[icell, 1] % 2 == 0 and TFirstDivH522[icell+1, 1] == TFirstDivH522[icell, 1]+1: #assure that sister cell also divides
                sister1 = np.concatenate((sister1, TFirstDivH522[icell, :].reshape(1, 4)), axis=0)
            elif TFirstDivH522[icell, 1] % 2 != 0 and TFirstDivH522[icell-1, 1] == TFirstDivH522[icell, 1]-1:
                sister2 = np.concatenate((sister2, TFirstDivH522[icell, :].reshape(1, 4)), axis=0)

sister1 = sister1[1:, :]
sister2 = sister2[1:, :]

randsister1 = np.zeros((len(sister1), 4), float)
randsister2 = np.zeros((len(sister2), 4), float)
PearsonCoeffH522 = np.zeros((nsamples, 1), float)

for iPearson in range(0, nsamples):

    rand = np.random.binomial(1, 0.5, len(sister1))
    rand0 = np.where(rand == 0)
    rand1 = np.where(rand == 1)
    randsister1 = np.concatenate((sister1[rand0[0], :], sister2[rand1[0], :]), axis=0)
    randsister2 = np.concatenate((sister2[rand0[0], :], sister1[rand1[0], :]), axis=0)

    P = stats.pearsonr(randsister1[:, 3], randsister2[:, 3])
    PearsonCoeffH522[iPearson] = P[0]

meanPearsonCoeffH522 = np.mean(PearsonCoeffH522)
medPearsonCoeffH522 = np.median(PearsonCoeffH522)
stdPearsonCoeffH522 = np.std(PearsonCoeffH522)

#H550
nsamples = 100
sister1 = np.zeros((1, 4), float)
sister2 = np.zeros((1, 4), float)

for icell in range(1, len(TFirstDivH550)):
    #even numbered cells
    if TFirstDivH550[icell, 2] != 0: #need sister pairs - get rid of 0th division/first cell
        if icell == len(TFirstDivH550) - 1: #if last cell
            if TFirstDivH550[icell, 1] % 2 != 0 and TFirstDivH550[icell - 1, 1] == TFirstDivH550[icell, 1] - 1:
                sister2 = np.concatenate((sister2, TFirstDivH550[icell, :].reshape(1, 4)), axis=0)
        elif icell == 1: #if first cell
            if TFirstDivH550[icell, 1] % 2 == 0 and TFirstDivH550[icell+1, 1] == TFirstDivH550[icell, 1]+1: #assure that sister cell also divides
                sister1 = np.concatenate((sister1, TFirstDivH550[icell, :].reshape(1, 4)), axis=0)
        else:
            if TFirstDivH550[icell, 1] % 2 == 0 and TFirstDivH550[icell+1, 1] == TFirstDivH550[icell, 1]+1: #assure that sister cell also divides
                sister1 = np.concatenate((sister1, TFirstDivH550[icell, :].reshape(1, 4)), axis=0)
            elif TFirstDivH550[icell, 1] % 2 != 0 and TFirstDivH550[icell-1, 1] == TFirstDivH550[icell, 1]-1:
                sister2 = np.concatenate((sister2, TFirstDivH550[icell, :].reshape(1, 4)), axis=0)

sister1 = sister1[1:, :]
sister2 = sister2[1:, :]

randsister1 = np.zeros((len(sister1), 4), float)
randsister2 = np.zeros((len(sister2), 4), float)
PearsonCoeffH550 = np.zeros((nsamples, 1), float)

for iPearson in range(0, nsamples):

    rand = np.random.binomial(1, 0.5, len(sister1))
    rand0 = np.where(rand == 0)
    rand1 = np.where(rand == 1)
    randsister1 = np.concatenate((sister1[rand0[0], :], sister2[rand1[0], :]), axis=0)
    randsister2 = np.concatenate((sister2[rand0[0], :], sister1[rand1[0], :]), axis=0)

    P = stats.pearsonr(randsister1[:, 3], randsister2[:, 3])
    PearsonCoeffH550[iPearson] = P[0]

meanPearsonCoeffH550 = np.mean(PearsonCoeffH550)
stdPearsonCoeffH550 = np.std(PearsonCoeffH550)

#short/long sister - distribution comparison
#M354
sister1 = np.zeros((1, 4), float)
sister2 = np.zeros((1, 4), float)

for icell in range(1, len(TFirstDivM354)):
    #even numbered cells
    if TFirstDivM354[icell, 2] != 0: #need sister pairs - get rid of 0th division/first cell
        if icell == len(TFirstDivM354) - 1: #if last cell
            if TFirstDivM354[icell, 1] % 2 != 0 and TFirstDivM354[icell - 1, 1] == TFirstDivM354[icell, 1] - 1:
                sister2 = np.concatenate((sister2, TFirstDivM354[icell, :].reshape(1, 4)), axis=0)
        elif icell == 1: #if first cell
            if TFirstDivM354[icell, 1] % 2 == 0 and TFirstDivM354[icell+1, 1] == TFirstDivM354[icell, 1]+1: #assure that sister cell also divides
                sister1 = np.concatenate((sister1, TFirstDivM354[icell, :].reshape(1, 4)), axis=0)
        else:
            if TFirstDivM354[icell, 1] % 2 == 0 and TFirstDivM354[icell+1, 1] == TFirstDivM354[icell, 1]+1: #assure that sister cell also divides
                sister1 = np.concatenate((sister1, TFirstDivM354[icell, :].reshape(1, 4)), axis=0)
            elif TFirstDivM354[icell, 1] % 2 != 0 and TFirstDivM354[icell-1, 1] == TFirstDivM354[icell, 1]-1:
                sister2 = np.concatenate((sister2, TFirstDivM354[icell, :].reshape(1, 4)), axis=0)

sister1 = sister1[1:, :]
sister2 = sister2[1:, :]

shortsisterM354  = np.zeros((len(sister1), 4), float)
longsisterM354  = np.zeros((len(sister1), 4), float)

for ilength in range(0, len(sister1)):
    if sister1[ilength,3] <= sister2[ilength,3]:
        shortsisterM354[ilength,:] = sister1[ilength, :]
        longsisterM354[ilength,:] = sister2[ilength, :]
    elif sister1[ilength,3] > sister2[ilength,3]:
        shortsisterM354[ilength, :] = sister2[ilength, :]
        longsisterM354[ilength, :] = sister1[ilength, :]

RatioM354 = np.divide(shortsisterM354[:, 3], longsisterM354[:, 3])

#H522
sister1 = np.zeros((1, 4), float)
sister2 = np.zeros((1, 4), float)

for icell in range(1, len(TFirstDivH522)):
    #even numbered cells
    if TFirstDivH522[icell, 2] != 0: #need sister pairs - get rid of 0th division/first cell
        if icell == len(TFirstDivH522) - 1: #if last cell
            if TFirstDivH522[icell, 1] % 2 != 0 and TFirstDivH522[icell - 1, 1] == TFirstDivH522[icell, 1] - 1:
                sister2 = np.concatenate((sister2, TFirstDivH522[icell, :].reshape(1, 4)), axis=0)
        elif icell == 1: #if first cell
            if TFirstDivH522[icell, 1] % 2 == 0 and TFirstDivH522[icell+1, 1] == TFirstDivH522[icell, 1]+1: #assure that sister cell also divides
                sister1 = np.concatenate((sister1, TFirstDivH522[icell, :].reshape(1, 4)), axis=0)
        else:
            if TFirstDivH522[icell, 1] % 2 == 0 and TFirstDivH522[icell+1, 1] == TFirstDivH522[icell, 1]+1: #assure that sister cell also divides
                sister1 = np.concatenate((sister1, TFirstDivH522[icell, :].reshape(1, 4)), axis=0)
            elif TFirstDivH522[icell, 1] % 2 != 0 and TFirstDivH522[icell-1, 1] == TFirstDivH522[icell, 1]-1:
                sister2 = np.concatenate((sister2, TFirstDivH522[icell, :].reshape(1, 4)), axis=0)

sister1 = sister1[1:, :]
sister2 = sister2[1:, :]

shortsisterH522  = np.zeros((len(sister1), 4), float)
longsisterH522  = np.zeros((len(sister1), 4), float)

for ilength in range(0, len(sister1)):
    if sister1[ilength,3] <= sister2[ilength,3]:
        shortsisterH522[ilength,:] = sister1[ilength, :]
        longsisterH522[ilength,:] = sister2[ilength, :]
    elif sister1[ilength,3] > sister2[ilength,3]:
        shortsisterH522[ilength, :] = sister2[ilength, :]
        longsisterH522[ilength, :] = sister1[ilength, :]

RatioH522 = np.divide(shortsisterH522[:, 3], longsisterH522[:, 3])

#H550
sister1 = np.zeros((1, 4), float)
sister2 = np.zeros((1, 4), float)

for icell in range(1, len(TFirstDivH550)):
    #even numbered cells
    if TFirstDivH550[icell, 2] != 0: #need sister pairs - get rid of 0th division/first cell
        if icell == len(TFirstDivH550) - 1: #if last cell
            if TFirstDivH550[icell, 1] % 2 != 0 and TFirstDivH550[icell - 1, 1] == TFirstDivH550[icell, 1] - 1:
                sister2 = np.concatenate((sister2, TFirstDivH550[icell, :].reshape(1, 4)), axis=0)
        elif icell == 1: #if first cell
            if TFirstDivH550[icell, 1] % 2 == 0 and TFirstDivH550[icell+1, 1] == TFirstDivH550[icell, 1]+1: #assure that sister cell also divides
                sister1 = np.concatenate((sister1, TFirstDivH550[icell, :].reshape(1, 4)), axis=0)
        else:
            if TFirstDivH550[icell, 1] % 2 == 0 and TFirstDivH550[icell+1, 1] == TFirstDivH550[icell, 1]+1: #assure that sister cell also divides
                sister1 = np.concatenate((sister1, TFirstDivH550[icell, :].reshape(1, 4)), axis=0)
            elif TFirstDivH550[icell, 1] % 2 != 0 and TFirstDivH550[icell-1, 1] == TFirstDivH550[icell, 1]-1:
                sister2 = np.concatenate((sister2, TFirstDivH550[icell, :].reshape(1, 4)), axis=0)

sister1 = sister1[1:, :]
sister2 = sister2[1:, :]

shortsisterH550  = np.zeros((len(sister1), 4), float)
longsisterH550  = np.zeros((len(sister1), 4), float)

for ilength in range(0, len(sister1)):
    if sister1[ilength,3] <= sister2[ilength,3]:
        shortsisterH550[ilength,:] = sister1[ilength, :]
        longsisterH550[ilength,:] = sister2[ilength, :]
    elif sister1[ilength,3] > sister2[ilength,3]:
        shortsisterH550[ilength, :] = sister2[ilength, :]
        longsisterH550[ilength, :] = sister1[ilength, :]

RatioH550 = np.divide(shortsisterH550[:, 3], longsisterH550[:, 3])

#Kruskal-Wallis test
KW_M354_H522_H550 = stats.kruskal(RatioM354, RatioH522, RatioH550)

#post-hoc tests - Dunn's test
ratiosExp3 = [RatioM354, RatioH522, RatioH550]
DT_bonferroni_Exp3 = sp.posthoc_dunn(ratiosExp3, p_adjust = 'bonferroni')

#boxplots
numcellsM3541Ratio = np.where(shortsisterM354[:, 2] == 1)
numcellsM3542Ratio = np.where(shortsisterM354[:, 2] == 2)
numcellsM3543Ratio = np.where(shortsisterM354[:, 2] == 3)
numcellsM3544Ratio = np.where(shortsisterM354[:, 2] == 4)

numcellsH5501Ratio = np.where(shortsisterH550[:, 2] == 1)
numcellsH5502Ratio = np.where(shortsisterH550[:, 2] == 2)
numcellsH5503Ratio = np.where(shortsisterH550[:, 2] == 3)
numcellsH5504Ratio = np.where(shortsisterH550[:, 2] == 4)

numcellsH5221Ratio = np.where(shortsisterH522[:, 2] == 1)
numcellsH5222Ratio = np.where(shortsisterH522[:, 2] == 2)
numcellsH5223Ratio = np.where(shortsisterH522[:, 2] == 3)
numcellsH5224Ratio = np.where(shortsisterH522[:, 2] == 4)

plt.figure()
ax = plt.subplot(111)
df = [RatioM354, RatioH550, RatioH522]
x = np.random.normal(1, 0.04, size=len(RatioM354))
plt.plot(x[numcellsM3541Ratio], RatioM354[numcellsM3541Ratio], '.', color=(255/255, 204/255, 204/255), markeredgecolor='k', zorder=10)
plt.plot(x[numcellsM3542Ratio], RatioM354[numcellsM3542Ratio], '.', color=(255/255, 102/255, 102/255), markeredgecolor='k', zorder=10)
plt.plot(x[numcellsM3543Ratio], RatioM354[numcellsM3543Ratio], '.', color=(255/255, 51/255, 51/255), markeredgecolor='k', zorder=10)
plt.plot(x[numcellsM3544Ratio], RatioM354[numcellsM3544Ratio], '.', color=(153/255, 0/255, 0/255), markeredgecolor='k', zorder=10)
x = np.random.normal(2, 0.04, size=len(RatioH550))
plt.plot(x[numcellsH5501Ratio], RatioH550[numcellsH5501Ratio], '.', color=(204/255, 229/255, 255/255), markeredgecolor='k', zorder=10)
plt.plot(x[numcellsH5502Ratio], RatioH550[numcellsH5502Ratio], '.', color=(153/255, 204/255, 255/255), markeredgecolor='k', zorder=10)
plt.plot(x[numcellsH5503Ratio], RatioH550[numcellsH5503Ratio], '.', color=(51/255, 153/255, 255/255), markeredgecolor='k', zorder=10)
plt.plot(x[numcellsH5504Ratio], RatioH550[numcellsH5504Ratio], '.', color=(0/255, 76/255, 153/255), markeredgecolor='k', zorder=10)
x = np.random.normal(3, 0.04, size=len(RatioH522))
plt.plot(x[numcellsH5221Ratio], RatioH522[numcellsH5221Ratio], '.', color=(204/255, 229/255, 255/255), markeredgecolor='k', zorder=10)
plt.plot(x[numcellsH5222Ratio], RatioH522[numcellsH5222Ratio], '.', color=(153/255, 204/255, 255/255), markeredgecolor='k', zorder=10)
plt.plot(x[numcellsH5223Ratio], RatioH522[numcellsH5223Ratio], '.', color=(51/255, 153/255, 255/255), markeredgecolor='k', zorder=10)
plt.plot(x[numcellsH5224Ratio], RatioH522[numcellsH5224Ratio], '.', color=(0/255, 76/255, 153/255), markeredgecolor='k', zorder=10)
box = plt.boxplot(df, patch_artist=True, showfliers=False)
colors = [[255/255, 255/255, 255/255], [255/255, 255/255, 255/255], [255/255, 255/255, 255/255]]
for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)
for median in box['medians']:
    median.set(color='black')
plt.axes().set_xticklabels(['M354', 'H550', 'H522'])
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.ylabel('sister cell cycle ratio')
plt.ylim([0.2, 1.1])
plotpath = 'SistersDivLengthRatioBoxplot_Exp3.pdf'
plt.savefig(plotpath)
