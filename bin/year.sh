for book in "$@"
do
	title=$(bash book_summary.sh "$book" Title | cut -d ':' -f 2- | cut -d ' ' -f 2-)
	year=$(grep "$title" ../titles.txt | cut -d ',' -f 2)
	echo $year >> foo
done
echo Printing unique years among filenames to stdout

echo $(sort ./foo | uniq)

# Cleanup
rm foo
