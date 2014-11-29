#!/usr/bin/sh
# Input arguments: <input.pdf> <spellcheck>
#
# Generates read and parsed text output at - input.pdf.txt
# Generates extracted metadata at - input.pdf.meta
#

pdftotext $1 input.txt

meta=$(exiftool $1)

author=$(echo "$meta" | grep Author)
creator=$(echo "$meta" | grep Creator)
title=$(echo "$meta" | grep Title)
date=$(echo "$meta" | grep Create Date)
publisher=$(echo "$meta" | grep Publisher)
description=$(echo "$meta" | grep Description)
issn=$(echo "$meta" | grep ISSN)
doi=$(echo "$meta" | grep Doi)

echo "$author \n$creator \n$title \n$date \n$publisher \n$description \n$issn \n$doi \n" > $1.meta

# ASCII only filter
tr -cd '\11\12\15\40-\176' < input.txt > input-ascii.txt
mv input-ascii.txt input.txt

wordMask=$(spell input.txt)

line=$(cat input.txt)

if [ "$2" = "spellcheck" ]

	then
	echo "Performing spell check..."

	for i in $wordMask
	do
   # do whatever on $i

	#echo "$i"

	line=$(echo "$line" | sed 's/'$i'/ /')
	#echo "test"
	done

fi

line=$(echo "$line" | sed 's/^.\{,8\}$//') #Remove short random characters (upto 8) starting on e new line

line=$(echo "$line" | sed 'N;/^\n$/d;P;D') # Remove blank lines and leave a single line

line=$(echo "$line" | sed '/^[0-9][0-9]*$/d') # Remove lines starting with single/few numbers

line=$(echo "$line" | sed 's/(.*)//') # Remove short stuff between brackets ()

#line=$(echo "$line" | sed -i '/^.$/d')

line=$(echo "$line" | sed 's/Page//') # Remove Page
#line=$(echo "$line" | sed 's/page//')

echo "$line" > "$1".txt

# Useful Trash
#line=$(sed 's/298/ /' $1 ) # Remove unnecessary stuff from heading
#sed -i 's/[\d128-\d255]//' FILENAME
