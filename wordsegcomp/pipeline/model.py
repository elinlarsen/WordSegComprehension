#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 16:18:08 2017

@author: elinlarsen
"""

import plotly 
#plotly must have downloaded  cf https://plot.ly/python/getting-started/
# open spyder from terminal !
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import itertools

# Scientific libraries
import numpy as np
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error

#import file
import read
import analyze


def linear_algo_CDI(path_ortho,path_res, sub, algos, unit,ages, CDI_file,freq_file="/freq-words.txt", out='r2',evaluation="true_positive", miss_inc=False):
    df_r_2=pd.DataFrame(0, columns=ages, index=algos)
    df_std_err=pd.DataFrame(0, columns=ages, index=algos)
    df_gold=analyze.freq_token_in_corpus(path_ortho)
    for age in ages: 
        df_CDI=read.read_CDI_data_by_age(CDI_file, age, save_file=False)
        for algo in algos:    
            if algo=='gold': 
                df_algo=df_gold
            else : 
                tp=read.create_df_freq_by_algo_all_sub(path_res, sub, algo,unit, freq_file)
                if evaluation=='true_positive': 
                    df_algo=tp
                elif evaluation=='recall':
                    df_algo=pd.DataFrame(tp['Freq'+algo]).div(df_gold.Freqgold, axis='index') 
                    df_algo['Type']=tp['Type']
            if miss_inc :  # word not found b algo but are in the CDI also considered
                df_CDI_gold=pd.merge(df_CDI, df_gold[['Type']], on=['Type'],how='inner')
                df_data=pd.merge(df_CDI_gold, df_algo, on=['Type'], how='outer')
                df_data=df_data.dropna(subset=['lexical_classes', 'Type','prop', 'age'])
                df_data=df_data.fillna(1) # log(1)=0
            else:
                df_data=pd.merge(df_CDI, df_algo, on=['Type'], how='inner')
            x=np.log(df_data['Freq'+algo])
            y=df_data['prop']
            slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
            df_r_2.iloc[algos.index(algo), ages.index(age)]=r_value**2
            df_r_2['unit']=np.repeat(unit,len(df_r_2.index))

            df_std_err.iloc[algos.index(algo), ages.index(age)]=std_err
            df_std_err['unit']=np.repeat(unit,len(df_std_err.index))

    if out=='r2' :
        return(df_r_2)
    elif out=='std_err': 
        return(df_std_err)
    
    
### simple logistic regression 
def logistic_algo_CDI(path_ortho,path_res, sub, algos, unit,ages, CDI_file,freq_file="/freq-words.txt"):
    df_r_2_clf=pd.DataFrame(0, columns=ages, index=algos)
    df_std_err=pd.DataFrame(0, columns=ages, index=algos)
    for age in ages:  
        for algo in algos:
            df_CDI=read.read_CDI_data_by_age(CDI_file, age, save_file=False)
            if algo=='gold': 
                df_algo=analyze.freq_token_in_corpus(path_ortho)
            else : 
                df_algo=read.create_df_freq_by_algo_all_sub(path_res, sub, algo,unit, freq_file)
            df_data=pd.merge(df_CDI, df_algo, on=['Type'], how='inner')
            x=np.log(df_data['Freq'+algo])
            y=np.log(df_data['prop']/(np.repeat(1,len(df_data['prop']))-df_data['prop']))
            slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
            df_r_2_clf.iloc[algos.index(algo), ages.index(age)]=r_value**2
            df_std_err.iloc[algos.index(algo), ages.index(age)]=std_err       
    return(df_r_2_clf)


#### using proportion of infants understanding a word and number of infant for each age => getting number of infants per age understanding a word 
def logistic_nb_infant_algo_CDI(path_ortho,path_res, sub, algos, unit,ages, CDI_file, NbInfant_file="CDI_NbInfantByAge",freq_file="/freq-words.txt", Test_size=0.5, out='r2'):
    df_nb_i=pd.read_csv(NbInfant_file,sep=";")
    r_2=pd.DataFrame(0, columns=ages, index=algos)
    std_err=pd.DataFrame(0, columns=ages, index=algos)
    
    for age in ages : 
        for algo in algos : 
            nb_infant_by_age=df_nb_i.loc[df_nb_i['age'] == age].values[0][1]
            if algo=='gold': 
                df_algo=analyze.freq_token_in_corpus(path_ortho)
            else : 
                df_algo=read.create_df_freq_by_algo_all_sub(path_res, sub, algo,unit, freq_file)
            df_CDI=read.read_CDI_data_by_age(CDI_file, age, save_file=False)
            df_data=pd.merge(df_CDI, df_algo, on=['Type'], how='inner')
        
            nb_words=len(df_data)
            vec=np.repeat(nb_infant_by_age, nb_words)
  
            X=np.transpose(np.matrix(np.log(df_data['Freq'+algo]))) # LogisticRegression from scikit takes only a matrix as input
          
            y=df_data['prop'].to_frame()
            y_binary=[]
            
            for row in y.itertuples():
                if row[1]> 0.5 :
                    y_binary.append(1)
                else :
                    y_binary.append(0)
            y_t=np.transpose(np.matrix(y_binary))
            
            clf = LogisticRegression(fit_intercept = True , C = 1e9, max_iter=10000, solver='liblinear') # SAG : stochastic average gradiant, useful for big dataset (INRIA) # C : higher it is, the less it penalize
                                     
            X_train, X_test, Y_train, Y_test, vec_train, vect_test = \
            train_test_split(X, y_t, vec,test_size=Test_size, random_state=np.random.RandomState(42))
            
            clf.fit(X_train, Y_train, sample_weight=vec_train)
            y_pred=clf.predict_proba(X_test) # returns a dataframe of 2 colums : first P(X=0|X_test) and second, P(X=1|X_test)
            
            r_2.iloc[algos.index(algo), ages.index(age)]=r2_score(Y_test, y_pred[:,1])  

            r_2['unit']=np.repeat(unit,len(r_2.index))
            std_err.iloc[algos.index(algo), ages.index(age)]=mean_squared_error(Y_test, y_pred[:,1])

            std_err['unit']=np.repeat(unit,len(std_err.index))
    if out=='r2' :
        return(r_2)
    elif out=='std_err': 
        return(std_err)
    
# look at the effect of lexical class
def R2_by_lexical_class(path_res, sub, algos,unit, ages, lexical_classes, CDI_file="PropUnderstandCDI.csv", freq_file="/freq-words.txt", out="r2"):
    R2=pd.DataFrame(0, columns=lexical_classes, index=algos)
    Err=pd.DataFrame(0, columns=lexical_classes, index=algos)
    for age in ages: 
        for algo in algos:
            df_CDI=read.read_CDI_data_by_age(CDI_file, age, save_file=False)
            df_algo=read.create_df_freq_by_algo_all_sub(path_res, sub, algo,unit, freq_file)
            df_data=pd.merge(df_CDI, df_algo, on=['Type'], how='inner')
            for lc in lexical_classes:
                gb_lc=df_data.groupby('lexical_classes').get_group(lc)
                x=np.log(gb_lc['Freq'+algo])
                y=gb_lc['prop']
                
                slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)             

                R2.iloc[algos.index(algo),lexical_classes.index(lc)]=r_value**2
                Err.iloc[algos.index(algo), lexical_classes.index(lc)]=std_err
    if out=='r2' :
        return(R2)
    elif out=='std_err': 
        return(Err)
    
# look at the effect of type length
def R2_by_type_length(path_res, sub, algos,unit, ages, length_type, which_length="num_syllables", CDI_file="PropUnderstandCDI.csv", freq_file="/freq-words.txt", out="r2"):
    
    group_length=length_type.groupby(which_length, sort=True, group_keys=True).groups.keys()
    R2=pd.DataFrame(0, columns=group_length, index=algos)
    Err=pd.DataFrame(0, columns=group_length, index=algos)
    
    for age in ages: 
        for algo in algos:
            df_CDI=read.read_CDI_data_by_age(CDI_file, age, save_file=False)
            CDI_combined=pd.merge(df_CDI, length_type)
            df_algo=read.create_df_freq_by_algo_all_sub(path_res, sub, algo,unit, freq_file)
            df_data=pd.merge(CDI_combined, df_algo, on=['Type'], how='inner')
            group_length_data=df_data.groupby(which_length, sort=True, group_keys=True).groups.keys()
            for i in group_length_data:
                gb_lc=df_data.groupby(which_length).get_group(i)
                x=np.log(gb_lc['Freq'+algo])
                y=gb_lc['prop']
                
                slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)             

                R2.iloc[algos.index(algo),group_length.index(i)]=r_value**2
                Err.iloc[algos.index(algo), group_length.index(i)]=std_err
                         
    if out=='r2' :
        return(R2)
    elif out=='std_err': 
        return(Err)
            

                   