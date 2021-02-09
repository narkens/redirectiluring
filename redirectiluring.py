from http.server import BaseHTTPRequestHandler,HTTPServer
from sys import argv
import json

conf_file = open('test.json')
server_data = json.load(conf_file)

class skurkHandler(BaseHTTPRequestHandler):
    def _set_response(self, handler_rules):
        if not handler_rules:
            self._set_response(server_data["default"])
        else:
            if not self.path in handler_rules:
                if not "default" in handler_rules:
                    self.path = "default"
                else:
                    handler_rules = server_data["default"]
                    self.path = "default"

            self.send_response(int(handler_rules[self.path]["code"]))
            for header in handler_rules[self.path]["headers"]:
                self.send_header(header, handler_rules[self.path]["headers"][header])
            self.end_headers()
        
    def do_GET(self):
        self._set_response(server_data["GET"])

    def do_POST(self):
        self._set_response(server_data["POST"])

    def do_PUT(self):
        self._set_response(server_data["PUT"])

    def do_HEAD(self):
        self._set_response(server_data["HEAD"])

    def do_OPTIONS(self):
        self._set_response(server_data["OPTIONS"])

    def do_PATCH(self):
        self._set_response(server_data["PATCH"])

    def do_DELETE(self):
        self._set_response(server_data["DELETE"])

    def do_CONNECT(self):
        self._set_response(server_data["CONNECT"])

    def do_TRACE(self):
        self._set_response(server_data["TRACE"])


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
