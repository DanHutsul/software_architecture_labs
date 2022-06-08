"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import uuid
import hazelcast
class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        response = []
        
        client = hazelcast.HazelcastClient()
        my_map = client.get_map("log-map").blocking()
        response = my_map.entry_set()
        print("Get request: ")
        print(response)
        print("\n\n\n")
        self._set_response()
        self.wfile.write("{0}".format(response).encode('utf-8'))
        client.shutdown()

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # Size of Data
        post_data = self.rfile.read(content_length)#.decode() # Data
        post_msg = post_data.decode().split("msg=")[1]
        post_uuid = post_data.decode().split("msg=")[0].split("UUID=")[1][:-2]

        print("msg = ", post_msg, " UUID = ", post_uuid)

        client = hazelcast.HazelcastClient()
        my_map = client.get_map("log-map").blocking()
        my_map.put(post_uuid, post_msg)

        self._set_response()
        self.wfile.write("POST request {}".format(post_data).encode('utf-8'))
        client.shutdown()



def run(server_class=HTTPServer, handler_class=S, port=8082):
    print("Launched on port ", str(port), "\n")
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run(HTTPServer, 5, 8082)
    #run(HTTPServer, 5, 8083)
    #run(HTTPServer, 5, 8084)