import requests
import json
import sys
class gsj():
    def __init__(self,url):
        self.url=url
    def get_fun(self,timeout=10):
        req=requests.session()

        response=req.get(self.url,timeout=timeout)

        return response.content,response.status_code

if __name__=="__main__":
    url = sys.argv[1]
    value = sys.argv[2]
    try:
        gsj=gsj("http://%s"%url)
        mes,status=gsj.get_fun()
        mes_status=json.loads(mes.decode('utf-8'))['%s'%value]
    except Exception as e:
        print("%s"%url +"\n\n下面是错误信息\n\n"+ "%s"%e)
    if int(mes_status)!=0 or int(status)!=200:
        print("%s"%url +"\n\n下面是错误信息\n\n"+json.loads(mes.decode('utf-8')))
        exit(2)
    else:
        print("老铁没毛病")
        exit(0)