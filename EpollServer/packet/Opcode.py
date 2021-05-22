
from handler.Account import *
from packet.OpcodeList import OpCodeData
from packet.Packet import ReadPacket, SendPacket
from logcat.Log import LogCat


class Opcode:
    @staticmethod
    def recvdata(socket, fd, bytedata):
        try:
            client = socket[fd]
            packet = ReadPacket(bytedata)
            opcode = packet.readShort()

            if opcode == OpCodeData.login_id:  # 로그인요청
                Account.login_id(client, packet)
            elif opcode == OpCodeData.login_email:
                Account.login_email(client, packet)
            else:
                print(opcode, 'no Opcode')

        except ConnectionResetError:
            raise ConnectionResetError()
        except Exception as e:
            LogCat.log('(심각)Opcode.py-Server().recvUser', type(e), e)
