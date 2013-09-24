# -*- coding: utf-8 -*-
from urlparse import urljoin
from BeautifulSoup import BeautifulSoup

from imagelister import ImageLister

class ARTImageLister(ImageLister):
    def __init__(self, first_page):
        ImageLister.__init__(self, first_page)
        data = self.getHtmlSrc(first_page)
        self.title = self.anlzTitle(data)
        self.pages = self.anlzAllPageUrls(data, first_page)
        
    # 分析得到所有分页页面链接
    # 该函数实现部分不必深究，具有页面特异性
    def anlzAllPageUrls(self, data, first_page):
        soup = BeautifulSoup(data, fromEncoding="gb18030")
        pages = []
        pages.append(first_page)
        pagination = soup.find("ul", {"class": "pageno"})
        iter = soup.find(text=u"上一页").parent.findNextSibling("a")
        while iter.string != u"下一页":
            page_link = iter["href"]
            page = urljoin(first_page, page_link)
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
            img_links = soup.find("ul", {"class": "photo"}).findAll("img")
            for img_link in img_links:
                image = img_link["src"].strip()
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
    lister = ARTImageLister("http://www.airenti.org/Html/Disp/4373_1.html")
    #print lister.getTitle()
    #print lister.getInfo()
    print "\n".join(lister.getPages())
    print "\n".join(lister.getImages())
