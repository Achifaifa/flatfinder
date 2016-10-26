#!/bin/bash

python getlist.py > new.txt
comm <(sort old.txt) <(sort new.txt) -3 > update.txt
mv old.txt old_save.txt
mv new.txt old.txt
xargs sensible-browser < update.txt
