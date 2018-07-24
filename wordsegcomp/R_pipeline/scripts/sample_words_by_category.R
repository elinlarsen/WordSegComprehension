#select randomly X word types for different lexical classes and look at the evolution of understanding over age***

proportion_for_sampled_types<-function(data_prop, lc_name, sample_size, sampling=TRUE, legend_name="lex")
{
  grouped_by_lex<-data_prop%>%
    select(age, Type, lexical_classes)%>%
    filter(age==13, lexical_classes %in% lc_name)%>%
    group_by(lexical_classes)
  
  if (sampling==TRUE)
  { sampled_types<- grouped_by_lex%>%
    nest()%>%
    mutate(n = sample_size) %>%
    mutate(samp = map2(data,n, sample_n))%>%
    select(lexical_classes, samp) %>%
    unnest()
  }
  else
  {
    sampled_types<- grouped_by_lex
  }
  
  sub_prop <- data_prop%>%
    filter(Type %in% as.list(sampled_types$Type)) # for all ages
  
  if (legend_name=="lex"){
    ggplot(data=sub_prop, aes(x = age, y = prop, group=Type)) +
      geom_point()+ 
      geom_line()+
      geom_smooth(aes(colour = lexical_classes, fill = lexical_classes)) +
      facet_wrap(~ lexical_classes)+
      ylim(0, 1)+
      labs(title="Evolution of reported word comprehension over age ", x="Age (month)", y="Proportion of infant reported to understand words")
  }
  else
  {
    ggplot(data=sub_prop, aes(x = age, y = prop, colour=Type, group=Type)) +
      geom_point()+ 
      geom_line()+
      ylim(0, 1)+
      labs(title="Evolution of reported word comprehension over age ", x="Age (month)", y="Proportion of infant reported to understand words")
  }
}

#select randomly X word types for different lexical open_close and look at the evolution of understanding over age***
proportion_for_sampled_types<-function(data_prop, open_close_name, sample_size, sampling=TRUE, legend_name="lex")
{
  grouped_by_cat<-data_prop%>%
    select(age, Type, open_close)%>%
    filter(age==13, open_close %in% open_close_name)%>%
    group_by(open_close)
  
  if (sampling==TRUE)
  { sampled_types<- grouped_by_cat%>%
    nest()%>%
    mutate(n = sample_size) %>%
    mutate(samp = map2(data,n, sample_n))%>%
    select(open_close, samp) %>%
    unnest()
  }
  else
  {sampled_types<- grouped_by_cat}
  
  sub_prop <- data_prop%>%
    filter(Type %in% as.list(sampled_types$Type)) # for all ages
  
  if (legend_name=="lex"){
    ggplot(data=sub_prop, aes(x = age, y = prop, group=Type)) +
      geom_point()+ 
      geom_line()+
      geom_smooth(aes(colour = open_close, fill = open_close)) +
      facet_wrap(~ open_close)+
      ylim(0, 1)+
      labs(title="Evolution of reported word comprehension over age ", x="Age (month)", y="Proportion of infant reported to understand words")
  }
  else
  {
    ggplot(data=sub_prop, aes(x = age, y = prop, colour=Type, group=Type)) +
      geom_point()+ 
      geom_line()+
      ylim(0, 1)+
      labs(title="Evolution of reported word comprehension over age ", x="Age (month)", y="Proportion of infant reported to understand words")
  }
}


