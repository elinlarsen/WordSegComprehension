#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 19:52:01 2017

@author: elinlarsen
"""

# check if the effect of age detected on R2 is due to the imprecision on the number of infant in the CDI
# idea : subsample the number of infant atage 13 take a subsample that has a size equivalent to age 8
# script  in R 'Sample_CDI_infant_age_13.R'
import os 
import pandas as pd
import numpy as np

import read
os.chdir('/Users/elinlarsen/Documents/CDSwordSeg/ElinDev/')
reload(read)

os.chdir('/Users/elinlarsen/Documents/CDSwordSeg_Pipeline/CDI_wordbank/')

prop_13_sample=pd.read_csv("prop_13_sample.csv")

prop_13_sample.drop(df.columns[[0]], axis=1)

prop_13_sample=prop_13_sample[[1,2]]
prop_13_sample.columns = ['Type', 'prop']
prop_13_sample['age']=np.repeat(13, len(prop_13_sample))

prop_13_sample.to_csv("PropUnderstandCDI_13_sample.csv", sep='\t', index=False)

R2_ALGOs_CDI_phoneme_13_sample=linear_algo_CDI(path_ortho,path_res,["full_corpus"], ALGOS, "phoneme", [13], CDI_file="PropUnderstandCDI_13_sample.csv", freq_file="/freq-words.txt", out='r2', evaluation='true_positive')

R2_ALGOs_CDI_syllable_13_sample=linear_algo_CDI(path_ortho,path_res,["full_corpus"], ALGOS, "syllable", [13], CDI_file="PropUnderstandCDI_13_sample.csv", freq_file="/freq-words.txt", out='r2',evaluation='true_positive')


std_err_ALGOs_CDI_phoneme_13_sample=linear_algo_CDI(path_ortho,path_res,["full_corpus"], ALGOS, "phoneme", [13], CDI_file="PropUnderstandCDI_13_sample.csv", freq_file="/freq-words.txt", out='std_err',evaluation='true_positive')

std_err_ALGOs_CDI_syllable_13_sample=linear_algo_CDI(path_ortho,path_res,["full_corpus"], ALGOS, "syllable", [13], CDI_file="PropUnderstandCDI_13_sample.csv", freq_file="/freq-words.txt", out='std_err',evaluation='true_positive')
