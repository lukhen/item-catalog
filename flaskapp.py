from http.server import HTTPServer, BaseHTTPRequestHandler


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()


def main():
    server_address = ("", 5000)
    httpd = HTTPServer(server_address, Handler)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
