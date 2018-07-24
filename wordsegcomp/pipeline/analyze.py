# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 11:47:40 2016
@author: elinlarsen
"""


import numpy as np
import collections
import pandas as pd
from collections import Counter

# import file
import read

#########################  Count lines of text and occurences of words in text files
def count_lines_corpus(corpus_file):
    ''' count the number of lines in a text file '''
    non_blank_count=0
    with open(corpus_file,'r') as text:
        for line in text:
            if line.strip():
                non_blank_count+=1
    print('number of non-blank lines found: %d' % non_blank_count)
    return(non_blank_count)

def create_freq_top_gold(path_gold, path_res, subs):
    for SS in subs:
        path=path_gold+"/"+SS+"/gold.txt"
        df=freq_token_in_corpus(path)
        path_out=path_res+"/"+SS+"/"+"gold"+"/freq-top.txt"
        df.to_csv(path_out, sep='\t', index=False)


def freq_token_in_corpus(path_file):
    c=Counter()
    list_o=read.corpus_as_list(path_file)
    list_o=[x.lower() for x in list_o]
    for word in list_o :
        c.update([word])
    df=pd.DataFrame.from_dict(c, orient='index')
    df.reset_index(level=0, inplace=True)
    df.columns=['Type', 'Freq']
    #cols = df.columns.tolist()
    #cols=cols[1]+cols[0]
    ddf = df[['Freq', 'Type']]
    ddf.sort_values('Freq', ascending=False, inplace=True)
    
    ddf.reset_index(drop=True, inplace=True)
    return(ddf)



######################### SPLIT BETWEEN BAD AND WELL SEGMENTED TOKEN
#  by checking if they belong to the dictionnary
def split_segmented_token(dic, list_token):
    ortho_inter=[]
    bad_seg_inter=[]
    d={}
    for item in list_token:
        if dic.has_key(item)==False:
            bad_seg_inter.append(item)
        else:
            ortho_inter.append(dic[item])
    d['wrong_segmentation']=bad_seg_inter
    d['ortho']=ortho_inter
    return(d)


######################### Comparison of algorithms intersection between sub-corpus
def compare_token_btw_algo(path_res, dic_corpus, sub=["sub0","sub1","sub2","sub3","sub4","sub5","sub6","sub7","sub8","sub9"],
                          algos=['dibs','ngrams','tps','puddle','dmcmc','AGu'],algo_ref="dibs",unit='syllable', freq_file="/freq-top.txt"):
    res=[]
    for i in range(len(sub)):
        dic_inter={}
        ref=read.list_freq_token_per_algo(algo_ref,sub[i],path_res,unit, freq_file)[0]
        for j in range(len(algos)):
            if algos[j]!=algo_ref:
                b=read.list_freq_token_per_algo(algos[j],sub[i],path_res,unit,freq_file)[0]
                list_inter=list(set(ref).intersection(set(b)))
                dic_inter[algos[j]]=split_segmented_token(dic_corpus, list_inter)
        res.append(dic_inter)
    return(res)


def intersection_all_algo(path_res, dic_corpus, sub=["sub0","sub1","sub2","sub3","sub4","sub5","sub6","sub7","sub8","sub9"],
                          algos=['dibs','ngrams','tps','puddle','dmcmc','AGu'],algo_ref="dibs",unit='syllable', freq_file="/freq-top.txt"):
    """for each sub-corpus, look at types segmented by all algorithms """
    res=[]
    n=len(algos)-2
    for ss in sub:
        dic={}
        ref_ortho=compare_token_btw_algo(path_res, dic_corpus,[ss],algos,algo_ref,unit, freq_file)[0].values()[n]["ortho"]
        ref_wrong_seg=compare_token_btw_algo(path_res, dic_corpus,[ss],algos,algo_ref,unit, freq_file)[0].values()[n]["wrong_segmentation"]
        for algo in algos:
            a_ortho={}
            a_wrong_seg={}
            if not algo==algo_ref:
                a_ortho[algo]=compare_token_btw_algo(path_res, dic_corpus,[ss],algos,algo_ref,unit, freq_file)[0][algo]["ortho"]
                a_wrong_seg[algo]=compare_token_btw_algo(path_res, dic_corpus,[ss],algos,algo_ref,unit, freq_file)[0][algo]["wrong_segmentation"]
                ref_ortho=list(set(ref_ortho).intersection(set(a_ortho[algo])))
                ref_wrong_seg=list(set(ref_wrong_seg).intersection(set(a_wrong_seg[algo])))
        dic["ortho"]=ref_ortho
        dic["wrong_segmentation"]=ref_wrong_seg
        print(dic["ortho"][0])
        res.append(dic)
    file = open("TypesBySubsInAllAlgos.txt", "w")
    for i in range(len(sub)):
        file.write(sub[i] +"\n"+"\n")
        mean_o=0
        for j in ["ortho"]:
            count=0
            file.write(j+"\n"+"\n")
            for types in res[i][j]:
                file.write(types +"\n")
                count+=1
            file.write("Number of types well segmented by all algorithms in " + sub[i] + " are : " + str(count) +"\n"+"\n")
        mean_o+=count
        mean_ws=0
        for jj in ["wrong_segmentation"]:
            count=0
            file.write(jj+"\n"+"\n")
            for types in res[i][jj]:
                file.write(types +"\n")
                count+=1
            file.write("Number of types badly segmented by all algorithms in the subcorpus " + sub[i] + " are : " + str(count) +"\n"+"\n")
        mean_ws+=count
    mean_o=mean_o/len(sub)
    mean_ws=mean_ws/len(sub)
    file.write("Mean word per sub is :"+str(mean_o)+ "\n")
    file.write("Mean wrong segmented types per sub is :"+str(mean_ws)+"\n")
    file.close()
    return(res)


def inter_all_algo_inter_all_sub(res_all_algo):
  """look at types segmented by all algorithms  in all sub"""
  n=len(res_all_algo)
  ortho=set(res_all_algo[n-1]["ortho"])
  ws=set(res_all_algo[n-1]['wrong_segmentation'])
  file=open("IntersectionAllAlgoAllSub.txt","w")
  for i in range(n-1):
        file.write("\n"+"Number of intersection between subcorpus : "+ str(i+2) + "\n")
        for ii in range(i):
            ortho= set(ortho) & set(res_all_algo[ii]["ortho"])
            ws= set(ws) & set(res_all_algo[ii]['wrong_segmentation'])
        file.write("\n"+"Words types : "+"\n" )
        for word in ortho:
            file.write(word + "\n")
        file.write("\n"+"Badly segmented"+ "\n")
        for word in ws:
            file.write( word + "\n")
        file.write("\n"+ "Number of words types segmented in all algo between subcorpus : "+ str(len(ortho)) + "\n")
        file.write("\n"+"Number of types badly segmented in all algo between subcorpus : "+ str(len(ws)) + "\n")
  return([ortho,ws])


def compare_token_btw_sub(path_res,dic_corpus,sub=["sub0","sub1","sub2","sub3","sub4","sub5","sub6","sub7","sub8","sub9"],sub_ref="sub0",
                          algos=['dibs','ngrams','tps','puddle','dmcmc','AGu'],unit='syllable', freq_file="/freq-top.txt"):
    '''for each algo, comparison of intersection of words and non words segmented in two different corpus for all subcorpus'''
    res={}
    for j in range(len(algos)):
        comparison_sub_for_one_algo=[]
        ref=read.list_freq_token_per_algo(algos[j],sub_ref,path_res,unit, freq_file)[0]
        for i in range(len(sub)):
            dic_inter={} #empty dictionnary
            b=read.list_freq_token_per_algo(algos[j],sub[i],path_res,unit, freq_file)[0]
            list_inter=list(set(ref).intersection(set(b)))# intersection of token of sub[i] and sub_ref for one algo
            dic_inter[sub[i]]=split_segmented_token(dic_corpus, list_inter) # distinction of token as word or badly segmented for one sub_corpus
            comparison_sub_for_one_algo.append(dic_inter) # add the comparison in a list
        res[algos[j]]=comparison_sub_for_one_algo
    return(res)

def compare_token_all_sub(path_res,dic_corpus,sub=["sub0","sub1","sub2","sub3","sub4","sub5","sub6","sub7","sub8","sub9"],algos=['dibs','ngrams','tps','puddle','dmcmc','AGu'],unit='syllable', freq_file="/freq-top.txt"):
    n=len(sub)-1
    res={}
    for i in range(len(algos)):
        comp_all_sub_per_algo=read.list_freq_token_per_algo(algos[i],sub[n],path_res,unit, freq_file)[0]# list of freq words for algo[i] computed in  sub[n]
        for j in range(n):
            a=read.list_freq_token_per_algo(algos[i],sub[j],path_res,unit, freq_file)[0]
            comp_all_sub_per_algo=list(set(a).intersection(set(comp_all_sub_per_algo)))
        all_sub_per_algo_dis=split_segmented_token(dic_corpus, comp_all_sub_per_algo)
        res[algos[i]]=all_sub_per_algo_dis
    file = open("TypesByAlgosInAllSubs.txt", "w")
    for i in algos:
        file.write(i +"\n"+"\n")
        for j in ["ortho"]:
            count=0
            file.write(j+"\n"+"\n")
            for types in res[i][j]:
                file.write(types +"\n")
                count+=1
        file.write("Number of types well segmented by " + i + " are : " + str(count) +"\n"+"\n")
        for jj in ["wrong_segmentation"]:
            count=0
            file.write(jj+"\n"+"\n")
            for types in res[i][jj]:
                file.write(types +"\n")
                count+=1
        file.write("Number of types badly segmented by " + i + " are : " + str(count) +"\n"+"\n")
    file.close()
    return(res)

########################
def differentiate_token_btwn_algo(path_res,dic_corpus,sub=["sub0","sub1","sub2","sub3","sub4","sub5","sub6","sub7","sub8","sub9"],algo_ref="dibs",
                          algos=['dibs','ngrams','tps','puddle','dmcmc','AGu'], unit='syllable', freq_file="/freq-top.txt"):
    res=[]
    for i in range(len(sub)):
        dic_inter={}
        ref=list_freq_token_per_algo(algo_ref,sub[i],path_res,unit, freq_file)[0]
        for j in range(len(algos)):
            if algos[j]!=algo_ref:
                b=read.list_freq_token_per_algo(algos[j],sub[i],path_res,unit, freq_file)[0]
                list_diff=[k for k in ref if not k in b]
                dic_inter[algos[j]]=split_segmented_token(dic_corpus, list_diff)
        res.append(dic_inter)
    return(res)

def signature_algo(path_res,dic_corpus,sub=["sub0","sub1","sub2","sub3","sub4","sub5","sub6","sub7","sub8","sub9"],algo_ref="dibs",
                          algos=['dibs','ngrams','tps','puddle','dmcmc','AGu'],unit='syllable', freq_file="/freq-top.txt"):
    res=[]
    n=len(algos)
    for i in range(len(sub)):
        dic_inter={}
        ref=read.list_freq_token_per_algo(algo_ref,sub[i],path_res,unit, freq_file)[0]
        for j in range(n):
            if not algos[j]==algo_ref:
                b=read.list_freq_token_per_algo(algos[j],sub[i],path_res, unit, freq_file)[0]
                dic_inter[algos[j]]=[k for k in ref if not k in b] # which token is segmented in ref and not in algo j
        sign_ref=dic_inter.values()[0]
        for j in range(n-1):
            if not algos[j]==algo_ref:
                sign_ref=set(sign_ref) & set(dic_inter[algos[j]])
        token_algo_ref=split_segmented_token(dic_corpus,sign_ref)
        res.append(token_algo_ref)
    return(res)

def in_common_two_algo( path_res,dic_corpus, sub, algos, algo1, algo2,unit, freq_file):
    dic_inter={}
    ref1=read.list_freq_token_per_algo(algo1,sub,path_res,unit,freq_file)[0]
    ref2=read.list_freq_token_per_algo(algo2,sub,path_res,unit, freq_file)[0]
    inter=list(set(ref1).intersection(set(ref2)))
    for j in range(len(algos)):
        if (algos[j]!=algo1 and algos[j]!=algo2):
            inter=[x for x in inter if x not in list(set(ref1).intersection(set(algos[j])))]
            #create intersection of token belonging only to algo1 and algo2
    dic_inter[algo1,algo2]=split_segmented_token(dic_corpus, inter)
    return(dic_inter)

def common_type_in_all_sub(sub, path_data,name_gold="ortholines.txt"):
    sub_ref=sub[0]
    path_ref=path=path_data+"/"+str(sub_ref)+"/"+name_gold
    list_ref=read.corpus_as_list(path_ref)
    count_freq={}
    file=open("TypesCommonsInAllSUBs.txt", "w")
    for i in sub:
        if not sub==sub_ref:
            path=path_data+"/"+str(i)+"/"+name_gold
            list_sub=read.corpus_as_list(corpus_file=path)
            list_sub=[x for x in list_sub if x in list_ref] # list of all token in all subcorpus
    #=> need to find the types and its frequencies
    for token in list_sub:
        try:
            count_freq[token]+=1 # count the frequency of the token common in ALL in the LAST subcorpus
        except:
            count_freq[token]=1
    print("There are {} types in common in all sub-corpus".format(len(count_freq)))
    file.write("Number of words that are in all subs :" + str(len(count_freq))+"\n"+"\n")
    for i in range(len(count_freq)):
        file.write(count_freq.keys()[i]+ " "+ str(count_freq.values()[i]) + "\n")
    file.close()
    return(count_freq)


def intersection_exclusive_in_2_algo( path_res, dic_corpus, sub, algos, unit='syllable', freq_file="/freq-top.txt"):
    '''for one sub !!!! '''
    res=[]
    z=list(np.copy(algos))
    file = open("TypesCommonsIn2Algos.txt", "w")
    for algo1 in z:
        for algo2 in z:
            if algo2!=algo1:
                res.append(in_common_two_algo(path_res,dic_corpus, sub, z, algo1, algo2,unit,  freq_file))
    for i in range(len(res)):
        file.write(str(res[i].keys()[0]) +"\n"+"\n")
        count=0
        file.write(str("ortho")+"\n"+"\n")
        for types in res[i].values()[0].values()[0]:
            file.write(types +"\n")
            count+=1
        file.write("Number of types well segmented in common all " + str(res[i].keys()[0])+  str(sub) +" are : " + str(count) +"\n"+"\n")
        count=0
        file.write(str("wrong_segmentation")+"\n"+"\n")
        for types in res[i].values()[0].values()[1]:
            file.write(types +"\n")
            count+=1
        file.write("Number of types badly segmented in common by  " +str(res[i].keys()[0]) + " in" + str(sub) + " are : " + str(count) +"\n"+"\n")
    file.close()
    return(res)

def average_inter_per_sub( path_res, dic_corpus, sub, algos, unit='syllable',freq_file="/freq-top.txt"):
    res=[]
    for ss in sub:
        res.append(intersection_exclusive_in_2_algo(path_res, dic_corpus, ss, algos, unit,freq_file="/freq-top.txt"))

def count_type_segmented_per_algo_per_sub(algos,sub,path_res, unit, freq_file="/freq-top.txt"):
    res=[]
    file=open("NumberTypesPerAlgoPerSub.txt","w")
    for i in sub:
        file.write("\n"+i+"\n")
        for j in algos:
            count=read.list_freq_token_per_algo(j,i,path_res,unit, freq_file)[1]
            file.write(j+" " +str(count)+"\n")
            res.append(count)
    file.close()
    return(res)

def count_type_well_segmented_per_algo_per_sub(dic,algos,sub,path_res,unit='syllable',freq_file="/freq-top.txt"):
    file=open("NumberTypesPerAlgoPerSub.txt","w")
    for i in sub:
        file.write("\n"+i+"\n")
        for j in algos:
            list_type=read.list_freq_token_per_algo(j,i,path_res,unit, freq_file)[0]
            splitted=split_segmented_token(dic, list_type)
            count_o=len(splitted["ortho"])
            file.write(j+" " + str("ortho")+" " +str(count_o)+"\n")
            count_ws=len(splitted['wrong_segmentation'])
            file.write(j+" " +str("wrong_segmentation")+" " +str(count_ws)+"\n")
    file.close()

def mean_token_segmented_per_sub(algos, sub,path_res, dic, unit, freq_file):
    freq={}
    seg_freq={}
    res={}
    mean_o=collections.defaultdict(int)
    mean_ws=collections.defaultdict(int)
    count_o={}
    count_ws={}
    for algo in algos:
        for ss in sub:
            freq[ss]=read.list_freq_token_per_algo(algo,ss,path_res, unit, freq_file)[0]
            seg_freq[ss]=split_segmented_token(dic, freq[ss])
            count_o[ss]=len(seg_freq[ss].values()[0])
            print(count_o[ss])
            count_ws[ss]=len(seg_freq[ss].values()[1])
            mean_o[algo]+=count_o[ss]
            mean_ws[algo]+=count_ws[ss]
        mean_o[algo]=mean_o[algo]/len(sub)
        mean_ws[algo]=mean_ws[algo]/len(sub)
        res["ortho"]=mean_o
        res["wrong_segmentation"]=mean_ws
    return(res)

def mean_signature_all_sub(signature, sub):
    mean_sign_o=0
    mean_sign_ws=0
    for i in range(len(sub)):
        mean_sign_o+=len(signature[i].values()[0])
        mean_sign_ws+=len(signature[i].values()[1])
    mean_sign_o=mean_sign_o/len(sub)
    mean_sign_ws=mean_sign_ws/len(sub)
    res=[mean_sign_o, mean_sign_ws]
    print(res)
    return(res)

def Inter_signature_per_sub(nb_inter, signature):
    """" signature of one algo for each sub corpus"""
    ortho=set(signature[0]["ortho"])
    ws=set(signature[0]['wrong_segmentation'])
    for i in range(nb_inter):
        if not i==0:
            ortho= set(ortho) & set(signature[i]["ortho"])
            ws= set(ws) & set(signature[i]['wrong_segmentation'])
    print("ortho : " +str(len(ortho)) +" and wrong segmented "+ str(len(ws)))
    return([ortho,ws])

def Inter_signature(signature,name_algo):
    """" signature of one algo for each sub corpus"""
    n=len(signature)
    ortho=set(signature[n-1]["ortho"])
    ws=set(signature[n-1]['wrong_segmentation'])
    file=open("Signature"+ name_algo+"PerSub.txt","w")
    for i in range(n-1):
        file.write("\n"+"Number of intersection between subcorpus : "+ str(i+2) + "\n")
        for ii in range(i):
            ortho= set(ortho) & set(signature[ii]["ortho"])
            ws= set(ws) & set(signature[ii]['wrong_segmentation'])
        file.write("\n"+"Words types : "+"\n" )
        for word in ortho:
            file.write(word + "\n")
        file.write("\n"+"Badly segmented"+ "\n")
        for word in ws:
            file.write( word + "\n")
        file.write("\n"+ "Number of words types segmented in common between subcorpus : "+ str(len(ortho)) + "\n")
        file.write("\n"+"Number of types badly segmented in common between subcorpus : "+ str(len(ws)) + "\n")
    return([ortho,ws])


def average_signature_per_sub(signature):
    n=len(signature)
    ref_ortho=signature[n-1].values()[0]
    ref_ws=signature[n-1].values()[1]
    for i in range(n):
        ref_ortho=set(signature[i].values()[0]).intersection(set(ref_ortho))
        ref_ws=set(signature[i].values()[1]).intersection(set(ref_ws))
    return[ref_ortho,ref_ws]

def average_len_signature_per_sub(signature):
    n=len(signature)
    len_o=[]
    len_ws=[]
    res={}
    for i in range(n):
        len_o.append(len(signature[i].values()[0]))
        len_ws.append(len(signature[i].values()[1]))
    res["ortho"]=sum(len_o)/len(len_o)
    res["ws"]=sum(len_ws)/len(len_ws)
    return res
