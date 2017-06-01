from AsyncWeb import Framework
import logging
logging.basicConfig(level=logging.DEBUG)
app = Framework()


@app.route("/")
async def index(request):
    return "It works!"


@app.route("/add/")
async def add(request):
    a = request.args['a']
    b = request.args.get('b', 1)
    a, b = int(a), int(b)
    return str(a + b)


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

app.run()
