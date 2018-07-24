#Number of parental reports per age
get_parental_reports_nb_per_age=function(data_CDI, ages=c(8:18), form_name, measure_name, language)
{
  df=setNames(data.frame(matrix(ncol = 5, nrow = length(ages))), c( "age", "nb_reports", "form", "measure", "language"))
  i=0
  #df$form=rep(name,length(ages))
  for (a in ages)
  {
    i=i+1
    gp<- data_CDI%>%
      filter(age==a)%>%
      group_by(data_id)
    df$age[i]=a
    df$nb_reports[i]=n_groups(gp)
    df$form[i]=form_name
    df$measure[i]=measure_name
    df$language[i]=language
  }
  return(df)
}
