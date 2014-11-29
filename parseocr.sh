#!/usr/bin/sh

pdftotext $1 input.txt

wordMask=$(spell input.txt)

line=$(cat input.txt)

#for i in $wordMask
#do
   # do whatever on $i

#sed 's/$i/ /' tmp.txt > tmp.txt

#echo "$i"
#echo "$line"

#sed 's/$i/ /' tmp.txt > tmp2.txt 
#sed -e '/^[[:blank:]]*$/d' tmp2.txt > tmp.txt

#line=$(echo "$line" | sed s/$i//)
#echo "test"
#done

line=$(echo "$line" | sed 's/^.\{,8\}$//') #Remove short random characters (upto 8) starting on e new line

line=$(echo "$line" | sed 'N;/^\n$/d;P;D') # Remove blank lines and leave a single line

line=$(echo "$line" | sed '/^[0-9][0-9]*$/d') # Remove lines starting with single/few numbers

line=$(echo "$line" | sed 's/(.*)//') # Remove short stuff between brackets ()

#line=$(echo "$line" | sed -i '/^.$/d')

line=$(echo "$line" | sed 's/Page//') # Remove Page
#line=$(echo "$line" | sed 's/page//')

echo "$line" > parsed.txt

# Useful Trash
#line=$(sed 's/298/ /' $1 ) # Remove unnecessary stuff from heading
#sed -i 's/[\d128-\d255]//' FILENAME

