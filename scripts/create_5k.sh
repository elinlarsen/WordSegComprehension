cd $1
mkdir ../5k/
for i in {0..9}
do
	head -n 5000 ortholines$i.txt > ../5k/ortholines$i.txt
	head -n 5000 tags$i.txt > ../5k/tags$i.txt
done
