import pexpect
# -*- coding: utf-8 -*-
#! /usr/local/python3/bin/python3
import pymysql
import logging
import datetime
import os
from conf import config as CONFIG
try:
    import json
except ImportError:
    import simplejson as json
def connect(user, host, password):
    connStr = "ansible-playbook --ask-pass -u %s -e \"name=%s\" -e \"password=%s\" -e \"hosts=%s\" /etc/ansible/usermanagement.yml" % (CONFIG.ROOT_USER,user,password,host)

    # 为ssh命令生成一个spawn类的对象
    child = pexpect.spawn(connStr)

    # 期望有ssh_newkey字符、提示输入密码的字符出现，否则超时
    ret = child.expect([pexpect.TIMEOUT, "SSH", '[P|p]assword: '])

    # 匹配到超时TIMEOUT
    if ret == 0:
        print('[-] Error Connecting')
        return

    # 匹配到ssh_newkey
    if ret == 1:
        # 发送yes回应ssh_newkey并期望提示输入密码的字符出现
        child.sendline(CONFIG.ROOT_PASSWD)
    print(child)
    if child:

        return True
    else:
        return False

def logwrite(content):
    logpath = '/data/devops/cron_log.log'

    if not os.path.isdir(logpath):
        os.makedirs(logpath)

    t = datetime.datetime.now()
    daytime = t.strftime('%Y-%m-%d')
    daylogfile = logpath + '/' + str(daytime) + '.log'
    logging.basicConfig(filename=daylogfile, level=logging.DEBUG)
    logging.info('*' * 130)
    logging.debug(str(t) + str(content))
