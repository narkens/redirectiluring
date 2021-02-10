from http.server import BaseHTTPRequestHandler,HTTPServer
from sys import argv
import json

conf_file = open('test.json')
server_data = json.load(conf_file)

class skurkHandler(BaseHTTPRequestHandler):

    def _get_path(self):
        s = self.path
        sep = [s.find('?'), s.find('&'), s.find('#'), len(s)]
        sep = min([x for x in sep if x != -1])
        print(sep)
        self.path = self.path[:sep]

    def _set_response(self, method):
        handler_rules = server_data[method]
        self._get_path()
        if not handler_rules:
            self._set_response("default")
        else:
            if not self.path in handler_rules:
                print("Path not in config - setting to /")
                self.path = "/"

            self.send_response(int(handler_rules[self.path]["code"]))
            for header in handler_rules[self.path]["headers"]:
                self.send_header(header, handler_rules[self.path]["headers"][header])
            self.end_headers()
            if  handler_rules[self.path]["file"] != "":
                f = open(handler_rules[self.path]["file"],'r')
                body = f.read()
                f.close()
                self.wfile.write(body.encode('utf-8'))
            elif handler_rules[self.path]["body"] != "":
                self.wfile.write(handler_rules[self.path]["body"].encode('utf-8'))
        
    def do_GET(self):
        self._set_response("GET")

    def do_POST(self):
        self._set_response("POST")

    def do_PUT(self):
        self._set_response("PUT")

    def do_HEAD(self):
        self._set_response("HEAD")

    def do_OPTIONS(self):
        self._set_response("OPTIONS")

    def do_PATCH(self):
        self._set_response("PATCH")

    def do_DELETE(self):
        self._set_response("DELETE")

    def do_CONNECT(self):
        self._set_response("CONNECT")

    def do_TRACE(self):
        self._set_response("TRACE")


def run(server_class=HTTPServer, handler_class=skurkHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == '__main__':
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
