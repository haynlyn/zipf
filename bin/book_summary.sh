# Get author information from a Project Gutenberg eBook.
# Usage: bash book_summary.sh /path/to/file.txt field_name
head -n 17 ../data/$1 | tail -n 8 | grep $2
