# let $1, $2 be the names of the directory, filename extension, respectively
#
# Attempt 1: find $1 -name *$2 | wc -l | sort -n -r | head -n 1
#
# This attempt didn't work because you need $(...) to capture the output as an array to pass to
# wc. The way it was written just takes the literal output of find, which is 8 lines, and passes
# that to wc as its literal input.
#
# Attempt 2: wc -l $(find $1 -name *$2) | sort -n -r | grep $2 | head -n 1
#
# This attempt gets us 95% there, but it doesn't return only the filename. Instead, it also returns
# the name of the directory in which the file is found, and its number of lines. We need another
# command to cut down to just the information requested.

# Attempt 3: wc -l $(find $1 -name *$2) | sort -n -r | grep $2 | head -n 1 | cut -d '/' -f 2-
# This attempt gets us close, but it needs to be run in ZIPF and not ZIPF/bin, which is
# probably where it should be. Additionally, find wouldn't work when called in bin and used with -name.

wc -l $1/* | sort -n -r | grep $2 | head -n 1 | cut -d '/' -f 3-
