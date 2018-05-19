library(gam)
library(readr)
library(dplyr)
library(tidyr)
library(purrr)
library(ggplot2)
library(knitr)
library(reshape2) # for box plot

library(lme4)

data_by_nb_infant<-function(data, nb_infant, AGE)
{ new_data<-data%>%
    filter(age==AGE)
  u=as.vector(sample(new_data$data_id, nb_infant))
  final_data<-new_data%>%
    filter(data_id==u[1])
  for (i in (2:length(u)))
  {
    temp<-new_data%>%
      filter(data_id==u[i])
    final_data=rbind(final_data, temp)
  }
  return(final_data)
}

get_prop<-function(data)
{
  dat_prop<-data%>%
    group_by(lexical_class, Type, age, data_id)%>%
    summarise(uni_value = any(value)) %>% # attention, if summarise dont work , do : detach(package:plyr)
    group_by(lexical_class, Type,age) %>%
    summarise(num_true = sum(uni_value, na.rm = TRUE),
              num_false = n() - num_true,
              prop = mean(uni_value, na.rm = TRUE))
  return(dat_prop) 
}

#model fitted with all words type in CDI for a certain age
fit_prop<-function(dat_CDI,dat_freq_algo,dat_gp, nb_infant, AGE)
{
  temp=data_by_nb_infant(dat_CDI,nb_infant, AGE)
  dat_prop=get_prop(temp)
  
  dat_age<- dat_prop%>%
    filter(age==AGE)%>%
    filter(!Type %in% dat_gp$Type)
  
  train=merge(dat_age, dat_freq_algo, by='Type') # dataset to train the linear regression, need prop, type, freq algo
  test=merge(dat_gp, dat_prop, by='Type') # dataset to test the linear model on words belonging to two different class frequency in TP lexicon

  m<-lm(prop~as.vector(log_freq_tps), train)
  
  fitted<-as.data.frame(predict(m, test, se.fit = FALSE))
  names(fitted)='prop_fitted'
  fitted$Type=test$Type
  prop=as.data.frame(subset(test, select=c('prop', 'Type', 'group')))
  
  res=merge(fitted, prop, by='Type')
  HF=subset(res, group=='HF')
  LF=subset(res, group=='LF')
  
  #print(t.test(HF$prop, LF$prop)) #Student test with unequal sample sizes, unequal variances : Welch t-test
  #print(t.test(HF$prop_fitted, LF$prop_fitted))
  #print(ks.test(HF$prop, LF$prop, alternative="two.sided")) #Kolmogorov–Smirnov test 
  #print(ks.test(HF$prop_fitted, LF$prop_fitted, alternative="two.sided"))
  print(wilcox.test(HF$prop, LF$prop, alternative="two.sided")) #Wilcoxon Rank Sumtest 
  print(wilcox.test(HF$prop_fitted, LF$prop_fitted, alternative="two.sided"))
  #print(summary(m))
  #return(summary(m)$adj.r.squared)
  #return(t.test(HF$prop_fitted, LF$prop_fitted)$statistic)
  mean=rbind(mean(HF$prop), mean(LF$prop))
  return(mean)
}



## DATA
#********* CDI***** ENGLISH **** MEASURE = UNDERSTAND
english_all_data_understand <- read_delim("~/Documents/CDSwordSeg_Pipeline/results/res-brent-CDS/Analysis_algos_CDI/CDI_data/english_all_data_understand.csv", 
                                          "\t", escape_double = FALSE, trim_ws = TRUE)
eng_understand=english_all_data_understand %>%
  rename(Type=uni_lemma)

#********* gold *********
freq_brent <- read_delim("~/Documents/CDSwordSeg_Pipeline/results/res-brent-CDS/Analysis_algos_CDI/freq_brent.csv", "\t", escape_double = FALSE, trim_ws = TRUE, col_names = TRUE)%>%
  rename(word_count=Freqgold)%>%
  mutate(log_freq=log(word_count/sum(word_count)),
         frequency=scale(log_freq,center=TRUE, scale=TRUE) # centered at 0, and divided by standard deviation
  )

#********* word counts of words segmented by TPs******
freq_TPs <- read_delim("~/Documents/CDSwordSeg_Pipeline/results/res-brent-CDS/full_corpus/TPs/syllable/freq-words.txt", 
                       "\t", escape_double = FALSE, trim_ws = TRUE)%>%
  mutate(log_freq_tps=scale(log(Freq/sum(Freq)), center=TRUE, scale=TRUE))

#********* get two groups of different frequency by TPs
hf_tp <- read_delim("~/Documents/CDSwordSeg_Pipeline/results/res-brent-CDS/Analysis_algos_CDI/power_analysis/TPs/gold_150_400/HF_TP_150-400.txt", 
                    "\t", escape_double = FALSE, trim_ws = TRUE)
hf_tp$group=rep('HF', nrow(hf_tp))
lf_tp <- read_delim("~/Documents/CDSwordSeg_Pipeline/results/res-brent-CDS/Analysis_algos_CDI/power_analysis/TPs/gold_150_400/LF_TP_6-70.txt", 
                    "\t", escape_double = FALSE, trim_ws = TRUE)
lf_tp$group=rep('LF', nrow(lf_tp))

tp_groups=rbind(lf_tp, hf_tp)%>%
  mutate(log_freq=scale(log(Freqtps/sum(Freqtps)), center=TRUE, scale=TRUE))
         #log_freq_gold=scale(log(Freqgold/sum(Freqgold)), center=TRUE, scale=TRUE))


res_200_13mo_gold=fit_prop(eng_understand,freq_tps,tp_groups, 200, 13) # be sure that freq_tps has log_freq (scaled and centered)


# ***** BOX PLOT **** Frequency groups for TPs AND Gold
df_group_tp=cbind(subset(tp_groups, select=c('Type', 'group', 'Freqtps')), data.frame(algo=rep('TPs', nrow(tp_groups))))
colnames(df_group_tp)=c('Type', 'group', 'Freq', 'algo')            
df_group_gold=cbind(subset(tp_groups, select=c('Type', 'group', 'Freqgold')), data.frame(algo=rep('Gold', nrow(tp_groups))))
colnames(df_group_gold)=c('Type', 'group', 'Freq', 'algo')     
df_group=rbind(df_group_tp, df_group_gold)
boxplots.double = boxplot(Freq~group + algo, data = df_group, at = c(1, 2, 4,5), xaxt='n',ylab='Number of occurences of words',col=c('palevioletred1','royalblue2'))
axis(side=1, at=c(1.5, 4.5), labels=c('TPs', 'Gold'), line=0.5, lwd=0)
text(c(1, 2, 4, 5), c(130, 100, 130, 130), c('High ', 'Low ', 'High', 'Low'))# add  labels near the box plots

boxplot(prop~group*lexical_class, res_10_13mo,col=c('green', 'red'), ylab="Proportion ", xlab= "Lexical classes", main="Proportion of 13-month-old infants understanding words of different lexical classes")

boxplot(Freqgold~group,res_10_13mo, ylab="Number of occurences in Brent corpus", xlab= "Groups of high and low frequency")

boxplot(Freqtps~group, res_10_13mo, ylab="Number of occurences of words segmented by TPs", xlab= "Groups of high and low frequency")

boxplot(prop_fitted~ group,res_200_13mo , xlab= "Groups of words with high and low occurrences in TPs lexicon", ylab="Predicted proportion of 200 13-months-old infants ")


#####
x= seq(10,750, by=10)
df_r_squared=matrix(0,length(x),1)
for (i in seq(1:length(x)))
{
  df_r_squared[i,1]=fit_prop(eng_understand,freq_tps,tp_groups, i, 13)
}

plot(seq(10,750, by=10), df_r_squared, xlab="Number of infants used for the prediction", ylab="Adjusted R squared of the linear correlation", xlim=c(0,750), ylim=c(0,0.3))

#####
df_t_test=matrix(0,length(x),1)
for (i in seq(1:length(x)))
{
  df_t_test[i,1]=fit_prop(eng_understand,freq_tps,tp_groups, i, 13)
}

plot(seq(10,750, by=10), df_t_test, xlab="Number of infants used for the prediction", ylab="Student statistic between the mean prediction of the two groups of words")


#####
x= seq(25,250, by=25)
res=fit_prop(eng_understand,freq_tps,tp_groups, 10, 13)
for (i in x)
{
  res=cbind(res, fit_prop(eng_understand,freq_tps,tp_groups, i, 13))
}


## Proportion
x=c(20,30,40,50,75,100,125,150,175,200,250,300,400,500,600,700)
mean_prop=fit_prop(eng_understand,freq_tps,tp_groups, 10, 13)
for (i in x)
{
  mean_prop=cbind(mean_prop, fit_prop(eng_understand,freq_tps,tp_groups, i, 13))
}


## Predicted Proportion
x=c(20,30,40,50,75,100,125,150,175,200,250,300,400,500,600,700)
mean_fit=fit_prop(eng_understand,freq_tps,tp_groups, 10, 13)
for (i in x)
{
  mean_fit=cbind(mean_fit, fit_prop(eng_understand,freq_tps,tp_groups, i, 13))
}

plot(c(10,x),mean_prop[1,],col="red", ylim=c(0,0.7), ylab="Mean proportion of infants understanding words in groups", xlab="Number of infants")
points(c(10,x),mean_prop[2,], col="green")
points(c(10,x),mean_fit[1,],col="red", pch=20 )
points(c(10,x),mean_fit[2,], col="green", pch=20)
legend("topright", c("High occurences","Low occurrences", "Fitted - High occurences","Fitted - Low occurrences"), pch = c(1, 1, 20, 20), col=c("red","green", "red", "green"))

# get the distribution of all subsample for a given number of infants, 

dist_mean_prop_700=fit_prop(eng_understand,freq_tps,tp_groups, 700, 13)

y=seq(1,110, 1)
for (i in y)
{dist_mean_prop_700=cbind(dist_mean_prop_700,fit_prop(eng_understand,freq_tps,tp_groups, 700, 13))
}

dist_mean_prop_150_fin= cbind(dist_mean_prop_150,dist_mean_prop_150_bis)

hist(dist_mean_prop_700[2,], main='Histogram of subsampling for 700 infants', xlab='Mean proportion of infants reported to understand low frequency words', ylim=c(0,200))
hist(dist_mean_prop_700[1,], main='Histogram of subsampling for 700 infants', xlab='Mean proportion of infants reported to understand high frequency words',  ylim=c(0,200))

mean(dist_mean_prop_700[1,])
sd(dist_mean_prop_700[1,])

mean(dist_mean_prop_700[2,])
sd(dist_mean_prop_700[2,])

mean(dist_mean_prop_150_fin[2,])
sd(dist_mean_prop_150_fin[2,])

