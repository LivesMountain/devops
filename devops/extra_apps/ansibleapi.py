#!/usr/bin/python
# --*-- coding:utf-8 --*--

import json
import logging
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
from collections import namedtuple
from ansible import constants as C
import ansible.executor.task_result
import multiprocessing


class ResultsCollector(CallbackBase):
	def v2_runner_on_ok(self, result):
		host = result._host
		logging.basicConfig(level=logging.DEBUG,
		                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
		                    datefmt='%a, %d %b %Y %H:%M:%S',
		                    filename='/root/cmdb/script/publish.log',
		                    filemode='w'
		                    )
		logging.warning('===v2_runner_on_ok===host=%s===result=%s' % (host, result._result))

	# print(json.dumps({host.name: result._result}, indent=4))

	def v2_runner_on_failed(self, result, ignore_errors=False):
		host = result._host
		logging.warning('===v2_runner_on_failed====host=%s===result=%s' % (host, result._result))

	def v2_runner_on_unreachable(self, result):
		host = result._host
		logging.warning('===v2_runner_on_unreachable====host=%s===result=%s' % (host, result._result))


class AnsibleAPI(object):
	def __init__(self, hostlist, image_name, playbooks, *args, **kwargs):
		self.playbooks = playbooks
		self.passwords = None
		self.callback = None
		Options = namedtuple('Options',
		                     ['connection', 'remote_user', 'ask_sudo_pass', 'verbosity', 'ack_pass', 'module_path',
		                      'forks', 'become', 'become_method', 'become_user', 'check', 'listhosts', 'listtasks',
		                      'listtags', 'syntax', 'sudo_user', 'sudo', 'diff'])
		self.options = Options(connection='smart', remote_user='root', ack_pass=None, sudo_user='root', forks=5,
		                       sudo='yes', ask_sudo_pass=False, verbosity=5, module_path=None, become=True,
		                       become_method='sudo', become_user='root', check=None, listhosts=False, listtasks=False,
		                       listtags=None, syntax=None, diff=False)
		self.loader = DataLoader()
		self.inventory = InventoryManager(loader=self.loader, sources=['hosts'])
		self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
		self.variable_manager.extra_vars = {"image_name": image_name, 'host': hostlist}

	def runplaybook(self):
		playbook = PlaybookExecutor(
			playbooks=self.playbooks,
			inventory=self.inventory,
			variable_manager=self.variable_manager,
			loader=self.loader,
			options=self.options,
			passwords=None)
		playbook._tqm._stdout_callback = ResultsCollector()

		playbook.run()


if __name__ == '__main__':
	# 创建对象
	an1 = AnsibleAPI('192.168.194.129,192.168.194.128', 'common-oss-dc3a25.tar', ['/etc/ansible/update.yml'])
	# an2 = AnsibleAPI('192.168.194.128','common-oss-dc3a25.tar',['/etc/ansible/update.yml'])
	# processes = []
	p1 = multiprocessing.Process(name='process_one', target=an1.runplaybook)
	# p2 = multiprocessing.Process(name='process_two',target=an1.runplaybook)
	# processes.append(p1)
	# processes.append(p2)
	# for p in processes:
	#	p.start()

	# 等待子进程结束，主进程退出
	# for p in processes:
	#	p.join()	#可以加浮点数参数，等待多久就不等了
	p1.start()
	if p1.is_alive():
		print('正在发布')
	else:
		print('发布结束')