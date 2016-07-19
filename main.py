from itertools import permutations
from argparse import ArgumentParser
from json import load
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler
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
    
    newMatrix = transfer(matrix, config)

    newMatrix = StandardScaler().fit_transform(newMatrix)

    for j in range(n_cols):
        weight[j] = config['feature'][j]['weight']

    return np.dot(newMatrix, weight)

def cov(matrix, config):
    newMatrix = transfer(matrix, config)
    weight = np.std(newMatrix, axis=0) / np.mean(newMatrix, axis=0)
    weight = np.nan_to_num(weight)
    weight = weight / np.sum(weight)
    newMatrix = StandardScaler().fit_transform(newMatrix)
    return np.dot(newMatrix, weight)

def ent(matrix, config):
    newMatrix = transfer(matrix, config)
    absMatrix = np.abs(newMatrix)
    percentage = newMatrix / np.sum(absMatrix, axis=0).reshape((1, -1))
    percentage = np.nan_to_num(percentage)
    entropy = - np.sum(percentage * np.nan_to_num(np.log2(percentage)), axis=0)
    weight = np.log2(newMatrix.shape[0]) - entropy
    weight = weight / np.sum(weight)
    newMatrix = StandardScaler().fit_transform(newMatrix)
    return np.dot(newMatrix, weight)

def em(matrix, config, compute, n_jobs):
    computeNorm = stats.norm(0, 1).pdf

    newMatrix = transfer(matrix, config)
    funcList = compute.values()

    n_components = len(funcList)
    model =GMM(n_components=n_components) 
    model.fit(newMatrix)
    rList = model.predict(newMatrix)
    pList = model.predict_proba(newMatrix)

    maxProb = 0
    bestMapping = None
    matrixList = [matrix[rList == i] for i in range(n_components)]
    for mapping in permutations(range(n_components), n_components):
        probComponent = 0
        scoreList = Parallel(n_jobs=n_jobs)(delayed(funcList[mapping[i]])(matrixList[i], config) for i in range(n_components))
        probList = np.array(map(lambda x:reduce(lambda y,z:y*computeNorm(z), x, 1), scoreList))
        weightList = np.array(map(lambda x:x.shape[0], matrixList), dtype=np.float64) / newMatrix.shape[0]
        prob = np.dot(probList, weightList)
        if prob > maxProb:
            maxProb = prob
            bestMapping = mapping


    scoreMatrix = np.array(Parallel(n_jobs=n_jobs)(delayed(funcList[bestMapping[i]])(matrix, config) for i in range(n_components))).T
    weightList = pList / np.sum(pList, axis=1).reshape((-1,1))
    return np.sum(scoreMatrix * weightList, axis=1)

def main():
    parser = ArgumentParser(description='Evaluate Trojan')
    parser.add_argument('action', action='store', choices=('fahp', 'cov', 'em', 'ent'), help='Action')
    parser.add_argument('filepath', action='store', help='Filepath')
    parser.add_argument('-c', action='store', dest='configure', default='./conf/feature.json',  help='Configure File')
    parser.add_argument('-d', action='store', dest='delimiter', default='\t',  help='Delimiter')
    parser.add_argument('-n', action='store', dest='n_jobs', type=int, default=1,  help='Delimiter')
    args = parser.parse_args()

    matrix = np.loadtxt(args.filepath, dtype=np.str, delimiter=args.delimiter)
    with open(args.configure) as f:
        config = load(f, encoding='cp936')

    compute = {'fahp':fahp, 'cov':cov, 'ent':ent}
    if args.action == 'em':
        assert(args.n_jobs > 0)
        scoreList = em(matrix, config, compute, args.n_jobs)
    else:
        scoreList = compute[args.action](matrix, config)
    for score in scoreList:
        print score

if __name__ == '__main__':
    main()
