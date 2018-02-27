for line in $(find $1 -name '*gold*'); do
     python /Users/gladysbaudet/Desktop/PFE/scripts/process_segmented.py $line ""
done
