# -*- coding: utf-8 -*-

import os
import time
import threading
import Queue

from imagecatcher import ImageCatcher
from factory import UMFactory, CCFactory, ARTFactory

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
                imageLister = self.factory.createImageLister(sub)
                imageCatcher = ImageCatcher(imageLister, self.dirname, thread_num=thread_num)
                d_subjects.append(sub)
                self._saveSubjectUrls(d_filename, subjects=d_subjects)
                

"""
class ThreadPool:
    def __init__(self, work_queue, thread_num=10, timeout=10):
        self.threads = []
        self.work_queue = work_queue
        self.timeout = timeout
        self.__recruitThreads(thread_num)
    
    def __recruitThreads(self, thread_num):
        for i in range(thread_num):
            thread = SubjectCatcherThread(self.work_queue, self.timeout)
            self.threads.append(thread)
    
    def start(self):
        for thread in self.threads:
            thread.start()
            print u"线程 %s 已启动" % thread.getName()
        
    def waitComplete(self):
        for thread in self.threads:
            if thread.isAlive():
                thread.join()
            else:
                self.threads.remove(thread)
                print u"线程 %s 已结束" % thread.getName()
        print u"所有线程已结束"
        
    def add_job(self, url):
        self.work_queue.put(url)

class SubjectCatcherThread(threading.Thread):
    count = 0
    def __init__(self, work_queue, timeout=10):
        threading.Thread.__init__(self) 
        self.work_queue = work_queue
        self.timeout = timeout
        SubjectCatcherThread.count += 1
    
    def run(self):
        while True:
            try:
                url = self.work_queue.get(timeout=self.timeout)
                print u"线程 %s 正在运行" % self.getName()
                catcher = SubjectCatcher(CCFactory(url))
            except Queue.Empty:
                print u"线程 %s 已结束" % self.getName()
                break
"""

# 获取主题
if __name__ == "__main__":
    #tasks = Queue.Queue()  
    #tp = ThreadPool(tasks, 10)
    #tp.add_job("http://ccrt.cc/html/yazhou/")
    #tp.start()
    #tp.add_job("http://www.umei.cc/p/gaoqing/gangtai/text_index-1.htm")
    #tp.add_job("http://www.umei.cc/p/gaoqing/cn/text_index-1.htm")
    #tp.waitComplete()
    tasks = []
    tasks.append("http://www.umei.cc/p/gaoqing/gangtai/text_index-1.htm")
    tasks.append("http://www.umei.cc/p/gaoqing/rihan/text_index-1.htm")
    tasks.append("http://www.umei.cc/p/gaoqing/cn/text_index-1.htm")
    tasks.append("http://ccrt.cc/html/yazhou/")
    tasks.append("http://ccrt.cc/html/oumei/")
    tasks.append("http://www.airenti.org/Html/Type/1_1.html")
    tasks.append("http://www.airenti.org/Html/Type/2_1.html")

    import sys
    import time
    sys.stderr = open("error.log", "a")
    sys.stderr.write("################################################################\n")
    sys.stderr.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    sys.stderr.write("\n")
    import re
    for task in tasks:
        if re.search("umei.cc", task):
            factory = UMFactory(task)
        elif re.search("ccrt.cc", task):
            factory = CCFactory(task)
        elif re.search("airenti.org", task):
            factory = ARTFactory(task)
        else:
            raise
        catcher = SubjectCatcher(factory, out_of_date=10, thread_num=10)

