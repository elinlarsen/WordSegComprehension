for line in $(find $1 -name '*segmented*'); do 
     python /Users/gladysbaudet/Desktop/PFE/scripts/process_segmented.py $line ""
done
