import pexpect
# -*- coding: utf-8 -*-
#! /usr/local/python3/bin/python3
import pymysql
import logging
import datetime
import os
try:
    import json
except ImportError:
    import simplejson as json
def connect(user, host, password):
    connStr = "ansible-playbook --ask-pass -u likun -e \"name=%s\" -e \"password=%s\" -e \"hosts=%s\" /etc/ansible/usermanagement.yml" % (user,password,host)

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
        child.sendline(password)
    return child

def hostinfo():
    db = pymysql.connect(host="172.17.17.3", user="root", password="Wangxiaobao,123456", db="devops", port=3306)
    cur = db.cursor()
    sql = "select * from account_apply where user_check=1"
    try:
        cur.execute(sql)  # 执行sql语句
        results = cur.fetchall()  # 获取查询的所有记录
    except Exception as e:
        raise e
    finally:
        db.close()
    return results
    
def deladduser():
    db = pymysql.connect(host="172.17.17.3", user="root", password="Wangxiaobao,123456", db="devops", port=3306)
    cur = db.cursor()
    sql = "delete from account_apply where user_check=%s;"
    try:
        cur.execute(sql%(1))  # 执行sql语句
        db.commit()  # 获取查询的所有记录
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
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

def main():
    adddata = hostinfo()
    if len(adddata):
        try:
            for a in adddata:
                host = a[4]
                user = a[1]
                password = a[2]
                print(host, user, password)
                child = connect(user, host, password)
                child.expect(pexpect.EOF)
                logwrite(child.before)
            deladduser()
        except Exception as e:
            print(e)
    else:
        pass
if __name__ == '__main__':
    main()
