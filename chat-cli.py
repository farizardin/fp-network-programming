import socket
import os
import json

TARGET_IP = "127.0.0.1"
TARGET_PORT = 8887

perintah = "1. kirim pesan\n2. inbox\n3. bergabung ke grup\n4. membuat grup\n5. meninggalkan grup\n6. inbox grup\n7. anggota grup\n8. kirim pesan grup.\n9. kirim file\n10. logout\n"

class ChatClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (TARGET_IP,TARGET_PORT)
        self.sock.connect(self.server_address)
        self.tokenid=""
        self.currentclient=""

    def proses(self,cmdline):
        try:
            command = cmdline
            if (command=='auth'):
                username=raw_input("Masukkan Username : ")
                password=raw_input("Masukkan Password : ")
                return self.login(username,password)
            # kirim pesan
            elif (command=='1'):
                temp_message = []
                usernameto = raw_input("Tujuan : ")
                message = raw_input("Isi pesan : ")
                temp_message.append(message)
                for w in temp_message[2:]:
                    message="{} {}" . format(message,w)
                print self.sendmessage(usernameto,message)
                return perintah
            
            # inbox
            elif (command=='2'):
                print self.inbox()
                return perintah

            # logout
            elif (command=='10'):
                self.tokenid=""
                print "Anda telah logout, login dengan perintah 'auth' untuk menggunakan fitur chat."
                return self.tokenid

            # gabung grup
            elif (command == '3'):
                group_token = raw_input("Masukkan token grup : ")
                print self.join_group(group_token)
                print ""
                return perintah
            
            # membuat grup
            elif (command == '4'):
                group_name = raw_input("Masukkan nama grup : ")
                print self.create_group(group_name)
                print ""
                return perintah
            # meninggalkan grup
            elif (command == '5'):
                group_token = raw_input("Masukkan token grup : ")
                print self.leave_group(group_token)
                print ""
                return perintah

            # membuka inbox grup
            elif (command == '6'):
                group_name = raw_input("Masukkan token grup : ")
                print self.inbox_group(group_name)
                print ""
                return perintah

            # membuka daftar grup
            elif (command == '7'):
                group_name = raw_input("Masukkan token grup : ")
                print self.list_group(group_name)
                print ""
                return perintah
            
            # mengirimkan pesan kedalam grup
            elif (command == '8'):
                tmp_msg_grp = []
                group_token = raw_input("Masukkan token grup : ")
                message=raw_input("Masukkan pesan : ")
                tmp_msg_grp.append(message)
                for w in tmp_msg_grp[2:]:
                    message="{} {}" . format(message, w)
                print self.send_group(group_token, message)
                print ""
                return perintah

            # mengirimkan file
            elif (command == '9'):
                usernameto = raw_input("Masukkan tujuan : ")
                filename = raw_input("Masukkan nama file : ")
                print self.send_file(usernameto, filename)
                print ""
                return perintah
            else:
                return "*Maaf, command tidak benar"
        except IndexError:
            return "-Maaf, command tidak benar"

    def sendstring(self,string):
        try:
            self.sock.sendall(string)
            receivemsg = ""
            while True:
                data = self.sock.recv(10)
                if (data):
                    receivemsg = "{}{}" . format(receivemsg,data)
                    if receivemsg[-4:]=="\r\n\r\n":
                        return json.loads(receivemsg)
        except:
            self.sock.close()
    def login(self,username,password):
        string="auth {} {} \r\n" . format(username,password)
        result = self.sendstring(string)
        if result['status']=='OK':
            self.tokenid=result['tokenid']
            print "Berhasil login dengan username {}, token anda adalah {} \nKetikan command berikut untuk melakukan aktifitas chat" .format(username,self.tokenid)
            print "Untuk melakukan aktifitas fitur chat, anda dapat mengetikan command sebagai berikut."
            return perintah
        else:
            return "Error, {}" . format(result['message'])
    def sendmessage(self,usernameto="xxx",message="xxx"):
        if (self.tokenid==""):
            return "Error, not authorized"
        # kirim pesan
        string="1 {} {} {} \r\n" . format(self.tokenid,usernameto,message)
        result = self.sendstring(string)
        if result['status']=='OK':
            return "message sent to {}" . format(usernameto)
        else:
            return "Error, {}" . format(result['message'])
    def inbox(self):
        if (self.tokenid==""):
            return "Error, not authorized"
        string="2 {} \r\n" . format(self.tokenid)
        result = self.sendstring(string)
        if result['status']=='OK':
            return "{}" . format(json.dumps(result['messages']))
        else:
            return "Error, {}" . format(result['message'])
    def send_file(self, usernameto, filename):
        if (self.tokenid==""):
            return "Error, not authorized"

        string="9 {} {} {} \r\n" . format(self.tokenid, usernameto, filename)
        self.sock.sendall(string)
        try:
            with open(filename, 'rb') as file:
                while True:
                    bytes = file.read(1024)
                    if not bytes:
                        result = self.sendstring("DONE")
                        break
                    self.sock.sendall(bytes)
                file.close()
        except IOError:
            return "Error, file not found"
        if result['status']=='OK':
            return "{} successfully sent to {}" . format(filename,usernameto)
        else:
            return "Error, {}" . format(result['message'])

    def create_group(self, group_name):
        if (self.tokenid==""):
            return "Error, not authorized"
        string = "4 {} {} \r\n" . format(self.tokenid, group_name)
        result = self.sendstring(string)

        if result['status']=='OK':
            return "{}" . format(result['messages'])
        else:
            return "Error, {}" . format(json.dumps(result['messages']))

    def join_group(self, group_token):
        if (self.tokenid==""):
            return "Error, not authorized"
        string = "3 {} {} \r\n" . format(self.tokenid, group_token)
        result = self.sendstring(string)

        if result['status']=='OK':
            return "{}" . format(result['message'])
        else:
            return "Error, {}" . format(result['message'])

    def leave_group(self, group_token):
        if (self.tokenid==""):
            return "Error, not authorized"
        string = "5 {} {} \r\n" . format(self.tokenid, group_token)
        result = self.sendstring(string)

        if result['status']=='OK':
            return "{}" . format(result['message'])
        else:
            return "Error, {}" . format(result['message'])

    def inbox_group(self, group_token):
        if (self.tokenid == ""):
            return "Error, not authorized"
        string = "6 {} {} \r\n".format(self.tokenid, group_token)
        result = self.sendstring(string)

        if result['status'] == 'OK':
            for i in result['message']:
                print i
            return ""
        else:
            return "Error, {}".format(result['message'])

    def list_group(self, group_token):
        if (self.tokenid==""):
            return "Error, not authorized"
        string = "7 {} {} \r\n" . format(self.tokenid, group_token)
        result = self.sendstring(string)

        if result['status']=='OK':
            return "{}" . format(json.dumps(result['message']))
        else:
            return "Error, {}" . format(result['message'])

    def send_group(self, group_token, message):
        if (self.tokenid==""):
            return "Error, not authorized"
        string = "8 {} {} {} \r\n" . format(self.tokenid, group_token, message)
        result = self.sendstring(string)
        print result

        if result['status']=='OK':
            return "{}" . format(result['message'])
        else:
            return "Error, {}" . format(result['message'])


if __name__=="__main__":
    cc = ChatClient()
    print "Haloo!! ketikan 'auth' untuk login ke chat"
    while True:
        cmdline = raw_input()
        print cc.proses(cmdline)