#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import sqlite3
import json

def find_composers(str):
    composers = c.execute(  "SELECT distinct p.name, s.genre, s.key, s.incipit, s.year, e.name, e.year, prt.partiture " +
                            "FROM person AS p JOIN score_author AS sa ON p.id = sa.composer " + 
                                             "JOIN score AS s ON s.id = sa.score " +
                                             "JOIN edition AS e ON s.id = e.score " +
                                             "JOIN print AS prt ON prt.edition = e.id " + 
                                             "WHERE p.name LIKE '%Bach%'")
    return composers.fetchall()

conn = sqlite3.connect( 'scorelib.dat' )
c = conn.cursor()
name = sys.argv[1]
composers = find_composers(name)
if not composers:
    print("Composer/s not found")
else: 
    for comp in composers:  
        d = {}
        d["composer"] = comp
        json.dump(d, sys.stdout, indent=2 )

conn.commit()

