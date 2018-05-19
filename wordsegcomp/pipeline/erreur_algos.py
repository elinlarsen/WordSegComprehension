#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 18:04:12 2018

@author: elinlarsen

Detecting word over- and under- segmentation errors when they happen once per utterance

Assumption : each utterance is a ligne in a phonologized text corpus

"""


def count_segmentation_errors(segmented, gold):
    g = open(gold).read().splitlines()
    s= open(segmented).read().splitlines()
    under=0
    over=0
    error_1=0
    N_utt=len(g)
    N_utt_match=0
    for utt1, utt2 in zip(s, g):
        N_word_gold=len(utt2.split())
        N_word_seg=len(utt1.split())
        N_utt+=1
        if utt1==utt2: 
            N_utt_match+=1
        else : 
            N_word_match= len(set(utt1.split()).intersection(utt2.split()))
        if (N_word_match==N_word_seg -1) & ( N_word_seg==N_word_gold-1) : 
            under+=1
            error_1+=1
        elif (N_word_match==N_word_seg -2) & (N_word_seg== N_word_gold +1) : 
            over+=1
            error_1+=1
    
        ratio=N_utt_match/N_utt
    return([round(ratio,5),round(error_1/N_utt,4), round(under/error_1,4),round(over/error_1,4)])


        
ALGOS=['TPs', 'DiBS','PUDDLE', 'AGu']    
unit=['phoneme', 'syllable'] 
path=  "/Users/elinlarsen/Google Drive/CDSwordSeg_Pipeline/results/res-brent-CDS/full_corpus/"
with open("/Users/elinlarsen/Desktop/res_errors_algos.txt", 'a') as file_out:    
    file_out.write("algos"+ "\t"+  "unit"+ "\t" + "%MatchedUtt" + "\t" + "%1error"+ "\t" + "%Underseg" + "\t" + "%Overseg")
    file_out.write("\n")
    for a in ALGOS:  
        for u in unit : 
            file_out.write(a +"\t" + u +"\t" )
            g=path + "gold" + "/"+ u+ "/gold.txt"
            s=path + a + "/"+ u+ "/cfgold.txt"
            results=count_segmentation_errors(s, g)
            for r in results:
                file_out.write( str(r) + "\t")
            file_out.write("\n")
        
            

    
