#encoding=utf-8

class Login(object):
    def __init__(self, user, passwd):
        self.user = user
        self.passwd = passwd
        self.cookie = ''
    
    def get_cookie(self):
        return self.cookie
