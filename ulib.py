# -*- coding: utf-8 -*-
import urllib2
from urllib2 import Request, urlopen, HTTPError, URLError
from time import sleep
import socket

RETRY_TIMES = 5
SLEEP_TIME = 10

def uopen(url, headers={}, timeout=None, verbose=True):
    retryTimes = RETRY_TIMES
    sleepTime = SLEEP_TIME

    if headers:
        try:
            r = Request(url, headers=headers)
            u = urlopen(r)
        except HTTPError, e:
            print e
            print u"服务器已禁止断点续传"
        else:
            return u

    while retryTimes > 0:
        try:
            u = urlopen(url)
            if verbose:
                print u"正在连接：", url
            # 连接成功
            if u.code == 200:
                return u
            elif u.code == 201:
                break
        except HTTPError, e:
            print e
            if e.code == 404:
                break
        except URLError, e:
            print e
        except socket.timeout, e:
            print u"连接超时，等待重试……"
        except KeyboardInterrupt, e:
            print u"用户强制中止"
            exit()
        except BaseException, e:
            print e
        retryTimes -= 1
        #if verbose:
        #    print u"读取失败，等待重试……"
        try:
            # 少量多次，见机中止
            while sleepTime > 0:
                sleep(1)
                sleepTime -= 1
        except KeyboardInterrupt, e:
            print u"用户强制中止"
    if retryTimes == 0:
        exit()
    return None

def uread(u):
    data = u.read()
    return data

def uclose(u):
    u.close()

# 格式化文件大小
# 如 10 => "10B", 1024 => "1.00KB"...
def formatSize(size):
    if size > pow(1024, 2):
        new_size = size / pow(1024, 2)
        postfix = "MB"
    elif size > 1024:
        new_size = size / 1024
        postfix = "KB"
    else:
        new_size = size
        postfix = "B"
    strsize = "%.2f" % new_size
    return strsize + postfix

if __name__ == "__main__":
    #u = uopen("http://localhost/sleep.php")
    url = "http://tu.xixirenti.com/pic100/10091-42.jpg"
    #url = "http://img3.douban.com/view/photo/raw/public/p1924145611.jpg"
    u = uopen(url, headers={"Range": "bytes=0-1"})
    print u.info()
    print u.code
    data = u.read()
    uclose(u)
    print formatSize(len(data))
    
