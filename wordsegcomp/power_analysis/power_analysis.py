#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 16:43:11 2017
@author: elinlarsen
"""

#import libraries
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import ttest_ind

# importing python scripts
os.chdir('/Users/elinlarsen/Documents/CDSwordSeg/ElinDev')
reload(visualize)
import translate
import visualize
import model
import categorize
import analyze
import read


os.chdir('/Users/elinlarsen/Documents/CDSwordSeg_Pipeline/results/res-brent-CDS/Analysis_algos_CDI/')

# *******  parameters *****
path_res='/Users/elinlarsen/Documents/CDSwordSeg_Pipeline/results/res-brent-CDS'
path_ortho="/Users/elinlarsen/Documents/CDSwordSeg_Pipeline/recipes/childes/data/Brent/ortholines.txt"
path_gold="/Users/elinlarsen/Documents/CDSwordSeg_Pipeline/recipes/childes/data/Brent/gold.txt"

ALGOS=['tps','dibs','puddle_py','AGu', 'gold']
ALGOS_=['tps','dibs','puddle_py','AGu']
SUB=['full_corpus']
lexical_classes=['nouns','function_words', 'adjectives', 'verbs', 'other']
unit="syllable"
CDI_file="CDI_data/PropUnderstandCDI.csv"
freq_file="/freq-words.txt"
nb_i_file="CDI_data/CDI_NbInfantByAge"
ages=range(8,19)
df_gold=analyze.freq_token_in_corpus(path_ortho)

##get lexical classes of the corpus 
df_lc_corpus=categorize.part_of_seech_tagger(path_file=path_ortho)
df_gold_lc=pd.merge(df_gold, df_lc_corpus, on="Type", how="inner")
df_gold_lc.columns=['Type', 'Freqgold', 'abbrev_tags', 'lexical_class']

#POWER ANALYSIS
born_inf=  5
born_sup= 5.85

born_inf_lf=  0
born_sup_lf= 4.3

born_inf_hf=  5
born_sup_hf= 6

## step 1: determine two groups of word that vary in frenquency in TP bu not un the gold,  HF (high frequency), LF : low frequency
#function that select word in an interval 
def subset_data(born_inf, born_sup, dat, column_to_subset):
    sup=dat.loc[lambda dat: np.log(dat[column_to_subset]) > born_inf, :]
    inf=dat.loc[lambda dat:  np.log(dat[column_to_subset]) < born_sup, :]
    gp=pd.merge(sup, inf)
    
    stat=pd.DataFrame()
    stat['mean']=gp.mean()
    stat['std_dev']=gp.std()
    
    res={}
    res['data']=gp
    res['stat']=stat
    
    return(res)

def get_two_freq_group(born_inf, born_sup, born_inf_lf, born_sup_lf, born_inf_hf, born_sup_hf,
                       path_res, sub=['full_corpus'], algo=['TPs'], df_gold=df_gold, unit='syllable', 
                       CDI_file="CDI_data/PropUnderstandCDI.csv",  name_vis="TPs vs gold "): 

    res_algo_vs_gold=visualize.plot_algo_gold(path_res, sub, [algo], df_gold, unit, CDI_file,"/freq-words.txt", name_vis)  

    dat=res_algo_vs_gold['data'][['Type', 'Freqgold', 'Freq'+algo]]

    np.log(dat[['Freqgold', 'Freq'+algo]]).hist()

    #get all the words in the interval [born_inf, born_sup]
    gp_gold=subset_data(born_inf, born_sup,dat, 'Freqgold')
    
    # slipt this group in two group : high and low frequency in TP
    hf_tp=subset_data(born_inf_hf, born_sup_hf,gp_gold['data'],  'Freq'+algo)
    lf_tp=subset_data(born_inf_lf, born_sup_lf,gp_gold['data'],  'Freq'+algo)
    
    hf_tp['data'].hist()
    lf_tp['data'].hist()
    
    #test the signifant difference between the two groups for the words in the corpus (gold) and for the word segmented by the algo
    print ttest_ind(hf_tp['data']['Freqgold'],lf_tp['data']['Freq'+algo] )
    print ttest_ind(hf_tp['data']['Freqgold'],lf_tp['data']['Freqgold'] )
    
    subset={}
    subset['gold']=gp_gold
    subset['HF']=hf_tp
    subset['LF']=lf_tp
    
    return(subset)

tp_subset=get_two_freq_group(born_inf, born_sup, born_inf_lf, born_sup_lf, born_inf_hf, born_sup_hf,
                       path_res, ['full_corpus'], 'TPs', df_gold, 'syllable', 
                       CDI_file,  "TPs vs gold ")

agu_subset=get_two_freq_group(born_inf, born_sup, born_inf_lf, born_sup_lf, born_inf_hf, born_sup_hf,
                       path_res, ['full_corpus'], 'AGu', df_gold, 'syllable', 
                       CDI_file,  "TPs vs gold ")


'''
lf.to_csv("LF_11-70.txt", sep='\t')
hf.to_csv("HF_158-250.txt", sep='\t')
'''

## step 2 : determine the effect size by looking at the mean diffeence of prediction by TP 
#for two groups of words : HF (high frequency), LF : low frequency

# get the predicted proportion of infants at age 13 understand the words in the two groups
tp_reg_info=model.linear_algo_CDI(path_ortho,path_res, ['full_corpus'], ['TPs'], 'syllable',[13], CDI_file,freq_file="/freq-words.txt", evaluation="true_positive", miss_inc=False)['regression']
agu_reg_info=model.linear_algo_CDI(path_ortho,path_res, ['full_corpus'], ['AGu'], 'syllable',[13], CDI_file,freq_file="/freq-words.txt", evaluation="true_positive", miss_inc=False)['regression']
    

def get_fitted_prop_lin_reg(regression_info, algo, group_tp):
    fitted_prop=regression_info['slope'][0]*np.log(group_tp['data']['Freq'+algo])+regression_info['intercept'][0]*np.repeat(1,len(group_tp['data']['Freq'+algo]))
    fitted_prop=fitted_prop.to_frame()
    fitted_prop.columns=['fitted_prop']
    fitted_prop['Type']=group_tp['data']['Type']
    fitted_prop['Freq'+algo]=group_tp['data']['Freq'+algo]
    fitted_prop['logFreq'+algo]=np.log(group_tp['data']['Freq'+algo])
    
    return(fitted_prop)
    
#tp
tp_hf_fitted=get_fitted_prop_lin_reg(tp_reg_info, 'TPs', tp_subset['HF'])
tp_lf_fitted=get_fitted_prop_lin_reg(tp_reg_info, 'TPs', tp_subset['LF'])

#agu
agu_hf_fitted=get_fitted_prop_lin_reg(agu_reg_info, 'AGu', agu_subset['HF'])
agu_lf_fitted=get_fitted_prop_lin_reg(agu_reg_info, 'AGu', agu_subset['LF'])


# t test testing the signifance difference of mean of two independant samples. Null hyp : mean of sample are equal
# if pvalue <0.05, the null is rejected with 5% of error 
ttest_ind(tp_lf_fitted['fitted_prop'],tp_hf_fitted['fitted_prop'] )

ttest_ind(agu_lf_fitted['fitted_prop'],agu_hf_fitted['fitted_prop'] )

ttest_ind(tp_hf_fitted['fitted_prop'],agu_hf_fitted['fitted_prop'] )
ttest_ind(tp_lf_fitted['fitted_prop'],agu_lf_fitted['fitted_prop'] )

# correlation with CDI at age 13
df_CDI=read.read_CDI_data_by_age(CDI_file, age=13, save_file=False)
tp_cdi_hf=pd.merge(df_CDI, tp_hf_fitted, on='Type', how='inner')[['Type', 'prop', 'fitted_prop']]
tp_cdi_lf=pd.merge(df_CDI, tp_lf_fitted, on='Type', how='inner')[['Type', 'prop', 'fitted_prop']]


agu_cdi_hf=pd.merge(df_CDI, agu_hf_fitted, on='Type', how='inner')[['Type', 'prop', 'fitted_prop']]
agu_cdi_lf=pd.merge(df_CDI, agu_lf_fitted, on='Type', how='inner')[['Type', 'prop', 'fitted_prop']]


ttest_ind(agu_cdi_lf['prop'],agu_cdi_lf['fitted_prop'])
ttest_ind(tp_cdi_lf['prop'],tp_cdi_lf['fitted_prop'])

np.corrcoef(agu_cdi_lf['prop'],agu_cdi_lf['fitted_prop'])

np.corrcoef(tp_cdi_hf['prop'],tp_cdi_hf['fitted_prop'])
np.corrcoef(agu_cdi_hf['prop'],agu_cdi_hf['fitted_prop'])

# effect size : cohen's d: 
    
def cohens_d(m1, m2, s1, s2, N1,N2): 
    n1=N1-1
    n2=N2-1
    n=N1+N2
    
    m=m1-m2
    s=(n1*s1**2+n2*s2**2)/n
    
    c=m/sqrt(s)
    return(c)


def hedges_g(m1, m2, s1, s2, N1,N2): 
    n1=N1-1
    n2=N2-1
    n=N1+N2-2
    m=m1-m2
    s=(n1*s1**2+n2*s2**2)/n  
    c=m/sqrt(s)
    return(c)

#size of the correlation effect between the algo lexicon and the prop of infant understanding words
g_tp_prop_hf=hedges_g(tp_cdi_hf['prop'].mean(),tp_cdi_hf['fitted_prop'].mean(), tp_cdi_hf['fitted_prop'].std(), tp_cdi_hf['prop'].std(), len(tp_cdi_hf['fitted_prop']), len(tp_cdi_hf['prop']))
g_tp_prop_lf=hedges_g(tp_cdi_lf['prop'].mean(),tp_cdi_lf['fitted_prop'].mean(), tp_cdi_lf['fitted_prop'].std(), tp_cdi_lf['prop'].std(), len(tp_cdi_lf['fitted_prop']), len(tp_cdi_lf['prop']))

g_agu_prop_hf=hedges_g(agu_cdi_hf['prop'].mean(),agu_cdi_hf['fitted_prop'].mean(), agu_cdi_hf['fitted_prop'].std(), agu_cdi_hf['prop'].std(), len(agu_cdi_hf['fitted_prop']), len(agu_cdi_hf['prop']))
g_agu_prop_lf=hedges_g(agu_cdi_lf['prop'].mean(),agu_cdi_lf['fitted_prop'].mean(), agu_cdi_lf['fitted_prop'].std(), agu_cdi_lf['prop'].std(), len(agu_cdi_lf['fitted_prop']), len(agu_cdi_lf['prop']))

g_tp_lf_hf=hedges_g(tp_cdi_hf['fitted_prop'].mean(),tp_cdi_lf['fitted_prop'].mean(), tp_cdi_hf['fitted_prop'].std(), tp_cdi_lf['fitted_prop'].std(), len(tp_cdi_hf['fitted_prop']), len(tp_cdi_lf['fitted_prop']))
g_agu_lf_hf=hedges_g(agu_cdi_hf['fitted_prop'].mean(),agu_cdi_lf['fitted_prop'].mean(), agu_cdi_hf['fitted_prop'].std(), agu_cdi_lf['fitted_prop'].std(), len(tp_cdi_hf['fitted_prop']), len(agu_cdi_lf['fitted_prop']))

## step 3: determine the sample size required to get a significant difference between the two groups of words 
# predicting proportion of infants understanding a word