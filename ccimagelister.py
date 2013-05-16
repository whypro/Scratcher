# -*- coding: utf-8 -*-

from urlparse import urljoin
from BeautifulSoup import BeautifulSoup
from imagelister import ImageLister

class CCImageLister(ImageLister):
    def __init__(self, first_page):
        ImageLister.__init__(self, first_page)
        data = self.getHtmlSrc(first_page)
        self.title = self.anlzTitle(data)
        self.pages = self.anlzAllPageUrls(data, first_page)
        
    # 分析得到所有分页页面链接
    # 该函数实现部分不必深究，具有页面特异性
    def anlzAllPageUrls(self, data, first_page):
        pages = []
        pages.append(first_page)
        soup = BeautifulSoup(data, fromEncoding="gb18030")
        iter =  soup.find("div", {"class": "pp"}).find(text="[1]").parent.findNextSibling("a")
        
        while iter:
            page = urljoin(first_page, iter["href"])
            pages.append(page)
            iter = iter.findNextSibling("a")
            
        #print "\n".join(pages)
        return pages

    # 分析所有分页得到所有图片链接
    # 该函数实现部分不必深究，具有页面特异性
    def anlzAllImageUrls(self):
        pages = self.getPages()
        images = []
        for page in pages:
            data = self.getHtmlSrc(page)
            soup = BeautifulSoup(data, fromEncoding="gb18030")
            img_links = soup.find("div", {"class": "pp"}).findAll("img")
            for img_link in img_links:
                image = img_link["src"]
                images.append(image)
        return images
    
    def getPages(self):
        if not self.pages:
            data = self.getHtmlSrc(self.first_page)
            self.pages = self.anlzAllPageUrls(data, self.first_page)
        return self.pages
        
    def getImages(self):
        if not self.images:
            self.images = self.anlzAllImageUrls()
        return self.images
        
# 单元测试 only
if __name__ == "__main__":
    lister = CCImageLister("http://ccrt.cc/html/yazhou/gb157.htm")
    print lister.getTitle()
    #print lister.getInfo()
    print "\n".join(lister.getPages())
    print "\n".join(lister.getImages())
