for i in "tp"
do
	for u in "syllable"
	do
		python all_algo.py ../Brent/tags.txt "" "full_corpus" $i $u
	done
done 
