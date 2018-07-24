#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 17:48:38 2018

@author: elinlarsen
"""

import translate
import analyze
import argparse


def from_segmented_to_word_frequencies(path_res, path_gold, path_ortho, algos, unit, segmented_file_name="segmented.txt"):
    """ 
    From the segmented text file, create a text file containing word correctly 
    segmented in orthographic form with their corresponding occurrences in the segmented file
    
    """
    #create segmented frequencies file in phonologized form
    for a in algos: 
        print(a)
        seq=(path_res, a, unit, segmented_file_name)
        r="/".join(seq)
        freq_top=analyze.freq_token_in_corpus(r)
        freq_top.to_csv(path_res+ 'freq-top.txt', sep="\t", index=False)
        
    #create dictionnary
    d=translate.build_phono_to_ortho(path_gold, path_ortho)
    dic=translate.build_phono_to_ortho_representative(d)[0]
    
    #create freq-word
    translate.create_file_word_freq(path_res, dic, [''], algos,unit, freq_file="/freq-top.txt")
    
    return(dic)

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--path_res", type =str, help="path of the folder containing the segmented file, will be the path of the folder containing the output file")
    
    parser.add_argument("-g", "--path_gold", type=str, help="path of the gold file : phonologized version of the corpus")
    parser.add_argument("-o", "--path_ortho", type=str, help="path of the corpus orthographically transcribed")
    parser.add_argument("-a", "--algos",nargs='*',
                                        type=str, default=['gold'],help="list of the algorithms that segmented the corpus")
    parser.add_argument("-u", "--unit", type=str, choices=['syllable','phoneme'], help="either phoneme or syllable")
    parser.add_argument("-s","--segmented_file_name", type =str, help="name of the file containing the segmented corpus ", default="segmented.txt")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", default=False, action="store_true")
    
    args = parser.parse_args()
    
    from_segmented_to_word_frequencies(args.path_res,  args.path_gold, args.path_ortho, args.algos, args.unit, args.segmented_file_name)



#CORPUS="brent/full_corpus/"
#folder directory storing the results for the correlation
#folder_res="Analysis_algos_CDI"
#algos=['baseline0', 'baseline1']
#path_data="/Users/elinlarsen/Documents/XSSeg/xsseg/raw_data/"  +CORPUS +"/"
#path_ortho=path_data +"/ortholines.txt"
#path_gold=path_data + "/gold.txt"
#path_res='/Users/elinlarsen/Documents/XSSeg/xsseg/results/' + CORPUS 
#create file with top frequented words
#path_file="/Users/elinlarsen/Documents/XSSeg/xsseg/results/fernald/utterances/XS_segmentation/syllable/"
#name_file="segmented.txt"



