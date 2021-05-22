from pymysqlpool.pool import Pool
from logcat.Log import LogCat

pool = Pool(host='220.88.163.147', port=3306, user='root', password='ss1235', db='MESSENGER', autocommit=True)


class MySQLPool:
    @staticmethod
    def startSQLPool():
        pool.init()

    @staticmethod
    def getConnection():
        return pool.get_conn()

    @staticmethod
    def release(connection):
        pool.release(connection)
