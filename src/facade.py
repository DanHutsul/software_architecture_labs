from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import uuid


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        to_send_url_logger = "http://localhost:8081"
        response_logger = requests.get(to_send_url_logger)
        to_send_url_message = "http://localhost:8082"
        response_message = requests.get(to_send_url_message)
        self._set_response()
        self.wfile.write("{0}".format([response_logger.text, response_message.text]).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # Size of Data
        post_data = self.rfile.read(content_length)#.decode() # Data
        post_msg = post_data.decode().split("msg=")[0]
        data_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS , post_msg)) # Get UUID
        self._set_response()
        self.wfile.write("POST request {}".format(post_data).encode('utf-8'))
        to_send_data = {'UUID': data_uuid, 'msg': post_msg}
        to_send_url = "http://localhost:8081"
        response = requests.post(to_send_url, to_send_data)


def run(server_class=HTTPServer, handler_class=S, port=8080):
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
        run()