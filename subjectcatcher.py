# -*- coding: utf-8 -*-

import os
import time
import threading
import Queue

from imagecatcher import ImageCatcher

class SubjectCatcher:
    def __init__(self, factory, out_of_date=10, thread_num=10):
        self.factory = factory
        self.subject_lister = factory.createSubjectLister()
        self.dirname = factory.getSavePath()
        self.filename = os.path.join(self.dirname, factory.getFileName())
        self.d_filename = os.path.join(self.dirname, factory.getDFileName())
        
        self.first_page = self.subject_lister.getFirstPage()
        self.title = self.subject_lister.getTitle()
        self.subjects = []
        self.d_subjects = []

        self._createDir(self.dirname, verbose=False)
        self.downAllSubjects(out_of_date=out_of_date, thread_num=thread_num)    # 过期时间（单位为天数）
        
    # 创建文件夹
    def _createDir(self, dirname, verbose=True):
        if not os.path.exists(dirname):
            os.makedirs(dirname)
            if verbose:
                print u"已创建：%s" % dirname
            return True
        else:
            if verbose:
                print u"已存在：%s" % dirname
            return False
     
    # 通过文件静态获取主题 URL
    def _readSubjectUrls(self, filename, verbose=True):
        f = open(filename, "r")
        subjects = []
        for url in f: 
            subjects.append(url.rstrip("\n"))
        f.close()
        if verbose:
            print u"搜索到 %d 个主题" % len(subjects)
        return subjects
        
    # 远程读取主题 URL，并保存至文件
    def _saveSubjectUrls(self, filename, subjects=[], verbose=True):
        if not subjects:
            subjects = self.subject_lister.getSubjects()
        #subjects = []
        f = open(filename, "w")
        for sub in subjects:
            f.write(sub)
            f.write("\n")
        f.close()
        if verbose:
            print u"已写入：%d 个" % len(subjects)
        return subjects
    
    # out_of_date，过期时间，单位为天数
    def downAllSubjects(self, out_of_date, thread_num, verbose=True):
        filename = self.filename
        d_filename = self.d_filename
        # 通过文件静态获取
        # 文件存在，且未过期
        if os.path.exists(filename) and (time.time() - os.path.getmtime(filename)) < out_of_date * 24 * 60 * 60:
            if verbose:
                print u"已存在：%s" % filename
            subjects = self._readSubjectUrls(filename, verbose=False)   # verbose=False
            if verbose:
                print u"搜索到：%d 个主题" % len(subjects)
        # 文件过期
        # 远程读取 url，并保存至文件
        elif os.path.exists(filename):
            if verbose:
                print u"已过期：%s" % filename
            subjects = self._saveSubjectUrls(filename, verbose=verbose)
        # 远程读取 url，并保存至文件
        else:
            subjects = self._saveSubjectUrls(filename, verbose=verbose)
        
        if os.path.exists(d_filename):
            if verbose:
                print u"已存在：%s" % d_filename
            d_subjects = self._readSubjectUrls(d_filename, verbose=False)   # verbose=False
            if verbose:
                print u"已跳过：%d 个主题" % len(d_subjects)
        else:
            d_subjects = []
            
        self.subjects = subjects
        self.d_subjects = d_subjects
        
        for sub in subjects:
            if not sub in d_subjects:
                print u"第 %d 个主题，共 %d 个主题" % (len(d_subjects) + 1, len(subjects))
                try:
                    imageLister = self.factory.createImageLister(sub)
                # 页面不合法，如返回 404 页面
                except AttributeError:
                    print u"imageLister 创建失败：%s" % sub
                    f = open("except.txt", "a")
                    f.write(sub)
                    f.write("\n")
                    f.close()
                    continue
                except:
                    raise
                else:
                    imageCatcher = ImageCatcher(imageLister, self.dirname, thread_num=thread_num)
                    d_subjects.append(sub)
                    self._saveSubjectUrls(d_filename, subjects=d_subjects)
