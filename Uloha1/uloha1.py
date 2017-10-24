# -*- coding: utf-8 -*-
import re
from collections import Counter

f = open(r'scorelib.txt', 'r', encoding = "UTF-8")
regexComposer = re.compile( r"Composer: (.*)" )
regexCentury = re.compile( r"Composition Year: (.*)" )
regexTitle = re.compile( r"Title: (.*)")
regexKey = re.compile( r"Key: (.*)")
comps = Counter()
cents = Counter()
keys = Counter()
for line in f:
    # How many pieces of each Composer
    composer = regexComposer.match(line)
    if composer is not None:
        if composer.group(1).strip() != "":
             comps[composer.group(1).strip()] += 1    
    
    # How many pieces of each Century
    year = regexCentury.match(line) 
    if year is not None:
        cent = year.group(1)
        splited_date = cent.split(" ")
        for i in splited_date:
            regexYear = re.compile(r"\d{3,4}")
            y = regexYear.match(i)
            if y is not None:
                cent = y.group(0).strip()
                cent = (int(cent) - 1) / 100 + 1 
                cents[int(cent)] += 1
    
    # How many pieces of key c minor
    title = regexTitle.match(line)
    if title is not None:
        if "c min" in title.group(1):
            keys["key c minor"] += 1
    key = regexKey.match(line)
    if key is not None:
        if "c min" in key.group(1):
            keys["key c minor"] += 1

# Prints composers 
for k, v in sorted(comps.items()):
    print(k + ": " + repr(v))

print("\n")
#  Prints centuries
for k, v in sorted(cents.items()):
    print(repr(k) + "th century: " + repr(v))
    
print("\n")
# Prints key c minor
for k, v in keys.items():
    print(k + ": " + repr(v))
    

    


