require(tidyverse) 
path_to_CDI="/Users/elinlarsen/GoogleDrive/PhD_elin/Projets/CDSwordseg_Pipeline/CDI/english/"
path_to_CDI_lexClass="/Users/elinlarsen/GoogleDrive/PhD_elin/Projets/CDSwordSeg_Pipeline//CDI/english/New_lexclass.csv"

lexClass <- read_delim(path_to_CDI_lexClass, "\t", escape_double = FALSE, trim_ws = TRUE)
open_close_class<-lexClass%>%
  select( Type, lexical_classes)%>%
  mutate(open_close=lexical_classes)%>%
  select( Type, open_close)

open_close_class$open_close<-gsub("adverbs", "function", open_close_class$open_close) # order is important !!!
open_close_class$open_close<-gsub("pronouns", "function", open_close_class$open_close)# order is important !!!
open_close_class$open_close<-gsub("verbs", "content", open_close_class$open_close)
open_close_class$open_close<-gsub("nouns", "content", open_close_class$open_close)
open_close_class$open_close<-gsub("adjectives", "content", open_close_class$open_close)
open_close_class$open_close<-gsub("exclamation", "content", open_close_class$open_close)
open_close_class$open_close<-gsub("prepositions", "function", open_close_class$open_close)
open_close_class$open_close<-gsub("onomatopoeia", "other", open_close_class$open_close)
open_close_class$open_close<-gsub("determiners", "function", open_close_class$open_close)
open_close_class$open_close<-gsub("wh-", "function", open_close_class$open_close)

#Writing a new file with final lexical classes
write.table(open_close_class, paste(path_to_CDI, "/open_close_class.csv", sep=""), na = "NA", append = FALSE, col.names = TRUE, sep="\t", row.names = FALSE)

