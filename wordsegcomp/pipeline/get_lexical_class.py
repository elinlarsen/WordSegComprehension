#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 14:14:22 2017

@author: elinlarsen
"""
import os 
import nltk
from nltk import tokenize
from collections import defaultdict
from nltk.data import load
import pandas as pd


def part_of_seech_tagger(path_file):
    
    text_file=open(path_file,"r")
    p = text_file.read()

    text = nltk.tokenize.word_tokenize(p)
    text_tagged=nltk.pos_tag(text)
    dic_tags=dict(text_tagged)

    tagdict_file = defaultdict(list)
    for key, value in sorted(dic_tags.iteritems()):
        tagdict_file[value].append(key)


    df_tag_file=pd.DataFrame.from_dict(dic_tags, orient='index')
    df_tag_file.columns=['abbrev_tags']
    df_tag_file['lexical_class']=df_tag_file['abbrev_tags']
    
    # to get the list of tags
    tagset=nltk.help.upenn_tagset()
    tagdict = load('help/tagsets/upenn_tagset.pickle')
    tagdict['NN'][0]
    list_tags=[]
    for t1, t2 in tagdict.values():
        list_tags.append(t1)
    df_tags=pd.DataFrame(tagdict.keys())
    df_tags.columns=['abbrev_tags']
    df_tags['def_tags']=list_tags

    df_tags['lexical_class']=['function_words', 'verbs', 'verbs', 'punc', 'verbs', 'punc', 'punc', 'verbs', 
       'function_words', 'adjectives', 'function_words', 'verbs', 'function_words', 'function_words', 'others', 
       'nouns', 'punc','punc', 'others', 'function_words', 'punc', 'function_words','others', 'function_words', 'punc', 
       'nouns', 'nouns', 'verbs', 'function_words', 'function_words', 'function_words', 'function_words', 'function_words', 'function_words', 'function_words' , 'function_words', 'function_words', 'function_words' , 'function_words', 'nouns', 'punc', 'function_words', 'function_words' , 'others', 'others']

    df_tag_file.lexical_class.replace(df_tags['abbrev_tags'].tolist(), df_tags['lexical_class'].tolist(), inplace=True)
    df_tag_file['Type']=df_tag_file.index
    df_tag_file['Type']=df_tag_file['Type'].str.lower()
    df_tag_file.reset_index(drop=True)
    
    return(df_tag_file)



