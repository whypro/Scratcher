# -*- coding: utf-8 -*-

from ulib import uopen, uclose
from BeautifulSoup import BeautifulSoup

class SubjectLister(object):
    def __init__(self, first_page):
        self.first_page = first_page
        self.title = ""
        self.subjects = []
        self.pages = []
        
    def getFirstPage(self):
        return self.first_page
    
    def getPages(self):
        return self.pages
    
    def getSubjects(self):
        return self.subjects

    def getTitle(self):
        return self.title
    
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

    def anlzAllSubjectUrls(self):
        pass


