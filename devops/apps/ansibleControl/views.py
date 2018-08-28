from django.shortcuts import render
from .forms import AddForm
from django.http import HttpResponse

from .models import palypath
from extra_apps.ansible_api import ANSRunner
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

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

        return HttpResponse(json.dumps(rbt.get_playbook_result()['status'], indent=4))
    elif request.method == 'GET':  # 当正常访问时
        # form = AddForm(request.POST)
        # if form.is_valid():
        # 	ip = form.cleaned_data['ip']
        # 	b = form.cleaned_data['playbook_path']
        # 	c=form.cleaned_data['book_type']
        # 	print(ip,b,c)
        form = AddForm()
    return render(request, 'index.html', {'form': form})
