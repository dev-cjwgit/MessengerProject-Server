import struct
from logcat.Log import LogCat

'''
Little Endian Packet
'''

showSendPacket = True


class SendPacket:
    def __init__(self, client):
        try:
            self.client = client
            self.data = bytes()
        except Exception as e:
            LogCat.log('Packet.py-SendPacket().__init__', type(e), e)

    def __str__(self):
        try:
            return self.data.__str__()
        except Exception as e:
            LogCat.log('Packet.py-SendPacket().__str__', type(e), e)
            return None

    def write(self, obj):
        try:
            if type(obj) == int:
                self.writeInt(obj)
            elif type(obj) == float:
                self.writeDouble(obj)
            elif type(obj) == str:
                self.writeString(obj)
            elif type(obj) == bytes:
                self.writeByte(obj)
            else:
                raise Exception('지원하지 않는 데이터입니다.')
        except Exception as e:
            LogCat.log('Packet.py-SendPacket().write', type(e), e)

    def writeShort(self, obj):
        try:
            if type(obj) is not int:
                return
            self.data += struct.pack('<h', obj)
        except Exception as e:
            LogCat.log('Packet.py-SendPacket().writeShort', type(e), e)

    def writeInt(self, obj):
        try:
            if type(obj) is not int:
                return
            self.data += struct.pack('<i', obj)
        except Exception as e:
            LogCat.log('Packet.py-SendPacket().writeInt', type(e), e)

    def writeUInt(self, obj):
        try:
            if type(obj) is not int:
                return
            self.data += struct.pack('<I', obj)
        except Exception as e:
            LogCat.log('Packet.py-SendPacket().writeUInt', type(e), e)

    def makeInt(self, obj):
        try:
            if type(obj) is not int:
                return
            return struct.pack('<i', obj)
        except Exception as e:
            LogCat.log('Packet.py-SendPacket().makeInt', type(e), e)

    def writeByte(self, obj):
        try:
            if type(obj) is not bytes:
                return
            self.writeInt(len(obj))
            self.data += obj
        except Exception as e:
            LogCat.log('Packet.py-SendPacket().writeByte', type(e), e)

    def writeString(self, obj):
        try:
            if type(obj) is not str:
                return
            self.writeInt(SendPacket.getStringSize(obj))
            self.data += obj.encode()
        except Exception as e:
            LogCat.log('Packet.py-SendPacket().writeString', type(e), e)

    def writeDouble(self, obj):
        try:
            if type(obj) is not float:
                return
            self.data += struct.pack('<d', obj)
        except Exception as e:
            LogCat.log('Packet.py-SendPacket().writeDouble', type(e), e)

    def getData(self):
        try:
            return self.data
        except Exception as e:
            LogCat.log('Packet.py-SendPacket().getData', type(e), e)
            return bytes()

    @staticmethod
    def getStringSize(data):
        try:
            data = data.encode()
            return len(data)
        except Exception as e:
            LogCat.log('Packet.py-SendPacket().getStringSize', type(e), e)

    def send(self):
        try:
            self.data = self.makeInt(len(self.data)) + self.data
            sendlen = self.client.send(self.data)
            if showSendPacket:
                print(sendlen, '|SendData :', self.client.getpeername(), ':', end='')
                for i in self.data:
                    print(i, end=' ')
                print()
        except Exception as e:
            LogCat.log('Packet.py-SendPacket().send', type(e), e)


class ReadPacket:
    def __init__(self, bytedata=bytes()):
        try:
            if type(bytedata) is SendPacket:
                self.data = bytedata.data
            elif type(bytedata) is bytes:
                self.data = bytedata
            self.maxlen = len(self.data) + 1
            self.pos = 0
        except Exception as e:
            LogCat.log('Packet.py-ReadPacket().__init__', type(e), e)

    def ableRead(self, size):
        try:
            return self.pos + size < self.maxlen
        except Exception as e:
            LogCat.log('Packet.py-ReadPacket().ableRead', type(e), e)
            return None

    def readInt(self):
        try:
            if self.ableRead(4):
                self.pos += 4
                return int.from_bytes(self.data[self.pos - 4:self.pos], byteorder='little', signed=True)
            else:
                return None
        except Exception as e:
            LogCat.log('Packet.py-ReadPacket().readInt', type(e), e)

    def readUInt(self):
        try:
            if self.ableRead(4):
                self.pos += 4
                return int.from_bytes(self.data[self.pos - 4:self.pos], byteorder='little', signed=False)
            else:
                return None
        except Exception as e:
            LogCat.log('Packet.py-ReadPacket().readUInt', type(e), e)

    def readShort(self):
        try:
            if self.ableRead(2):
                self.pos += 2
                return int.from_bytes(self.data[self.pos - 2:self.pos], byteorder='little', signed=True)
            else:
                return None
        except Exception as e:
            LogCat.log('Packet.py-ReadPacket().readShort', type(e), e)

    def readByte(self):
        try:
            size = self.readInt()
            if self.ableRead(size):
                self.pos += size
                return self.data[self.pos - size:self.pos]
            else:
                self.pos += 4
                return None
        except Exception as e:
            LogCat.log('Packet.py-ReadPacket().readByte', type(e), e)

    def readString(self):
        try:
            size = self.readInt()
            if self.ableRead(size):
                self.pos += size
                return self.data[self.pos - size:self.pos].decode('utf-8')
            else:
                self.pos += 4
                return None
        except Exception as e:
            LogCat.log('Packet.py-ReadPacket().readString', type(e), e)

    def readDouble(self):
        try:
            if self.ableRead(8):
                self.pos += 8
                return struct.unpack('d', self.data[self.pos - 8:self.pos])[0]
            else:
                return None
        except Exception as e:
            LogCat.log('Packet.py-ReadPacket().readDouble', type(e), e)
