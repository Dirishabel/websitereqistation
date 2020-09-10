""" db work library """
import mysql.connector
from loguru import logger

from app_code.database.queries import QUERIES_LK
from config import SERVER_LK


class StaticConenction():
    """ connection to db class """

    def __init__(self):
        self.conn = None

    def get_connection(self):
        """ check connection """
        if self.conn is None:
            self.__connect()
        if not self.conn.is_connected():
            self.__connect()
        return self.conn

    def __connect(self):
        self.conn = mysql.connector.connect(**SERVER_LK)


cnn = StaticConenction()


def sql_lk(action: str, query_name: str, *args):
    """ sql handler """
    res = None
    if args:
        query = QUERIES_LK[query_name] % args[0]
    else:
        query = QUERIES_LK[query_name]
    try:
        base_connection = cnn.get_connection()
        cur = base_connection.cursor(dictionary=True)
        cur.execute(query)
        if action == 'select_one':
            row = cur.fetchall()
            if row:
                res = row[0]
        if action == 'select_all':
            res = cur.fetchall()
        if action in ('insert', 'update'):
            base_connection.commit()
    except mysql.connector.Error as err:
        logger.exception('SQL {} error: {}'.format(query_name, err))
    finally:
        if cur:
            cur.close()
        if base_connection:
            base_connection.close()
    return res
