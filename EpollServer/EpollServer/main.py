import sys
import time
import threading
from database.MySQLConnection import MySQLPool
from serverConstants.ServerConstant import Server
from logcat.Log import LogCat
from database.MySQLAccess import SQLAccess

'''
추후DB의 keyvalue를 DB가아닌 이 서버에 포함시키면 암호화될듯.
'''


def dbClear():
    try:
        pass
    except Exception as e:
        LogCat.log('(심각)main.py-main().dbClear', type(e), e)


def serverThread(PORT, WORKERS):
    try:
        cnt = 0
        server = Server(PORT=PORT, WORKERS=WORKERS)
        while not server.openServer():
            cnt += 1
            print('서버설정에 실패하였습니다.', PORT, ' 재시도중', cnt)
            time.sleep(3)  # 서버개방 실패시, 재오픈까지의 시간

        print('포트개방 PORT =', PORT)
        server.recvUser()
        del server
    except Exception as e:
        LogCat.log('(심각)main.py-main().serverThread', type(e), e)


def main():
    threadlist = []
    MySQLPool.startSQLPool()

    dbClear()
    print('DB정리 완료')
    for i in range(5000, 5001):  # 2000~2005 포트개방
        thread = threading.Thread(target=serverThread, args=(i, 12,))
        thread.daemon = True  # Main Thread가 죽으면 하위 스레드도 죽음
        thread.start()
        threadlist.append(thread)  # 추후 Thread관리 시 필요한 목록
        time.sleep(0.001)

    while True:
        str = input("명령어 입력")
        if str == 'q':
            sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        1
    except Exception as e:
        LogCat.log('(매우심각)main.py-main', type(e), e)

'''
MYSQL Using Giude(del 쓰면 알아서 closeSQL호출)
from database.MySQLConnection import MySQL
mysql = MySQL()
if mysql.connectSQL():
    print(mysql.executeSQL('SQL'))
    mysql.closeSQL()
else:
    print('fail sql connect')
del mysql

Server Open Guide
from serverConstants.ServerConstant import Server
server = Server(PORT=,WOKERS=)
    if server.openServer():
        print('server open')
    else:
        print('fail server')
        return
    server.recvUser()

logcat Using Guide
from logcat.Log import LogCat
Logcat.log(Position, ExceptionName, Body)
ex: LogCat.log('filename.py-classname().methodname',type(e),e)

packet Using Guide
from packet.Packet import SendPacket, ReadPacket
p = SendPacket(client)
p.write(data)
p.send()
p = ReadPacket(SendPacket or bytesdata)
print(p.readInt(), p.readDouble(), p.readString())

AESCipher Using Guide
from crypto.ChiperAES import AEScipher
aes = AEScipher()
e = aes.encrypt("")
d = aes.decrypt(e)
'''
