#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 11:46:24 2017

@author: elinlarsen
"""

#import libraries
import os
import pandas as pd

# importing python scripts
os.chdir('/Users/elinlarsen/Documents/CDSwordSeg/ElinDev')

import translate
import visualize
import model

from CDI import prop
# parameters
from CDI import df_CDI_lexical_classes
from CDI import length_type
from CDI import cat_concreteness
from CDI import cat_babiness

os.chdir('/Users/elinlarsen/Documents/CDSwordSeg_Pipeline/results/res-bern-CDS/Analysis_algos_CDI/')

# *******  parameters *****
path_res='/Users/elinlarsen/Documents/CDSwordSeg_Pipeline/results/res-bern-CDS'
path_ortho="/Users/elinlarsen/Documents/CDSwordSeg_Pipeline/recipes/bernstein/data/CDS/ortho/ortholines.txt"
path_gold="/Users/elinlarsen/Documents/CDSwordSeg_Pipeline/recipes/bernstein/data/CDS/phono/gold.txt"

ALGOS=['tps','dibs','puddle','AGu', 'gold']
ALGOS_=['tps','dibs','puddle_py','AGu']
SUB=['full_corpus']
SUBS=['sub0','sub1','sub2','sub3','sub4','sub5','sub6','sub7','sub8','sub9']
lexical_classes=['nouns','function_words', 'adjectives', 'verbs', 'other']
unit="syllable" 
CDI_file="CDI_data/PropUnderstandCDI.csv"
freq_file="/freq-words.txt"
nb_i_file="CDI_data/CDI_NbInfantByAge"

d=translate.build_phono_to_ortho(path_gold,path_ortho)
dic_corpus= translate.build_phono_to_ortho_representative(d)[0]
freq_tokens_bern=translate.build_phono_to_ortho_representative(d)[1]
#save freq-word for gold

freq_gold = pd.DataFrame(freq_tokens_bern, columns=['Freq', 'Type'])
freq_gold.to_csv(path_res+ "/full_corpus/gold/freq-words.txt", sep='\t', index=False)


#check if freq-words.txt has been created for each algo
#else : 
translate.create_file_word_freq(path_res, dic_corpus, SUBS, ALGOS, "",freq_file="/freq-top.txt")

results_bernstein_sub0=model.linear_algo_CDI(path_ortho,path_res,["sub0"], ALGOS, "", range(8,19), CDI_file, freq_file, evaluation='true_positive', miss_inc=False)
