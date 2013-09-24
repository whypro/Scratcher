# -*- coding: utf-8 -*-
import re
from urlparse import urljoin
from BeautifulSoup import BeautifulSoup

from subjectlister import SubjectLister

class CCSubjectLister(SubjectLister):
    def __init__(self, first_page):
        SubjectLister.__init__(self, first_page)
        #print self.main_page
        data = self.getHtmlSrc(first_page)
        self.title = self.anlzTitle(data)

    # 分析得到所有分页页面链接
    # 该函数实现部分不必深究，具有页面特异性
    def anlzAllPageUrls(self, data, first_page):
        pages = []
        pages.append(first_page)
        # 循环读取所有分页
        while True:
            soup = BeautifulSoup(data, fromEncoding="gb18030")
            iter = soup.find("a", {"class": "thispg"}).findNextSibling("a")
            if not iter:
                break
            while iter.string != u"末页":
                page = urljoin(first_page, iter["href"])
                pages.append(page)
                iter = iter.findNextSibling()
            data = self.getHtmlSrc(page)
            
        return pages

    # 分析所有分页得到所有主题链接
    # 该函数实现部分不必深究，具有页面特异性
    def anlzAllSubjectUrls(self):
        pages = self.getPages()
        subjects = []
        for page in pages:
            data = self.getHtmlSrc(page)
            soup = BeautifulSoup(data, fromEncoding="gb18030")
            sub_links = soup.find("div", {"class": "fitCont_2"}).ul.findAll("li")
            for sub_link in sub_links:
                subject = urljoin(page, sub_link.a["href"])
                subjects.append(subject)
        return subjects
    
    def getPages(self):
        if not self.pages:
            data = self.getHtmlSrc(self.first_page)
            self.pages = self.anlzAllPageUrls(data, self.first_page)
        return self.pages
        
    def getSubjects(self):
        if not self.subjects:
            self.subjects = self.anlzAllSubjectUrls()
        return self.subjects
        
# 单元测试 only
if __name__ == "__main__":
    lister = CCSubjectLister("http://ccrt.cc/html/yazhou/index.html")
    print lister.getTitle()
    print "\n".join(lister.getPages())
    print "\n".join(lister.getSubjects())
