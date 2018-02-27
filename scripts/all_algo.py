#!/usr/bin/env python

import json
import sys
import argparse
import copy

from wordseg.evaluate import evaluate
from wordseg.prepare import prepare, gold
from wordseg.algos import tp, puddle, dibs, baseline, dpseg
from wordseg.statistics import CorpusStatistics
from wordseg.separator import Separator

import time
import datetime

PATH = "/Users/gladysbaudet/Desktop/PFE/"
PATH_RES = PATH+"Results/"+sys.argv[3]+"/"

'''
ARGS : TODO to do in parse_args
1 - corpus (tags.txt)
2 - number sub (if number)
3 - corpus (full_corpus, 10k...100k)
# 4 - algo (?)
4 - unit

'''

#______________________________________________________________________________

def stats(f):
    info.write("Computing statistics"+'\n')
    stats = CorpusStatistics(text, separator).describe_all()
    f.write(
        '* Statistics\n\n' +
        json.dumps(stats, indent=4) + '\n')
#______________________________________________________________________________


def compute(algo, *args):
    '''
    When using this method :
        - info is open
        - f is open
        - prepared is known
        - gold is known
        - score_list is known
    '''
    init = time.time()
    info.write("starting "+algo.__name__+"\n")
    segmented = algo.segment(prepared, *args)
    if algo is tp :
        name = args[0]+args[1]
        g = open(PATH_RES+algo.__name__.split('.')[-1]+"/"+name+"/"+sep_unit+"/segmented"+sys.argv[2]+'.txt', 'w')

    else :
        g = open(PATH_RES+algo.__name__.split('.')[-1]+"/"+sep_unit+"/segmented"+sys.argv[2]+'.txt', 'w') ## TODO put number in name
    seg_to_process = list(segmented)
    seg_to_process_line = [s+'\n' for s in seg_to_process]
    # seg = seg_to_process[:]
    g.writelines(seg_to_process_line)

    evaluation = evaluate(seg_to_process, gold)
    info.write(algo.__name__+" done\n")
    info.write(str(time.time()-init)+'\n')
    f.write(algo.__name__+"\t"+'\t'.join((['%.2g' % evaluation[score] for score in score_list]))+'\n')
#______________________________________________________________________________

def compute_all(algos):
    for algo in algos: #algos = [*algo]
        if algo is tp : # we need to distinguish rel/abs, for/back
            for threshold in ["relative", "absolute"]:
                for proba in ["forward", "backward"]:
                    print(threshold, proba)
                    compute(algo, threshold, proba)
                    print(threshold, proba)
        elif algo is dibs : # summary needed
            summary = dibs.CorpusSummary(text[:200])
            compute(algo, summary)
        elif algo is puddle : # window depends on unit
            if sep_unit is 'syllable':
                compute(algo,1)
            else :
                compute(algo)
        else :
            compute(algo)
        print(algo.__name__+" done\n")
#______________________________________________________________________________


def main():
    global now
    now = datetime.datetime.now()
    print(time.asctime( time.localtime(time.time()) ))

    # # # 'tp_forward_rel', 'tp_backward_rel', 'tp_forward_abs', 'tp_backward_abs', 'puddle', 'dibs'
    # parser = argparse.ArgumentParser(description='')
    # args = parser.parse_args()

    global text
    text = open(sys.argv[1], 'r').readlines()
    global info
    info = open(PATH_RES+"info.txt", 'a')
    global f
    f = open(PATH_RES+'eval'+sys.argv[2]+'.txt', 'a') #TODO put number in name instead of str(now.hour), str(now.minute)

    global sep_unit
    # sep_unit = 'phone'
    sep_unit = sys.argv[4]
    # if args.unit :
    #     if args.unit is 's':
    #         sep_unit = 'syllable'

    global score_list
    score_list = ["type_fscore", "type_recall", "type_precision", "token_fscore",
    "token_recall", "token_precision", "boundary_fscore", "boundary_recall", "boundary_precision"]

    head = ['Algorithm']
    head.extend(score_list)

    f.write(
        '\n* Evaluation '+str(sep_unit)+'\n\n' +
        '\t'.join((head)) + '\n' +
        '\t'.join(('-'*14, '-'*14, '-'*14, '-'*14, '-'*14, '-'*14, '-'*14, '-'*14, '-'*14, '-'*14)) + '\n')

    algos = [tp, dibs, puddle, baseline]
    # algos = [baseline]
    # algos = [dpseg]
    # algos_ = [TP, DiBS, PUDDLE]
    # algos = [dibs]
    # algos = [tp]
    # if args.algos :
    #     algos = args.algos



    global separator
    separator = Separator(phone=' ', syllable=';esyll', word=';eword')
    # if args.stats :
    #     stats(f) #or other than f...

    if sep_unit=="phoneme":
        sep = "phone"
    else :
        sep = sep_unit
    global prepared
    prepared = list(prepare(text, unit=sep)) #unit='phone'

    global gold
    gold = list(gold(text))

    compute_all(algos)


    print(time.asctime( time.localtime(time.time()) ))

if __name__ == '__main__':
    main()



'''
By default :
- does not compute statistics
- all algorithms
- for phones
- only output is eval
- every log is written in info
- gold and prepared are computed here


Needed :
-a --algos [*algo] : compute these algorithms (all by default)
-g --gold [path/to/gold] : computed gold
-i --input : directory in which to find tags.txt [,gold.txt, prepared.txt]
-l --language : language of the corpus
-o --output : directory in which to write outputs
-p --prepared [path/to/prepared] : computed prepared
-r --res : generates segmented outputs
-s --stats : compute statistics
-u --unit [s/p]: compute with phones/syllables
-v --verbose : all in info on terminal (?)
'''
