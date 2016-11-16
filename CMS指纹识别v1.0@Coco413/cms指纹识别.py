#!/usr/bin/env python
# coding=utf-8
# CMS版本识别
    # 1.MD5方式
    # 2.响应码方式
    # 3.Title方式
    # 4.响应头方式
    # 5.内容识别方式 
# res: http://bbs.ichunqiu.com/forum.php?mod=viewthread&tid=14068&highlight=cms
# res: http://www.freebuf.com/articles/2555.html
# 在线cms检测: http://whatweb.bugscaner.com/look/
#             http://whatweb.yidianhan.com/
#             http://cms.im-fox.com/

import time
import optparse
import glob
import requests
import re
import hashlib
import sys
import os
import threading

Welcome_message = """
            **************************************************

                        CMS指纹识别v1.0@Coco413

            **************************************************
                          """
print Welcome_message


def scan():
    print '正则匹配识别模式'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    cms_list = glob.glob('./cms/*')  # 本地路径/cms/文件夹下的全部
    num = len(cms_list)
    count = 0
    for cms in cms_list:
        for line in open(cms, 'r'):
            line = line.strip().split('------')
            if len(line) != 3:  # 正常长度都是3
                continue
            try:
                r = requests.get(sys.argv[1] + line[0])
                if r.status_code != 200:
                    continue         # 状态码不是200或者出现报错就继续。
            except:
                continue
            data = r.text

            if re.compile(r'(?i)' + line[1]).search(data):
                print '[+]当前站点: ' + sys.argv[1] + ' CMS版本为: ' + line[2] + "，用时:{}".format(time.clock() - start)
                sys.exit(0)  # 并不需要扫完，发现了直接退出。
        count += 1
        print "[+]扫描进度:{}/{}".format(count, num)
    scan1(num)


def scan1(num):
    print 'MD5匹配识别模式'
    data = {} 
    alldata = []
    cms_list2 = os.path.abspath(os.path.split(
        os.path.realpath(__file__))[0] + r"/cms1/cmsmd5.txt")
    file = open(cms_list2)
    try:
        for line in file:
            txt = line.strip().split(" ")
            if len(txt) == 3:
                data["url"] = txt[0]
                data["name"] = txt[1]
                data["md5"] = txt[2]
            alldata.append(data)  # 变成列表目的就是下面跑循环
    finally:
        file.close()
    num2 = len(alldata)
    count = 0

    url = sys.argv[1].rstrip("/")
    for dataline in alldata:
        cmsurl = sys.argv[1] + dataline['url']
        try:
            r = requests.get(cmsurl, timeout=10) 
            content = r.content
        except:
            content = ''
        values = hashlib.md5(content).hexdigest()
        if values == dataline['md5']:
            print '[+]当前站点:' + url + ' CMS版本为: ' + dataline['name'] + "，用时:{}".format(time.clock() - start)
            sys.exit(0)
        count += 1
        print "[+]扫描进度:{}/{}".format(count, num2)
    print '[+]当前站点CMS指纹识别失败或者指纹信息未收录。'
    sys.exit(0)

def main():
    try:
        threads = []
        for i in xrange(20):
            t = threading.Thread(target=scan,)
            t.start()
            threads.append(t)
        for i in threads:
            i.join(timeout=10)
    except:
        pass

if __name__ == '__main__':
    start = time.clock()
    if len(sys.argv) != 2 or 'http://' not in sys.argv[1]:
        print '''\
        Example: python cms识别.py http://www.baidu.com/
        '''
        sys.exit(1)
    main()
