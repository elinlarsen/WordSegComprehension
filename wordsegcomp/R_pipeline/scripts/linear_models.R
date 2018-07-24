#r model_by_corpus WG
R2_by_parameters=function(DATA, AGES, ALGOS, CORPUS, MEASURE)
{
  df=setNames(data.frame(matrix(ncol = 8, nrow = length(AGES)*length( ALGOS)*length(CORPUS)*length(MEASURE))), c("age", "corpus", "measure", "au", "algo", "unit", "R2", "nbtokens"))
  index=0
  for (c in CORPUS)
  {
    #print(c)
    for (f in MEASURE)
    {
      #print(f)
      for (a in AGES)
      {
        for (A in ALGOS)
        {
          #print(A)
          index=index+1
          #print(paste(a, A, f, c, sep=" "))
          d<-DATA%>%
            filter(au %in% A,  age %in% a, corpus %in% c, measure%in% f)
          
          #print(d)
          
          nb_tokens=d%>%
            group_by(uni_lemma)%>%
            n_groups()
          model=lm(prop ~  log(freq_smoothed), data=d)
          df$corpus[index]=c
          df$measure[index]=f
          df$age[index]=a
          df$au[index]=A
         
         
          
          if(A!="gold"){
            aa=head(strsplit(A[1], "/")[[1]], -1)
            if (length(aa)==2){df$algo[index]=paste(aa[1], aa[2], sep="/")}
            else(df$algo[index]=aa)
            df$unit[index]=last(strsplit(A[1], "/")[[1]])}
          
          if(A=="gold"){
            df$algo[index]=A
            df$unit[index]=" "
          }
          df$R2[index]=summary(model)$r.squared
          df$nbtokens[index]=nb_tokens
        }
      }
    }
  }
  return(R2_results=as_tibble(df))
}


###OLD 

#Model per algo per age per unit**
Linear_model=function(data, AGES,ALGOS, UNIT, predictor)
{ 
  df=setNames(data.frame(matrix(ncol = 5, nrow = length(AGES)*length(ALGOS)*length(UNIT))), c("age", "algo", "unit", "R2", "nbtokens"))
  index=0
  for (u in UNIT) 
  {
    for (a in AGES)
    {
      for (A in ALGOS)
      {
        index=index+1
        d<-data%>%
          filter(algos %in% A,  age %in% a, unit %in% u)
        
        nb_tokens=d%>%
          group_by(Type)%>%
          n_groups()
        model=lm(prop ~ predictor, data=d)
        #model=lm(prop ~  log(freq_smoothed), data=d)
        df$unit[index]=u
        df$age[index]=a
        df$algo[index]=A
        df$R2[index]=summary(model)$r.squared
        df$nbtokens[index]=nb_tokens
      }
    }
  }
  return(as_tibble(df))
}


#Pipeline for sample CDI reports
mean_R2_over_CDI_reports=function(data_CDI, data_algo, sample_size, range_of_age, nb_of_sample,algos, unit )
{
  #initialisation
  d=by_word_type(d_comprehension, sample_size, range_of_age, TRUE, 2)
  all_dat=merge(data_algo, d, by='Type')
  res=Linear_model(all_dat,range_of_age, algos, unit)
  mean_R2=as.data.frame(res$R2)
  
  for (n in seq(2,nb_of_sample,1))
  {
    d=by_word_type(d_comprehension, sample_size, range_of_age, TRUE, 2)
    all_dat=merge(data_algo, d, by='Type')
    R2=Linear_model(all_dat, range_of_age, algos, unit)
    mean_R2[paste("R2", n, sep="")]=R2$R2
  }
  res$R2=apply(mean_R2, 1, mean)
  res$sd=apply(mean_R2, 1, sd)
  return(res)
}


#Clustering by lexical open_close (function versus content) or lexical open_close*
Linear_model_by_group=function(data, AGES,ALGOS, UNIT, group1= "open_close", var_group1 = c("function", "content"), group2="NA", var_group2=c("NA"))
{ 
  df=setNames(data.frame(matrix(ncol = 7, nrow = length(AGES)*length(ALGOS)*length(UNIT)*length(var_group1)*length(var_group2))), c("age", "algo", "unit",  "group1", "group2", "R2", "nbtokens"))
  index=0
  for (v in var_group1)
  {
    for (vv in var_group2)
    {
      for (u in UNIT) 
      {
        for (a in AGES)
        {
          for (A in ALGOS)
          {
            index=index+1
            df$unit[index]=u
            df$age[index]=a
            df$algo[index]=A
            df$group1[index]=v
            df$group2[index]=vv
            d<-data%>%
              filter(algos==A,  age== a, unit==u, get(group1) == v)
            nb_tokens=d%>%
              group_by(Type)%>%
              n_groups()
            df$nbtokens[index]=nb_tokens
            if (group2!="NA")
            {
              d<- d%>%
                filter(get(group2) ==vv)
              nb_tokens=d%>%
                group_by(Type)%>%
                n_groups()
              df$nbtokens[index]=nb_tokens
            }
            if (dim(d)[1]!=0)
            {
              model=lm(prop ~ log(Freq), data=d)
              df$R2[index]=summary(model)$r.squared
            }
            else
            {
              df$R2[index]=0
              print(paste(c(A,"has no token segmented in group", v, "or" , vv) , collapse = " "))
            }
          }
        }
      }
    }
  }
  return(as_tibble(df))
}
