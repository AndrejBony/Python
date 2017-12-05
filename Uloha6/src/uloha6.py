#!/usr/bin/python
# -*- coding: utf-8 -*-

from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import json
import sqlite3
import sys
from urllib.parse import urlparse, parse_qs

PORT = 8000


class Server(BaseHTTPRequestHandler):   
    def _set_headers(self, mimetype):
        self.send_response(200)
        self.send_header('Content-type', mimetype)
        self.end_headers()
     
    def do_GET(self):
        if self.path.endswith("html"):
            mimetype = 'text/html'
            self._set_headers(mimetype)
            url = "http://localhost:8000" + self.path
            par = parse_qs(urlparse(url).query)
            if par['f'][0] == "html":
                output = find_name(par['q'][0])
                html = "<html> <head><title> Composers </title> </head> <body>"
                for c in output:
                    html = html + """<p> Composer: <b>%s</b><br/>
                    Genre: %s<br/>
                    Key: %s<br/>
                    Incipit: %s<br/>
                    Composition year: %s<br/>
                    Edition: %s<br/>
                    Publication year: %s<br/>
                    Partiture: %s<br/>
                    Voices: %s </p>""" % (c["Composer"], c["Genre"], c["Key"], c["Incipit"], c["Composition year"], c["Edition"], c["Publication year"], c["Partiture"], str(c["Voice"]), )
                html = html + "</body> </html>" 
                self.wfile.write(bytes(html, 'UTF-8')) 
        elif self.path.endswith("json"):    
            mimetype = 'application/json'
            self._set_headers(mimetype)
            url = "http://localhost:8000" + self.path
            par = parse_qs(urlparse(url).query)
            if par['f'][0] == "json":
                output = find_name(par['q'][0])
                html = json.dumps(output, indent = 2)
                self.wfile.write(bytes(html, 'UTF-8'))
        else:
            html = """<!DOCTYPE html><html><head><meta charset="UTF-8" /><title>Response from python</title></head>
            <body>
            <form action="/result" method="get">
            Composer name:<br />
            <input type="text" name="q" /><br />
            Format:<br />
            <select name="f">
                <option value="json">Json</option>
                <option value="html" selected>Html</option>
            </select>
            <br />
            <br />
            <input type="submit" value="Submit" />
            </form>
            </body>
            </html>"""
            mimetype = 'text/html'
            self._set_headers(mimetype)
            self.wfile.write(bytes(html, 'UTF-8'))
            return
            
            
            
                      
def run(server_class=HTTPServer, handler_class=Server, port=PORT):
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        print('Starting httpd..., serving on port: %d' % PORT)
        httpd.serve_forever()
        
def find_composers(c,str):
    composers = c.execute("SELECT DISTINCT s.id, p.name, s.genre, s.key, s.incipit, s.year, e.name, e.year, prt.partiture " +
                          "FROM person AS p JOIN score_author AS sa ON p.id = sa.composer " + 
                          "JOIN score AS s ON s.id = sa.score " +
                          "JOIN edition AS e ON s.id = e.score " +
                          "JOIN print AS prt ON prt.edition = e.id " + 
                          "WHERE p.name LIKE (?)", ['%' + str + '%'])
    return composers.fetchall()

def find_voices(c,str):
    voices = c.execute("SELECT DISTINCT v.score, v.number, v.name " + 
                       "FROM voice AS v JOIN score_author AS sa ON v.score = sa.score " +
                       "JOIN person AS p ON sa.composer = p.id " +
                       "WHERE p.name LIKE (?)", ['%' + str + '%'])
    return voices.fetchall()    
    
def find_name(name):
    s = []
    conn = sqlite3.connect('scorelib.dat')
    c = conn.cursor()
    composers = find_composers(c,name)
    voices = find_voices(c,name)
    if not composers:
        print("Composer/s not found")
    else:
        i = 0
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
            s.append(d)
        return s
    
    
    
    
if __name__ == "__main__":
    run()
    
