# -*- coding: utf-8 -*-
import re # regular expressions
import sqlite3
import os

# This is a base class for objects that represent database items. It implements
# the store() method in terms of fetch_id and do_store, which need to be
# implemented in every derived class (see Person below for an example).

class DBItem:
    def __init__( self, conn ):
        self.id = None
        self.cursor = conn.cursor()

    def store( self ):
        self.fetch_id()
        if ( self.id is None ):
            self.do_store()
            self.cursor.execute( "select last_insert_rowid()" )
            self.id = self.cursor.fetchone()[ 0 ]

# Example of a class which represents a single row of a single database table.
# This is a very simple example, since it does not contain any references to
# other objects.

class Person( DBItem ):
    def __init__( self, conn, string ):
        super().__init__( conn )
        self.born = self.died = None
        self.name = re.sub( '\([0-9/+-]+\)', '', string ).strip()
        # NB. The code below was part of the exercise (extracting years of birth & death
        # from the string).
        m = re.search( "([0-9]+)--([0-9]+)", string )
        if not m is None:
            self.born = int( m.group( 1 ) )
            self.died = int( m.group( 2 ) )

    # TODO: Update born/died if the name is already present but has null values for
    # those fields. We assume that names are unique (not entirely true in practice).
    def fetch_id( self ):
        self.cursor.execute( "select id, born, died from person where name = ?", (self.name,) )
        
        # NB. The below lines had a bug in the original version of
        # scorelib-import.py (which however only becomes relevant when you
        # start implementing the Score class).
        res = self.cursor.fetchone()
        if not res is None: # TODO born/died update should be done inside this if
            self.id = res[ 0 ]
            if (res[ 1 ] is None and self.born is not None) or (res[ 2 ] is None and self.died is not None):
                self.cursor.execute(" update person set born = ? and died = ? where id = ?", (self.born, self.died, self.id,))

    def do_store( self ):
        print ("storing '%s'" % self.name)
        # NB. Part of the exercise was adding the born/died columns to the below query.
        self.cursor.execute( "insert into person (name, born, died) values (?, ?, ?)",
                             ( self.name, self.born, self.died ) )


class ScoreAuthor( DBItem ):
    def __init__( self, conn, scoreId, composerId ):
        super().__init__( conn )
        self.scoreId = scoreId
        self.composerId = composerId
        
    def fetch_id( self ):
        self.cursor.execute( "select id from score_author where score = ? and composer = ?", (self.scoreId, self.composerId,) )
        res = self.cursor.fetchone()
        if not res is None:
            self.id = res[ 0 ]
            
    def do_store( self ):
        print ("storing score_author '%s', '%s'" % (self.scoreId, self.composerId,))
        self.cursor.execute( "insert into score_author (score, composer) values (?, ?)",
                             ( self.scoreId, self.composerId) )


class EditionAuthor( DBItem ):
    def __init__( self, conn, editionId, editorId ):
        super().__init__( conn )
        self.editionId = editionId
        self.editorId = editorId
        
    def fetch_id( self ):
        self.cursor.execute( "select id from edition_author where edition = ? and editor = ?", (self.editionId, self.editorId,) )
        res = self.cursor.fetchone()
        if not res is None: 
            self.id = res[ 0 ]
            
    def do_store( self ):
        print ("storing edition_author '%s', '%s'" % (self.editionId, self.editorId,))
        self.cursor.execute( "insert into edition_author (edition, editor) values (?, ?)",
                             ( self.editionId, self.editorId) )


class Print( DBItem ):
    def __init__( self, conn, partiture, editionId  ):
        super().__init__( conn )
        self.partiture = partiture
        self.editionId = editionId
        
    def fetch_id( self ):
        self.cursor.execute( "select id from print where partiture = ? and edition = ?", (self.editionId, self.editionId,) )
        res = self.cursor.fetchone()
        if not res is None: 
            self.id = res[ 0 ]
            
    def do_store( self ):
        print ("storing print '%s', '%s'" % (self.editionId, self.partiture,))
        self.cursor.execute( "insert into print (partiture, edition) values (?, ?)",
                             ( self.partiture, self.editionId) )


class Voice( DBItem ):
    def __init__( self, conn):
        super().__init__( conn )
        self.number = None
        self.scoreId = None
        self.name = None
        
    def fetch_id( self ):
        self.cursor.execute( "select id from voice where score = ? and name = ? and number = ?", (self.scoreId, self.name, self.number,) )
        res = self.cursor.fetchone()
        if not res is None:
            self.id = res[ 0 ]
            
    def do_store( self ):
        print ("storing voice '%s', '%s', '%s'" % (self.number, self.scoreId, self.name,))
        self.cursor.execute( "insert into voice (number, score, name) values (?, ?, ?)",
                             ( self.number, self.scoreId, self.name) )
     
                             
class Edition( DBItem ):
    def __init__( self, conn):
        super().__init__( conn )
        self.scoreId = None
        self.name = None
        self.year = None
        self.partiture = "N"
        self.editors = []
        
    def fetch_id( self ):
        self.cursor.execute( "select id from edition where score = ? and name = ? and year = ?", (self.scoreId, self.name, self.year,) )
        res = self.cursor.fetchone()
        if not res is None:
            self.id = res[ 0 ]
            
    def do_store( self ):
        print ("storing edition '%s', '%s', '%s'" % (self.scoreId, self.name, self.year,))
        self.cursor.execute( "insert into edition (score, name, year) values (?, ?, ?)",
                             ( self.scoreId, self.name, self.year ) )


class Score( DBItem ):
    def __init__( self, conn):
        super().__init__( conn )
        self.genre = None
        self.key = None
        self.incipit = None
        self.year = None
        self.composers = []
        self.voices = []
        self.editions = []

    def fetch_id( self ):
        self.cursor.execute( "select id from score where genre = ? and key = ? and incipit = ? and year = ?", (self.genre, self.key, self.incipit, self.year,) )
        res = self.cursor.fetchone()
        if not res is None:
            self.id = res[ 0 ]

    def do_store( self ):
        print ("storing score '%s' , '%s' , '%s' , '%s'  " % (self.genre, self.key, self.incipit, self.year))
        self.cursor.execute( "insert into score (genre, key, incipit, year) values (?, ?, ?, ?)",
                             ( self.genre, self.key, self.incipit, self.year ) )
          
            
def process (k, v, score, edition): 
    if k == 'Editor':
        for c in v.split(','):
            if c is None or c.strip() == "":
                continue
            p = Person( conn, c.strip() )
            p.store()
            edition.editors.append(p)
    elif k == 'Composer':
        for c in v.split(';'):
            if c is None or c.strip() == "":
                continue
            p = Person( conn, c.strip() )
            p.store()
            score.composers.append(p)       
    elif k == 'Genre':
        score.genre = v.strip()
    elif k == 'Key':
        score.key = v.strip()
    elif k == 'Composition Year':
        score.year = v.strip()
    elif 'Voice' in k:
        c = k.split(" ")
        if c[0] == 'Voice':
            voice = Voice(conn)
            voice.number = c[1]
            voice.name = v.strip()
            score.voices.append(voice)
    elif k == 'Partiture':
        if 'yes' in v:
            if 'partial' in v:
                edition.partiture = "P"
            else: edition.partiture = "Y"   
    elif k == 'Publication Year':
        edition.year = v.strip()
    elif k == 'Edition':
        edition.name = v.strip()
        score.editions.append(edition)
    elif k == 'Incipit':        
        score.incipit = v.strip()
        return True
    return False

    
# Database initialisation: sqlite3 scorelib.dat ".read scorelib.sql"
os.remove('scorelib.dat')
conn = sqlite3.connect( 'scorelib.dat' )
f = open( 'scorelib.sql', 'r')
conn.executescript(f.read())
score = Score(conn)
edition = Edition(conn)
rx = re.compile( r"(.*): (.*)" )
for line in open( 'scorelib.txt', 'r', encoding='utf-8' ):
    m = rx.match( line )
    if m is None: continue
    if process( m.group( 1 ), m.group( 2 ), score, edition):
        score.store()
        for com in score.composers:
            score_author = ScoreAuthor(conn, score.id, com.id)
            score_author.store()
        for voi in score.voices:
            voi.scoreId = score.id
            voi.store()
        for edi in score.editions:
            edi.scoreId = score.id
            edi.store()
        for e in edition.editors:
            edition_author = EditionAuthor(conn, edition.id, e.id)
            edition_author.store()
        p = Print(conn, edition.partiture, edition.id)
        p.store()
        score = Score(conn)
        edition = Edition(conn)
        
conn.commit()
