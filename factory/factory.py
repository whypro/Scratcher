# -*- coding: utf-8 -*-
import urlparse
import os

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

        