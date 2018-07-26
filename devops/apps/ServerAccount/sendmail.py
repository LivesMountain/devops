import smtplib
from email.header import Header
from email.mime.text import MIMEText

class sendmail():
    def __init__(self,msg,to_mail,object):
        self.msg = msg
        self.to_mail=to_mail
        self.object = object
    def send(self):#发送邮件
        from_addr = 'likun@guoshengtianfeng.com'
        password = 'MImaWANGle632'
        to_addr = [self.to_mail]
        smtp_server = 'smtp.exmail.qq.com'
        smtp_port = 587
        msg = MIMEText(r'%s'%self.msg, 'plain', 'utf-8')
        msg['From'] = '运维小分队<%s>'%from_addr
        msg['To'] = '%s'%to_addr
        msg['Subject'] = Header(u'%s'%self.object).encode("utf-8")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        # server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()
