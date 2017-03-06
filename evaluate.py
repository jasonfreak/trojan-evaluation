from itertools import permutations
from argparse import ArgumentParser
from json import load
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.mixture import GMM
from sklearn.externals.joblib import Parallel, delayed

def transfer(matrix, config):
    n_rows, n_cols = matrix.shape
    newMatrix = np.zeros(matrix.shape)

    for i in range(n_rows):
        for j in range(n_cols):
            if config['feature'][j]['compute']:
                name = config['feature'][j]['name']
                newMatrix[i,j] = reduce(lambda x,y: x+config['value'][name].get(y, 0), matrix[i,j].split('+'), 0)
            else:
                newMatrix[i,j] = np.float64(matrix[i,j])

    return newMatrix

def fahp(matrix, config):
    n_rows, n_cols = matrix.shape
    weight = np.zeros(n_cols)

    for j in range(n_cols):
        weight[j] = config['feature'][j]['weight']

    return weight

def cov(matrix, config):
    weight = np.std(matrix, axis=0) / np.abs(np.mean(matrix, axis=0))
    weight = np.nan_to_num(weight)
    weight = weight / np.sum(weight)
    return weight

def ent(matrix, config):
    absMatrix = np.abs(matrix) + 1
    percentage = absMatrix / np.sum(absMatrix, axis=0)
    entropy = - np.sum(percentage * np.log2(percentage), axis=0)
    weight = np.log2(matrix.shape[0]) - entropy
    weight = weight / np.sum(weight)
    return weight

def grey(matrix, config):
    X0 = np.max(matrix, axis=0)
    delta = np.abs(X0.reshape((1,-1)) - matrix)
    minmin = np.min(delta)
    maxmax = np.max(delta)
    corr = (minmin + config['r'] * maxmax) / (delta + config['r'] * maxmax)
    weight = np.sum(corr, axis=0)
    weight = weight / np.sum(weight)
    return weight

def main():
    parser = ArgumentParser(description='Evaluate Trojan')
    parser.add_argument('action', action='store', choices=('fahp', 'cov', 'ent', 'grey', 'bias', 'mult', 'cred'), help='Action')
    parser.add_argument('filepath', action='store', help='Filepath')
    parser.add_argument('-c', action='store', dest='configure', default='./conf/feature.json',  help='Configure File')
    parser.add_argument('-d', action='store', dest='delimiter', default='\t',  help='Delimiter')
    parser.add_argument('-s', action='append', dest='subject', default=[],  help='Subject Weighing Methods')
    parser.add_argument('-o', action='store', dest='object', default='ent',  help='Object Weighing Method')
    parser.add_argument('-l', action='store', dest='lmd', type=float, default=0.5,  help='Lambda')
    parser.add_argument('-n', action='store', dest='n_jobs', type=int, default=1,  help='Number Of Jobs')
    args = parser.parse_args()

    matrix = np.loadtxt(args.filepath, dtype=np.str, delimiter=args.delimiter)
    with open(args.configure) as f:
        config = load(f, encoding='cp936')

    newMatrix = transfer(matrix, config)

    compute = {'fahp':fahp, 'cov':cov, 'ent':ent, 'grey':grey}
    if args.action == 'bias':
        assert(args.n_jobs > 0)
        assert(len(args.subject) > 1)
        weightList = np.array(Parallel(n_jobs=args.n_jobs)(delayed(compute[action])(newMatrix, config) for action in args.subject))
        objectWeight = compute[args.object](newMatrix, config)
        sim = 1 - np.abs(weightList - objectWeight.reshape((1,-1)))
        weightList = weightList * sim
        weight = np.sum(weightList, axis=0)
        weight = weight / np.sum(weight)
    elif args.action == 'mult':
        assert(args.n_jobs > 0)
        assert(len(args.subject) == 1)
        subjectWeight = compute[args.subject[0]](newMatrix, config)
        objectWeight = compute[args.object](newMatrix, config)
        weight = subjectWeight * objectWeight
        weight = weight / np.sum(weight)
    elif args.action == 'cred':
        assert(args.n_jobs > 0)
        assert(len(args.subject) == 1)
        assert(0 < args.lmd and args.lmd < 1)
        subjectWeight = compute[args.subject[0]](newMatrix, config)
        objectWeight = compute[args.object](newMatrix, config)
        weight = subjectWeight * args.lmd + objectWeight * (1 - args.lmd)
        weight = weight / np.sum(weight)
    else:
        weight = compute[args.action](newMatrix, config) 
#    newMatrix = StandardScaler().fit_transform(newMatrix)
    newMatrix = MinMaxScaler().fit_transform(newMatrix)
    scoreList = np.dot(newMatrix, weight)
    for score in scoreList:
        print score

if __name__ == '__main__':
    main()
