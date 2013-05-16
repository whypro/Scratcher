# -*- coding: utf-8 -*-

import re
from urlparse import urljoin
from BeautifulSoup import BeautifulSoup
from subjectlister import SubjectLister

class UMSubjectLister(SubjectLister):
    def __init__(self, first_page):
        super(UMSubjectLister, self).__init__(first_page)
        #print self.main_page
        data = self.getHtmlSrc(first_page)
        self.title = self.anlzTitle(data)
        self.first_page = first_page        

    # 分析得到所有分页页面链接
    # 该函数实现部分不必深究，具有页面特异性
    def anlzAllPageUrls(self, data, first_page):
        pages = []
        pages.append(first_page)
        soup = BeautifulSoup(data, fromEncoding="gb18030")
        iter = soup.find("div", {"id": "pagination"}).find("span", {"class": "current"}).findNextSibling("a")
        while iter:
            page = urljoin(first_page, iter["href"])
            pages.append(page)
            iter = iter.findNextSibling("a")
            
        return pages

    # 分析所有分页得到所有图片链接
    # 该函数实现部分不必深究，具有页面特异性
    def anlzAllSubjectUrls(self):
        pages = self.getPages()
        subjects = []
        for page in pages:
            data = self.getHtmlSrc(page)
            soup = BeautifulSoup(data, fromEncoding="gb18030")
            sub_links = soup.find("div", {"id": "msy"}).findAll("div", {"class": "down_title D_list"})
            # 自适应
            if not sub_links:
                sub_links = soup.find("div", {"id": "msy"}).findAll("div", {"class": "title"})
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
    lister = UMSubjectLister("http://www.umei.cc/p/gaoqing/cn/text_index-1.htm")
    print lister.getTitle()
    print "\n".join(lister.getPages())
    subs = lister.getSubjects()
    print "\n".join(subs)
    print len(subs)
