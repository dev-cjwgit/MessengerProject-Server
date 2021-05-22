'''
각 클래스 메소드에대한 예외처리 추후 필요.
(안해도상관은없는데 해당 함수를 쓰는곳으로 에러위치가 나옴)
'''
from database.MySQLConnection import MySQLPool

'''
        @staticmethod
        def login_email(email, pw):
            conn = None
            try:
                conn = MySQLPool.getConnection()
                cur = conn.cursor()
                cur.execute('SELECT uid, pw FROM ACCOUNT WHERE email = "%s"' % (email))
                cur.fetchone()  # fetchall()
            except Exception as e:
                pass
            finally:
                if conn is not None:
                    MySQLPool.release(conn)
'''


class SQLAccess:
    class Account:
        @staticmethod
        def login_id(id, pw):
            conn = None
            try:
                conn = MySQLPool.getConnection()
                cur = conn.cursor()
                cur.execute('SELECT uid, pw FROM ACCOUNT WHERE id = "%s"' % (id))
                result = cur.fetchone()
                if result is None:
                    return 1, None
                if result['pw'] == pw:
                    return 5, result['uid']
                else:
                    return 2, None
            except Exception as e:
                pass
            finally:
                if conn is not None:
                    MySQLPool.release(conn)

        @staticmethod
        def login_email(email, pw):
            conn = None
            try:
                conn = MySQLPool.getConnection()
                cur = conn.cursor()
                cur.execute('SELECT uid, pw FROM ACCOUNT WHERE email = "%s"' % (email))
                result = cur.fetchone()
                if result is None:
                    return 1, None
                if result['pw'] == pw:
                    return 5, result['uid']
                else:
                    return 2, None
            except Exception as e:
                pass
            finally:
                if conn is not None:
                    MySQLPool.release(conn)

        @staticmethod
        def get_user_info(uid):
            conn = None
            try:
                conn = MySQLPool.getConnection()
                cur = conn.cursor()
                cur.execute('SELECT nick_name, introduce FROM ACCOUNT WHERE uid = %d' % (uid))
                result = cur.fetchone()
                return result['nick_name'], result['introduce']
            except Exception as e:
                pass
            finally:
                if conn is not None:
                    MySQLPool.release(conn)
