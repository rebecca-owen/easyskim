#!/bin/sh
# Input arguments: <input.pdf> <spellcheck>
#
# Generates read and parsed text output at - input.pdf.txt
# Generates extracted metadata at - input.pdf.meta
#

pdftotext $1 input.txt

meta=$(exiftool $1)

author=$(echo "$meta" | grep Author | sed 's/.*://')
#creator=$(echo "$meta" | grep Creator | sed 's/.*://' )
title=$(echo "$meta" | grep Title | sed 's/.*://')
date=$(echo "$meta" | grep Create | sed 's/Create Date//')
publisher=$(echo "$meta" | grep Publisher | sed 's/.*://')
description=$(echo "$meta" | grep Description | sed 's/.*://')
issn=$(echo "$meta" | grep ISSN | sed 's/.*://')
doi=$(echo "$meta" | grep Doi | sed 's/.*://')

author=$(echo "$author" | sed 's/^[ \t]*//' | sed -r 's/([a-zA-Z0-9]+) ([a-zA-Z0-9]+)/\2 \1/' | sed 's/ /; /') # Swap author first, last name and separate them with a semicolon ;

metacsv=$(echo "{\"Author\":\"$author\",\n
\"Title\":\"$title\",\n
\"Date\":\"$date\",\n
\"Publisher\":\"$publisher\",\n
\"Description\":\"$description\",\n
\"ISSN\":\"$issn\",\n
\"DOI\":\"$doi\"}\n")


echo "$metacsv" > $1.met

# ASCII only filter
tr -cd '\11\12\15\40-\176' < input.txt > input-ascii.txt
mv input-ascii.txt input.txt

#wordMask=$(spell input.txt)

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

line=$(echo "$line" | sed 's/.*address.*//') # Remove lines with address in them i.e. e-mail address


#line=$(echo "$line" | sed -i '/^.$/d')

line=$(echo "$line" | sed 's/Page//') # Remove Page
#line=$(echo "$line" | sed 's/page//')

echo "$line" #> "$1".txt

rm input.txt

# Useful Trash
#line=$(sed 's/298/ /' $1 ) # Remove unnecessary stuff from heading
#sed -i 's/[\d128-\d255]//' FILENAME
