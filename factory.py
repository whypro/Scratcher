# -*- coding: utf-8 -*-
import urlparse
import os

from umsubjectlister import UMSubjectLister
from umimagelister import UMImageLister
from ccsubjectlister import CCSubjectLister
from ccimagelister import CCImageLister
from artsubjectlister import ARTSubjectLister
from artimagelister import ARTImageLister

class Factory(object):
    def __init__(self):
        self.save_path = ""
        self.filename = ""
        self.d_filename = ""
        
    def getSavePath(self):
        return self.save_path
        
    def getFileName(self):
        return self.filename

    def getDFileName(self):
        return self.d_filename
    
class UMFactory(Factory):
    # first_page = "http://www.umei.cc/p/gaoqing/gangtai/text_index-1.htm"
    def __init__(self, first_page):
        Factory.__init__(self)
        self.first_page = first_page
        self.category = urlparse.urlsplit(first_page).path.split("/")[3]
        self.save_path = os.path.join("umei", self.category)
        self.filename = "subject_urls_" + self.category + ".txt"
        self.d_filename = "subject_urls_" + self.category + "_d.txt"
        
    def createSubjectLister(self):
        return UMSubjectLister(self.first_page)
    
    def createImageLister(self, first_page):
        return UMImageLister(first_page)
    
class CCFactory(Factory):
    # first_page = "http://ccrt.cc/html/yazhou/"
    def __init__(self, first_page):
        Factory.__init__(self)
        self.first_page = first_page
        self.category = urlparse.urlsplit(first_page).path.split("/")[2]
        self.save_path = os.path.join("ccrt", self.category)
        self.filename = "subject_urls_" + self.category + ".txt"
        self.d_filename = "subject_urls_" + self.category + "_d.txt"
        
    def createSubjectLister(self):
        return CCSubjectLister(self.first_page)
    
    def createImageLister(self, first_page):
        return CCImageLister(first_page)
    
class ARTFactory(Factory):
    # first_page = "http://www.airenti.org/Html/Type/1_1.html"
    def __init__(self, first_page):
        Factory.__init__(self)
        self.first_page = first_page
        p = urlparse.urlsplit(first_page).path.split("/")[-1]
        if p == "1_1.html":
            self.category = "yazhou"
        elif p == "2_1.html":
            self.category = "oumei"
        assert(self.category)
        self.save_path = os.path.join("art", self.category)
        self.filename = "subject_urls_" + self.category + ".txt"
        self.d_filename = "subject_urls_" + self.category + "_d.txt"
        
    def createSubjectLister(self):
        return ARTSubjectLister(self.first_page)
    
    def createImageLister(self, first_page):
        return ARTImageLister(first_page)


if __name__ == "__main__":
    url1 = "http://ccrt.cc/html/yazhou/"
    url2 = "http://www.umei.cc/p/gaoqing/gangtai/text_index-1.htm"
    url3 = "http://www.airenti.org/Html/Type/1_1.html"
    factory1 = CCFactory(url1)
    factory2 = UMFactory(url2)
    factory3 = ARTFactory(url3)
        