This python code aims at analyzing this output of several word segmentation algorithms in a specified corpus. 
For the study, the corpus has been divided in 10 creating « sub corpus» in order to look at the robustness of the algorithm€™ segmentation. 

The idea is : 
1. to look at the multiple possible intersection between different word segmentation output. 
2. compare the output to the word understood (and in a second step produced) by children (that are listed in CDI). 

We used
* algos : 
	*	dibs ( diphone based segmentation algorithm) : Robert Daland and Janet B Pierrehumbert. Learning diphone-based segmentation.
	*	TPs (transitional probabilities): Amanda Saksida, Alan Langus, and Marina Nespor. Co-occurrence statistics as a language-dependent cue for speech segmentation.)
	*	AGu (adaptor grammar) : Johnson et al., 2014)
	*	puddle : Padraic Monaghan and Morten H. Christiansen.Words in puddles of sound: modelling psycholinguistic effec tsin speech segmentation.
-  Brent corpus of child directed speech 
-  the http://wordbank.stanford.edu/ database

Python code is divided by function purpose : 

* read.py 
	* takes text files input such as « freq-top.txt»  : results of segmentation created by the package wordseg
	* or read data frames (such as the CDI data frames and transforms it into respectively in list or data frame

* translate.py translates phonological form to orthographic ones by creating a dictionary . 

* analyze.py different function to analyse the results of algo

* visualize.py plot CDI score versus Algos score for different ages and compare to the gold. Histogram and fitted regression is also plotted.

* robustness.py looked at the variability of  word segmentation algorithms F-scores for different samples of the same child-directed speech corpus created by the script divide.py in the folder CDS

* get_lexical_class.py : do a part of speech of the Child directed speech corpus and simplify the syntactic categories into 5 lexical classes.

* power_analysis.py : 
	* look at the effect of frequency in the regression. Divide word segmented by a corpus into two frequency groups but matched in term of number of occurrences in the CDS corpus
	* test the number of parental reports necessary to get a statistical difference between the two groups



