#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import sqlite3
import json

def find_composers(printId):
    composers = c.execute("select p.name from person as p where p.id in (" + 
                            "select sa.id from score_author as sa where sa.score in (" +
                            "select e.score from edition as e join print on e.id = print.edition where print.id = ?))", [printId])
    return composers.fetchall()

conn = sqlite3.connect( 'scorelib.dat' )
c = conn.cursor()
printId = sys.argv[1]
composers = find_composers(printId)
if not composers:
    print("Composer/s not found")
else: 
    for comp in composers:  
        d = {}
        d["Composer"] = comp[0]
        json.dump(d, sys.stdout, indent=2)   

conn.commit()

