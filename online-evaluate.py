# coding:cp936
from argparse import ArgumentParser
from json import load
import numpy as np
from matplotlib import pyplot as plt

def analyze(config, scoreList, secondList, tickList):
    plt.axis([0, secondList[-1], -0.1, 1.1])
    plt.xticks(secondList, tickList, rotation=-90)
    plt.ylabel(u'定量评估结果')
    plt.xlabel(u'时间（秒）')
    plt.title(config['title'])
    plt.plot(secondList, scoreList, '.-')
    plt.show()

def f(G, i, X, Y):
    N = G['N']
    weight = np.array(N[X]['weight'][Y])
    data = N[X]['data'][Y][i,:-1]
    return np.dot(weight, data)

def g(G, i, X, Y, tickList):
    S = G['S']
    N = G['N']
    O = G['O']
    D = G['D']
    data = N[X]['data'][Y][i]
    idx = N[X]['pro'][Y]
    if data[idx] and Y not in O:
        tickList[i] = u'{second}:节点{Y}已成为据点'.format(second=tickList[i], Y=Y)
        O.add(Y)
    if data[-1] and X not in D:
        tickList[i] = u'{second}:节点{X}已被防御'.format(second=tickList[i], X=X)
        D.add(X)
    lbd = N[Y]['lambda']

    if Y in O:
        return 1
    elif X in D:
        return 0
    else:
        maxf = 0
        if X != S:
            for pri in N[X]['pri']:
                temp = g(G, i, pri, X, tickList)
                if temp > maxf:
                    maxf = temp
        return lbd * f(G, i, X, Y) + (1 - lbd) * maxf

def At(G, i):
    T = G['T']
    N = G['N']
    weight = np.array(N[T]['weight'])
    data = N[T]['data'][i,:-1]
    return np.dot(weight, data)

def A(G, i, tickList):
    T = G['T']
    S = G['S']
    N = G['N']
    lbd = G['N'][T]['lambda']
    maxf = 0
    if T != S:
        for pri in N[T]['pri']:
            temp = g(G, i, pri, T, tickList)
            if temp > maxf:
                maxf = temp
    return lbd * At(G, i) + (1 - lbd) * maxf

def main():
    parser = ArgumentParser(description='Analyze')
    parser.add_argument('dirpath', action='store', help=' Dirpath')
    parser.add_argument('-c', action='store', dest='configure', default='conf/online.json', help='Configure File')
    parser.add_argument('-d', action='store', dest='delimiter', default='\t',  help='Delimiter')
    parser.add_argument('-s', action='store', dest='second', default=10,  help='Second')

    args = parser.parse_args()
    
    with open(args.configure) as f:
        config = load(f, encoding='cp936')
    G = config['G']
    T = G['T']
    S = G['S']
    N = G['N']
    G['O'] = set(S)
    G['D'] = set()
    for node in N:
        if node == T:
            N[node]['data'] = np.loadtxt('{dirpath}/{node}.txt'.format(dirpath=args.dirpath, node=node), dtype=np.float64, delimiter=args.delimiter)
        else:
            N[node]['data'] = dict()
            for pro in N[node]['pro']:
                N[node]['data'][pro] = np.loadtxt('{dirpath}/{node}-{pro}.txt'.format(dirpath=args.dirpath, node=node, pro=pro), dtype=np.float64, delimiter=args.delimiter)

    secondList = []
    tickList = []
    scoreList = []
    for i in range(config['count']):
        secondList.append(i*args.second)
        tickList.append('{second}'.format(second=i*args.second))
        scoreList.append(A(G, i, tickList))

    analyze(config, scoreList, secondList, tickList)

if __name__ == '__main__':
    main()
