# -*- coding: utf-8 -*-

import os
from time import clock
import urlparse
import re
import threading
import Queue

from ulib import uopen, uclose, formatSize
from urllib import unquote

IMAGE_URL_FILE = "image_urls.txt"       # 图片地址文件
IMAGE_INFO_FILE = "image_info.txt"      # 图片简介文件
DOWNLOAD_BUFFER_SIZE = 8192             # 下载缓冲区大小（字节）

class ImageCatcher(object):
    def __init__(self, image_lister, save_path, thread_num=10):
        self.image_lister = image_lister
        self.thread_num = thread_num        # 线程数目
        
        self.outLock = threading.Lock()     # 控制台输出锁
        self.interruptEvent = threading.Event() # 中断事件标志
        
        self.total_size = 0                 # 下载的文件总大小
        self.spent_time = 0                 # 共花费的时间

        self.first_page = image_lister.getFirstPage()   # 网页首地址 
        self.title = self._validateTitle(image_lister.getTitle())  # 页面标题
        self.info = image_lister.getInfo()              # 页面备注信息
        self.dirname = os.path.join(save_path, self.title); # 存储子目录 dirname = save_path + title
        self.images = []
        
        self._createDir(self.dirname, verbose=False)
        #print self.first_page
        print self.title
        #print self.info
        #print self.dirname
        self.downAllImages()

    # 去除标题中的非法字符 (Windows)
    def _validateTitle(self, title):
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/\:*?"<>|'
        new_title = re.sub(rstr, "", title)
        return new_title
    
    # 创建图片文件夹
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

    # 下载所有图片
    def downAllImages(self, verbose=True):
        filename = os.path.join(self.dirname, IMAGE_URL_FILE)
        # 通过文件静态获取
        if os.path.exists(filename):
            if verbose:
                print u"已存在：%s" % filename
            images = self._readImageUrls(filename, verbose=verbose)
        # 远程读取 url，并保存至文件
        else:
            images = self._saveImageUrls(filename, verbose=verbose)
        self.images = images

        imageNum = len(images)
        start = clock()
        
        # 多线程
        self.image_queue = Queue.Queue()
        for image in images:
            self.image_queue.put(image)
        self.threads = []
        for i in range(self.thread_num):
            t_name = str(i + 1)
            thread = threading.Thread(target=self._multiDownload, kwargs={"t_name": t_name, "verbose": verbose})
            #thread.setDaemon(True)
            self.threads.append(thread)
            
        for thread in self.threads:
            thread.start()
            
        self.interruptEvent.clear()
        
        try:
            while True:
                alive = False
                for thread in self.threads:
                    alive = alive or thread.isAlive()
                if not alive:
                    break
        except KeyboardInterrupt:
            self.interruptEvent.set()
            raise KeyboardInterrupt
        except:
            print u"未知异常，主线程中止"
            raise

        ###########################################
        # 单线程
        #i = 0
        #for image in images:
        #    i += 1
        #    if verbose:
        #        print "[%d/%d]" % (i, imageNum)
        #        print image
        #    self._saveImage(image)
        ###########################################

        # 保存信息文件
        filename = os.path.join(self.dirname, IMAGE_INFO_FILE)
        self._saveInfo(filename, verbose=verbose)
        end = clock()
        self.spent_time = end - start
        if verbose:
            print u"共耗时：%.2f 秒" % self.spent_time
            print u"平均速度：%.2fKB/s" % (float(self.total_size) / 1024 / self.spent_time)

    # 线程函数，多线程下载图片
    def _multiDownload(self, t_name, verbose=True):
        if verbose:
            self.outLock.acquire()
            print u"线程 %s 已启动" % t_name
            self.outLock.release()
        while True:
            try:
                image = self.image_queue.get_nowait()
                if verbose:
                    self.outLock.acquire()
                    print u"线程 %s 获得任务" % t_name
                    self.outLock.release()
                self._saveImage(image)                  # 图片下载函数
            except Queue.Empty:
                if verbose:
                    self.outLock.acquire()
                    print u"线程 %s：任务列表已空" % t_name
                    self.outLock.release()
                break
            except KeyboardInterrupt:
                self.outLock.acquire()
                print u"用户强制中止主线程，线程 %s 已中止" % t_name
                self.outLock.release()
                break
            except:
                print u"未知异常，线程 %s 已中止" % t_name
                raise
        if False:
            self.outLock.acquire()
            print u"线程 %s 已退出" % t_name
            self.outLock.release()
                
    
    # 通过文件静态获取图片 URL
    def _readImageUrls(self, filename, verbose=True):
        f = open(filename, "r")
        images = []
        for line in f:
            images.append(line.rstrip("\n"))
        f.close()
        if verbose:
            print u"搜索到：%d 张" % len(images)
        return images

    # 远程读取图片 URL，并保存至文件
    def _saveImageUrls(self, filename, verbose=True):
        images = self.image_lister.getImages()
        if verbose:
            print u"搜索到：%d 张" % len(images)
        f = open(filename, "w")
        for image in images:
            f.write(image)
            f.write("\n")
        f.close()
        if verbose:
            print u"已写入：%s" % filename
        return images

    # 读取断点续传配置文件
    def _readResumeCfg(self, cfg_filename, verbose=True):
        if verbose:
            self.outLock.acquire()
            print u"正在准备断点续传：",
        f = open(cfg_filename, "r")
        total_size = 0
        downloaded_size = 0
        try:
            total_size = int(f.readline().rstrip("\n"))         # 文件总字节数
            downloaded_size = int(f.readline().rstrip("\n"))    # 已下载字节数
            if not total_size > downloaded_size:
                raise
        except:
            if verbose:
                print u"配置文件读取出错"
                self.outLock.release()
        else:
            if verbose:
                print u"%d/%d" % (downloaded_size, total_size) 
                self.outLock.release()
        finally:
            f.close()
            
        return (total_size, downloaded_size)

    # 将图片 URL 转换为本地路径
    def _convertImageUrl(self, url):
        basename = self._validateTitle(unquote(url.split("/")[-1]))     # 解引用，去除非法字符
        dirname = self.dirname
        assert(os.path.exists(dirname))
        filename = os.path.join(dirname, basename)
        return filename
    
    # 下载图片函数
    # 线程函数，要保证线程安全
    def _saveImage(self, url, override=False, verbose=True):
        filename = self._convertImageUrl(url)
        cfg_filename = filename + ".cfg"
        tmp_filename = filename + ".tmp"
        
        if os.path.exists(filename):
            if not override:
                self.outLock.acquire()
                print u"文件已存在：%s" % filename
                self.outLock.release()
                return 
            else:
                self.outLock.acquire()
                print u"文件已过期：%s" % filename
                self.outLock.release()
                os.remove(filename)

        # 准备下载
        isResume = False
        if os.path.exists(cfg_filename) and os.path.exists(tmp_filename):
            (file_size, downloaded_size) = self._readResumeCfg(cfg_filename)
            if file_size > downloaded_size:
                isResume = True
                
        # 断点续传
        if isResume:
            request_headers = {"Range": "bytes=%d-%d" % (downloaded_size, file_size)}
            u = uopen(url, headers=request_headers)
            response_headers = u.info()
            f = open(tmp_filename, "ab")
            f.seek(downloaded_size, os.SEEK_SET)     # 文件指针移动到断点处
        # 开始新的下载
        else:
            file_size = 0
            downloaded_size = 0     
            u = uopen(url)
            if u is None:
                return
            response_headers = u.info()
            if "Content-Length" in response_headers:
                file_size = int(response_headers["Content-Length"])
                self.outLock.acquire()
                print u"文件大小：%s" % formatSize(file_size)
                self.outLock.release()
            # 首先保存到临时文件，下载成功后重命名为原文件名
            f = open(tmp_filename, "wb")
            
        self.outLock.acquire()
        print u"正在下载：%s" % url
        self.outLock.release()
        start = clock()
        try:
            while True:
                if self.interruptEvent.isSet():
                    raise KeyboardInterrupt
                buffer = u.read(DOWNLOAD_BUFFER_SIZE) 
                if not buffer:  # EOF
                    break
                downloaded_size += len(buffer);
                f.write(buffer)

                # 显示下载进度
                if file_size:
                    print "%2.1f%%\r" % (float(downloaded_size * 100) / file_size),
                else:
                    print "...\r",
        finally:
            uclose(u)
            f.close()
            cfg_f = open(cfg_filename, "w")
            cfg_f.write(str(file_size))
            cfg_f.write("\n")
            cfg_f.write(str(downloaded_size))
            cfg_f.write("\n")
            cfg_f.close()

        os.rename(tmp_filename, filename)
        self.outLock.acquire()
        print u"文件已保存：%s" % os.path.abspath(filename)
        self.outLock.release()
            
        # 删除断点续传配置文件
        if os.path.exists(cfg_filename):
            os.remove(cfg_filename)
        end = clock()
        spend = end - start
        self.outLock.acquire()
        print u"耗时：%.2f 秒" % spend
        print u"平均速度：%.2fKB/s" % (float(downloaded_size) / 1024 / spend)
        self.outLock.release()
        self.total_size += file_size

        
    # 保存信息文件
    # 文件包括：url, title, info
    def _saveInfo(self, filename, verbose=True):
        if not os.path.exists(filename):
            info = self.image_lister.getInfo()
            f = open(filename, "w")
            f.write(self.first_page)
            f.write("\n")
            # 注意此处以将 Unicode 转换为 UTF-8 保存
            #if self.title:
            #    f.write(self.title.encode("utf-8"))
            #    f.write("\n")
            if self.info:
                f.write(self.info.encode("utf-8", "ignore"))
                f.write("\n")
            if verbose:
                print u"已写入：%s" % filename
                # 显式地转为 gbk 以便于向控制台输出
                # info = self.info.encode("gbk", "ignore")
                # print info
                print self.info
            return True
        else:
            if verbose:
                print u"已存在：%s" % filename
            return False
        
# 单元测试 only
if __name__ == "__main__":
    from ccimagelister import CCImageLister
    from umimagelister import UMImageLister
    lister = UMImageLister("http://www.umei.cc/p/gaoqing/rihan/20130309222555.htm")
    #lister = UMImageLister("http://www.umei.cc/p/gaoqing/cn/20120801211417.htm")
    #lister = CCImageLister("http://ccrt.cc/html/yazhou/hob5097.htm")
    ImageCatcher(lister, "abc", 5)
