dir="/Users/elinlarsen/GoogleDrive/PhD_elin/Projets/WordSegComprehension/wordsegcomp/R_pipeline/"
setwd(dir)
source("util.R")

#Parameters to fill NOW
language="spanish"
path_to_CDI=paste("/Users/elinlarsen/GoogleDrive/PhD_elin/Projets/CDSwordseg_Pipeline/CDI/", language, sep="/")
path_to_CDI_WG_und=paste(path_to_CDI, "/instrument_data_WG.csv", sep="/")
path_to_CDI_WG_prod="/Users/elinlarsen/GoogleDrive/PhD_elin/Projets/CrossLingWordSeg/raw_data/english/int_data_wg_prod.csv"
path_to_CDI_WS="/Users/elinlarsen/GoogleDrive/PhD_elin/Projets/CrossLingWordSeg/raw_data/english/int_data_WS.csv"
path_to_CDI_MonoPoly="/Users/elinlarsen/GoogleDrive/PhD_elin/Projets/CDSwordSeg_Pipeline//CDI/english/Mono_poly_CDI.csv"
path_to_CDI_lexClass="/Users/elinlarsen/GoogleDrive/PhD_elin/Projets/CDSwordSeg_Pipeline//CDI/english/New_lexclass.csv"
path_to_OpenClose="/Users/elinlarsen/GoogleDrive/PhD_elin/Projets/CDSwordSeg_Pipeline//CDI/english/open_close_class.csv"

path_to_CDI_WG_all=paste(path_to_CDI, "/instrument_data_WG.csv", sep="/")

# Data processing

### Word and Gesture comprehension form
# 1. get full per item per infant per age data
#data_per_infant <- get_instrument_data("English (American)", "WG", administrations = TRUE, iteminfo = TRUE) *** If R version < 3.4***
data_per_infant<- read_csv(path_to_CDI_WG_und)
data_per_infant[is.na(data_per_infant)] <- "NA"

# 2. change format of data comprehension
d_WG=read_csv(path_to_CDI_WG_all)
d_WG$form=rep("WG", nrow(d_WG))

d_WG[is.na(d_WG)] <- 0
  
d_WG_comprehension<-d_WG%>%
  filter(type == "word")%>%
  rename(task_score=value, Type=definition)%>%
  select(data_id, task_score, age, Type, form, item_id)

d_WG_comprehension<-d_WG_comprehension%>%
  mutate(form=rep("WG_comprehension", nrow(d_WG_comprehension)))

d_WG_comprehension$task_score[d_WG_comprehension$task_score=="produces"]=1
d_WG_comprehension$task_score[d_WG_comprehension$task_score=="understands"]=1
d_WG_comprehension$task_score=as.integer(d_WG_comprehension$task_score)

# 3. checks if there is the same number of item_id (ie word) per age###
grouped_by_item_age<- d_WG_comprehension%>%
  group_by(item_id, age)%>%
  summarise()

#Number of words in WG comprehension form
d_WG_comprehension%>%
  group_by(Type)%>%
  n_groups()

#Age range in WG comprehension form
age_range=d_WG_comprehension%>%
  group_by(age)%>%
  summarise()

age_range=age_range[[1]]
### Word and Gesture production form
# 1. get WS production
d_WG_prod<- read_csv(path_to_CDI_WG_prod)
# 2. change format of data production
d_WG_production<-d_WG_prod%>%
  #filter(type == "word", value %in% c("NA", "produces"), language=="English (American)")%>%
  filter(type == "word", language=="English (American)")%>%
  rename(task_score=value, Type=definition)%>%
  select(data_id, task_score, age, Type)

d_WG_production<-d_WG_production%>%
  mutate(form=rep("WG_production", nrow(d_WG_production)))

d_WG_production[is.na(d_WG_production)] <- 0
d_WG_production$task_score[d_WG_production$task_score=="produces"]=1
d_WG_production$task_score=as.integer(d_WG_production$task_score)

# 3. checks if there is the same number of item_id (ie word) per age###
d_WG_production%>%
  group_by(Type)%>%
  n_groups()
d_WG_production%>%
  group_by(age)%>%
  summarise(mean=mean(age))



### Word and Sentence production form
# 1. get WS production
d_WS<- read_csv(path_to_CDI_WS)
# 2. change format of data production
d_WS_production<-d_WS%>%
  #filter(type == "word", value %in% c("NA", "produces"), language=="English (American)")%>%
  filter(type == "word", language=="English (American)")%>%
  rename(task_score=value, Type=definition)%>%
  select(data_id, task_score, age, Type)

d_WS_production<-d_WS_production%>%
  mutate(form=rep("WS_production", nrow(d_WS_production)))
d_WS_production[is.na(d_WS_production)] <- 0
d_WS_production$task_score[d_WS_production$task_score=="produces"]=1
d_WS_production$task_score=as.integer(d_WS_production$task_score)



### Get the number of parental reports
df_WG_comp=get_parental_reports_nb_per_age(d_WG_comprehension, ages=age_range, "WG_comprehension")
df_WG_prod=get_parental_reports_nb_per_age(d_WG_production, ages=c(8:30),"WG_production")
df_WS_prod=get_parental_reports_nb_per_age(d_WS_production, ages=c(8:30), "WS_production")

df_nb_reports=rbind(df_WG_comp, df_WG_prod)
df_nb_reports=rbind(df_nb_reports,df_WS_prod)

##Histogram number of parental reports per age
#png( paste(path_to_figures, "Distribution_parental_reports_WG_French.png", sep="") ,width=1800,height=1800, res=200 )
ggplot(data=df_WG_comp, aes(x=age, y=nb_reports, fill = form)) + 
  geom_bar(stat="identity", width=1,position = "dodge") +
  #geom_text(aes(label=nb_reports), vjust=0, color="black", size=3, position = position_dodge(1))+
  labs(title="", y="Number of parental reports", x="Age (month)")+
  scale_x_discrete(limit = c(8:30), labels = c("8", "9", "10", "11", "12", "13", "14", "15","16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"))+
  theme_linedraw(base_size = 18)+
  theme(legend.position="top")
#dev.off()

###Get mean proportion of infants understanding/producing words
d_WG_comp_prop<-add_prop_column_all_ages(d_WG_comprehension, seq(8,18), "WG_comprehension")
d_WG_prod_prop<-add_prop_column_all_ages(d_WG_production, seq(8,18), "WG_production")
d_WS_prod_prop<-add_prop_column_all_ages(d_WS_production, seq(16,30), "WS_production")

write.csv(d_WG_comp_prop, paste(path_to_CDI, "WG_prop", language, ".csv", sep=""))

### Merge all forms
df_all_forms=rbind(d_WG_comp_prop, d_WG_prod_prop)
df_all_forms=rbind(df_all_forms, d_WS_prod_prop)


###Linguistic factors : lexical class, word length, open/close class
# NEW lexical classes
lc <- read_delim(path_to_CDI_lexClass, "\t", escape_double = FALSE, trim_ws = TRUE)%>%
  rename(lc=lexical_classes)

#CDI
cdi_words <- as.data.frame(lc$Type)
colnames(cdi_words)=c("Type")

#Word length : mono versus polysyllabic words
wordLength_cdi <- read_delim(path_to_CDI_MonoPoly, "\t", escape_double = FALSE, trim_ws = TRUE)%>%
  rename(length=num_syllables)%>%
  select(Type, length)
wordLength_cdi$length<-gsub("mono", "M", wordLength_cdi$length)
wordLength_cdi$length<-gsub("poly", "P", wordLength_cdi$length)
wordLength_cdi<-as.data.frame(wordLength_cdi)
wordLength_cdi$length<- as.factor(wordLength_cdi$length) # super important to specify this variable as being factor

#open close class : function versus content words
open_close_class <- read_delim(path_to_OpenClose, "\t", escape_double = FALSE, trim_ws = TRUE)


###Merging linguistic factor
df_linguistic=merge(open_close_class, wordLength_cdi, by="Type")
df_linguistic=merge(df_linguistic, lc, by='Type')

###Merging linguistic factor and CDI data 
df_linguistic_CDI=merge(df_linguistic, df_all_forms, by='Type')

###Store the reshaped database
if (save==TRUE)
{
  #write.table(df_linguistic, paste(path_to_CDI, "/cdi_linguistic_factors.csv", sep=""), na = "NA", append = FALSE, col.names = TRUE, sep="\t", row.names = FALSE)
  write.table(df_linguistic_CDI, paste(path_to_CDI, "/Prop_all_forms_reshaped.csv", sep=""), na = "NA", append = FALSE, col.names = TRUE, sep="\t", row.names = FALSE)
}

