#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 16:52:03 2017

@author: elinlarsen
"""

#import libraries
import os
import pandas as pd
from pandas import DataFrame
import numpy as np

# importing python scripts
os.chdir('/Users/elinlarsen/Documents/CDSwordSeg/ElinDev')
from wordsegcomp/pipeline import read
from wordsegcomp/pipeline import translate
from wordsegcomp/pipeline import analyze
from wordsegcomp/pipeline import visualize
from wordsegcomp/pipeline import model
from wordsegcomp/pipeline import robustness

import brent_cds

os.chdir('/Users/elinlarsen/Documents/CDSwordSeg_Pipeline/results/res-brent-CDS/Analysis_algos_CDI/')

# *******  parameters *****
path_res='/Users/elinlarsen/Documents/CDSwordSeg_Pipeline/results/res-brent-CDS'
ALGOS=['tps','dibs','puddle_py','AGu', 'gold']
SUB=['full_corpus']
SUBS=['sub0','sub1','sub2','sub3','sub4','sub5','sub6','sub7','sub8','sub9']
lexical_classes=['nouns','function_words', 'adjectives', 'verbs', 'other']
unit="syllable"
CDI_file="CDI_data/PropUnderstandCDI.csv"
freq_file="/freq-words.txt"
nb_i_file="CDI_data/CDI_NbInfantByAge"


# ******* Model selection : Linear or Logistics *******

# LINEAR
R2_ALGOs_CDI_phoneme=model.linear_algo_CDI(path_ortho,path_res,["full_corpus"], ALGOS, "phoneme", range(8,19), CDI_file, freq_file, out='r2', evaluation='true_positive')
R2_ALGOs_CDI_syllable=model.linear_algo_CDI(path_ortho,path_res,["full_corpus"], ALGOS, "syllable", range(8,19), CDI_file, freq_file, out='r2',evaluation='true_positive')

std_err_ALGOs_CDI_phoneme=model.linear_algo_CDI(path_ortho,path_res,["full_corpus"], ALGOS, "phoneme", range(8,19), CDI_file, freq_file, out='std_err',evaluation='true_positive')
std_err_ALGOs_CDI_syllable=model.linear_algo_CDI(path_ortho,path_res,["full_corpus"], ALGOS, "syllable", range(8,19), CDI_file, freq_file, out='std_err',evaluation='true_positive')

R2_lin=pd.concat([R2_ALGOs_CDI_syllable,R2_ALGOs_CDI_phoneme])
R2_lin.set_index([['TPs', 'DiBS', 'PUDDLE', 'AGu', 'Gold', 'TPs', 'DiBS', 'PUDDLE', 'AGu', 'Gold']], drop=True, inplace=True, verify_integrity=False)

std_err_lin=pd.concat([std_err_ALGOs_CDI_syllable,std_err_ALGOs_CDI_phoneme])
std_err_lin.set_index([['TPs', 'DiBS', 'PUDDLE', 'AGu', 'Gold', 'TPs', 'DiBS', 'PUDDLE', 'AGu', 'Gold']], drop=True, inplace=True, verify_integrity=False)

# test evaluation on recall
R2_recall_ph=R2_ALGOs_CDI_phoneme=linear_algo_CDI(path_ortho,path_res,["full_corpus"], ALGOS_, "phoneme", range(8,19), CDI_file, freq_file, out='r2', evaluation='recall')
R2_recall_syl=R2_ALGOs_CDI_phoneme=linear_algo_CDI(path_ortho,path_res,["full_corpus"], ALGOS_, "syllable", range(8,19), CDI_file, freq_file, out='r2', evaluation='recall')


# LOGISTIC
R2_log_phoneme=logistic_nb_infant_algo_CDI(path_ortho,path_res, SUB, ALGOS,'phoneme', range(8,19), CDI_file,nb_i_file ,freq_file, Test_size=0.20,out='r2')
R2_log_syllable=logistic_nb_infant_algo_CDI(path_ortho,path_res, SUB, ALGOS,'syllable', range(8,19),CDI_file,nb_i_file ,freq_file, Test_size=0.20,out='r2')

R2_log=pd.concat([R2_log_syllable, R2_log_phoneme])

std_err_log_ph=logistic_nb_infant_algo_CDI(path_ortho,path_res, SUB, ALGOS,'phoneme', range(8,19),  CDI_file,nb_i_file ,freq_file, Test_size=0.20,out='std_err')
std_err_log_syl=logistic_nb_infant_algo_CDI(path_ortho,path_res, SUB, ALGOS,'syllable', range(8,19),CDI_file,nb_i_file ,freq_file, Test_size=0.20,out='std_err')

std_err_log=pd.concat([std_err_log_syl, std_err_log_ph])


# *******  Visualisation *******
### scatter plot

visualize.plot_algos_CDI_by_age(path_ortho,path_res, False , ALGOS +['gold'], range(8,19), CDI_file,freq_file,name_vis= "CDIScore_AlgoScore_sans_fit")

visualize.plot_algos_CDI_by_age(path_ortho,path_res, ["full_corpus"], ALGOS,[8,18], CDI_file,freq_file, name_vis="plot_all_algos")

### R2 for differents ages

# linear
visualize.plot_bar_R2_algos_unit_by_age(R2_lin[[13,'unit']], std_err_lin[[13,'unit']], 13,ALGOS, ['syllable', 'phoneme'],name_vis="Age 13 months")
#logistic
visualize.plot_bar_R2_algos_unit_by_age(R2_log, std_err_log, range(8,19),ALGOS, ['syllable', 'phoneme'], name_vis="LOG R2 ALGOs versus CDI with phoneme representation")

# miss included
R2_lin_missed=pd.concat([lin_missed_syll, lin_missed_ph])
std_err_missed=pd.concat([lin_missed_syll_err, lin_missed_ph_err])

visualize.plot_bar_R2_algos_unit_by_age(R2_lin_missed, std_err_missed, range(8,19), ALGOS, ['syllable', 'phoneme'],name_vis="R2 ALGOs versus CDI - syllable and phoneme - missed word by algo included")


### Lexical classes

visualize.plot_by_lexical_classes(path_res, ['full_corpus'], ['TPs'], unit,[13], lexical_classes, save_file=False, CDI_file, freq_file, name_vis="lexical_classes_TPs_13")
visualize.plot_by_lexical_classes(path_res, ['full_corpus'], ['AGu'], unit,[13], lexical_classes, save_file=False, CDI_file, freq_file, name_vis="lexical_classes_AGu_13")
visualize.plot_by_lexical_classes(path_res, ['full_corpus'], ['puddle_py'],unit, [13], lexical_classes, save_file=False, CDI_file, freq_file, name_vis="lexical_classes_puddle_py_13")
visualize.plot_by_lexical_classes(path_res, ['full_corpus'], ['dibs'], unit,[13], lexical_classes, save_file=False, CDI_file, freq_file, name_vis="lexical_classes_dibs_13")
visualize.plot_by_lexical_classes(path_res, ['full_corpus'], ['gold'], unit,[18], lexical_classes, save_file=False, CDI_file, freq_file, name_vis="lexical_classes_gold_18")

# lc gold
lexical_classes=['nouns','function_words', 'adjectives', 'verbs', 'other']
unit="syllable"
R2_lc_13_syl=visualize.plot_by_lexical_classes(path_res, ['full_corpus'], ALGOS,unit, [13], lexical_classes, False, CDI_file,
                                  freq_file, name_vis="lexical_classes_algos_13", out="r2")
R2_lc_13_syl['unit']=np.repeat('syllable', 5)
R2_lc_13_ph=visualize.plot_by_lexical_classes(path_res, ['full_corpus'], ALGOS,'phoneme', [13], lexical_classes, False, CDI_file,
                                  freq_file, name_vis="lexical_classes_algos_13_phoneme", out="r2")
R2_lc_13_ph['unit']=np.repeat('phoneme', 5)
R2_lc_13=pd.concat([R2_lc_13_ph,R2_lc_13_syl])

#### algo vers gold
visualize.plot_algo_gold_lc(path_res,['full_corpus'], ['tps','dibs','puddle_py','AGu'],'gold', 'syllable', 'std_err',"PropUnderstandCDI.csv",lexical_classes, freq_file, name_vis="plot_algos_vs_gold_log_scale")

### Type length
R2_length_13_syl=model.R2_by_type_length(path_res, ['full_corpus'], ALGOS,'syllable', [13], length_type, "num_syllables", CDI_file, freq_file, out="r2")
R2_length_13_syl['unit']=np.repeat('syllable', 5)

R2_length_13_ph=model.R2_by_type_length(path_res, ['full_corpus'], ALGOS,'phoneme', [13], length_type, "num_syllables", CDI_file, freq_file, out="r2")
R2_length_13_ph['unit']=np.repeat('phoneme', 5)

R2_length_in_syl_13=pd.concat([R2_length_13_syl,R2_length_13_ph])
R2_length_in_syl_13.round(3).to_csv("R2_for_length_type_in_syl_13_mo.txt", sep='\t', header=True)


R2_length_13_syl=model.R2_by_type_length(path_res, ['full_corpus'], ALGOS,'syllable', [13], length_type, "num_phonemes", CDI_file, freq_file, out="r2")
R2_length_13_syl['unit']=np.repeat('syllable', 5)

R2_length_13_ph=model.R2_by_type_length(path_res, ['full_corpus'], ALGOS,'phoneme', [13], length_type, "num_phonemes", CDI_file, freq_file, out="r2")
R2_length_13_ph['unit']=np.repeat('phoneme', 5)

R2_length_in_ph_13=pd.concat([R2_length_13_syl,R2_length_13_ph])
R2_length_in_ph_13.round(3).to_csv("R2_for_length_type_in_ph_13_mo.txt", sep='\t', header=True)
