# From Mika Braginsky github
# Gets stems for a list of words in a given language.
# Uses Snowball if it is available, otherwise uses a special case stemmer
# So far: Croatian (uses Steven Koch's implementation of the Zagreb Stemer)
#croatian_path <- file.path(getwd(), "croatian.py")

stem <- function(words, language) {
  
  language <- tolower(language)
  
  if (language %in% SnowballC::getStemLanguages()) {
    SnowballC::wordStem(words, language)
    
  } else if (language == "croatian") {
    chunk_size <- 1000
    word_chunks <- split(words, ceiling(seq_along(words) / chunk_size))
    purrr::map(word_chunks, function(word_chunk) {
      system2("python", args = c("croatian.py", sprintf('"%s"', word_chunk)),
              stdout = TRUE)
    }) %>% unlist()
    
  } else {
    warning(sprintf("language %s not in list of stemmable languages", language))
    words
  }
}