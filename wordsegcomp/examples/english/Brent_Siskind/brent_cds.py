# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 14:07:10 2016

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


# *******  path where are the data *******
path_data='/Users/elinlarsen/Documents/CDSwordSeg_Pipeline/recipes/childes/data/Brent'
path_res='/Users/elinlarsen/Documents/CDSwordSeg_Pipeline/results/res-brent-CDS'
path_tags="/Users/elinlarsen/Documents/CDSwordSeg_Pipeline/recipes/childes/data/Brent/tags.txt"
path_gold="/Users/elinlarsen/Documents/CDSwordSeg_Pipeline/recipes/childes/data/Brent/gold.txt"
path_ortho="/Users/elinlarsen/Documents/CDSwordSeg_Pipeline/recipes/childes/data/Brent/ortholines.txt"
path_to_file_CDI= "/Users/elinlarsen/Documents/CDSwordSeg_Pipeline/results/res-brent-CDS/Analysis_algos_CDI/TypesAllSubsInCDI"
nb_i_file='/Users/elinlarsen/Documents/CDSwordSeg_Pipeline/results/res-brent-CDS/Analysis_algos_CDI/CDI_NbInfantByAge.csv'
fscore='/Users/elinlarsen/Documents/CDSwordSeg_Pipeline/results/res-brent-CDS/Analysis_algos_CDI/

# enter your current directory
os.chdir('/Users/elinlarsen/Documents/CDSwordSeg_Pipeline/results/res-brent-CDS/Analysis_algos_CDI/')

# *******  parameters *****
ALGOS=['tps','dibs','puddle_py','AGu', 'gold']
#SUBS=["sub0","sub1","sub2","sub3","sub4","sub5","sub6","sub7","sub8","sub9"]
SUB=['full_corpus']
SUBS=['sub0','sub1','sub2','sub3','sub4','sub5','sub6','sub7','sub8','sub9']
lexical_classes=['nouns','function_words', 'adjectives', 'verbs', 'other']
unit="syllable"


d=translate.build_phono_to_ortho(path_gold,path_ortho)
dic_corpus= translate.build_phono_to_ortho_representative(d)[0]
freq_tokens_brent=translate.build_phono_to_ortho_representative(d)[1]


#******* Analysis of Brent *******
list_tokens=read.corpus_as_list(path_ortho)
list_syl=read.corpus_as_list(path_input_syl)
list_ph=read.corpus_as_list(path_input_phoneme)
nb_tokens=len(list_tokens)
nb_syl=len(list_syl)
nb_ph=len(list_ph)
AWL_syl=float(nb_syl)/float(nb_tokens)
AWL_ph=float(nb_ph)/float(nb_tokens)
nb_utt_brent=analyze.count_lines_corpus(path_ortho)
AUL=float(nb_tokens)/float(nb_utt_brent)
freq_brent=pd.read_table('/Users/elinlarsen/Documents/CDSwordSeg_Pipeline/results/res-brent-CDS/full_corpus/gold/freq-words.txt', sep='\t', header=0)


# Look at words in common in all sub corpus and sort by frequency
In_all_SUB=analyze.common_type_in_all_sub(SUB, path_data,name_gold="ortholines.txt")
df_in_all_sub=DataFrame(In_all_SUB.items(), columns=['Type', 'Freq'])
df_sorted=df_in_all_sub.sort('Freq', ascending=False)


# ******* Segmented words by ALGOS *******

###### Occurence of words segmented by all algos across sub
#create_file_word_freq(path_res, dic_corpus, SUBS, ALGOS, "/freq-top.txt")
translate.create_file_word_freq(path_res, dic_corpus, SUB, ALGO, unit,freq_file="/freq-top.txt")


# ******* Qualitative analyse *******

countType=analyze.count_type_segmented_per_algo_per_sub(ALGOS,SUBS,path_res,freq_file="/freq-top.txt")
countTypeSplit=analyze.count_type_well_segmented_per_algo_per_sub(dic_corpus,ALGOS,SUBS,path_res,freq_file="/freq-top.txt")

intersection_btw_algo=analyze.compare_token_btw_algo(path_res,dic_corpus,SUBS,ALGOS,"dibs","/freq-top.txt")

intersection_btw_sub=analyze.compare_token_btw_sub(path_res,dic_corpus,SUBS,sub_ref="sub0",algos=ALGOS,freq_file="/freq-top.txt")

intersection_all_sub=analyze.compare_token_all_sub(path_res,dic_corpus,sub=SUBS,algos=ALGOS,freq_file="/freq-top.txt" )

inter_all_algo=analyze.intersection_all_algo(path_res, dic_corpus, sub=SUBS,algos=ALGOS,algo_ref="dibs",freq_file="/freq-top.txt")

dibs_signature=analyze.signature_algo(path_res,dic_corpus,sub=SUBS,algo_ref="dibs",algos=ALGOS,freq_file="/freq-top.txt")
tps_signature=analyze.signature_algo(path_res,dic_corpus,sub=SUBS,algo_ref="tps",algos=ALGOS,freq_file="/freq-top.txt")
puddle_signature=analyze.signature_algo(path_res,dic_corpus,sub=SUBS,algo_ref="puddle",algos=ALGOS,freq_file="/freq-top.txt")
AGu_signature=analyze.signature_algo(path_res,dic_corpus,sub=SUBS,algo_ref="AGu",algos=ALGOS,freq_file="/freq-top.txt")

analyze.Inter_signature(dibs_signature,'dibs')
analyze.Inter_signature(puddle_signature, 'puddle')
analyze.Inter_signature(tps_signature, 'TPs')
analyze.Inter_signature(AGu_signature, 'AGu')

inter_all_algo=analyze.intersection_all_algo(path_res, dic_corpus, sub=SUBS,algos=ALGOS,algo_ref="dibs",freq_file="/freq-top.txt")

#  ******* test robustness f-score *******

mean_score_dibs=robustness.search_f_score_file_by_algo(path_res, subs=SUBS,algo='dibs',text_file="/cfgold-res.txt")
mean_score_TPs=robustness.search_f_score_file_by_algo(path_res, subs=SUBS,algo='TPs',text_file="/cfgold-res.txt")
mean_score_AGu=robustness.search_f_score_file_by_algo(path_res, subs=SUBS,algo='AGu',text_file="/cfgold-res.txt")
mean_score_puddle=robustness.search_f_score_file_by_algo(path_res, subs=SUBS,algo='puddle',text_file="/cfgold-res.txt")

# ******** test the effect of missed word by algo
lin_missed=linear_algo_CDI_miss_(path_ortho,path_res, ['full_corpus'], ALGOS,'syllable',[13],"PropUndestandCDI.csv","/freq-words.txt", out='r2',evaluation="true_positive")
