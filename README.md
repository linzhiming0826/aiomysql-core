


## Aiomysql-Core

### Simple framework for aiomysql

## Introduce

simple package, easy to use

[aiomysql](https://github.com/aio-libs/aiomysql)

## Document

[click me](https://aiomysql-core.readthedocs.io)

## Installation
```linux
pip install aiomysql-core
```

## Simple uses
```python
import asyncio
import aiomysql
from aiomysql_core import AioMysqlCore


async def test_example(loop):
    pool = await aiomysql.create_pool(host='', port=3308,
                                      user='', password='',
                                      db='', loop=loop)
    core = AioMysqlCore(pool=pool)
    rows = await core.query('select * from users where uid=%s', 113)
    print(rows)
    rows = await core.gener('select * from users limit 100')
    async for row in rows:
        print(row)
    row = await core.get('select * from users where uid=%(uid)s', {'uid': 113})
    print(row)
    rowcount = await core.execute_rowcount('select * from users where uid=%(uid)s', {'uid': 113})
    print(rowcount)
    pool.close()
    await pool.wait_closed()


loop = asyncio.get_event_loop()
loop.run_until_complete(test_example(loop))
```