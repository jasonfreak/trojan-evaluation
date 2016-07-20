# coding:cp936
from argparse import ArgumentParser
from json import load
import numpy as np
from matplotlib import pyplot as plt

def accuracyAnalyze(config, matrix):
    start = 0
    for grade in config['gradeList']:
        grade['range'] = np.arange(start, start+grade['n_samples'])
        start += grade['n_samples']

    scatterList = []
    labelList = []
    for grade in config['gradeList']:
        scatter = plt.scatter(grade['range']+1, matrix[grade['range']], c=grade['color'], alpha=0.5)
        scatterList.append(scatter)
        labelList.append(grade['label'])

    plt.axis([0, matrix.size+2, -1, 1])
    plt.ylabel(u'评估结果')
    plt.xlabel(u'木马病毒序号')
    plt.legend(scatterList, labelList, loc='best', scatterpoints=1)
    plt.title(config['title'])
    plt.show()

def main():
    parser = ArgumentParser(description='Analyze')
    parser.add_argument('filepath', action='store', help=' Filepath')
    parser.add_argument('-c', action='store', dest='configure', default='conf/analyze.json', help='Configure File')
    parser.add_argument('-d', action='store', dest='delimiter', default='\t',  help='Delimiter')

    args = parser.parse_args()
    
    matrix = np.loadtxt(args.filepath, dtype=np.str, delimiter=args.delimiter)
    with open(args.configure) as f:
        config = load(f, encoding='cp936')

    accuracyAnalyze(config, matrix)

if __name__ == '__main__':
    main()
