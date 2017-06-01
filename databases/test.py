import asyncio
connect = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'Mysql_5211314',
    'db': 'test',
    'charset': 'utf8'
}

async def pr():
    print(await select("select * from article where id = ?", 3))

from databases.db_connect import *
loop = asyncio.get_event_loop()
# tasks = [
#     create_pool(loop, **connect),
#     pr()
# ]

loop.run_until_complete(create_pool(loop, **connect))


# class A:
#     def __init__(self):
#         self.b = 'fuck'
#
#
# a = A()
#
# print(getattr(a, 'a', "FUCKL"))