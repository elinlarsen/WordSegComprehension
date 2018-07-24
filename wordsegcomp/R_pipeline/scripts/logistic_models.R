#Logistic regression in R
Logistic_nb_infant_algo_CDI=function(DATA, AGES, ALGOS, CORPUS, MEASURE)
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
          d<-DATA%>%
            filter(au %in% A,  age %in% a, corpus %in% c, measure%in% f)
          
          df$corpus[index]=c
          df$measure[index]=f
          df$age[index]=a
          df$au[index]=A
          
          #print(d)
          
          nb_tokens=d%>%
            group_by(uni_lemma)%>%
            n_groups()
          log_mod=glm(cbind(num_true, num_false) ~  log(freq_smoothed), data=d,family = "binomial" )
          nullmodel <- glm(cbind(num_true, num_false)~1, data=d,family="binomial")
       
          if(A!="gold"){
            aa=head(strsplit(A[1], "/")[[1]], -1)
            if (length(aa)==2){df$algo[index]=paste(aa[1], aa[2], sep="/")}
            else(df$algo[index]=aa)
            df$unit[index]=last(strsplit(A[1], "/")[[1]])}
          
          if(A=="gold"){
            df$algo[index]=A
            df$unit[index]=" "
          }
          df$R2[index]=1-logLik(log_mod)/logLik(nullmodel)
          df$nbtokens[index]=nb_tokens
        }
      }
    }
  }
  return(R2_results=as_tibble(df))
}

