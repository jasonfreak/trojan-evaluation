from argparse import ArgumentParser
from json import load
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler

def transfer(matrix, config):
    n_rows, n_cols = matrix.shape
    new_matrix = np.zeros(matrix.shape)

    for i in range(n_rows):
        for j in range(n_cols):
            if config['feature'][j]['compute']:
                name = config['feature'][j]['name']
                new_matrix[i,j] = reduce(lambda x,y: x+config['value'][name].get(y, 0), matrix[i,j].split('+'), 0)
            else:
                new_matrix[i,j] = np.float64(matrix[i,j])

    return new_matrix

def fahp(matrix, config):
    n_rows, n_cols = matrix.shape
    weight = np.zeros(n_cols)
    
    new_matrix = transfer(matrix, config)

    new_matrix = StandardScaler().fit_transform(new_matrix)

    for j in range(n_cols):
        weight[j] = config['feature'][j]['weight']

    return np.dot(new_matrix, weight)

def cov(matrix, config):
    new_matrix = transfer(matrix, config)
    weight = np.std(new_matrix, axis=0) / np.mean(new_matrix, axis=0)
    weight = np.nan_to_num(weight)
    weight = weight / np.sum(weight)
    new_matrix = StandardScaler().fit_transform(new_matrix)
    return np.dot(new_matrix, weight)

def em(matrix, weight):
    matrix = matrix.astype(np.float64)
    mean = np.mean(matrix, axis=0)
    std = np.std(matrix, axis=0)

    norm = stats.norm(mean, std)

    p = norm.pdf(matrix)

    weight = p * weight

    weight = weight / np.sum(weight, axis=1, keepdims=True)


    return np.sum(matrix * weight, axis=1)

def main():
    parser = ArgumentParser(description='Evaluate Trojan')
    parser.add_argument('action', action='store', choices=('fahp', 'cov', 'em'), help='Action')
    parser.add_argument('filepath', action='store', help='Filepath')
    parser.add_argument('-c', action='store', dest='configure', default='./conf/feature.json',  help='Configure File')
    parser.add_argument('-d', action='store', dest='delimiter', default='\t',  help='Delimiter')
    parser.add_argument('-w', action='store', dest='weight', default=1,  help='Weight')
    args = parser.parse_args()

    matrix = np.loadtxt(args.filepath, dtype=np.str, delimiter=args.delimiter)
    with open(args.configure) as f:
        config = load(f, encoding='cp936')

    if args.action == 'fahp':
        scoreList = fahp(matrix, config)
    elif args.action == 'cov':
        scoreList = cov(matrix, config)
    elif args.action == 'em':
        scoreList = em(matrix, args.weight)
    for score in scoreList:
        print score

if __name__ == '__main__':
    main()
