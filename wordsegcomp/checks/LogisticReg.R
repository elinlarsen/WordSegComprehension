#******* Logistic regression in R
library(readr)
library(plyr)
library(car)

Logistic_nb_infant_algo_CDI=function(path_res, ages, algos, prop,infant_nb, unit, type_regression="linear")
{
  #prop <- read_delim(infant_prop, delim="\t", escape_double = FALSE, trim_ws = TRUE)
  nb=read.csv(infant_nb, sep=";",header = TRUE)
  
  df_R=data.frame(matrix(nrow=length(algos), ncol = length(ages)))
  colnames(df_R)=ages
  rownames(df_R)=algos

  for (i in 1:length(ages))
  {
    Age=ages[i]
    #getting the two column matrix giving the number of children understanding a word and the number of children not understanding it
    df=subset(prop,age==Age, select=c(prop,Type))
    
    nb_age=as.integer(subset(nb, age==Age, select = NbInfant))
    
    nb_undertsand=df$prop*nb_age
    
    matrix_understanding_type= as.data.frame(cbind(df$prop*nb_age, (rep(1,nrow(df))-df$prop)*nb_age))
    matrix_understanding_type=cbind(matrix_understanding_type, df$Type)
    names( matrix_understanding_type)=c('NbUnderstand', 'NbDontUnderstand', 'Type')
    
    
    for (j in 1:length(algos))
    {
      algo=algos[j]
      #get data about algo results
      file_freq=paste(path_res, '/',algo,'/', unit,'/freq-words.txt', sep="")
      freq=read.table(file=file_freq, header=TRUE)
      
      # logistic model
      if (type_regression=="logistics")
      {
        #combining data 
        dat=merge(matrix_understanding_type,freq,by.y='Type', all=TRUE)
        dat=na.omit(dat)
        mat=as.matrix(cbind(dat$NbUnderstand,  dat$NbDontUnderstand))
        model=glm(formula=mat ~ log(Freq) , data=dat, family = "binomial")
        nullmodel <- glm(mat~1, data=dat,family="binomial")
        df_R[j,i]=1-logLik(model)/logLik(nullmodel)
      }
      
      else
        {#combining data
        dat=merge(df, freq, by.y='Type', all=TRUE)
        model=lm(prop ~ log(Freq), data=dat)
        df_R[j,i]=summary(model)$r.squared
        
        mypath <- file.path(paste( unit, "/", type_regression,  "/ResidualsVsFitted/ResidualsVsFitted", Age, algo, ".jpg", sep = ""))
        png(file=mypath)
        mytitle = paste("QQ plot for algo", algo, "and age",  Age)
        #qqnorm(model$residuals, main = mytitle)
       # plot(model$fitted.values, model$residuals)
        leveragePlots(model) 
        dev.off()
        }
    }
  }

  return(df_R)
}

# *******  parameters *****
ALGOS=c('tps','dibs','puddle_py','AGu', 'gold')
path_res='/Users/elinlarsen/Documents/CDSwordSeg_Pipeline/results/res-brent-CDS/full_corpus/'
path_ortho="/Users/elinlarsen/Documents/CDSwordSeg_Pipeline/recipes/childes/data/Brent/ortholines.txt"
nb_i_file='/Users/elinlarsen/Documents/CDSwordSeg_Pipeline/results/res-brent-CDS/Analysis_algos_CDI/CDI_NbInfantByAge.csv'

# *******  enter your current directory
setwd('/Users/elinlarsen/Documents/CDSwordSeg_Pipeline/results/res-brent-CDS/Analysis_algos_CDI/')

#names(PropUnderstandCDI)<- gsub("words","Type", names(PropUnderstandCDI))
#write_delim(x=PropUnderstandCDI, path='PropUndestandCDI.csv', delim='\t')
#write.table(PropUnderstandCDI, file='PropUndestandCDI.txt', sep='\t', col.names = TRUE, row.names=FALSE, quote=FALSE)

# ******* test
PropUnderstandCDI <- read_delim("~/Documents/CDSwordSeg_Pipeline/results/res-brent-CDS/Analysis_algos_CDI/PropUnderstandCDI.csv", 
                               +     "\t", escape_double = FALSE, trim_ws = TRUE)

df_R2_syl_log=Logistic_nb_infant_algo_CDI(path_res, ages=c(8:18), algos=ALGOS, PropUnderstandCDI,infant_nb=nb_i_file, unit='syllable', type_regression="linear")

