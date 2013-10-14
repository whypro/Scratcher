# -*- coding: utf-8 -*-
from factory.umfactory import UMFactory
from factory.ccfactory import CCFactory
from factory.artfactory import ARTFactory
from subjectcatcher import SubjectCatcher

import getopt
import sys


# 获取主题
if __name__ == '__main__':

    debug = False      # 调试
    thread_num = 10    # 线程数量
    out_of_date = 10   # 任务列表过期时间
    proxies = None     # 代理服务器
    tasks_file = 'tasks.txt'
    save_path = '../media'

    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'df:s:t:e:p:', ['debug', 'file=', 'sites=', 'thread=', 'expired=', 'proxies='])
    except getopt.GetoptError:
        print 'Usage: %s -p|--pages [url] -t|--thread [number]' % sys.argv[0]  
        exit(1)

    for opt, arg in opts:
        if opt in ('-d', '--debug'):
            debug = True
        elif opt in ('-f', '--file'):
            tasks_file = arg
        elif opt in ('-s', '--sites'): 
            pass
        elif opt in ('-t', '--thread'):
            thread_num = int(arg)           
        elif opt in ('-e', '--expired'):
            out_of_date = int(arg)
        elif opt in ('-p', '--proxies'): 
            import urllib2
            proxies = arg
            proxies_dict = dict([proxies.split('://')])
            proxy_handler = urllib2.ProxyHandler(proxies_dict)
            opener = urllib2.build_opener(proxy_handler)
            urllib2.install_opener(opener)

    if not debug:
        import sys
        import time
        sys.stderr = open("error.log", "a")
        sys.stderr.write("################################################################\n")
        sys.stderr.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        sys.stderr.write("\n")

    print u'调试模式：%s\n任务文件：%s\n线程池大小：%d\n有效时间：%d 天\n代理服务器：%s\n目标文件夹：%s' % (debug, tasks_file, thread_num, out_of_date, proxies, save_path)

    factories = {
        'umei.cc': UMFactory,
        'ccrt.cc': CCFactory,
        'airenti.org': ARTFactory,
    }

    f = open(tasks_file, 'r')
    tasks = f.readlines()
    f.close()

    for task in tasks:
        factory = None
        for url, fact in factories.items():
            if url in task:
                factory = fact(task.strip())
                break
        if not factory:
            raise
        catcher = SubjectCatcher(factory, save_path=save_path, out_of_date=out_of_date, thread_num=thread_num)

