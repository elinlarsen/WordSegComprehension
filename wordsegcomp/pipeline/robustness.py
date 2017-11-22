#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 17:40:33 2017

@author: elinlarsen
"""

import pandas as pd


# stability of f-score on 10 sub-corpus (corpus divided in 10 linearly -same number of utterances in each)
def search_f_score_file_by_algo(path_res, subs,algo,text_file="/cfgold-res.txt"):
    list_score=[]
    for SS in subs:
        path=path_res+"/"+SS+"/"+algo+text_file
        df=pd.read_csv(path,delim_whitespace=True, header=0)
        df['sub']=SS
        list_score.append(df)
    list_score=pd.concat(list_score, axis=0)
    mean = pd.Series(list_score.mean(0), index=list_score.columns)
    std =pd.Series(list_score.std(0), index=list_score.columns)
    result = list_score.append(mean, ignore_index=True)
    result = result.append(std, ignore_index=True)
    return(result)


"""
TODO :  stability of the correlation with CDI over the 10 subcorpus
"""
