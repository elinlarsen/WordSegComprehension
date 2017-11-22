# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 11:39:15 2016

@author: elinlarsen
"""
### importing libraries

import glob
import pandas as pd


#########################  MERGE data files (ortholines, tags, gold) of each child to get a big corpus
def merge_data_files(corpus_path, name_corpus, name_file):
    ''' name_file ="/ortholines.txt", "/tags.txt", "/gold.txt" '''
    ''' the output is writtent in the current working directory'''
    path=corpus_path + "*" + "/"+ name_file
    for file in glob.glob(path):
        with open(file,'r') as infile:
            with open(corpus_path+name_file,'a') as outfile:
                for line in infile:
                    outfile.write(line)

######################### OPEN TEXT FILE AS LIST OF TOKEN
def corpus_as_list(corpus_file):
    ''' open a text file and form a list of tokens'''
    list_corpus=[]
    with open(corpus_file,'r') as text:
        for line in text:
            for word in line.split():
                list_corpus.append(word)
    return(list_corpus)

######################### OPEN FREQ FILE AS A LIST OF TOKEN
def list_freq_token_per_algo(algo,sub,path_res,unit="syllable",freq_file="/freq-top.txt"):
    algo_list=[]
    res_folder= path_res+"/"+sub+"/"+algo+ "/" + unit
    if algo!="ngrams":
    ### read only the second columns: top frequent phonological type segmented
        with open(res_folder + freq_file) as inf:
            for line in inf:
                parts = line.split() # split line into parts
                if len(parts) > 1:   # if at least 2 parts/columns
                    #if parts[0]>1:
                    algo_list.append(parts[1])
    else :
        with open(res_folder +freq_file) as inf:
            for line in inf:
                parts = line.split() # split line into parts
                if len(parts) > 2:   # if at least 3 parts/columns
                    #if parts[0]>1:
                    algo_list.append(parts[2])
    #res=[algo_list,len(algo_list)]
    res=algo_list
    return(res)

######################### read the CDI database
#create a dataframe of CDI words for the age wanted

def clean_CDI(CDI_file,save_file=True):
    '''remove the regular expression * '''
    df_CDI=pd.read_csv(CDI_file, sep=None, header=0)
    df_CDI['words']=df_CDI['words'].str.replace('*', '')
    return(df_CDI)

def read_CDI_data_by_age(CDI_file="PropUnderstandCDI.csv", age=8, save_file=True):
    '''  age must be an integer between 8 and 18 or 'all' meaning that all age will be considered and averaged'''
    ''' save_file is a boolean indicating if you want to save file in you current directory '''
    df=pd.read_csv(CDI_file, sep=None, header=0)
    if isinstance(age, int):
        grouped_age=df.groupby('age')
        df_age=grouped_age.get_group(age) # get the words and the proportion of understanding at age defined
        if len(df_age.columns)==4:
           df_age.columns=['lexical_classes','Type','prop','age']
        elif len(df_age.columns)==3:
            df_age.columns=['Type','prop','age']
        if save_file==True:
            df_age.to_csv('Prop_understand_CDI_at_age_'+str(age)+'.csv', sep='\t', index=False)
        return(df_age)
    else :
        grouped_random_age=df.groupby('age').get_group(10)
        df_mean=df.groupby('words').mean()
        df_mean['lexical_classes']=grouped_random_age['lexical_classes']
        del df_mean['age']
        df_mean['Type']=df_mean.index
        if save_file==True:
            df_mean.to_csv('Mean_prop_understand_CDI_Age.csv', sep='\t', index=False)
        return(df_mean)

def create_df_freq_by_algo_all_sub(path_res, sub, algo='dibs',unit="syllable", freq_file="/freq-words.txt"):
    df_sub=pd.read_table(path_res+"/"+sub[0]+"/"+algo+"/" + unit+freq_file,sep=None, header=0)
    for SS in sub:
        if SS!=sub[0]:
            #df_algo=pd.read_table(path_res+"/"+SS+"/"+algo+freq_file,sep=None, header=0, names=('Freq'+''+ algo, 'Type'))
            path_temp=path_res+"/"+SS+"/"+algo+"/" + unit +freq_file
            df_algo=pd.read_table(path_temp,sep=None, header=0)
            df_sub=pd.merge(df_sub, df_algo, how='outer', on='Type')
    df_sub.fillna(0, inplace=True)
    df_final=pd.DataFrame(df_sub.sum(axis=1))
    df_final.columns = ['Freq'+algo]
    df_final['Type']=pd.DataFrame(df_sub['Type'])
    return(df_final)

def create_df_freq_average_algo_all_sub(path_res, sub, algos, freq_file="/freq-words.txt"):
    ''' when averaging onalgos,  algos must be a list of strings of algos'''
    df_algo_0=pd.read_table(path_res+"/"+sub[0]+"/"+algos[0]+freq_file,sep=None, header=0, names=('Freq'+ ''+ algos[0] , 'Type'))
    for algo in algos:
        if algo!= algos[0]:
            df_0=pd.read_table(path_res+"/"+sub[0]+"/"+algo+freq_file,sep=None, header=0, names=('Freq'+''+ algo, 'Type'))
            df_algo_0=pd.merge(df_0, df_algo_0,how='inner', on=['Type'])
        df_sub=pd.DataFrame(df_algo_0[["Freq"+s for s in algos]].mean(axis=1))
        df_sub['Type']=pd.DataFrame(df_algo_0['Type'])
        for SS in sub:
            if SS!=sub[0]:
                df_algo=pd.read_table(path_res+"/"+SS+"/"+algos[0]+freq_file,sep=None, header=0, names=('Freq'+''+ algos[0], 'Type'))
                for algo in algos:
                    if algo!= "dibs":
                        df_=pd.read_table(path_res+"/"+SS+"/"+algo+freq_file,sep=None, header=0, names=('Freq'+''+ algo, 'Type'))
                        df_algo=pd.merge(df_, df_algo,how='inner', on=['Type'])
                df_mean=pd.DataFrame(df_algo[["Freq"+s for s in algos]].mean(axis=1))
                df_mean['Type']=pd.DataFrame(df_algo['Type'])
                df_sub=pd.merge(df_sub, df_algo, how='outer', on='Type')
        df_sub.fillna(0, inplace=True)
        df_final=pd.DataFrame(df_sub.sum(axis=1))
        df_final.columns = ['SumMeanFreq']
    return(df_final)
  
