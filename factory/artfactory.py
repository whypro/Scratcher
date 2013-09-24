# -*- coding: utf-8 -*-
import urlparse
import os

from factory import Factory
from subjectlister.artsubjectlister import ARTSubjectLister
from imagelister.artimagelister import ARTImageLister


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