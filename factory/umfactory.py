# -*- coding: utf-8 -*-
import urlparse
import os

from factory import Factory
from subjectlister.umsubjectlister import UMSubjectLister
from imagelister.umimagelister import UMImageLister
    
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
        