# created by elin larsen november 20th 2016
# use the wordbankr package created by http://wordbank.stanford.edu/ team
# #Frank, M. C., Braginsky, M., Yurovsky, D., & Marchman, V. A. (in press). 
# Wordbank: An open repository for developmental vocabulary data. Journal of Child Language.
# another useful website : http://mb-cdi.stanford.edu/

# goal : check if word segmented by all algos (puddle, dibs, TPs, ngrams and AGu) 
# belongs MacArthur-Bates CDIs in English and Spanish with children 8-30 months. 

library(magrittr)
library( dplyr)
library(assertthat)
library(stringr)
library(ggplot2)
library(knitr)
opts_chunk$set(message = FALSE, warning = FALSE, cache = TRUE, fig.align = "center")
library(dplyr)
library(tidyr)
library(purrr)
library(readr)

install.packages("devtools")
devtools::install_github("langcog/langcog")
library(wordbankr)
library(langcog)
library(ggrepel)
library(directlabels)
library(feather)

setwd("/Users/elinlarsen/Documents/")

### Abbreviations :
# aoa : age of acquistion 
# form : 2 types: WS : words and sentences and  WG : words and gestures
#  %>% : pipe symbole used in the library magrittr that put the LHS argument into the Right hand side
# Iconicity : the conceived similarity or analogy between the form of a sign 
#(linguistic or otherwise) and its meaning, as opposed to arbitrariness.


############## ESTIMATING AGE OF ACQUISITION :AOA

# come from https://github.com/mikabr/aoa-prediction
aoa_data <- feather::read_feather("aoa-prediction-master/aoa_estimation/saved_data/aoa_data.feather")

### connection to wordbank database
data_mode <- "remote"

admins <- get_administration_data(mode = data_mode) %>%
  select(data_id, age, language, form)

# all items in all languages
items <- get_item_data(mode = data_mode) %>%
  mutate(num_item_id = as.numeric(substr(item_id, 6, nchar(item_id))),
         definition = tolower(definition))

languages <- c( "English", "French (Quebec)", "Italian",
               "Norwegian", "Russian", "Spanish", "Swedish", "Turkish")

# choose words in english
words <- items %>%
  filter(type == "word", language=="English")

invalid_uni_lemmas <- words %>%
  group_by(uni_lemma) %>%
  filter(n() > 1,
         length(unique(lexical_class)) > 1) %>%
  select(language, uni_lemma, lexical_class, definition) %>%
  arrange(language, uni_lemma)

get_inst_data <- function(inst_items) {
  inst_language <- unique(inst_items$language)
  inst_form <- unique(inst_items$form)
  inst_admins <- filter(admins, language == inst_language, form == inst_form)
  get_instrument_data(instrument_language = inst_language,
                      instrument_form = inst_form,
                      items = inst_items$item_id,
                      administrations = inst_admins,
                      iteminfo = inst_items,
                      mode = data_mode) %>%
    filter(!is.na(age)) %>%
    mutate(produces = !is.na(value) & value == "produces",
           understands = !is.na(value) &
             (value == "understands" | value == "produces")) %>%
    select(-value) %>%
    gather(measure, value, produces, understands) %>%
    mutate(language = inst_language,
           form = inst_form)
}

get_lang_data <- function(lang_items) {
  lang_items %>%
    split(.$form) %>%
    map_df(get_inst_data) %>%
    # production for WS & WG, comprehension for WG only
    filter(measure == "produces" | form == "WG")
}

raw_data <- words %>%
  split(.$language) %>%
  map(get_lang_data)

#Fit models to predict the proportion of children of each age 
# who are reported to understands/produce each word, and the word's age of acquisition.

fit_inst_measure_uni <- function(inst_measure_uni_data) {
  
  ages <- min(inst_measure_uni_data$age):max(inst_measure_uni_data$age)
  
  constants <- inst_measure_uni_data %>%
    ungroup() %>%
    select(language, measure, uni_lemma, lexical_class, words) %>%
    distinct() %>%
    group_by(language, measure, uni_lemma) %>%
    summarise(lexical_classes = lexical_class %>% unique() %>% sort() %>%
                paste(collapse = ", "),
              words = words %>% strsplit(", ") %>% unlist() %>% unique() %>%
                paste(collapse = ", "))
  
  props <- inst_measure_uni_data %>%
    ungroup() %>%
    select(age, prop)
  
  tryCatch({
    model <- robustbase::glmrob(cbind(num_true, num_false) ~ age,
                                family = "binomial",
                                data = inst_measure_uni_data, y = TRUE)
    fit <- predict(model, newdata = data.frame(age = ages), se.fit = TRUE)
    aoa <- -model$coefficients[["(Intercept)"]] / model$coefficients[["age"]]
    fit_prop <- inv.logit(fit$fit)
    fit_se <- fit$se.fit
  }, error = function(e) {
    aoa <<- fit <<- fit_prop <<- fit_se <<- NA
  })
  
  data_frame(age = ages, fit_prop = fit_prop, fit_se = fit_se,
             aoa = aoa, language = constants$language,
             measure = constants$measure,
             uni_lemma = constants$uni_lemma,
             lexical_classes = constants$lexical_classes,
             words = constants$words) %>%
    left_join(props, by = "age")
}

fit_inst_measure <- function(inst_measure_data) {
  inst_measure_by_uni <- inst_measure_data %>%
    group_by(language, measure, lexical_class, uni_lemma, age, data_id) %>%
    summarise(uni_value = any(value),
              words = definition %>% sort() %>% paste(collapse = ", ")) %>%
    group_by(language, measure, lexical_class, uni_lemma, words, age) %>%
    summarise(num_true = sum(uni_value, na.rm = TRUE),
              num_false = n() - num_true,
              prop = mean(uni_value, na.rm = TRUE))
  inst_measure_by_uni %>%
    split(.$uni_lemma) %>%
    map_df(fit_inst_measure_uni)
}

fit_inst <- function(inst_data) {
  print(unique(inst_data$language))
  lang_uni_lemmas <- inst_data %>%
    select(uni_lemma, definition) %>%
    distinct() %>%
    filter(!is.na(uni_lemma))
  inst_data_mapped <- inst_data %>%
    select(-uni_lemma) %>%
    left_join(lang_uni_lemmas) %>%
    filter(!is.na(uni_lemma)) %>%
    group_by(definition) %>%
    filter("WG" %in% form)
  inst_data_mapped %>%
    split(.$measure) %>%
    map_df(fit_inst_measure)
}

all_prop_data <- map_df(raw_data, fit_inst)
feather::write_feather(all_prop_data, "aoa-prediction-master/aoa_estimation/saved_data/all_prop_data_english.feather")


# Narrow down data to proportion of kids knowing or producing the word
prop_data <- all_prop_data %>%
  select(language, measure, lexical_classes, words, prop) %>%
  distinct()

words_all_algos=WordsSegmentedAllAlgosIn10sub

prop_understands= subset(prop_data, measure=="understands", select=c(language, lexical_classes, words, prop))
colnames(prop_understands)[3]<-"uni_lemma"
prop_understands=subset(prop_understands, select=c( lexical_classes, uni_lemma, prop))



#Get items, words, and uni_lemmas.
aoa_data <- feather::read_feather("aoa-prediction-master/aoa_estimation/saved_data/aoa_data.feather")
languages <- unique(aoa_data$language)
norm_lang <- function(lang) {
  lang %>% tolower() %>%
    map_chr(~.x %>% strsplit(" ") %>% unlist() %>% .[1])
}


#Get measure extracted from CHILDES -- unigram count, mean sentence length, utterance-final position count, singleton count.

childes_data_en<-read_csv("aoa-prediction-master/aoa_prediction/predictors/childes/data/childes_english.csv")
colnames(childes_data_en)[1]<-"uni_lemma"

summary_childes_en<-read_csv("aoa-prediction-master/aoa_prediction/predictors/childes/data/childes_english.csv")%>%
  filter(!is.na(word)) %>%
  summarise(MLU = weighted.mean(mean_sent_length, word_count, na.rm = TRUE),
            word_count = sum(word_count, na.rm = TRUE),
            MLU = ifelse(word_count < 10, NA, MLU),
            final_count = sum(final_count, na.rm = TRUE),
            solo_count = sum(solo_count, na.rm = TRUE))

#safe_log <- function(x) ifelse(x == 0, NaN, log(x))
uni_childes <- childes_data_en %>%
  filter(!is.na(word)) %>%
  filter(word_count != 0) %>%
  mutate(word_count = word_count + 1,
         frequency = log(word_count / sum(word_count)),
         final_count = final_count + 1,
         final_freq = log((final_count - solo_count) /
                            sum(final_count - solo_count)),
         solo_count = solo_count + 1,
         solo_freq = log(solo_count / sum(solo_count)))

uni_childes$final_frequency <- lm(final_freq ~ frequency,
                                  data = uni_childes)$residuals
uni_childes$solo_frequency <- lm(solo_freq ~ frequency,
                                 data = uni_childes)$residuals
uni_childes$language<-matrix("English",nrow(uni_childes),1)

colnames(uni_childes)[1]<-"uni_lemma"

#### Valence
valence <- read_csv("aoa-prediction-master/aoa_prediction/predictors/valence/valence.csv") %>%
  select(Word, V.Mean.Sum, A.Mean.Sum, D.Mean.Sum) %>%
  rename(word = Word, valence = V.Mean.Sum, arousal = A.Mean.Sum,
         dominance = D.Mean.Sum)

replacements_valence <- read_csv("aoa-prediction-master/aoa_prediction/predictors/valence/valence_replace.csv")
uni_valences <- uni_lemmas %>%
  left_join(replacements_valence) %>%
  rowwise() %>%
  mutate(word = if (!is.na(replacement) & replacement != "") replacement else uni_lemma) %>%
  select(-replacement) %>%
  left_join(valence) %>%
  select(-word)


#concretness
concreteness <- read_csv("aoa-prediction-master/aoa_prediction/predictors/concreteness/concreteness.csv")

replacements_concreteness <- read_csv("aoa-prediction-master/aoa_prediction/predictors/concreteness/concreteness_replace.csv")
uni_concreteness <- uni_lemmas %>%
  left_join(replacements_concreteness) %>%
  rowwise() %>%
  mutate(Word = if (!is.na(replacement) & replacement != "") replacement else uni_lemma) %>%
  select(-replacement) %>%
  left_join(concreteness) %>%
  rename(concreteness = Conc.M) %>%
  select(uni_lemma, concreteness)


#Get estimates of iconicity and babiness.
babiness <- read_csv("aoa-prediction-master/aoa_prediction/predictors/babiness_iconicity/english_iconicity.csv") %>%
  group_by(word) %>%
  summarise(iconicity = mean(rating),
            babiness = mean(babyAVG))

replacements_babiness <- read_csv("aoa-prediction-master/aoa_prediction/predictors/babiness_iconicity/babiness_iconicity_replace.csv")
uni_babiness <- uni_lemmas %>%
  left_join(replacements_babiness) %>%
  rowwise() %>%
  mutate(word = if (!is.na(replacement) & replacement != "") replacement else uni_lemma) %>%
  select(-replacement) %>%
  left_join(babiness) %>%
  select(-word)


# get english phonemes and syllabe
phonemes <- read_csv("aoa-prediction-master/aoa_prediction/predictors/phonemes/english_phonemes.csv") %>%
  mutate(num_syllables = unlist(map(strsplit(syllables, " "), length)),
         num_phonemes = nchar(gsub("[', ]", "", syllables))) %>%
  select(-phones, -syllables)


#Put together data and predictors.
uni_joined <- prop_understands %>%
  left_join(uni_childes) %>%
  left_join(uni_valences) %>%
  left_join(uni_babiness) %>%
  left_join(uni_concreteness) %>%
  left_join(phonemes) %>%
  distinct()


#Function to get number of characters from item definitions.
#```{r}
num_characters <- function(words) {
  words %>%
    strsplit(", ") %>%
    map(function(word_set) {
      word_set %>%
        unlist() %>%
        strsplit(" [(].*[)]") %>%
        unlist() %>%
        strsplit("/") %>%
        unlist() %>%
        gsub("[*' ]", "", .) %>%
        nchar() %>%
        mean()
    }) %>%
    unlist()
}

#predictors <- c("frequency", "MLU", "final_frequency", "solo_frequency", "length",
                "concreteness", "valence", "arousal", "babiness")

predictors <- c("frequency", "final_frequency", "solo_frequency", "length",
                "concreteness", "valence", "arousal", "babiness")

english <- filter(uni_joined, language == "English")
#ggplot(english, aes(x = log_freq)) + geom_density()
mean_concreteness <- mean(english$concreteness, na.rm = TRUE)
mean_babiness <- mean(english$babiness, na.rm = TRUE)
mean_iconicity <- mean(english$iconicity, na.rm = TRUE)
mean_valence <- mean(english$valence, na.rm = TRUE)
mean_arousal <- mean(english$arousal, na.rm = TRUE)

lang_data_fun <- function(lang, uni_joined, predictors) {
  uni_joined %>%
    #filter(language == lang) %>%
    #mutate(concreteness = ifelse(is.na(concreteness), mean_concreteness, concreteness),
           #babiness = ifelse(is.na(babiness), mean_babiness, babiness),
           #valence = ifelse(is.na(valence), mean_valence, valence),
           #arousal = ifelse(is.na(arousal), mean_arousal, arousal)) %>%
    rowwise() %>%
    mutate(length = num_characters(uni_lemma)) %>%
    ungroup() %>%
    select_(.dots = c("language", "lexical_classes", "uni_lemma", "prop",
                      # select_(.dots = c("language", "measure", "lexical_classes", "uni_lemma", "age", "prop",
                      predictors)) %>%
    group_by(language) %>%
    mutate_each_(funs(as.numeric(scale(.))), predictors) %>%
    ungroup() %>%
    filter(complete.cases(.))
}

lang_model_fun <- function(lang_measure_data, predictors) {
  predictor_formula <- as.formula(
    sprintf("prop ~ %s", paste(predictors, collapse = " + "))
  )
  lm(predictor_formula, data = lang_measure_data, y = TRUE)
}

lang_coef_fun <- function(lang_model) {
  broom::tidy(lang_model) %>%
    filter(term != "(Intercept)") %>%
    select(term, estimate, std.error)
}

all_lang_data <- languages %>%
  map_df(~lang_data_fun(.x, uni_joined, predictors))



#Fit AoA prediction models for each measure across languages.
crossling_model_fun <- function(measure_data, predictors) {
  print("Fitting lmer...")
  predictor_formula <- as.formula(
    sprintf("aoa ~ %s + (1 + %s | language)",
            paste(predictors, collapse = " + "),
            paste(predictors, collapse = " + "))
  )
  lme4::lmer(predictor_formula, data = measure_data,
             control = lme4::lmerControl(optCtrl = list(maxfun = 1e5)))
}

crossling_coef_fun <- function(crossling_model) {
  data.frame(term = row.names(summary(crossling_model)$coefficients),
             estimate = summary(crossling_model)$coefficients[,"Estimate"],
             std.error = summary(crossling_model)$coefficients[,"Std. Error"],
             row.names = NULL) %>%
    filter(term != "(Intercept)")
}

rsq <- function(object) {
  1 - sum(residuals(object, type = "response") ^ 2) / sum((object$y - mean(object$y)) ^ 2)
}

adj_rsq <- function(object) {
  rsq <- rsq(object)
  p <- summary(object)$df[1] - 1  # p
  n_p <- summary(object)$df[2]  # n - p - 1
  rsq - (1 - rsq) * (p / n_p)
}

crossling_rsq_fun <- function(crossling_model) {
  crossling_fit <- lm(
    model.response(model.frame(crossling_model)) ~ fitted(crossling_model),
    y = TRUE
  )
  adj_rsq(crossling_fit)
}

crossling_models <- all_lang_data %>%
  group_by(measure) %>%
  nest() %>%
  mutate(model = map(data, ~crossling_model_fun(.x, predictors)))

crossling_coefs <- crossling_models %>%
  mutate(coef = map(model, crossling_coef_fun),
         adj_rsq = map_dbl(model, crossling_rsq_fun)) %>%
  select(measure, coef, adj_rsq) %>%
  unnest() %>%
  mutate(language = "All Languages")


#Combine by-language coefficients with across-language coefficients.

term_order <- crossling_coefs %>%
  filter(measure == "understands") %>%
  arrange(desc(abs(estimate)))

joint_coefs <- bind_rows(lang_coefs, crossling_coefs) %>%
  split(.$measure) %>%
  map(~.x %>%
        arrange(desc(adj_rsq)) %>%
        mutate(language = factor(
          language, levels = c("All Languages",
                               unique(language) %>% discard(~.x == "All Languages"))),
          term = factor(term, levels = rev(term_order$term))))

coef_plot <- function(measure) {
  ggplot(joint_coefs[[measure]], aes(x = term, y = estimate)) +
    facet_wrap(~language, ncol = 4) +
    geom_rect(data = filter(joint_coefs[[measure]], language == "All Languages"),
              aes(fill = language), xmin = -Inf, xmax = Inf,
              ymin = -Inf, ymax = Inf, alpha = 0.03) +
    geom_pointrange(aes(ymin = estimate - 1.96 * std.error,
                        ymax = estimate + 1.96 * std.error,
                        colour = term)) +
    geom_hline(yintercept = 0, color = "grey", linetype = "dashed") +
    geom_text(aes(label = paste("bar(R)^2==", round(adj_rsq, 2))), parse = TRUE,
              y = max(joint_coefs[[measure]]$estimate + 1.96 *
                        joint_coefs[[measure]]$std.error),
              x = 9, family = font, size = 4, hjust = "right") +
    coord_flip() +
    scale_fill_solarized(guide = FALSE) +
    scale_colour_manual(guide = FALSE, values = rev(solarized_palette(length(predictors)))) +
    xlab("") +
    scale_y_continuous(name = "Coefficient Estimate (Months/SD)")
}
coef_plot("understands")
coef_plot("produces")
  
  

