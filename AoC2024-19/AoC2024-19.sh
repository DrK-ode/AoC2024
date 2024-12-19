#!/bin/sh
filename=input.txt
grep -c -E '^('"$(head -n 1 $filename | sed -e "s/,\ /|/g")"')+$' "$filename"