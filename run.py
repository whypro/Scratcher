# -*- coding: utf-8 -*-
from factory.umfactory import UMFactory
from factory.ccfactory import CCFactory
from factory.artfactory import ARTFactory
from subjectcatcher import SubjectCatcher

import getopt
import sys
# 获取主题
if __name__ == '__main__':
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'df:s:t:e:p:', ['debug', 'file=', 'sites=', 'thread=', 'expired=', 'proxies='])
    except getopt.GetoptError:
        print 'Usage: %s -p|--pages [url] -t|--thread [number]' % sys.argv[0]  
        exit(1)
    
    debug = True
    tasks_file = 'tasks.txt'
    thread_num = 10
    out_of_date = 10

    for opt, arg in opts:
        if opt in ('-d', '--debug'):
            DEBUG = True
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
            proxies = dict([arg.split('://')])
            proxy_handler = urllib2.ProxyHandler(proxies)
            opener = urllib2.build_opener(proxy_handler)
            urllib2.install_opener(opener)

    f = open(tasks_file, 'r')
    tasks = f.readlines()
    f.close()

    import sys
    import time
    if not debug:
        sys.stderr = open("error.log", "a")
        sys.stderr.write("################################################################\n")
        sys.stderr.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        sys.stderr.write("\n")

    factories = {
        'umei.cc': UMFactory,
        'ccrt.cc': CCFactory,
        'airenti.org': ARTFactory,
    }

    for task in tasks:
        factory = None
        for url, fact in factories.items():
            if url in task:
                factory = fact(task)
                break
        if not factory:
            raise
        catcher = SubjectCatcher(factory, out_of_date=out_of_date, thread_num=thread_num)

