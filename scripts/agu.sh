#!/bin/bash

# prepare the input for segmentation and generate the gold text
cat $1 | wordseg-prep -u phone --gold gold.txt > prepared.txt
#AG has a similar call but additional files can be provided
# GRAMMAR=test/data/ag/Colloc0_enFestival.lt
GRAMMAR=Colloc0_enFestival.lt
CATEGORY=Colloc0
cat prepared.txt | wordseg-ag  $GRAMMAR $CATEGORY --njobs 4 --verbose > segmented.ag.txt
cat segmented.ag.txt | wordseg-eval gold.txt > eval.ag.txt
