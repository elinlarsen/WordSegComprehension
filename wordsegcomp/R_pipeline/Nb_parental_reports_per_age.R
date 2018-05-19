#Number of parental reports per age
get_parental_reports_nb_per_age=function(data_CDI, ages=c(8:18), form_name)
{
  df=setNames(data.frame(matrix(ncol = 3, nrow = length(ages))), c( "age", "nb_reports", "form"))
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
  }
  return(df)
}
