# -*- coding: utf-8 -*-
import urlparse
import os

from factory import Factory
from subjectlister.ccsubjectlister import CCSubjectLister
from imagelister.ccimagelister import CCImageLister


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