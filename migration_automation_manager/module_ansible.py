# -*- coding: utf-8 -*-
"""


- Contributors
Elliann Marks <elian.markes@gmail.com>





**- Version 1.0 - 18/09/2019**
**Functions - main**
**Libraries - ModuleMain and time**
**Dependencies - no**
**Parameters - no**

"""

# custom libraries
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.parsing.dataloader import DataLoader
from ansible.executor import playbook_executor
from ansible import context
from ansible.module_utils.common.collections import ImmutableDict


class ModuleAnsible(object):

    def __init__(self, module_log, module_configuration, migration_server=False, user_ansible="root", verbosity=0):
        try:
            self._log = module_log
            self.moduleConfiguration = module_configuration
            self._migration_server = migration_server
            self._verbosity = verbosity
            self._user_ansible = user_ansible
            if self._migration_server:
                self._private_keypath = self.moduleConfiguration.private_keypath
                self._log.debug("Key to migration server set")
            else:
                self._log.debug("Key to all server set")
                self._private_keypath = self.moduleConfiguration.private_keypath_all
                context.CLIARGS = ImmutableDict(connection='ssh', remote_user=self._user_ansible, forks=10,
                                                private_key_file=self._private_keypath, verbosity=self._verbosity, check=False, diff=False, host_key_checking=False,
                                                timeout=30, log_path=None, connect_timeout=30, connect_retries=30, connect_interval=30, become_method=None,
                                                roles_path=self.moduleConfiguration.ansible_roles, become_user=None, start_at_task=None, module_path=None, listhosts=None, subset=None,
                                                ask_vault_pass=None, vault_password_files=None, new_vault_password_file=None, output_file=None,
                                                one_line=None, tree=None, ask_sudo_pass=None, ask_su_pass=None, sudo=None, sudo_user=None,
                                                become=None, become_ask_pass=None, ask_pass=None, ssh_common_args=None, sftp_extra_args=None,
                                                scp_extra_args=None, ssh_extra_args=None, poll_interval=None, seconds=None, syntax=None, force_handlers=None,
                                                flush_cache=None, listtasks=None, listtags=None)
            self._passwords = {}
            self._loader = DataLoader()
            self._variable_manager = None
            self.playbook_execution = None
            self._inventory = None
            self.extra_vars = None
            self.playbook = None
            self.server_ip = None
            self.run_success = None
            self.stats = None
            self.result_hosts = None
            self.result_host = None
            self.summary = None

        except Exception as er:
            # generate a error log
            self._log.error("run playbook - {} - {}".format(__name__, er))

    def execute(self, playbook, extra_vars, server_ip):
        try:
            self.extra_vars = extra_vars
            self.playbook = playbook
            self.server_ip = str(server_ip) + ","
            self._inventory = InventoryManager(loader=self._loader, sources=self.server_ip)
            self._variable_manager = VariableManager(loader=self._loader, inventory=self._inventory)
            self._variable_manager.extra_vars.update(self.extra_vars)
            self.playbook_execution = playbook_executor.PlaybookExecutor(
                playbooks=[self.playbook],
                inventory=self._inventory,
                variable_manager=self._variable_manager,
                loader=self._loader,
                passwords=self._passwords)
            self.run_success = self.playbook_execution.run()
            self.stats = self.playbook_execution._tqm._stats
            if self.stats is not None and self.stats is not False:
                self.result_hosts = self.stats.processed.keys()
                if self.result_hosts is not None and self.result_hosts is not False:
                    for self.result_host in self.result_hosts:
                        self.summary = self.stats.summarize(self.result_host)
                        if self.summary['unreachable'] > 0 or self.summary['failures'] > 0:
                            return False
                        else:
                            return self.summary

        except Exception as er:
            # generate a error log
            self._log.error("run - {} - {}".format(__name__, er))
            return False
