class HTTPBase:
    def __init__(self, first_line, version="HTTP/1.0", header=None, content=b"", args=None, form=None):
        self.first_line = first_line
        self.version = version
        self.header = header if header else {}
        self.content = content
        self.content_length = len(content)
        self.args = args or []
        self.form = form or {}

    def set_content(self, content, encoding="utf-8"):
        self.content = content
        self.content_length = encoding

    def package(self, encoding='utf-8'):
        return "".join([self.first_line, "\r\n"] +
                       ["{}: {}\r\n".format(key, value) for key, value in self.header.items()] +
                       ["\r\n"]
                       ).encode(encoding) + self.content


class Response(HTTPBase):
    def __init__(self, status_code=200, status_note='OK', version='HTTP/1.0', header=None, content=b""):
        self.status_code = status_code
        self.status_note = status_note
        self.version = version
        HTTPBase.__init__(self, first_line="{} {} {}".format(version, status_code, status_note),
                          header=header, content=content)


class Request(HTTPBase):
    def __init__(self, method, url, version='HTTP/1.0', header=None, content=b""):
        self.method = method
        self.url = url
        self.protocol, self.host, self.port, self.relative_url = Request.url_parser(url)
        HTTPBase.__init__(self, "{} {} {}".format(method, url, version),
                          header=header,
                          content=content)

    def set_version(self, version):
        self.version = version
        self.first_line = "{} {} {}".format(self.method, self.relative_url, version)

    @staticmethod
    def url_parser(url):
        protocol = None
        host = None
        port = None
        relative_url = None

        if url[0] == "/":
            return protocol, host, port, url
        else:
            protocol_index = url.find("://")
            protocol = url[:protocol_index] if protocol_index != -1 else ""
            url = url.lstrip(protocol + "://")

            host_index = url.find(":")
            if host_index != -1:
                host = url[:host_index] if host_index != -1 else ""
            elif host_index == -1:
                host_index = url.find("/")
                if host_index != -1:
                    host = url[:host_index]
                else:
                    host = url
            url = url.lstrip(host)
            if url:
                if url[0] == ":":
                    port_index = url.find("/")
                    if port_index == -1:
                        port = int(url[1:])
                    else:
                        port = int(url[1:port_index])
                url = url.lstrip(":{}".format(port))

                relative_url = url

            return protocol, host, port, relative_url
