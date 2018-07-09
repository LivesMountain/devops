# -*- coding: utf-8 -*-
import json
from collections import namedtuple
from ansible.vars.manager import VariableManager
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.task_result import TaskResult
from ansible.plugins.callback import CallbackBase


class ResultCallback(CallbackBase):
    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host
        print(json.dumps({host.name: result._result}, indent=4))


Options = namedtuple('Options',
                     ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check', 'diff'])
# 用来加载解析yaml文件或JSON内容,并且支持vault的解密
loader = DataLoader()
print(loader)
options = Options(connection='local', module_path=None, forks=2, become=None, become_method=None, become_user=None,
                  check=False, diff=False)
# connection参数，如果执行本地节点用'local', 远端节点用'smart'

# passwords = dict(vault_pass='xxxxx')    #密钥方式取消这步
results_callback = ResultCallback()
# 根据inventory加载对应变量,此处host_list参数可以有两种格式：
# 1: hosts文件(需要),
# 2: 可以是IP列表,此处使用IP列表
# variable_manager = VariableManager()
inventory = InventoryManager
variable_manager = VariableManager(loader=loader, inventory=inventory)
variable_manager.set_inventory(inventory)

play_source = dict(
    name="Ansible Play",
    hosts='*',
    gather_facts='no',
    tasks=[
        dict(action=dict(module='shell', args='df -Th'), register='shell_out'),
        #        dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}')))
    ]
)

play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
tqm = None
try:
    tqm = TaskQueueManager(
        inventory=inventory,
        variable_manager=variable_manager,
        loader=loader,
        options=options,
        passwords=None,
        stdout_callback=results_callback,
    )
    result = tqm.run(play)
#    print(result)
finally:
    if tqm is not None:
        tqm.cleanup()
