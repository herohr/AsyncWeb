import aiomysql
import logging
async def create_pool(loop, **kwargs):
    global connection_pool
    connection_pool = await aiomysql.create_pool(

        host=kwargs.get('host'),
        port=kwargs.get('port'),
        user=kwargs.get('user'),
        password=kwargs.get('password'),
        db=kwargs.get("db"),
        charset=kwargs.get('charset', 'utf8'),
        autocommit=kwargs.get('autocommit', True),
        maxsize=kwargs.get('maxsize', 10),
        minsize=kwargs.get('minsize', 1),
        loop=loop
    )

async def select(sql, args=None, size=None):

    global connection_pool
    async with connection_pool.get() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            sql = sql.replace("?", "%s")
            # logging.info((sql, args or ()))
            await cur.execute(sql, args or ())
            if size:
                rs = await cur.fetchmany(size)
            else:
                rs = await cur.fetchall()
    return rs

async def execute(sql, args=None):
    # logging.info((sql, args))
    global connection_pool
    try:
        async with connection_pool.get() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql.replace('?', '%s'), args or ())
                affected = cur.rowcount
    except BaseException as e:
        raise e
    return affected
