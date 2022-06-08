from http.server import BaseHTTPRequestHandler, HTTPServer
import hazelcast
class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_response()

        client = hazelcast.HazelcastClient()
        queue = client.get_queue("message-queue").blocking()

        items = queue.iterator()
        messages_data = []
        for i in items:
            messages_data.append(i)

        self.wfile.write("Messages Service Get request {}".format(messages_data).encode('utf-8'))
        client.shutdown()

    def do_POST(self):
        client = hazelcast.HazelcastClient()
        queue = client.get_queue("message-queue").blocking()
        content_length = int(self.headers['Content-Length']) # Size of Data
        post_data = self.rfile.read(content_length)#.decode() # Data
        post_msg = post_data.decode().split("msg=")[1]
        print("Messages Service Post message = ", post_msg.split())
        queue.offer(post_msg)
        client.shutdown()


def run(server_class=HTTPServer, handler_class=S, port=8081):
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
        run()