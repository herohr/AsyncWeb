import logging
import databases
import private
from models import Article
from AsyncWeb import Web

logging.basicConfig(level=logging.DEBUG)

app = Web.Framework()


@app.route("/", methods=["GET", "POST"])
async def fuck(request):
    if request.method == 'GET':
        return '''<form action="/" method="POST">
        <input name='fuck' type="text"/>
        <input type="submit"/>
        </form>'''
    elif request.method == "POST":
        id = await request.form_get("fuck", defulat=None)
        # print(id)
        if id:
            return str(await Article.filter_by(id=id))
        if await request.form_get("fuck") == 'shit':
            return """
            <h1>恭喜你，进入了我的Web框架！</h1>
            """
        else:
            return "FUCK!"


app.run_task(databases.create_pool(app.loop, **private.connect))
app.run()
