#$1 : min-K
#$2 : max-K
#$3 : PATH/TO/RES/ ?
#for j in {$1..$2}
#for ((j=$1;j<=$2;j+10))
j=$1

	/Users/gladysbaudet/Desktop/PFE/scripts/create_archi.sh /Users/gladysbaudet/Desktop/PFE/Results/$j\k
	for i in {0..9}
	do
  		python all_algo.py /Users/gladysbaudet/Desktop/PFE/sub_corpus/$j\k/tags$i.txt $i $j\k 'phoneme'
  	echo sub $i done
	done


