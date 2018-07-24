# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 11:45:59 2016

@author: elinlarsen
"""

import collections
try:
    # Python 2
    from itertools import izip
except ImportError:
    # Python 3
    izip = zip
import pandas as pd

#import file
import read



def build_phono_to_ortho(phono_file, ortho_file):
    """
    Dictionnary from phono text to ortho text
    # open ortho and gold file and check if in each line, the number of words match
    # if not, skip the line and count the error,
    # then create a dictionarry with key each phono token and value a dictionary  of ortho token with their occurence
    """
    count_errors = 0
    d=collections.defaultdict(dict)
    with open(phono_file,'r') as phono, open(ortho_file,'r') as ortho:
            for line_phono, line_ortho in izip(phono, ortho):
                line_phono = line_phono.lower().split()
                line_ortho = line_ortho.lower().split()
                if len(line_phono) != len(line_ortho):
                    count_errors += 1
                else:
                    for word_phono, word_ortho in izip(line_phono, line_ortho):
                        count_freq = d[word_phono]
                        try:
                            count_freq[word_ortho] += 1
                        except:
                            count_freq[word_ortho] = 1
    print("There were {} errors".format(count_errors))
    return d


def build_phono_to_ortho_representative(d):
    """
    list of two dictionaries:
    # 1. one of phono token and the most representative ortho token
    # 2. one linking token to their freqency
    """
    res ={}
    token_freq={}
    for d_key,d_value in d.items():
        value_max=0
        key_max = 'undefined'
        for key, value in d_value.items():
            if value > value_max:
                value_max = value
                key_max = key
        res[d_key] = key_max
        token_freq[value_max]=key_max
    #freq_token = {v: k for k, v in token_freq.iteritems()}
    freq_res=sorted(token_freq.items(),reverse=True)
    return([res,freq_res])



def create_file_word_freq(path_res, dic, sub, algos,unit="syllable", freq_file="/freq-top.txt"):
    """
    look at true positive (ie well-segmented words) in all algos and in all subs-corpus
    from "freq-file.txt" in phonological form to orthographic form
    for each result of each algo in each subcorpus, create the file in the orthographic form
    Parameters :
    -----------
    path_res : string, absolute path to the folder that will contain the results
    dic : dictionnary, created by the function build_phono_to_ortho
    sub : list, list of names of the sample of corpus
    algos : list, list of names of algorithms used in the package wordseg
    unit : string, either syllable or phoneme, default is syllable
    freq_file : string, name of the file output by wordseg containing word segmented by the algorithms ordered by frequency
    """
    for SS in sub:
        for algo in algos:
            res_folder=path_res+"/"+SS+"/"+algo+ "/" +unit
            path=res_folder +freq_file
            df_token=pd.read_table(path,sep='\s+', header=None, names=('Freq','phono'),  index_col=None)
            list_token=read.list_freq_token_per_algo(algo,SS,path_res,unit,freq_file)
            d={}
            for item in list_token:
                if item in dic.keys():
                    d[item]=dic[item]
            df_dic_token=pd.DataFrame(list(d.items()),columns=['phono', 'Type']) 
            df_dic_token.columns=['phono', 'Type']
            s=pd.merge(df_token, df_dic_token, how='inner', on=['phono'])
            del s['phono']
            s.drop_duplicates(subset='Type', keep='first',inplace=True)
            path_out=res_folder+ "/freq-words.txt"
            s.to_csv(path_out, sep='\t', index=False)
    return(s)
