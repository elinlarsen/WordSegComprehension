echo $(dirname $1) done
touch $(dirname $1)/$(basename $1).txt

number=$(echo $(basename $1) | egrep -o '[[:digit:]]' | head -n1)

echo $number
echo $number\.txt
