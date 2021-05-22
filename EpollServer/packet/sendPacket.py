from logcat.Log import LogCat

showSendPacket = False


class SendPacket:
    @staticmethod
    def send(client, data):
        try:
            if showSendPacket:
                print('SendData : ', client.getpeername(), ':', data)
            client.send(bytes(data, encoding="utf-8"))
        except Exception as e:
            LogCat.log('(심각)sendPacket.py-SendPacket().send', type(e), e)
