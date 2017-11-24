"""
Created on Wed Mar 15 16:52:03 2017

@author: elinlarsen
"""

#import libraries
import os
import pandas as pd

# importing python scripts
os.chdir('/Users/elinlarsen/Documents/CDSwordSeg/ElinDev')
import translate
import visualize
import model
import categorize
import analyze
import read

reload(visualize)
from CDI import prop
# parameters
from CDI import df_CDI_lexical_classes
from CDI import length_type
from CDI import cat_concreteness
from CDI import cat_babiness


os.chdir('/Users/elinlarsen/Documents/CDSwordSeg_Pipeline/results/res-brent-CDS/Analysis_algos_CDI/')

# *******  parameters *****
path_res='/Users/elinlarsen/Documents/CDSwordSeg_Pipeline/results/res-brent-CDS'
path_ortho="/Users/elinlarsen/Documents/CDSwordSeg_Pipeline/recipes/childes/data/Brent/ortholines.txt"
path_gold="/Users/elinlarsen/Documents/CDSwordSeg_Pipeline/recipes/childes/data/Brent/gold.txt"

ALGOS=['tps','dibs','puddle_py','AGu', 'gold']
ALGOS_=['tps','dibs','puddle_py','AGu']
SUB=['full_corpus']
SUBS=['sub0','sub1','sub2','sub3','sub4','sub5','sub6','sub7','sub8','sub9']
lexical_classes=['nouns','function_words', 'adjectives', 'verbs', 'other']
unit="syllable"
CDI_file="CDI_data/PropUnderstandCDI.csv"
#CDI_file="CDI_data/PropProduceCDI.csv"
freq_file="/freq-words.txt"
nb_i_file="CDI_data/CDI_NbInfantByAge"
ages=range(8,19)
#ages=range(16, 31)
df_gold=analyze.freq_token_in_corpus(path_ortho)

##get lexical classes of the corpus 
df_lc_corpus=categorize.part_of_seech_tagger(path_file=path_ortho)
df_gold_lc=pd.merge(df_gold, df_lc_corpus, on="Type", how="inner")
df_gold_lc.columns=['Type', 'Freqgold', 'abbrev_tags', 'lexical_class']

# **** dictionnary
d=translate.build_phono_to_ortho(path_gold,path_ortho)
dic_corpus= translate.build_phono_to_ortho_representative(d)[0]


#algo resultas
df_tp=read.create_df_freq_by_algo_all_sub(path_res, ['full_corpus'], 'tps','syllable', freq_file="/freq-words.txt")
df_CDI=read.read_CDI_data_by_age(CDI_file, age=8, save_file=False) #age does not matter here
        

# ******* Model selection : Linear or Logistics *******

# LINEAR
results_full_corpus_ph=model.linear_algo_CDI(path_ortho,path_res,["full_corpus"], ALGOS, "phoneme", ages, CDI_file, freq_file, evaluation='true_positive', miss_inc=False)
len(results_full_corpus_ph['df_data'])

R2_ALGOs_CDI_phoneme=model.linear_algo_CDI(path_ortho,path_res,["full_corpus"], ALGOS, "phoneme", ages, CDI_file, freq_file, evaluation='true_positive', miss_inc=False)['R2']
R2_ALGOs_CDI_syllable=model.linear_algo_CDI(path_ortho,path_res,["full_corpus"], ALGOS, "syllable", ages, CDI_file, freq_file,evaluation='true_positive', miss_inc=False)['R2']

std_err_ALGOs_CDI_phoneme=model.linear_algo_CDI(path_ortho,path_res,["full_corpus"], ALGOS, "phoneme", ages, CDI_file, freq_file, evaluation='true_positive', miss_inc=False)['std_err']
std_err_ALGOs_CDI_syllable=model.linear_algo_CDI(path_ortho,path_res,["full_corpus"], ALGOS, "syllable", ages, CDI_file, freq_file, evaluation='true_positive', miss_inc=False)['std_err']

R2_lin=pd.concat([R2_ALGOs_CDI_syllable,R2_ALGOs_CDI_phoneme])
R2_lin.set_index([['TPs', 'DiBS', 'PUDDLE', 'AGu', 'Gold', 'TPs', 'DiBS', 'PUDDLE', 'AGu', 'Gold']], drop=True, inplace=True, verify_integrity=False)

std_err_lin=pd.concat([std_err_ALGOs_CDI_syllable,std_err_ALGOs_CDI_phoneme])
std_err_lin.set_index([['TPs', 'DiBS', 'PUDDLE', 'AGu', 'Gold', 'TPs', 'DiBS', 'PUDDLE', 'AGu', 'Gold']], drop=True, inplace=True, verify_integrity=False)

# correlation on phonologized forms : 
model.linear_algo_CDI_phono(path_gold,path_res, "full_corpus", ALGOS, 'syllable',ages, CDI_file,"/freq-top.txt", "true_positive", False)
    

# test evaluation on recall
R2_recall_ph=R2_ALGOs_CDI_phoneme=model.linear_algo_CDI(path_ortho,path_res,["full_corpus"], ALGOS_, "phoneme", ages, CDI_file, freq_file, evaluation='recall')
R2_recall_syl=R2_ALGOs_CDI_phoneme=model.linear_algo_CDI(path_ortho,path_res,["full_corpus"], ALGOS_, "syllable", ages, CDI_file, freq_file, evaluation='recall')


# LOGISTIC
R2_log_phoneme=model.logistic_nb_infant_algo_CDI(path_ortho,path_res, SUB, ALGOS,'phoneme', ages, CDI_file,nb_i_file ,freq_file, Test_size=0.20)['R2']
R2_log_syllable=model.logistic_nb_infant_algo_CDI(path_ortho,path_res, SUB, ALGOS,'syllable', ages,CDI_file,nb_i_file ,freq_file, Test_size=0.20) ['R2']

R2_log=pd.concat([R2_log_syllable, R2_log_phoneme])

std_err_log_ph=model.logistic_nb_infant_algo_CDI(path_ortho,path_res, SUB, ALGOS,'phoneme', ages,  CDI_file,nb_i_file ,freq_file, Test_size=0.20) ['std_err']
std_err_log_syl=model.logistic_nb_infant_algo_CDI(path_ortho,path_res, SUB, ALGOS,'syllable', ages,CDI_file,nb_i_file ,freq_file, Test_size=0.20)['std_err']

std_err_log=pd.concat([std_err_log_syl, std_err_log_ph])



# for one subcorpus (length divided by 10) => looking at the effect size of the corpus
R2_ALGOs_CDI_sub0=model.linear_algo_CDI(path_ortho,path_res,["sub0"], ALGOS, "", range(8,19), CDI_file, freq_file, evaluation='true_positive', miss_inc=False)['R2']
std_err_ALGOs_CDI_sub0=model.linear_algo_CDI(path_ortho,path_res,["sub0"], ALGOS, "", range(8,19), CDI_file, freq_file, evaluation='true_positive', miss_inc=False)['std_err']

results_sub0=model.linear_algo_CDI(path_ortho,path_res,["sub0"], ALGOS, "", range(8,19), CDI_file, freq_file, evaluation='true_positive', miss_inc=False)

len(results_sub0['df_data'])


# *******  Visualisation *******
### scatter plot

visualize.plot_algos_CDI_by_age(path_ortho,path_res, False , ALGOS +['gold'], range(8,19), CDI_file,freq_file,name_vis= "CDIScore_AlgoScore_sans_fit")

visualize.plot_algos_CDI_by_age(path_ortho,path_res, ["full_corpus"], ALGOS,[8,18], CDI_file,freq_file, name_vis="plot_all_algos")

### R2 for differents ages

# linear
#production for different ages
visualize.plot_bar_R2_algos_unit_by_age(R2_lin, std_err_lin, ages,ALGOS, ['syllable', 'phoneme'],name_vis="Correlation with infant lexicon production for 16-30-month-old")

visualize.plot_bar_R2_algos_unit_by_age(R2_lin[[13,'unit']], std_err_lin[[13,'unit']], 13,ALGOS, ['syllable', 'phoneme'],name_vis="Age 13 months")

#logistic
#production for different ages
visualize.plot_bar_R2_algos_unit_by_age(R2_log, std_err_log, ages,ALGOS, ['syllable', 'phoneme'],name_vis="Logistic Reg with infant lexicon production for 16-30-month-old ")

visualize.plot_bar_R2_algos_unit_by_age(R2_log, std_err_log, range(8,19),ALGOS, ['syllable', 'phoneme'], name_vis="LOG R2 ALGOs versus CDI with phoneme representation")

# miss included
R2_lin_missed=pd.concat([lin_missed_syll, lin_missed_ph])
std_err_missed=pd.concat([lin_missed_syll_err, lin_missed_ph_err])

visualize.plot_bar_R2_algos_unit_by_age(R2_lin_missed, std_err_missed, range(8,19), ALGOS, ['syllable', 'phoneme'],name_vis="R2 ALGOs versus CDI - syllable and phoneme - missed word by algo included")


### Lexical classes
visualize.plot_by_lexical_classes(path_res, ['full_corpus'], ['TPs'], unit,[13], lexical_classes, False, CDI_file, freq_file, name_vis="lexical_classes_TPs_13")
visualize.plot_by_lexical_classes(path_res, ['full_corpus'], ['AGu'], unit,[13], lexical_classes, False, CDI_file, freq_file, name_vis="lexical_classes_AGu_13")
visualize.plot_by_lexical_classes(path_res, ['full_corpus'], ['puddle_py'],unit, [13], lexical_classes, False, CDI_file, freq_file, name_vis="lexical_classes_puddle_py_13")
visualize.plot_by_lexical_classes(path_res, ['full_corpus'], ['dibs'], unit,[13], lexical_classes, False, CDI_file, freq_file, name_vis="lexical_classes_dibs_13")
visualize.plot_by_lexical_classes(path_res, ['full_corpus'], ['gold'], unit,[18], lexical_classes, False, CDI_file, freq_file, name_vis="lexical_classes_gold_18")

# lc gold
lexical_classes=['nouns','function_words', 'adjectives', 'verbs', 'other']
unit="syllable"
R2_lc_13_syl=visualize.plot_by_lexical_classes(path_res, ['full_corpus'], ALGOS,unit, [13], lexical_classes, False, CDI_file,
                                  freq_file, name_vis="lexical_classes_algos_13")

R2_lc_13_ph=visualize.plot_by_lexical_classes(path_res, ['full_corpus'], ALGOS,'phoneme', [13], lexical_classes, False, CDI_file,
                                  freq_file, name_vis="lexical_classes_algos_13_phoneme")
R2_lc_13=pd.concat([R2_lc_13_ph,R2_lc_13_syl])

#### algo vers gold
#when using words in CDI it should be "lexical_classes"
res_algo_gold=visualize.plot_algo_gold_lc(path_res,['full_corpus'], ['tps','dibs','puddle_py','AGu'],df_gold_lc, 'syllable',CDI_file, "lexical_class", lexical_classes, freq_file, name_vis="plot_algos_vs_gold_log_scale")
          
results_gold_TP=visualize.plot_algo_gold_lc(path_res,['full_corpus'], ['tps'],df_gold_lc, 'syllable',"", "lexical_class", lexical_classes, freq_file, name_vis="plot_TP_vs_gold_log_scale")

sup10=df_gold_lc.loc[lambda df_gold_lc: df_gold_lc.Freqgold > 10, :]
inf100=df_gold_lc.loc[lambda df_gold_lc:  df_gold_lc.Freqgold < 100, :]

pd.merge(sup10, inf100)


# no lexical class filter
res_algo_vs_gold=visualize.plot_algo_gold(path_res, ['full_corpus'], ['tps','dibs','puddle_py','AGu'], df_gold, 'syllable', CDI_file, freq_file="/freq-words.txt", name_vis="algo vs gold ")  
    

# ******** test the effect of missed word by algo  *******
lin_missed=model.linear_algo_CDI(path_ortho,path_res, ['full_corpus'], ALGOS,'syllable',[13], CDI_file ,"/freq-words.txt","true_positive",True)


# *******  EFFECT OF ... *******
### Lexical classes
R2_lexical_classes_syl=model.R2_by_parameter(path_res, ['full_corpus'], ALGOS,'syllable', [13], df_CDI_lexical_classes, "lexical_classes", CDI_file, freq_file)['R2']
R2_lexical_classes_ph=model.R2_by_parameter(path_res, ['full_corpus'], ALGOS,'phoneme', [13], df_CDI_lexical_classes, "lexical_classes", CDI_file, freq_file)['R2']
#pd.concat([R2_lexical_classes_syl,R2_lexical_classes_ph]).round(3).to_csv("correlation_CDI_algos/13_month_old/R2_lexical_classes_13_mo.txt", sep='\t', header=True)
R2_lexical_classes=pd.concat([R2_lexical_classes_syl,R2_lexical_classes_ph]).round(3)

err_lexical_classes_syl=model.R2_by_parameter(path_res, ['full_corpus'], ALGOS,'syllable', [13], df_CDI_lexical_classes, "lexical_classes", CDI_file, freq_file)['std_err']
err_lexical_classes_ph=model.R2_by_parameter(path_res, ['full_corpus'], ALGOS,'phoneme', [13], df_CDI_lexical_classes, "lexical_classes", CDI_file, freq_file)['std_err']
err_lexical_classes=pd.concat([err_lexical_classes_syl,err_lexical_classes_ph]).round(3)


visualize.plot_R2_by_parameter_for_one_age(R2_lexical_classes, err_lexical_classes, ALGOS, ['syllable', 'phoneme'],  name_vis="R2_lexical_classes")

### Type length
results_length_13_syl=model.R2_by_parameter(path_res, ['full_corpus'], ALGOS,'syllable', [13], length_type, "num_syllables", CDI_file, freq_file)
results_length_13_ph=model.R2_by_parameter(path_res, ['full_corpus'], ALGOS,'phoneme', [13], length_type, "num_syllables", CDI_file, freq_file)
R2_length_in_syl_13=pd.concat([results_length_13_syl['R2'],results_length_13_ph['R2']])
#R2_length_in_syl_13.round(3).to_csv("R2_for_length_type_in_syl_13_mo.txt", sep='\t', header=True)
err_length_in_syl=pd.concat([results_length_13_syl['std_err'],results_length_13_ph['std_err']])

res_length_13_syl=model.R2_by_parameter(path_res, ['full_corpus'], ALGOS,'syllable', [13], length_type, "num_phonemes", CDI_file, freq_file)
res_length_13_ph=model.R2_by_parameter(path_res, ['full_corpus'], ALGOS,'phoneme', [13], length_type, "num_phonemes", CDI_file, freq_file)
R2_length_in_ph_13=pd.concat([res_length_13_syl['R2'],res_length_13_ph['R2']])
err_length_in_ph_13=pd.concat([res_length_13_syl['std_err'],res_length_13_ph['std_err']])
#R2_length_in_ph_13.round(3).to_csv("R2_for_length_type_in_ph_13_mo.txt", sep='\t', header=True)

visualize.plot_R2_by_parameter_for_one_age(R2_length_in_ph_13, err_length_in_ph_13, ['TPs', 'DiBS', 'PUDDLE', 'AGu', 'Gold'], ['syllable', 'phoneme'], name_vis="R2_length_in_num_of_phonemes")


