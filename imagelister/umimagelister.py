# -*- coding: utf-8 -*-
import re
from urlparse import urljoin
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

from imagelister import ImageLister

class UMImageLister(ImageLister):
    def __init__(self, first_page):
        super(UMImageLister, self).__init__(first_page)
        data = self.getHtmlSrc(first_page)
        self.title = self.anlzTitle(data)
        self.info = self.anlzInfo(data)
        self.pages = self.anlzAllPageUrls(data, first_page)
    
    # 分析页面简介
    # 该函数实现部分不必深究，具有页面特异性
    def anlzInfo(self, data):
        soup = BeautifulSoup(data, fromEncoding="gb18030", convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
        comments = soup.find("div", {"class": "comment2"}).find("span", {"class": "i_user"})
        info = comments.string
        info += "\n"
        contents = comments.findNextSibling("font").contents
        for content in contents:
            if content.string:
                info += content.string.strip()
            else:
                info += "\n"
        return info
        
    # 分析得到所有分页页面链接
    # 该函数实现部分不必深究，具有页面特异性
    def anlzAllPageUrls(self, data, first_page):
        pages = []
        pages.append(first_page)
        soup = BeautifulSoup(data, fromEncoding="gb18030")
        iter = soup.find("div", {"id": "pagination"}).find("span", {"class": "current"}).findNextSibling("a")
        while iter.string != u"下一页":
            page = urljoin(first_page, iter["href"])
            pages.append(page)
            iter = iter.findNextSibling("a")
            
        return pages

    # 分析所有分页得到所有图片链接
    # 该函数实现部分不必深究，具有页面特异性
    def anlzAllImageUrls(self):
        pages = self.getPages()
        images = []
        for page in pages:
            data = self.getHtmlSrc(page)
            soup = BeautifulSoup(data, fromEncoding="gb18030")
            img_links = soup.findAll("img", {"class": "IMG_show"})
            for img_link in img_links:
                image = img_link["src"]
                images.append(image)
        return images
    
    def getImages(self):
        if not self.images:
            self.images = self.anlzAllImageUrls()
        return self.images

# 单元测试 only
if __name__ == "__main__":
    lister = UMImageLister("http://www.umei.cc/p/gaoqing/rihan/20130414172844.htm")
    print lister.getTitle()
    print lister.getInfo()
    print "\n".join(lister.getPages())
    print "\n".join(lister.getImages())
