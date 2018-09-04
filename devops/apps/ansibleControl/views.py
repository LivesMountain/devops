from django.shortcuts import render
from .forms import AddForm
from django.http import HttpResponse

from .models import palypath
from extra_apps.ansible_api import ANSRunner
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import logging
import json

# Create your views here.
@login_required
@csrf_exempt
def index(request):
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            ip = form.cleaned_data['ip']
            playbook_path_id = form.cleaned_data['playbook_path']
            playbook_path=palypath.objects.filter(id=playbook_path_id).distinct().values("path")

            iplist = ip.split(",")
            hosts = []
            for ip in iplist:
                host = {}
                host['username'] = 'likun'
                host['password'] = '123'
                host['ip'] = ip
                host['port'] = '22'
                hosts.append(host)
            resource = {
                "all": {
                    "hosts": hosts
                    ,
                    "vars": ''
                }
            }
            print(resource)
            rbt = ANSRunner(resource)
            rbt.run_playbook(playbook_path=playbook_path[0]['path'])
            playbook_log=rbt.get_playbook_result()
            logging.basicConfig(level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                                datefmt='%a, %d %b %Y %H:%M:%S',
                                filename='publish.log',
                                filemode='w'
                                )
            logging.warning('\n=====%s=====\n=result=%s' % (request.user,playbook_log))
        return HttpResponse(json.dumps(playbook_log['status'], indent=4))
    elif request.method == 'GET':  # 当正常访问时
        form = AddForm()
    return render(request, 'index.html', {'form': form})
