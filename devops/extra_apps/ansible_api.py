#!/usr/bin/env python
# -*- coding=utf-8 -*-


# import os,sys
# PROJECT_ROOT = '/Users/renren/Work/imoocc/code/iops'
# sys.path.insert(0,PROJECT_ROOT)
# os.environ["DJANGO_SETTINGS_MODULE"] = 'admin.settings.settings'
# import django
# django.setup()

import json,sys,os
from ansible import constants
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.inventory.host import Host,Group
from conf import config as CONFIG


class MyInventory():
    """
    this is IOPS ansible inventory object.
    """

    def __init__(self,resource,loader,variable_manager):
        self.resource = resource
        self.loader = DataLoader()
        self.inventory = InventoryManager(loader=self.loader, sources=['hosts'])
        # self.variable_manager.set_inventory(self.inventory)
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        if isinstance(self.resource, list):
            self.add_dynamic_group(self.resource, 'all')
        elif isinstance(self.resource, dict):
            # print(self.resource.items())
            for groupname, hosts_and_vars in self.resource.items():
                self.add_dynamic_group(hosts_and_vars.get("hosts"), groupname, hosts_and_vars.get("vars"))


    def add_dynamic_group(self, hosts, groupname, groupvars=None):
        """
            add hosts to a group
        """
        self.inventory.add_group(groupname)
        my_group = Group(name=groupname)



        # if group variables exists, add them to group
        if groupvars:
            for key, value in groupvars.items():
                my_group.set_variable(key, value)
            # print(my_group.get_vars())

        # add hosts to group
        for host in hosts:
            # set connection variables
            hostip = host.get('ip')
            hostname = host.get("hostname",hostip)
            hostport = host.get("port")
            username = host.get("username")
            password = host.get("password")
            ssh_key = host.get("ssh_key")
            my_host = Host(name=hostname, port=hostport)
            if not (username and password):
                username=CONFIG.ROOT_USER
                password=CONFIG.ROOT_PASSWD
            print(username)
            print(password)
            self.variable_manager.set_host_variable(host=my_host,varname='ansible_ssh_host',value=hostip)
            self.variable_manager.set_host_variable(host=my_host,varname='ansible_ssh_pass',value=password)
            self.variable_manager.set_host_variable(host=my_host,varname='ansible_ssh_port',value=hostport)
            self.variable_manager.set_host_variable(host=my_host,varname='ansible_ssh_user',value=username)
            self.variable_manager.set_host_variable(host=my_host,varname='ansible_ssh_private_key_file',value=ssh_key)
            self.variable_manager.extra_vars = my_group.get_vars()
            # print(self.variable_manager.get_vars(host=my_host))

            # my_host.set_variable('ansible_ssh_pass', password)
            # my_host.set_variable('ansible_ssh_private_key_file', ssh_key)


            # add to group

            self.inventory.add_host(host=hostname,group=groupname,port=hostport)
            # ghost = Host(name="192.168.8.119")


    def dynamic_inventory(self):
        """
            add hosts to inventory.
        """
        if isinstance(self.resource, list):
            self.add_dynamic_group(self.resource, 'default_group')
        elif isinstance(self.resource, dict):
            for groupname, hosts_and_vars in self.resource.iteritems():
                self.add_dynamic_group(hosts_and_vars.get("hosts"), groupname, hosts_and_vars.get("vars"))

class ModelResultsCollector(CallbackBase):

    def __init__(self, *args, **kwargs):
        super(ModelResultsCollector, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result,  *args, **kwargs):
        self.host_ok[result._host.get_name()] = result


    def v2_runner_on_failed(self, result,  *args, **kwargs):
        self.host_failed[result._host.get_name()] = result

class PlayBookResultsCollector(CallbackBase):
    CALLBACK_VERSION = 2.0
    def __init__(self, *args, **kwargs):
        super(PlayBookResultsCollector, self).__init__(*args, **kwargs)
        self.task_ok = {}
        self.task_skipped = {}
        self.task_failed = {}
        self.task_status = {}
        self.task_unreachable = {}

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.task_ok[result._host.get_name()]  = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.task_failed[result._host.get_name()] = result

    def v2_runner_on_unreachable(self, result):
        self.task_unreachable[result._host.get_name()] = result

    def v2_runner_on_skipped(self, result):
        self.task_ok[result._host.get_name()]  = result

    def v2_playbook_on_stats(self, stats):
        hosts = sorted(stats.processed.keys())
        for h in hosts:
            t = stats.summarize(h)
            self.task_status[h] = {
                                       "ok":t['ok'],
                                       "changed" : t['changed'],
                                       "unreachable":t['unreachable'],
                                       "skipped":t['skipped'],
                                       "failed":t['failures']
                                   }

class ANSRunner(object):
    """
    This is a General object for parallel execute modules.
    """
    def __init__(self,resource,connection='smart',*args, **kwargs):
        self.resource = resource
        self.inventory = None
        self.variable_manager = None
        self.loader = None
        self.options = None
        self.passwords = None
        self.callback = None
        self.results_raw = {}
        Options = namedtuple('Options', ['connection','module_path', 'forks', 'timeout',  'remote_user',
                'ask_pass', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
                'scp_extra_args', 'become', 'become_method', 'become_user', 'ask_value_pass', 'verbosity',
                'check', 'listhosts', 'listtasks', 'listtags', 'syntax','diff'])

        self.loader = DataLoader()
        self.options = Options(connection=connection, module_path=None, forks=100, timeout=10,
                remote_user='root', ask_pass=False, private_key_file=None, ssh_common_args=None, ssh_extra_args=None,
                sftp_extra_args=None, scp_extra_args=None, become=None, become_method=None,
                become_user='root', ask_value_pass=False, verbosity=None, check=False, listhosts=False,
                listtasks=False, listtags=False, syntax=False, diff=True)

        self.passwords = dict(sshpass=None, becomepass=None)
        myinvent = MyInventory(self.resource, self.loader, self.variable_manager)
        self.inventory = myinvent.inventory
        self.variable_manager = myinvent.variable_manager

        # self.variable_manager.set_inventory(self.inventory)
        # self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)

    def runcommand(self, module_name, module_args):
        play_source =  dict(
                name = "Test",
                hosts = 'all',
                gather_facts = 'no',
                tasks = [
                    dict(action=dict(module=module_name, args=module_args), register='shell_out'),
                 ]
            )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)
        self.callback = ModelResultsCollector()
        tqm = None
        try:
            tqm = TaskQueueManager(
                      inventory=self.inventory,
                      variable_manager=self.variable_manager,
                      loader=self.loader,
                      options=self.options,
                      passwords=None,
                      stdout_callback="minimal",
                  )
            result = tqm.run(play)
            print(result)
        finally:
            if tqm is not None:
                tqm.cleanup()


    def run_playbook(self, playbook_path,extra_vars=None):
        """
        run ansible palybook
        """
        try:
            # if self.redisKey:self.callback = PlayBookResultsCollectorToSave(self.redisKey,self.logId)
            self.callback = PlayBookResultsCollector()
            if extra_vars:self.variable_manager.extra_vars = extra_vars
            executor = PlaybookExecutor(
                playbooks=[playbook_path], inventory=self.inventory, variable_manager=self.variable_manager, loader=self.loader,
                options=self.options, passwords=self.passwords,
            )
            executor._tqm._stdout_callback = self.callback
            constants.HOST_KEY_CHECKING = False #关闭第一次使用ansible连接客户端是输入命令
            executor.run()
        except Exception as err:
            return False

    def get_model_result(self):
        self.results_raw = {'success':{}, 'failed':{}, 'unreachable':{}}
        for host, result in self.callback.host_ok.items():
            hostvisiable = host.replace('.','_')
            self.results_raw['success'][hostvisiable] = result._result


        for host, result in self.callback.host_failed.items():
            hostvisiable = host.replace('.','_')
            self.results_raw['failed'][hostvisiable] = result._result


        for host, result in self.callback.host_unreachable.items():
            hostvisiable = host.replace('.','_')
            self.results_raw['unreachable'][hostvisiable]= result._result

        # return json.dumps(self.results_raw)
        return self.results_raw

    def get_playbook_result(self):
        self.results_raw = {'skipped':{}, 'failed':{}, 'ok':{},"status":{},'unreachable':{},"changed":{}}
        for host, result in self.callback.task_ok.items():
            # print('1``````````````````````````````````',host,result,'1``````````````````````````````````')
            self.results_raw['ok'][host] = result._result

        for host, result in self.callback.task_failed.items():
            # print('2``````````````````````````````````',host, result , '2``````````````````````````````````')
            self.results_raw['failed'][host] = result._result

        for host, result in self.callback.task_status.items():
            # print('3``````````````````````````````````',host, result ,'3``````````````````````````````````')
            self.results_raw['status'][host] = result

        # for host, result in self.callback.task_changed.items():
        #     self.results_raw['changed'][host] = result

        for host, result in self.callback.task_skipped.items():
            # print('4``````````````````````````````````',host, result,'4``````````````````````````````````')
            self.results_raw['skipped'][host] = result._result

        for host, result in self.callback.task_unreachable.items():
            # print('5``````````````````````````````````',host, result , '5``````````````````````````````````')
            self.results_raw['unreachable'][host] = result._result
        return self.results_raw


if __name__ == '__main__':
    resource = [
                 {"ip": "localhost"},
                 {"hostname": "192.168.37.152"},
                 ]
    resource =  {
                    "all": {
                        "hosts": [
                                    {'ip': '192.168.37.160'},
                                  ],
                        "vars": {
                            'Responsible':123,
                            'Business_name':123,
                            'url':123
                        }
                    }
                }
    rbt = ANSRunner(resource)
    # Ansible Adhoc
    # rbt.runcommand(module_name='shell',module_args="ls /tmp")
    # data = rbt.get_model_result()
    # print(data)
    # Ansible playbook
    rbt.run_playbook(playbook_path='/data/devops/devops/apps/nagiosControl/nagios.yml')
    # print(rbt.get_playbook_result()['status'])
    # rbt.run_model(host_list=[],module_name='yum',module_args="name=htop state=present")
