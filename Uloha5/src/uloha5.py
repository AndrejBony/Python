#!/usr/bin/python
# -*- coding: utf-8 -*-

from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8000

class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
     
    def do_GET(self):
        self._set_headers()
        # Part 1
        self.wfile.write(bytes("<html> <head><title> Hello World </title> </head> <body> Hello World </body> </html>", 'UTF-8'))
        #Part 2
        path = self.path
        headers = self.headers
        path = headers['Referer']
        if path is not None:
            url = path.split("/")
            if url[-1] != "":
                output = "You asked for " + url[-1]
                print(output)         
 
def run(server_class=HTTPServer, handler_class=Server, port=PORT):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd..., serving on port: %d' % PORT)
    httpd.serve_forever()
    
if __name__ == "__main__":
    run()
