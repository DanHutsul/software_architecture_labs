"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import uuid

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        response = []
        with open('log.log', 'r') as f:
            lines = f.readlines()
            for line in lines:
                response.append(line.split('=')[1][:-1])

        self._set_response()
        self.wfile.write("{0}".format(response).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # Size of Data
        post_data = self.rfile.read(content_length)#.decode() # Data
        post_msg = post_data.decode().split("msg=")[1]
        post_uuid = post_data.decode().split("msg=")[0].split("UUID=")[1][:-2]

        with open('log.log', 'a') as f:
            f.write("{0}={1}\n".format(post_uuid, post_msg))

        self._set_response()
        self.wfile.write("POST request {}".format(post_data).encode('utf-8'))



def run(server_class=HTTPServer, handler_class=S, port=8081):
    logging.basicConfig(filename='example.log', level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()