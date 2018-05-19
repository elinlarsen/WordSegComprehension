 # check if the effect of age detected on R2 is due to the imprecision on the number of infant in the CDI
# idea : subsample the number of infant atage 13 take a subsample that has a size equivalent to age 8

install.packages("devtools")
devtools::install_github("langcog/langcog")
library(wordbankr)
library(langcog)
library(ggrepel)
library(directlabels)
library(feather)


######## download the intrument.csv data file
int_data<- read_csv("CDSwordseg_Pipeline/CDI_wordbank/instrument_data.csv")

# choose words in english
words <- int_data %>%
  filter(type == "word", value=="understands")

words_age_13 <- words %>%
  filter(age=='13')

words_age_8<- words %>%
  filter(age=='8')

words_age_18<- words %>%
  filter(age=='18')

#### sample on the number of infants (each infant has an ID)  at age 13
# get the number of infant at age 8 
id_8<-words_age_8['data_id']
nb_infants_8<- id_8[!duplicated(id_8),]

#get the number of infant at age 13<
id_13<-words_age_13['data_id']
nb_infants_13<- id_13[!duplicated(id_13),]

# sample the id of infant in order to have the approximate number of infant at age 8
nb_infant_wanted<- sample(t(as.vector(nb_infants_13)), nrow(nb_infants_8), replace=FALSE)

# dataframe at age 13 with the number of infant wanted
word_per_infant_13_wanted<- words_age_13 %>%
  filter(data_id %in% nb_infant_wanted )

#NB word_age_13 has higher number of words than word_age_8 because infants at 13 knows more words than at 8

#get the proportion of understandingat age 13
# get the number of infant understanding each word => subset on words 
type_13=word_per_infant_13_wanted['definition']

words_13_wanted<-word_per_infant_13_wanted[!duplicated(type_13),]

#for each word, count the number of times it appears (ie is understood) and divide by the number of infants
#=> get the proportion of a word to be understood for each word

df_count_words_13 <- table(word_per_infant_13_wanted['definition'])
prop_13<-df_count_words_13 /length(nb_infant_wanted)

write.csv(x=prop_13, file="prop_13_sample.csv", col.names = TRUE)

