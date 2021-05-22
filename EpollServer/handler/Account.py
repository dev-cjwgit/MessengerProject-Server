from database.MySQLAccess import SQLAccess
from packet.Packet import SendPacket


class Account:
    @staticmethod
    def login_id(client, packet):
        id = packet.readString()
        pw = packet.readString()
        '''
            -1 DB Error
            1 id 가 존재하지 않음
            2 pw 틀림
            5 성공
        '''
        var, uid = SQLAccess.Account.login_id(id, pw)
        s = SendPacket(client)
        s.writeShort(256)
        s.writeShort(var)
        if var == 5:
            nickname, introduce = SQLAccess.Account.get_user_info(uid)
            s.writeInt(uid)
            s.writeString(nickname)
            s.writeString(introduce)

        s.send()

    @staticmethod
    def login_email(client, packet):
        email = packet.readString()
        pw = packet.readString()
        '''
            -1 DB Error
            1 id 가 존재하지 않음
            2 pw 틀림
            5 성공
        '''
        var, uid = SQLAccess.Account.login_email(email, pw)
        s = SendPacket(client)
        s.writeShort(256)
        s.writeShort(var)
        if var == 5:
            nickname, introduce = SQLAccess.Account.get_user_info(uid)
            s.writeInt(uid)
            s.writeString(nickname)
            s.writeString(introduce)

        s.send()
