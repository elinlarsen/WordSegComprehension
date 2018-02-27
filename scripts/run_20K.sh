for i in {0..9}
do
  python all_algo.py /Users/gladysbaudet/Desktop/PFE/sub_corpus/10k/tags$i.txt $i '20k' 'phoneme'
  echo sub $i done
done
