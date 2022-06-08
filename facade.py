from http.server import BaseHTTPRequestHandler, HTTPServer
from random import randint
import requests
import uuid


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        to_send_url_logger_list = ["http://localhost:8082", "http://localhost:8083", "http://localhost:8084"]
        response_logger = requests.get(to_send_url_logger_list[randint(0,2)])
        i = 0
        while (response_logger.status_code != 200):
            response_logger = requests.get(to_send_url_logger_list[i])
            i = i + 1
            if i == len(to_send_url_logger_list):
                return
        print(response_logger.headers)
        print(response_logger.text)

        to_send_url_message_list = ["http://localhost:8081", "http://localhost:8085"]
        response_message = requests.get(to_send_url_message_list[randint(0,1)])
        i = 0
        while (response_message.status_code != 200):
            response_message = requests.get(response_message[i])
            i = i + 1
            if i == len(to_send_url_message_list):
                return
        print(response_message.headers)
        print(response_message.text)

        self._set_response()
        self.wfile.write("{0}".format([response_logger.text, response_message.text]).encode('utf-8'))


        ### Return like [[msg1, msg2, msg3], not implemented yet[]
        #logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        #self._set_response()
        #self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        
        content_length = int(self.headers['Content-Length']) # Size of Data
        post_data = self.rfile.read(content_length)#.decode() # Data
        print("received request ", post_data.decode())
        post_msg = post_data.decode().split("msg=")[1]
        data_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS , post_msg)) # Get UUID

        
        print("msg = ", post_msg, "   UUID ", data_uuid)
        self._set_response()
        self.wfile.write("POST request {}".format(post_data).encode('utf-8'))


        to_send_data = {'UUID': data_uuid, 'msg': post_msg}
        to_send_url_logger_list = ["http://localhost:8082", "http://localhost:8083", "http://localhost:8084"]
        response = requests.post(to_send_url_logger_list[randint(0,2)], to_send_data)
        i = 0
        while (response.status_code != 200):
            response = requests.post(to_send_url_logger_list[i], to_send_data)
            i = i + 1
            if i == 3:
                return
        print(response.text)

        to_send_data = {'msg': post_msg}
        to_send_url_message_list = ["http://localhost:8081", "http://localhost:8085"]
        response_message = requests.post(to_send_url_message_list[randint(0,1)], to_send_data)
        i = 0
        while (response_message.status_code != 200):
            response_message = requests.post(to_send_url_message_list[randint(0,1)], to_send_data)
            i = i + 1
            if i == len(to_send_url_message_list):
                return
        print(response_message.text)


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