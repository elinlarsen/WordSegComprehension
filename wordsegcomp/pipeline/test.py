#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 10 13:48:08 2018

@author: elinlarsen
"""

os.chdir('/Users/elinlarsen/GoogleDrive/PhD_elin/Projets/WordSegComprehension/wordsegcomp/pipeline/')

import read
import translate
from collections import Counter
import pandas as pd

ALGOS=['tp/relativeforward/', 'tp/absoluteforward/', 'tp/relativebackward/', 'tp/absolutebackward/', 'dibs','puddle', 'gold']
SUB=['full_corpus']
unit=['syllable', 'phoneme']
corpus='/buckeye/'

path_res='/Users/elinlarsen/GoogleDrive/PhD_elin/Projets/CDSwordSeg_Pipeline/results/'+corpus
o='/Users/elinlarsen/GoogleDrive/PhD_elin/Projets/CDSwordSeg_Pipeline/recipes/childes/data/' + corpus +'/ortholines.txt'
p='/Users/elinlarsen/GoogleDrive/PhD_elin/Projets/CDSwordSeg_Pipeline/recipes/childes/data/'+ corpus + '/gold.txt'

#for buckeye only
o='/Users/elinlarsen/GoogleDrive/PhD_elin/Projets/CDSwordSeg_Pipeline/recipes/' + corpus +'/ortholines.txt'
p='/Users/elinlarsen/GoogleDrive/PhD_elin/Projets/CDSwordSeg_Pipeline/recipes/'+ corpus + '/gold.txt'

d=translate.build_phono_to_ortho(p, o)
dic=translate.build_phono_to_ortho_representative(d)[0]



def from_text_file_to_df(file_path, path_out):
    t=read.corpus_as_list(file_path)

    freq_top=Counter(t)
    s=sorted(freq_top.items(), key=lambda pair: pair[1], reverse=True)
    df = pd.DataFrame(s)
    df.columns=['phono', 'Freq']
    
    df.to_csv("/".join((path_out, "freq-top.txt")) , sep='\t', index=False)
    return(df)


def from_segmented_to_freq_word_all(path_res, ALGOS, SUB,unit, name_segmented, dic):
    
    for SS in SUB:
        for algo in ALGOS:
            for u in unit: 
                res_folder="/".join((path_res, SS, algo,u))
                path="/".join((res_folder, name_segmented))
                
                freq_phono=from_text_file_to_df(path, res_folder)
               
                d={} # ortho dic
                for item in freq_phono['phono']:
                    if item in dic.keys():
                        d[item]=dic[item]
                phono_ortho=pd.DataFrame(list(d.items()),columns=['phono', 'Type']) 
                phono_ortho.columns=['phono', 'Type']
                freq_ortho=pd.merge(freq_phono, phono_ortho, how='inner', on=['phono'])
                
                del freq_ortho['phono']
                freq_ortho.drop_duplicates(subset='Type', keep='first',inplace=True)
                #print(freq_ortho.columns)
                #freq_ortho.sort_values(['Freq'], axis=1, ascending=False, inplace=True)
                freq_ortho.to_csv("/".join((res_folder, "freq-words.txt")) , sep='\t', index=False)
    return(freq_ortho)

df=from_segmented_to_freq_word_all(path_res, ['ag'], [''],unit, "segmented.txt", dic)
df_gold=from_text_file_to_df(path_res+'/full_corpus/gold/ortholines.txt', path_res+'/full_corpus/')