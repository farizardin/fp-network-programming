    
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May 12 14:34:42 2019
@author: temperantia
"""
import uuid
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.chatroom = {}
        
    def getRoom(self):
        msg = []
        for keys in self.chatroom:
            member = []
            for user in self.chatroom[keys].member:
                member.append(user.username)
            temp = {"key" : keys, "member" : member}
            msg.append(temp)
        return msg
        
class UserDB:
    def __init__(self):
        self.db = {}
        self.session ={}
        
    def createUser(self, username, password):
        user = User(username, password)
        self.db[username] = user
        
    def getUserTok(self, tokenid):
        if (tokenid in self.session):
            return self.session[tokenid]
        else:
            return False
        
    def getUserUsr(self, username):
        if (username in self.db):
            return self.db[username]
        else:
            return False
        
    def auth (self, username, password):
        user = self.getUserUsr(username)
        if(user == False):
            return {'status': True, 'message' : 'user not found'}
        if (user.password == password):
            tokenid = str(uuid.uuid4()) 
            self.session[tokenid] = user
            return {'status': True, 'tokenid' : tokenid}
        return {'status': False, 'message' : 'password missmatch'}
    
    def logout (self, tokenid):
        try:
            del self.session[tokenid]
            return {'status': True, 'message' : ""}
        except KeyError:
            return {'status': False, 'message' : "token not found"}
