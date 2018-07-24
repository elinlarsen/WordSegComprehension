#Sample CDI reports to have the same number across ages***

get_prop=function(x)
{
  p=mean(x)
  return(as.data.frame(p))
}


sampling_CDI_reports=function(data, sample_size, age_to_sample_at=13)
{
  #Sample the number of parental reports ie infant id for a given age "age_to_sample_at"
  #Arguments : 
  #  data: dataframe containing as columns "Type", "prop", "age", etc
  #  sample_size: int, number of parental reports for a given age
  #  age_to_sample_at: int between 8 and 18
  
  d_age<- data%>%
    filter(age==age_to_sample_at)
  
  infants_id<-d_age%>%
    group_by(data_id)%>%
    tally()%>%
    select(data_id)
  
  sampled_data_id=sample(infants_id$data_id, sample_size, replace=FALSE)
  
  sampled<-d_age%>%
    filter(data_id %in% sampled_data_id)
  
  return(sampled)
}


# Add a prop column for a given age: proportion of infant reported to understand a word  ***
add_prop_column=function(data_sampled, age_sampled_at, form_name)
{
  prop<-data_sampled%>%
    group_by(Type)%>%
    do(get_prop(x=.$task_score))%>%
    mutate(age=age_sampled_at, form=form_name)%>%
    ungroup()
  return(prop)
}

# Add a prop column for a range of ages
add_prop_column_all_ages=function(df_form, age_range, form_name)
{
  d_prop<-df_form%>%
    filter(age==age_range[1])
  
  d_prop<-add_prop_column(d_prop, age_range[1], form_name)
  for (a in age_range[-1])
  {
    d<-df_form%>%filter(age==a)
    d<-add_prop_column(d, a, form_name)
    d_prop<-rbind(d_prop,d)
  }
  return(d_prop)
}


average_sampling_CDI_reports=function(data, sample_size, age_to_sample_at=13, nb_of_sample=10)
{
  #Arguments : 
  #  data: dataframe containing as columns "Type", "prop", "age", etc
  #  sample_size: number of parental reports for each ages
  # age_to_sample_at : age at which filter the dataset
  # nb_of_sample : number of sample to average on 
  
  #initialisation
  average=sampling_CDI_reports(data, sample_size, age_to_sample_at)
  average=add_prop_column(average, age_to_sample_at)
  prop_sample=average # dataframe in which all proportion samples will be stored
  
  if (nb_of_sample!=1)
  {  
    #iteration if the number of sample >1
    for (n in seq(2, nb_of_sample, 1))
    {
      s=sampling_CDI_reports(data, sample_size, age_to_sample_at)
      s=add_prop_column(s, age_to_sample_at)
      prop_sample[paste("prop", n, sep="")]=s$prop
    }
  }
  else
  {}
  
  myvars <- names(prop_sample) %in% c("Type", "age") #excluding Type and age
  new <- prop_sample[!myvars]
  average$mean=apply(new, 1, mean)  
  average$sd=apply(new, 1, sd)
  return(average)
}

by_word_type=function(data, sample_size, range_of_age, average=TRUE, nb_of_sample=10)
  #if average=TRUE, compute the proportion of reported infant to understand a word for "sample_size" CDI reports averaged on "nb_of_sampled" sampled
{
  age0=range_of_age[1]
  
  #initiation  
  if (average==TRUE)
  {by_word=average_sampling_CDI_reports(data, sample_size, age0, nb_of_sample)}
  else
  {
    s=sampling_CDI_reports(data, sample_size, age0)
    by_word=add_prop_column(s, age0)
  }
  
  #iteration 
  for (a in range_of_age[-1])
  {
    if (average==TRUE)
    {by_word_by_age=average_sampling_CDI_reports(data, sample_size, a, nb_of_sample)}
    else
    {
      ss=sampling_CDI_reports(data, sample_size, a)
      by_word_by_age=add_prop_column(ss, age0)
    }
    by_word=rbind(by_word, by_word_by_age)
  }
  names(by_word)[names(by_word)=="Type"] <- "Type"
  return(by_word)
}
