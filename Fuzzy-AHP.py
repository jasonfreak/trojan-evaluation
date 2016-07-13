from argparse import ArgumentParser
import numpy as np

def isConsistent(matrix):
    n_indicators = matrix.shape[0]
    for i in range(n_indicators):
        for j in range(n_indicators):
            for k in range(n_indicators):
                if matrix[i,j] != matrix[i, k] - matrix[j, k] + 0.5:
                    return False
    return True

def transfor(matrix):
    n_indicators = matrix.shape[0]
    r = np.sum(matrix, axis=1)
    consistencyList = np.array([])
    for i in range(n_indicators):
        for j in range(n_indicators):
            consistencyList = np.append(consistencyList, (r[i]-r[j])/(2*(n_indicators-1))+0.5)
    return consistencyList.reshape((n_indicators, n_indicators))

def compute(matrix):
    n_indicators = matrix.shape[0]
    r = np.sum(matrix, axis=1)
    if not isConsistent(matrix):
        matrix = transfor(matrix)

    weightList = np.array([])
    for i in range(n_indicators):
        weightList = np.append(weightList, (r[i]+n_indicators*1.0/2-1)/(n_indicators*(n_indicators-1)))
    return weightList

def main():
    parser = ArgumentParser(description='Computue Weights By Fuzzy-AHP')
    parser.add_argument('filepath', action='store', help='Filepath')
    parser.add_argument('-d', action='store', dest='delimiter', default='\t',  help='Delimiter')
    args = parser.parse_args()

    matrix = np.loadtxt(args.filepath, delimiter=args.delimiter)
    assert(len(matrix.shape) == 2 and matrix.shape[0] == matrix.shape[1])

    weight = compute(matrix)
    print weight

if __name__ == '__main__':
    main()


