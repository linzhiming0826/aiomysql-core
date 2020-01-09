
__all__ = ('AioMysqlCore', 'Util')


class AioMysqlCore(object):

    def __init__(self, pool):
        self.pool = pool

    async def gener(self, query, *args, **kwargs):
        """Execute a query
        :param str query: Query to execute.
        :param args: parameters used with query. (optional)
        :type args: tuple, list or dict
        :return: An generator for the number of affected rows
        :rtype: list
        If args is a list or tuple, %s can be used as a placeholder in the query.
        If args is a dict, %(name)s can be used as a placeholder in the query.
        """
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, *args, **kwargs)
                column_names = [d[0] for d in cur.description]
                return Util.async_generator([Row(zip(column_names, row)) for row in cur._rows])

    async def query(self, query, *args, **kwargs):
        """Execute a query
        :param str query: Query to execute.
        :param args: parameters used with query. (optional)
        :type args: tuple, list or dict
        :return: Number of affected rows
        :rtype: list
        If args is a list or tuple, %s can be used as a placeholder in the query.
        If args is a dict, %(name)s can be used as a placeholder in the query.
        """
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, *args, **kwargs)
                column_names = [d[0] for d in cur.description]
                return [Row(zip(column_names, row)) for row in cur._rows]

    async def get(self, query, *args, **kwargs):
        """Execute a query
        :param str query: Query to execute.
        :param args: parameters used with query. (optional)
        :type args: tuple, list or dict
        :return: Number of affected first row
        :rtype: dict
        If args is a list or tuple, %s can be used as a placeholder in the query.
        If args is a dict, %(name)s can be used as a placeholder in the query.
        """
        rows = await self.query(query, *args, **kwargs)
        if not rows:
            return None
        elif len(rows) > 1:
            raise Exception("Multiple rows returned for Database.get() query")
        else:
            return rows[0]

    async def execute(self, query, *args, **kwargs):
        """Execute a query
        :param str query: Query to execute.
        :param args: parameters used with query. (optional)
        :type args: tuple, list or dict
        :return: lastrowid
        :rtype: int
        If args is a list or tuple, %s can be used as a placeholder in the query.
        If args is a dict, %(name)s can be used as a placeholder in the query.
        """
        return await self.execute_lastrowid(query, *args, **kwargs)

    async def execute_lastrowid(self, query, *args, **kwargs):
        """Execute a query
        :param str query: Query to execute.
        :param args: parameters used with query. (optional)
        :type args: tuple, list or dict
        :return: lastrowid
        :rtype: int
        If args is a list or tuple, %s can be used as a placeholder in the query.
        If args is a dict, %(name)s can be used as a placeholder in the query.
        """
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, *args, **kwargs)
                return cur.lastrowid

    async def execute_rowcount(self, query, *args, **kwargs):
        """Execute a query
        :param str query: Query to execute.
        :param args: parameters used with query. (optional)
        :type args: tuple, list or dict
        :return: rowcount
        :rtype: int
        If args is a list or tuple, %s can be used as a placeholder in the query.
        If args is a dict, %(name)s can be used as a placeholder in the query.
        """
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, *args, **kwargs)
                return cur.rowcount

    async def executemany(self, query, parameters):
        """Run several data against one query
        :param query: query to execute on server
        :param args:  Sequence of sequences or mappings.  It is used as parameter.
        :return: lastrowid.
        This method improves performance on multiple-row INSERT and
        REPLACE. Otherwise it is equivalent to looping over args with
        execute().
        """
        return await self.executemany_lastrowid(query, parameters)

    async def executemany_lastrowid(self, query, parameters):
        """Run several data against one query
        :param query: query to execute on server
        :param args:  Sequence of sequences or mappings.  It is used as parameter.
        :return: lastrowid.
        This method improves performance on multiple-row INSERT and
        REPLACE. Otherwise it is equivalent to looping over args with
        execute().
        """
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.executemany(query, parameters)
                return cur.lastrowid

    async def executemany_rowcount(self, query, parameters):
        """Run several data against one query
        :param query: query to execute on server
        :param args:  Sequence of sequences or mappings.  It is used as parameter.
        :return: rowcount.
        This method improves performance on multiple-row INSERT and
        REPLACE. Otherwise it is equivalent to looping over args with
        execute().
        """
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.executemany(query, parameters)
                return cur.rowcount


class Row(dict):
    """
    A dict that allows for object-like property access syntax.
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)


class Util(object):

    @classmethod
    async def async_generator(cls, rows):
        """
        :param rows: list
        :return: An generator for the rows.
        """
        for row in rows:
            yield row
