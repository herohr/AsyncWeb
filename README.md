# AsyncWeb

A async web framework with aiohttp & asyncio

This framework is so naive, but I'm very proud of it...

Thanks for your bugs commit!

I love Flask, I will make it Flaskable.



## Get Start

You can run a simple server like this

```python
from AsyncWeb import Framework

app = Framework()


@app.route("/")
async def index(request):
    return "It works!"


app.run()
```



The server will run on http://localhost:8888 . If you open the URL you will find this.

Because of async ,  every function will be async.

With app init , a loop will be create. You can make database connection with `app.run_task`  before a server loop run.





## Router Object

A app instance have a router instance. URL mappings are saved in router.

You can use decorator to make a mapping of URL.

```python
@app.route("/page/", methods=["GET", "POST"])
def page(request):
    pass
```

Parament `methods` is unnecessary, it default `GET`.

You can add default 404 handler to a router, use `Router.set_404(self, handler)`



## Request Object

Just like Flask

### propoties of request

Request has `method`, `url`(the fully URL), `version`,`header`(the dict of header).

The Request object is the subclass aiohttp.web.Request object.



### get arguments of the URL

`request.args`  is a **dict** that have all paraments in the url. You can get value from it.

```python
@app.route("/add/")
async def add(request):
    a = request.args['a']
    b = request.args.get('b', 1)
    a, b = int(a), int(b)
    return str(a + b)
```



If you get `http://localhost:8888/add/?a=33&b=44`, you will see 77 !



### get form of the request

`request.form` is a property of Request instance.But this property is a coroutine. It means you have to call it with `await`. Because of it,  you can't use `request.form.get(key[, default])`  method. But here is a async method `request.form_get(key,[default=None])` can complete the same thing.

```python
@app.route("/login/", methods=["POST", "GET"])
async def login(request):
    if request.method == "GET":
        return '''<form action="/login/" method="POST">
        <input name='user' type="text"/>
        <input name='password' type='password'/>
        <input type="submit"/>
        </form>'''
    else:
        username = await request.form_get("user")
        password = await request.form_get("password", default="")
        if username == "administrator":
            return "<h1>You are disallowed! Password {} is wrong</h1>".format(password)
        else:
            return "<h1>Welcome</h1>"
```



## Response Object

### propoties of request

Response has `status_code=200`, `status_note='OK'`, `version='HTTP/1.1'`, `header=None`, `content=b""`, `content_type='text/html'`, `charset="utf-8"`



### view handler return

A async url handler can return a string or a Response object.



