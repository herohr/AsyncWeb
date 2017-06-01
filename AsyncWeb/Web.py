from aiohttp import web
from AsyncWeb.HTTPBases import BaseResponse, BaseRequest
import asyncio
import logging


class Router:
    def __init__(self, not_found=None):
        self._routes = {}
        self.not_found = not_found or None

    @property
    def routes(self):
        return self._routes

    def add_route(self, url, method, handler):
        self._routes[(url, method)] = handler

    def get_handler(self, request):
        print(request.path, request.method)
        handler = self._routes.get((request.path, request.method), None)
        if handler:
            return handler
        else:
            return self.not_found

    def set_404(self, handler):
        self.not_found = handler


class Framework:
    def __init__(self, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.server = web.Server(handler=self.base_handler)
        self.port = None
        self.host = None
        self.router = Router()
        self.router.set_404(self.not_found_default)

    def route(self, url, methods=("GET", )):
        def _deco(func):
            async def _handler(request):
                res = await func(request)
                if isinstance(res, str):
                    return web.Response(body=res.encode('utf-8'), content_type="text/html", charset='utf-8')
                elif isinstance(res, Response):
                    return res.to_raw()
                else:
                    raise Exception("Handler response can't be {}".format(type(res)))

            for method in methods:
                self.router.add_route(url, method, _handler)
            return _handler
        return _deco

    async def create_server(self, host="localhost", port=8888):
        self.host = host
        self.port = port
        return await self.loop.create_server(self.server, host=host, port=port)

    def run_task(self, task):
        return self.loop.run_until_complete(task)

    def run(self, host="localhost", port=8888):
        logging.info("Server running on http://{}:{}".format(host, port))
        self.run_task(self.create_server(host, port))
        self.loop.run_forever()

    async def base_handler(self, a_request):
        request = Request(a_request)
        handler = self.router.get_handler(request)
        return await handler(request)

    @staticmethod
    async def not_found_default(request):
        return Response(status_code=404, status_note='Not Found', content="<h3>{}  not found</h3>".format(request.url).
                        encode('utf-8')).to_raw()


class Request(BaseRequest):
    def __init__(self, request):
        super(Request, self).__init__(request.method, str(request.url), request.version, request.headers)
        self.args = dict(request.GET)
        self.path = request.path

        self._request = request

    @property
    async def form(self):
        dic = await self._request.post()
        return dict(dic)

    async def form_get(self, key, **kwargs):
        dic = await self.form
        try:
            return dic[key]
        except KeyError:
            default = kwargs.get('default')
            return default


class Response(BaseResponse):
    def __init__(self, status_code=200, status_note='OK', version='HTTP/1.0', header=None,
                 content=b"", content_type='text/html', charset="utf-8"):
        super(Response, self).__init__(status_code, status_note, version, header, content, content_type)
        self.charset = charset

    def to_raw(self):
        if isinstance(self.content, str):
            self.content = self.content.encode('utf-8')
            self.charset = 'utf-8'
        raw_response = web.Response(body=self.content, status=self.status_code, reason=self.status_note,
                                    charset=self.charset, content_type=self.content_type
                                    )
        raw_response.headers.update(self.header)
        return raw_response
