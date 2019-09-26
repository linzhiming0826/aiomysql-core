import asyncio
import aiomysql
from aiomysql_core import AioMysqlCore


async def test_example(loop):
    pool = await aiomysql.create_pool(host='', port=3306,
                                      user='', password='',
                                      db='', loop=loop)
    core = AioMysqlCore(pool=pool)
    rows = await core.query('select * from users where uid=%s', 113)
    print(rows)
    row = await core.get('select * from users where uid=%(uid)s', {'uid': 113})
    print(row)
    execute_rowcount = await core.execute_rowcount('select * from users where uid=%(uid)s', {'uid': 113})
    print(execute_rowcount)
    pool.close()
    await pool.wait_closed()


loop = asyncio.get_event_loop()
loop.run_until_complete(test_example(loop))
