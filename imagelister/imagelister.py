# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
from ulib import uopen, uclose

class ImageLister(object):
    def __init__(self, first_page):
        self.first_page = first_page
        self.title = ""
        self.info = ""
        self.pages = []
        self.images = []

    def getFirstPage(self):
        return self.first_page
    
    def getPages(self):
        return self.pages
    
    def getImages(self):
        return self.images
    
    def getTitle(self):
        return self.title
    
    def getInfo(self):
        return self.info

    def getHtmlSrc(self, url):
        u = uopen(url)
        src = u.read()
        uclose(u)
        return src

    # 分析页面标题
    def anlzTitle(self, data):
        soup = BeautifulSoup(data, fromEncoding="gb18030")
        title = soup.html.head.title.string.strip()
        return title
    
    def anlzAllPageUrls(self):
        pass

    def anlzAllImageUrls(self):
        pass


