#encoding=utf-8
import sys
import os
import urllib
import urllib2
import cookielib
import base64

cur_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(cur_path, '..'))
from login import Login


class BjguahaoLogin(Login):
    def __init__(self, user, passwd):
        super(BjguahaoLogin, self).__init__(user, passwd)
        self.login_url = 'http://www.bjguahao.gov.cn/quicklogin.htm'
    
    def get_cookie(self):
        post_dict = {
            'mobileNo': base64.b64encode(self.user),
            'password': base64.b64encode(self.passwd),
            'yzm': '',
            'isAjax': True
        }
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)

        post_data = urllib.urlencode(post_dict)
        request = urllib2.Request(url=self.login_url, data=post_data)
        response = urllib2.urlopen(request)
        info = response.info()
        cookie_set = set()
        cookie_list = info.getheaders('Set-Cookie')
        for cookie in cookie_list:
            items = cookie.split('; ')
            for item in items:
                cookie_set.add(item)
        return '; '.join(cookie_set)


if __name__ == "__main__":
    bj_login = BjguahaoLogin('15810542216', 'byd913198972')
    print bj_login.get_cookie()