#from https://stackoverflow.com/questions/48532301/python-postgres-psycopg2-threadedconnectionpool-exhausted

import gevent, sys, random, psycopg2, logging
from contextlib import contextmanager
from gevent.queue import Queue
from gevent.socket import wait_read, wait_write
from psycopg2.pool import ThreadedConnectionPool
from psycopg2 import extensions, OperationalError, IntegrityError
import sys
logger = logging.getLogger(__name__)

poolsize = 100  #number of max connections
pdsn = '' # put your dsn here

if sys.version_info[0] >= 3:
    integer_types = (int,)
else:
    import __builtin__
    integer_types = (int, __builtin__.long)



g_connection_setting_file_name = None

def set_connection_settings_file_name(name):
    g_connection_setting_file_name = name


def get_connection_settings_file_name():
    return g_connection_setting_file_name



class ConnectorError(Exception):
    """ This is a base class for all CONNECTOR related exceptions """
    pass


#singleton connection pool, gets reset if a connection is bad or drops
_pgpool = None
def pgpool():
    global _pgpool
    if not _pgpool:
        try:
            _pgpool = PostgresConnectionPool(maxsize=poolsize)
        except psycopg2.OperationalError as exc:
            _pgpool = None
    return _pgpool

class Pcursor(object):

    def __init__(self, **kwargs):
        #in case of a lost connection lets sit and wait till it's online
        global _pgpool
        if not _pgpool:
            while not _pgpool:
                try:
                    pgpool()
                except:
                    logger.debug('Attempting Connection To Postgres...')
                    gevent.sleep(1)

    def fetchone(self, PSQL, *args):
        with _pgpool.cursor() as cursor:
            try:
                cursor.execute(PSQL, args)
            except TypeError:
                cursor.execute(PSQL, args[0])
            except Exception as exc:
                print(sys._getframe().f_back.f_code)
                print(sys._getframe().f_back.f_code.co_name)
                logger.warning(str(exc))
            logger.debug(cursor.query)
            return cursor.fetchone()

    def fetchall(self, PSQL, *args):
        with _pgpool.cursor() as cursor:
            try:
                cursor.execute(PSQL, args)
            except TypeError:
                cursor.execute(PSQL, args[0])
            except Exception as exc:
                print(sys._getframe().f_back.f_code)
                print(sys._getframe().f_back.f_code.co_name)
                logger.warning(str(exc))
            logger.debug(cursor.query)
            return cursor.fetchall()

    def execute(self, PSQL, *args):
#        conn = _pgpool.connection()
        with _pgpool.cursor() as cursor:
            try:
                cursor.execute(PSQL, args)
            except TypeError:
                cursor.execute(PSQL, args[0])
            except IntegrityError:
                print("SKIPPING " + sql)
                conn.rollback()
            except Exception as exc:
                print(sys._getframe().f_back.f_code)
                print(sys._getframe().f_back.f_code.co_name)
                logger.warning(str(exc))
            finally:
                logger.debug(cursor.query)
#                conn.commit()
                return cursor.query

    def fetchmany(self, PSQL, *args):
        with _pgpool.cursor() as cursor:
            try:
                cursor.execute(PSQL, args)
            except TypeError:
                cursor.execute(PSQL, args[0])
            while 1:
                items = cursor.fetchmany()
                if not items:
                    break
                for item in items:
                    yield item

class AbstractDatabaseConnectionPool(object):

    def __init__(self, maxsize=poolsize):
        if not isinstance(maxsize, integer_types):
            raise TypeError('Expected integer, got %r' % (maxsize, ))
        self.maxsize = maxsize
        self.pool = Queue()
        self.size = 0

    def create_connection(self):
        #overridden by PostgresConnectionPool
        raise NotImplementedError()

    def get(self):
        pool = self.pool
        if self.size >= self.maxsize or pool.qsize():
            return pool.get()

        self.size += 1
        try:
            new_item = self.create_connection()
        except:
            self.size -= 1
            raise
        return new_item

    def put(self, item):
        self.pool.put(item)

    def closeall(self):
        while not self.pool.empty():
            conn = self.pool.get_nowait()
            try:
                conn.close()
            except Exception:
                pass

    @contextmanager
    def connection(self, isolation_level=None):
        conn = self.get()
        try:
            if isolation_level is not None:
                if conn.isolation_level == isolation_level:
                    isolation_level = None
                else:
                    conn.set_isolation_level(isolation_level)
            yield conn
        except:
            if conn.closed:
                conn = None
                self.closeall()
            raise
        else:
            if conn.closed:
                raise OperationalError("Cannot commit because connection was closed: %r" % (conn, ))
        finally:
            if conn is not None and not conn.closed:
                if isolation_level is not None:
                    conn.set_isolation_level(isolation_level)
                self.put(conn)

    @contextmanager
    def cursor(self, *args, **kwargs):
        isolation_level = kwargs.pop('isolation_level', None)
        with self.connection(isolation_level) as conn:
            try:
                yield conn.cursor(*args, **kwargs)
            except:
                global _pgpool
                _pgpool = None
                del(self)


class PostgresConnectionPool(AbstractDatabaseConnectionPool):
    def __init__(self,**kwargs):
        try:
            settings_file_name = "/media/ssd/MyProjects/pyfin/database/database_settings.txt"
            f = open(settings_file_name) #the path might not work for every app, should be added to sys.path
            lines = f.readlines()
            f.close()
#            host = lines[0]
            host = "127.0.0.1"
            dbname = lines[1].rstrip()
            user = lines[2].rstrip()
            passwd = lines[3].rstrip()

#            ReallyThreadedConnectionPool(5, 20, user=user,
#                                         password=passwd,
#                                         host=host,
#                                         database=dbname)

#            self.pconnect = ThreadedConnectionPool(1, poolsize, dsn=pdsn)
            self.pconnect = ThreadedConnectionPool(1, poolsize, user=user,
                                         password=passwd,
                                         host=host,
                                         database=dbname)
        except:
            global _pgpool
            _pgpool = None
            raise ConnectorError('Database Connection Failed')
        maxsize = kwargs.pop('maxsize', None)
        self.kwargs = kwargs
        AbstractDatabaseConnectionPool.__init__(self, maxsize)

    def create_connection(self):
        self.conn = self.pconnect.getconn()
        self.conn.autocommit = True
#        self.conn.autocommit = False
        return self.conn


def gevent_wait_callback(conn, timeout=None):
    """A wait callback useful to allow gevent to work with Psycopg."""
    while 1:
        state = conn.poll()
        if state == extensions.POLL_OK:
            break
        elif state == extensions.POLL_READ:
            wait_read(conn.fileno(), timeout=timeout)
        elif state == extensions.POLL_WRITE:
            wait_write(conn.fileno(), timeout=timeout)
        else:
            raise ConnectorError("Bad result from poll: %r" % state)

extensions.set_wait_callback(gevent_wait_callback)
