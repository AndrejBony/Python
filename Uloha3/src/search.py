#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import sqlite3
import json

def find_composers(str):
    composers = c.execute(  "SELECT s.id, p.name, s.genre, s.key, s.incipit, s.year, e.name, e.year, prt.partiture " +
                            "FROM person AS p JOIN score_author AS sa ON p.id = sa.composer " + 
                                             "JOIN score AS s ON s.id = sa.score " +
                                             "JOIN edition AS e ON s.id = e.score " +
                                             "JOIN print AS prt ON prt.edition = e.id " + 
                                             "WHERE p.name LIKE (?)", ['%'+ str +'%'])
    return composers.fetchall()

def find_voices(str):
    voices = c.execute( "SELECT v.score, v.number, v.name " + 
                        "FROM voice AS v JOIN score_author AS sa ON v.score = sa.score " +
                                        "JOIN person AS p ON sa.composer = p.id " + 
                                        "WHERE p.name LIKE (?)", ['%'+ str +'%'])
    return voices.fetchall()         
    
conn = sqlite3.connect( 'scorelib.dat' )
c = conn.cursor()
name = sys.argv[1]
composers = find_composers(name)
voices = find_voices(name)
if not composers:
    print("Composer/s not found")
else: 
    for comp in composers:  
        d = {}
        d["Composer"] = comp[1]
        d["Genre"] = comp[2]
        d["Key"] = comp[3]
        d["Incipit"] = comp[4]
        d["Composition year"] = comp[5]
        d["Edition"] = comp[6]
        d["Publication year"] = comp[7]
        d["Partiture"] = comp[8]
        d["Voice"] = {}
        for voice in voices:
            v = {}
            if comp[0] == voice[0]:
                for i in range(2, len(voice)):   
                        v[voice[i-1]] = voice[i]
                        d["Voice"].update(v)
        json.dump( d, sys.stdout, indent = 2 )


        # d["Voice"] = [{voice[i-1]: voice[i]} (i) for voice in voices for i in range(2, len(voice)) if voice[0] == comp[0]]
conn.commit()

