# -*- coding:utf-8 -*-
# !/usr/bin/env python
# 爆破Rar/Zip格式压缩包。

import zipfile
import rarfile
import optparse
from threading import Thread
import time
import traceback

Welcome_message = """
            **************************************************

                        压缩文件破解v1.0@Coco413

            **************************************************
                          """
print Welcome_message

def pojie_zip(Zfile, password):
    try:
        Zfile.extractall(pwd=password)  # 核心解析zip文件
        print "[+]破解成功！压缩密码为:{}".format(password)
        Zfile.close()
        return password
    except:
        pass

def pojie_rar(Rfile, password):
    try:
        Rfile.extractall(pwd=password)  # 核心解析rar文件
        print "[+]破解成功！压缩密码为:{}".format(password)
        Rfile.close()
        return password
    except:
        pass

def main():
    parser = optparse.OptionParser(
        "fountion: " + "-f <zipfile/rarfile> -d <dictionary>")
    parser.add_option('-f', dest='zname', type='string',
                      help='rar or zip file')
    parser.add_option('-d', dest='dname', type='string',
                      help='Crack Dictionary')
    (options, args) = parser.parse_args()
    if(options.zname == None) | (options.dname == None):
        print parser.usage
        exit(0)
    else:
        if ".zip" in options.zname:
            Zfile = zipfile.ZipFile(options.zname)
            passFile = open(options.dname, 'r')
            for line in passFile.readlines():
                password = line.strip('\n')   #如果是windows下的txt由于其换行是\t\n，所以代码修改为: password = line.strip('\t\n')。
                print '[+]正在尝试密码: %s' % password
                t = Thread(target=pojie_zip, args=(Zfile, password))
                t.start()
            passFile.close()
        else:
            Rfile = rarfile.RarFile(options.zname)
            passFile = open(options.dname, 'r')
            for line in passFile.readlines():
                password = line.strip('\n')   
                print '[+]正在尝试密码: %s' % password
                t = Thread(target=pojie_rar, args=(Rfile, password))
                t.start()
            passFile.close()

if __name__ == '__main__':
    start = time.clock()
    main()
    print "[+]当前爆破字典用时: (%.2f seconds)" % (time.clock() - start)
