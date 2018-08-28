from django.shortcuts import render
from .forms import AddForm
from django.http import HttpResponse

from .models import nagios_log
from extra_apps.ansible_api import ANSRunner
from django.views.decorators.csrf import csrf_exempt
from conf import Config as CONF
import json
import requests
# Create your views here.
@csrf_exempt
def index(request):
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            Responsible = form.cleaned_data['Responsible']
            Business_name = form.cleaned_data['Business_name']
            url=form.cleaned_data['url']
            isnull=nagios_log.objects.filter(Business_name=Business_name).filter(url=url)
            if isnull:
                return HttpResponse('%s is exist'%isnull[0])
            else:
                try:
                    req = requests.session()
                    response = req.get("http://%s"%url, timeout=10)
                    mes, status = response.content,response.status_code
                    mes_status = json.loads(mes.decode('utf-8'))['code']
                except Exception as e:
                    return HttpResponse("%s" % url + "\n\n下面是错误信息\n\n" + "%s" % e)
                if int(mes_status) != 0 or int(status) != 200:
                    return HttpResponse("%s" % url + "\n\n下面是错误信息\n\n" + json.loads(mes.decode('utf-8')))
                else:
                    nagios_log.objects.create(Responsible=Responsible,Business_name=Business_name,url=url)
                    resource = {
                        "all": {
                            "hosts": [{"ip": "127.0.0.1"}]
                            ,
                            "vars": {
                                'Responsible':Responsible,
                                'Business_name':Business_name,
                                'url':url
                            }
                        }
                    }
                    rbt=ANSRunner(resource)
                    rbt.run_playbook(playbook_path='/data/devops/devops/devops/apps/nagiosControl/nagios.yml')
                    return HttpResponse(json.dumps(rbt.get_playbook_result(), indent=4))
    elif request.method == 'GET':  # 当正常访问时
        form = AddForm()
    return render(request, 'nagios.html', {'form': form})
