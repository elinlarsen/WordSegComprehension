#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 15:51:05 2017

@author: elinlarsen
"""

#test correlation between results

import pandas as pd
import os

# Scientific libraries
import numpy as np
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error


path='/Users/elinlarsen/Documents/CDSwordSeg_Pipeline/results/res-brent-CDS/Analysis_algos_CDI/13mois/'


# reading results
token_f_score=pd.read_table(path+'token_fscore.txt', sep='\t', header=0, index_col=False)
lexicon_f_score=pd.read_table(path+'lexicon_f_score.txt', sep='\t', header=0,index_col=False)
boundary_f_score=pd.read_table(path+'boundary_fscore.txt', sep='\t', header=0, index_col=False)
R2=pd.read_table(path+'R2.txt', sep='\t', header=0, index_col=False)

results=pd.merge(token_f_score, lexicon_f_score, on =['algos', 'unit'], how='inner')

token_prec=pd.read_table(path+'token_prec.txt', sep='\t', header=0, index_col=False)
token_recall=pd.read_table(path+'token_recall.txt', sep='\t', header=0, index_col=False)

lexicon_prec_=pd.read_table(path+'lexicon_prec.txt', sep='\t', header=0, index_col=False)
lexicon_prec_=lexicon_prec_[['algos', 'lexicon_prec', 'unit']]
lexicon_recall_=pd.read_table(path+'lexicon_recall.txt', sep='\t', header=0, index_col=False)

boundary_fscore=pd.read_table(path+'boundary_fscore.txt', sep='\t', header=0, index_col=False)
boundary_prec=pd.read_table(path+'boundary_prec.txt', sep='\t', header=0, index_col=False)
boundary_recall=pd.read_table(path+'boundary_recall.txt', sep='\t', header=0, index_col=False)

# building the table of all results combined 
results=pd.merge(results, R2, on=['algos', 'unit'], how='inner')
results=pd.merge(results, boundary_fscore, on=['algos', 'unit'], how='inner')
results=pd.merge(results, boundary_prec, on=['algos', 'unit'], how='inner')
results=pd.merge(results, boundary_recall, on=['algos', 'unit'], how='inner')

results=pd.merge(results, token_prec, on=['algos', 'unit'], how='inner')
results=pd.merge(results, token_recall, on=['algos', 'unit'], how='inner')

results=pd.merge(results, lexicon_prec_, on=['algos', 'unit'], how='inner')
results=pd.merge(results, lexicon_recall_, on=['algos', 'unit'], how='inner')

#saving the final table 
results.to_csv('table_results_metrics.txt', sep='\t', header=True, index=False)



## Spearman correlation
stats.spearmanr(results['lexicon'], results['R2'], axis=0)
stats.spearmanr(results['lexicon_recall'], results['R2'], axis=0)
stats.spearmanr(results['lexicon_prec'], results['R2'], axis=0)

stats.spearmanr(results['token_recall'], results['R2'], axis=0)
stats.spearmanr(results['token_prec'], results['R2'], axis=0)
stats.spearmanr(results['token'], results['R2'], axis=0)


stats.spearmanr(results['boundary'], results['R2'], axis=0)
stats.spearmanr(results['boundary_prec'], results['R2'], axis=0)
stats.spearmanr(results['boundary_recall '], results['R2'], axis=0)

stats.spearmanr(results['boundary'], results['token'])

## pearson correlation 
stats.pearsonr(results['lexicon'], results['token'])
stats.pearsonr(results['boundary'], results['token'])

stats.pearsonr(results['lexicon'], results['R2'])
stats.pearsonr(results['lexicon_prec'], results['R2'])
stats.pearsonr(results['lexicon_recall'], results['R2'])

stats.pearsonr(results['R2'], results['token'])
stats.pearsonr(results['R2'], results['token_prec'])
stats.pearsonr(results['R2'], results['token_recall'])

stats.pearsonr(results['R2'], results['boundary'])
stats.pearsonr(results['R2'], results['boundary_prec'])
stats.pearsonr(results['R2'], results['boundary_recall '])

