# WordSegComprehension
Analyse the output of word segmentation algorithms fed with phonological transcription of Child-directed speech by looking at its correlation to reported infant word comprehension (available in wordbank) at different ages for a given language

# Requirement 
* python > 2.7
* plotly `pip install plotly`

# Package architecture
* pipeline : contains every python scripts to
	*  analyse word segmentation algorithms results (analyse.py)
	*  transform phonologized segmnented in orthographic words for correct segmentation (translate.py)
	*  read text file and transform them in dataframe (read.py)
	*  look at the correlation between corrected segmented occurrences of words by each algorithm with the reported proportion in CDI of infants understading those words (model.py)
	*  visualize this correlation (visualize.py)
	*  check the robustness of the correlation (robustness.py)
	*  do a part-of-speech tagging of the child-directed corpus and extract for each word its coarse lexical class (get_lexical_class.py)
* example
	* english/ brent-siskind : python script that use the pipeline for algorithms using the Brent-siskind child-directed corpus and english CDI

	

# Data and folder format
* For the CDS corpus segmented by different algorithms, the input file is a text file named  by default "freq-top.txt" that contains all segmented words in phologized form sorted by decreasing order with their occurrences number on the first column
* For the CDI, the input file is a csv file containing as columns : 
	* the types in the CDI ("Type")
	* the proportion of infants understanding (or producing) the types ("prop")
	* the age at which they understand (or produce) each type ("age")
	* the lexical class of the type ("lexical_class")
This dataframe can be created using the [wordbank R package](https://github.com/langcog/wordbank)
* The results of the word segmentation algorithms should be stored in folders having the following architecture (algo/unit/) and the following names
	* algorithms name should either "AGu", "PUDDLE", "DiBS", "gold", "TPs"
	* unit is either "phoneme" or "syllable"
* NB : the "gold" is not the name of an algorithm but refered rather as the gold corpus  
