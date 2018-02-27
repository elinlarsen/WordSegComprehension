import sys
from collections import defaultdict
'''
Que fait ce script
Given ? algo+unit ?
1. Il lit tous les eval*.txt pour un couple algo/unit
algo = PATH/TO/ALGO/
unit = phoneme, syllable
2. Computes the mean (+other stats ?) for each feature
3. Creates summary_algo_unit.txt with these values

Then we need another one that calls this for all algo, all unit and creates a general summary (bash ?)

'''


def eval_algo_unit(path_to_algo, unit):

    PATH_FILE = path_to_algo+unit+'/'

    for i in range(10):
        summary = defaultdict(float)
        f = open(PATH_FILE+'eval'+str(i)+'.txt','r').readlines()
        for line in f :
            line = line[:-1]
            key, val = line.split('\t')
            summary[key] += float(val)

    for key in summary :
        summary[key] /= 10

    g = open(PATH_FILE+'summary.txt', 'w')
    to_write = [str(key)+'\t'+str(summary[key])+'\n' for key in summary]
    g.writelines(to_write)

    return summary


path_to_algo = sys.argv[1]
unit = sys.argv[2]
eval_algo_unit(path_to_algo, unit)
