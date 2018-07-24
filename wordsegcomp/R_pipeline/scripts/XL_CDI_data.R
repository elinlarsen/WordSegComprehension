source("util.R")
reports_across_languages=function(path_to_CDI, LANGUAGES, FORM, MEASURE, age_range)
{
  datalist = list()
  index=0
  for (l in LANGUAGES)
  {
    index=index+1
    p=paste(path_to_CDI, l,  "/instrument_data_" , FORM, ".csv", sep="")
    df=read_csv(p)
    d<-df%>%
      filter(type == "word")%>%
      rename(task_score=value, Type=definition)%>%
      mutate(form=FORM, measure=MEASURE, language=l)%>%
      select(data_id, task_score, age, form, measure, Type)
  
      d$task_score[d$task_score=="produces"]=1
      d[is.na(d)] <- 0
      if (FORM=="WG"){d$task_score[d$task_score=="understands"]=1}
      d$task_score=as.integer(d$task_score)

      nb_reports=get_parental_reports_nb_per_age(d, ages=age_range, FORM, MEASURE, l)
      datalist[[index]]=nb_reports
      
      ### get proportion
      #d_prop=add_prop_column_all_ages(d, age_range, FORM)
      #write.csv(d_prop, paste(path_to_CDI, l, "/prop", FORM, l, ".csv", sep=""))
      
  }
 final <- dplyr::bind_rows(datalist)
 return(final)
}


LANGUAGES=c("spanish", "english", "swedish", "french", "danish")
FORM=c("WG")
MEASURE=c("understands")
path_to_CDI="/Users/elinlarsen/GoogleDrive/PhD_elin/Projets/CDSwordseg_Pipeline/CDI/"
d=reports_across_languages(path_to_CDI, LANGUAGES, FORM, MEASURE)

ggplot(d, aes(x=age, y=nb_reports, fill = language)) + 
  geom_bar(stat="identity", width=0.9,position =  position_dodge(width=0.95)) +
  geom_text(aes(label=nb_reports), vjust=0, color="black", size=3, position = position_dodge(1))+
  labs(title="", y="Number of parental reports", x="Age (month)")+
  scale_x_discrete(limit = c(8:18), labels = c("8", "9", "10", "11", "12", "13", "14", "15","16", "17", "18"))
  #"19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"))+
  theme_linedraw(base_size = 18)+
  theme(legend.position="top")
    #width=0.4, position = position_dodge(width=0.5)
  
  
#XLing R2 
path_res="/Users/elinlarsen/GoogleDrive/PhD_elin/Projets/CrossLingWordSeg/results"
load(paste(path_res, "/r2_all_50k.Rdata", sep=""))
  
#Visualising results
R2_res=as.tibble(R2_res)
R2_res$r2_score=as.numeric(levels(R2_res$r2_score))[R2_res$r2_score]

R2_14=R2_res%>%
  filter(age==14, au!="gold")

R2_14_gold=R2_res%>%
  filter(age==14, au=="gold")


png(paste(path_res, "/R2_danish_french_spanish_swedish_50K_14_mo.png", sep=""), width = 1000, height = 800)

ggplot(R2_14, aes(algo, r2_score, colour=language, shape=unit))+
  geom_point(size=3, alpha=0.9) +
  geom_hline(aes(yintercept=r2_score ), R2_14_gold)+
  #scale_linetype_manual(values = c("Gold" = "dashed"))+
   facet_grid( ~ language)+
  theme_bw(base_size=16)+
  scale_y_continuous(name="Coefficient of determination R2", limits=c(0, 0.2))+
  theme(axis.text.x = element_text(angle=60, hjust=1))

dev.off()
  



  
