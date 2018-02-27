import sys
from collections import defaultdict
import pandas as pd

'''
What does this do

Input : PATH/TO/RESULTS/ (containing algo/unit/...)
        example :
        (+ say if there are several eval*.txt in each, or only one ?)
        '0' for 10 files, '1' for one file

Output : PATH/TO/RESULTS/summary.txt, with columns score and lines algo, and content mean for all sub or just val [not needed if just val...]
         Use  pandas DataFrame ?
'''

def read_eval(f, summary, df, i):
    for line in f :
        line = line[:-1]
        key, val = line.split('\t')
        summary[key] += float(val)
        df.loc[key][i]=float(val)
#_______________________________________________________________________________

def eval_algo_unit(path_to_algo, unit):

    PATH_FILE = path_to_algo+unit+'/'
    summary = defaultdict(float)
    df = pd.DataFrame(index=keys, columns=[i for i in range(10)])
    if sys.argv[2] is '0':

        for i in range(10):
            f = open(PATH_FILE+'eval'+str(i)+'.txt','r').readlines()
            read_eval(f, summary, df, i)

        for key in summary :
            summary[key] /= 10
        df['mean']=df.mean(axis=1)
    else :
        f = open(PATH_FILE+'eval.txt','r').readlines()
        read_eval(f, summary)


    g = open(PATH_FILE+'summary.txt', 'w')
    to_write = [str(key)+'\t'+str(summary[key])+'\n' for key in summary]
    g.writelines(to_write)
    # print(df)
    df.to_csv(PATH_FILE+'summary_csv.txt')
    # print(path_to_algo, summary, '\n')
    return summary
#_______________________________________________________________________________


PATH_RES = sys.argv[1]
eval_res = [[],[]]
# ALGOS = ['ag', 'baseline', 'dibs', 'dpseg', 'puddle', 'tp/absoluteforward', 'tp/absolutebackward', 'tp/relativeforward', 'tp/relativebackward']
ALGOS = ['baseline', 'dibs', 'dpseg', 'puddle', 'tp/absoluteforward', 'tp/absolutebackward', 'tp/relativeforward', 'tp/relativebackward']
# ALGOS = ['baseline', 'dibs', 'dpseg', 'puddle', 'tp/absoluteforward', 'tp/absolutebackward', 'tp/relativeforward']

# ALGOS = ['baseline', 'dibs', 'dpseg', 'puddle', 'tp/relativeforward']
# ALGOS = ['tp/absolutebackward']
UNITS = ['phoneme', 'syllable']
global keys
keys = ["type_fscore", "type_recall", "type_precision", "token_fscore",
"token_recall", "token_precision", "boundary_fscore", "boundary_recall", "boundary_precision"]
for algo in ALGOS:
    for unit in UNITS:
        if unit=='phoneme':

            eval_res[0].append(eval_algo_unit(PATH_RES+algo+'/', unit))
        else :
            eval_res[1].append(eval_algo_unit(PATH_RES+algo+'/', unit))


for unit in UNITS:
    df = pd.DataFrame(index=ALGOS, columns=keys)
    f_res = open(PATH_RES+'eval_'+unit+".txt", 'w')

    f_res.write('algorithm'+'\t'+'\t'.join(([key for key in keys])))
    f_res.write('\n')
    if unit=='phoneme':
        for i in range(len(ALGOS)):
            f_res.write(ALGOS[i]+'\t'+'\t'.join(([str('%.2g' % eval_res[0][i][key]) for key in keys])))
            f_res.write('\n')
            for key in keys :
                df.loc[ALGOS[i]][key] = eval_res[0][i][key]
        df.to_csv(PATH_RES+'eval_'+unit+"_csv.txt")
        print(df)
    else :
        for i in range(len(ALGOS)):
            f_res.write(ALGOS[i]+'\t'+'\t'.join(([str('%.2g' % eval_res[1][i][key]) for key in keys])))
            f_res.write('\n')
            for key in keys :
                df.loc[ALGOS[i]][key] = eval_res[0][i][key]
        df.to_csv(PATH_RES+'eval_'+unit+"_csv.txt")
