


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
    pool = await aiomysql.create_pool(host='', port=3306,
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

## Simple SQLAlchemy uses
```python
import asyncio
from aiomysql.sa import create_engine
from aiomysql_core import AioMysqlAlchemyCore
from sqlalchemy import Column, Integer, String, MetaData, Table

metadata = MetaData()

Test = Table('test', metadata,
             Column('id', Integer, primary_key=True),
             Column('content', String(255), server_default="")
             )


async def test_example(loop):
    config = {'user': '', 'password': '', 'db': '',
              'host': '', 'port': 3306, 'autocommit': True, 'charset': 'utf8mb4'}
    engine = await create_engine(loop=loop, **config)
    core = AioMysqlAlchemyCore(engine=engine)
    # insert
    doc = {'content': 'insert'}
    query = Test.insert().values(**doc)
    rowcount = await core.execute_rowcount(query)
    print(rowcount)
    # search
    query = Test.select().where(Test.c.id == 1).limit(1)
    row = await core.get(query)
    print(row.id, row.content)
    query = Test.select().where(Test.c.id > 1)
    rows = await core.query(query)
    async for row in rows:
        print(row.id, row.content)
    # update
    doc = {'content': 'update'}
    query = Test.update().values(**doc).where(Test.c.id == 1)
    rowcount = await core.execute_rowcount(query)
    print(rowcount)
    # delete
    query = Test.delete().where(Test.c.id == 1)
    rowcount = await core.execute_rowcount(query)
    print(rowcount)
    await engine.wait_closed()


loop = asyncio.get_event_loop()
loop.run_until_complete(test_example(loop))
```