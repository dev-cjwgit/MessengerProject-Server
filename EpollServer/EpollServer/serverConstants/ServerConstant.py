import socket, select
import concurrent.futures
from logcat.Log import LogCat
from packet.Opcode import Opcode
from database.MySQLAccess import SQLAccess

showRecvPacket = True
fdmap = None


def exitClient(fd):
    try:
        pass
    except Exception as e:
        LogCat.log('(심각)ServerConstant.py-noClass().exitClient', type(e), e)


class Server():
    def __init__(self, PORT = 5000, WORKERS = 3):
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS)
        self.HOST = '192.168.48.130'
        self.PORT = PORT
        self.socket = socket.socket()
        self.epoll = None

        self.c = None

    def __del__(self):
        try:
            self.executor.shutdown()
        except Exception as e:
            LogCat.log('ServerCpmstamt.py-Server().__del__',type(e),e)

    def openServer(self):
        global fdmap
        try:
            self.socket.bind((self.HOST, self.PORT))
            self.socket.listen(10)
            self.socket.setblocking(0)

            fdmap = {self.socket.fileno(): self.socket}
            self.epoll = select.epoll()
            self.epoll.register(self.socket)
            return True
        except OSError as e:
            if str(e) != '[Errno 98] Address already in use':
                LogCat.log('(문제)ServerConstant.py-Server().openServer', type(e), e)
            return False
        except Exception as e:
            LogCat.log('(문제)ServerConstant.py-Server().openServer', type(e), e)
            return False

    def recvUser(self):
        global fdmap
        while True:
            events = self.epoll.poll()
            for fd, event in events:
                if fd is self.socket.fileno():
                    try:
                        self.c, addr = self.socket.accept()
                        self.c.setblocking(0)
                        self.epoll.register(self.c)
                        fdmap[self.c.fileno()] = self.c
                        print(self.c.getsockname()[1],'PORT :', fd, '서버에 접속됨 : ', addr)
                    except Exception as e:
                        LogCat.log('(심각)ServerConstant.py-Server().recvUser-if fd is fileno()', type(e), e)
                elif event & select.EPOLLIN:
                    try:
                        data = fdmap[fd].recv(1024)
                        #data = fdmap[fd].recv(8192, socket.MSG_WAITALL)
                        if not data: #접속 종료시 이상한 데이터가 들어옴
                            print('PORT :',self.c.getsockname()[1],fd, '클라이언트에서 접속 종료함')
                            self.epoll.unregister(fd)
                            del fdmap[fd]
                            exitClient(fd)
                        else:
                            if showRecvPacket:
                                print('RecvData :',data)
                            self.executor.submit(Opcode.recvdata,fdmap, fd, data)

                    except ConnectionResetError: #비정상적인 종료
                        print('[경고]PORT :',self.c.getsockname()[1],fd, '클라이언트에서 접속 종료함')
                        self.epoll.unregister(fd)
                        del fdmap[fd]
                        exitClient(fd)

                    except Exception as e:
                        LogCat.log('(심각)ServerConstant.py-Server().recvUser',type(e),e)
