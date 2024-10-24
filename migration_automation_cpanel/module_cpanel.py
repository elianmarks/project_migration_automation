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

# libraries
from migration_automation_manager.module_ansible import ModuleAnsible
from migration_automation_manager.module_database import ModuleDatabase
from migration_automation_manager.module_publish import ModulePublish
import os
import json
from contextlib import closing


class ModuleCPanel:

    def __init__(self, module_log, module_configuration):
        """
        Responsible for execute the checking playbooks and store result in dict.
        :param module_log: log instance
        :type module_log: Object
        """
        try:
            self._log = module_log
            self.module_configuration = module_configuration
            self.general_error = False
            # create the instances
            self.module_database = ModuleDatabase(self._log, self.module_configuration)
            # set playbooks
            self.playbook_cpanel = self.module_configuration.playbook_cpanel
            # get values collected
            self.server = None
            self.values_ticket = None
            self.src_server = None
            self.dst_server = None
            self.src_type = None
            self.dst_type = None
            self.main_domain = None
            self.ticket_id = None
            self.file_user_get_data = None
            self.result_user_get_data = None
            self.home = None
            self.user = None
            self.open_user_get_data = None
            self.message = None
            self.thread_id = None
            self.type_task = None
            self.report_casepath = None
            self.file_available_user = None
            self.values_database = None
            self.report_dir = self.module_configuration.report_dir
            self.summary_ansible = None
            self.module_ansible = None
            self.vars_ansible = None
            self.file_flag_restore_error = None
            self.file_flag_copy_error = None
            self.file_domain_available = None
            self.file_domain_unavailable_content = None
            self.open_domain_unavailable_content = None
            self.domain_unavailable_content = None
            self.src_ip = None
            self.dst_ip = None
            self.connect_ip = None
            self.queue_manager = ModulePublish(self._log, "manager", self.module_configuration.user_queue, self.module_configuration.password_queue,
                                               self.module_configuration.host_queue, self.module_configuration.port_queue, self.module_configuration.key("manager"))

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            self.general_error = True

    def initialize(self, values_ticket):
        try:
            # get values collected
            self.server = None
            self.values_ticket = None
            self.src_server = None
            self.dst_server = None
            self.src_type = None
            self.dst_type = None
            self.main_domain = None
            self.ticket_id = None
            self.user = None
            self.open_user_get_data = None
            self.file_user_get_data = None
            self.result_user_get_data = None
            self.home = None
            self.thread_id = None
            self.type_task = None
            self.values_database = None
            self.module_ansible = None
            self.report_casepath = None
            self.file_available_user = None
            self.file_flag_restore_error = None
            self.file_flag_copy_error = None
            self.file_domain_available = None
            self.file_domain_unavailable_content = None
            self.open_domain_unavailable_content = None
            self.domain_unavailable_content = None
            self.src_ip = None
            self.dst_ip = None
            self.connect_ip = None
            self.vars_ansible = None
            self.summary_ansible = False
            self.general_error = False
            # get values collected
            self.values_ticket = values_ticket
            self.ticket_id = self.values_ticket.get('id')
            self.thread_id = self.values_ticket.get('thread_id')
            self.type_task = self.values_ticket.get('type_task')
            # get values in database
            if self.ticket_id is not None and self.ticket_id is not False and \
                    self.thread_id is not None and self.thread_id is not False and \
                    self.type_task is not None and self.type_task is not False:
                self.values_database = self.module_database.get_values(self.ticket_id, self.thread_id, "cpanel")
                if self.values_database is not False and self.values_database is not None and len(self.values_database) == 9:
                    self.src_server = self.values_database[0]
                    self.dst_server = self.values_database[1]
                    self.src_type = self.values_database[2]
                    self.dst_type = self.values_database[3]
                    self.main_domain = self.values_database[4]
                    self.user = self.values_database[5]
                    self.src_ip = self.values_database[6]
                    self.dst_ip = self.values_database[7]
                    self.connect_ip = self.values_database[8]
                    self.report_casepath = os.path.join(self.report_dir, str(self.main_domain) + "_" + str(self.ticket_id) + "_" + str(self.thread_id))
                    self.file_flag_restore_error = os.path.join(self.report_casepath, "restore_error.flag")
                    self.file_flag_copy_error = os.path.join(self.report_casepath, "copy_error.flag")
                    self.file_available_user = os.path.join(self.report_casepath, "destination/user_available.flag")
                    self.file_domain_available = os.path.join(self.report_casepath, "destination/domain_available.flag")
                    self.file_domain_unavailable_content = os.path.join(self.report_casepath, "destination/domain_unavailable_content.flag")
                    # instance ansible module to all servers
                    self.module_ansible = ModuleAnsible(module_log=self._log, module_configuration=self.module_configuration)
                    if self.type_task == "restore":
                        if os.path.exists(self.file_domain_unavailable_content):
                            with closing(open(self.file_domain_unavailable_content)) as self.open_domain_unavailable_content:
                                self.domain_unavailable_content = self.open_domain_unavailable_content.read().replace("\n", "")
                        else:
                            self.domain_unavailable_content = False
                        self.vars_ansible = {
                            "domain": self.main_domain,
                            "ticketID": self.ticket_id,
                            "threadID": self.thread_id,
                            "dst_type": self.dst_type,
                            "src_type": self.src_type,
                            "user_available": os.path.exists(self.file_available_user),
                            "domain_available": os.path.exists(self.file_domain_available),
                            "domain_unavailable_content": self.domain_unavailable_content,
                            "user": self.user,
                            "restore": True,
                        }
                        if self.connect_ip == 1 and self.dst_ip is not None:
                            self.server = self.dst_ip
                        else:
                            self.server = self.dst_server
                        return True
                    elif self.type_task == "pkgacct":
                        self.vars_ansible = {
                            "domain": self.main_domain,
                            "ticketID": self.ticket_id,
                            "threadID": self.thread_id,
                            "user": self.user,
                            "pkgacct": True,
                        }
                        if self.connect_ip == 1 and self.src_ip is not None:
                            self.server = self.src_ip
                        else:
                            self.server = self.src_server
                        return True
                    else:
                        self.general_error = True
                        self._log.error("Invalid type cpanel - {}".format(self.values_ticket))
                        return False
                else:
                    self.general_error = True
                    self._log.error("Failed cpanel get values in database - {}".format(self.values_ticket))
                    return False
            else:
                self.general_error = True
                self._log.error("Failed cpanel get values in message - {}".format(self.values_ticket))
                return False

        except Exception as er:
            # generate a error log
            self._log.error("initialize cpanel - {} - {}".format(self.__class__.__name__, er))
            self.general_error = True
            return False

    def process(self):
        try:
            if self.general_error is False:
                if os.path.exists(self.file_flag_restore_error):
                    os.remove(self.file_flag_restore_error)
                if os.path.exists(self.file_flag_copy_error):
                    os.remove(self.file_flag_copy_error)
                # mark start ansible cpanel, 1 - start, 2 - failed, 3 - completed
                self.module_database.update_analyzing("cpanel_" + self.type_task, 1, self.thread_id)
                # debug log
                self._log.debug(self.vars_ansible)
                # execute playbook and get summary result
                self.summary_ansible = self.module_ansible.execute(self.playbook_cpanel, self.vars_ansible, self.server)
                # check if execution completed with success
                if os.path.exists(self.file_flag_restore_error) or os.path.exists(self.file_flag_copy_error) \
                        or self.summary_ansible is False or self.summary_ansible is None or self.summary_ansible['rescued'] > 0:
                    # update cpanel type with failed
                    self.module_database.update_analyzing("cpanel_" + self.type_task, 2, self.thread_id)
                    self.vars_ansible = None
                    self.summary_ansible = False
                    # error log
                    self._log.error("Ansible cpanel failed - {} - {}".format(self.type_task, self.values_ticket))
                    if self.message_manager():
                        self._log.info("Send manager {}".format(self.message))
                    else:
                        self._log.info("Failed send manager {}".format(self.message))
                else:
                    self.vars_ansible = None
                    self.summary_ansible = False
                    if self.type_task == "restore":
                        self.file_user_get_data = os.path.join(self.report_casepath, "user_get_data_destination.json")
                        if os.path.exists(self.file_user_get_data):
                            try:
                                with closing(open(self.file_user_get_data)) as self.open_user_get_data:
                                    self.result_user_get_data = json.load(self.open_user_get_data)
                                    if int(self.result_user_get_data['metadata']['result']) == 1:
                                        self.home = self.result_user_get_data['data']['userdata']['homedir']
                                        if self.home is not None and self.home is not False:
                                            self.module_database.update_analyzing("home_destination", self.home, self.thread_id)
                                            self.module_database.update_analyzing("cpanel_" + self.type_task, 3, self.thread_id)
                                            self._log.debug("Ansible cpanel completed - {} - {}".format(self.type_task, self.values_ticket))
                                            if self.message_manager():
                                                self._log.info("Send manager {}".format(self.message))
                                            else:
                                                self._log.info("Failed send manager {}".format(self.message))
                                        else:
                                            self._log.error("Failed get home in user_get_data.json - {}".format(self.values_ticket))
                                            self.module_database.update_analyzing("cpanel_" + self.type_task, 2, self.thread_id)

                            except Exception as er:
                                self.general_error = True
                                self._log.error("Failed cpanel restore user_get_data.json - {}".format(self.values_ticket, er))
                                self.module_database.update_analyzing("cpanel_" + self.type_task, 2, self.thread_id)
                                return False
                        else:
                            self.general_error = True
                            self._log.error("user_get_data.json not found - {}".format(self.values_ticket))
                            self.module_database.update_analyzing("cpanel_" + self.type_task, 2, self.thread_id)
                            return False
                    else:
                        # set completed with success in cpanel type
                        self.module_database.update_analyzing("cpanel_" + self.type_task, 3, self.thread_id)
                        # debug log
                        self._log.debug("Ansible cpanel completed - {} - {}".format(self.type_task, self.values_ticket))
                        if self.message_manager():
                            self._log.info("Send manager {}".format(self.message))
                        else:
                            self._log.info("Failed send manager {}".format(self.message))
                return True
            else:
                # critical log
                self._log.critical("Error - generalError {} - values {}".format(self.general_error, self.values_ticket))
                return False

        except Exception as er:
            # generate a error log
            self._log.error("process cpanel - {} - {}".format(self.__class__.__name__, er))
            return False

    def message_manager(self):
        try:
            self.message = dict()
            self.message.update({'sender': 'cpanel'})
            self.message.update({'id': self.ticket_id})
            self.message.update({'thread_id': self.thread_id})
            self.message.update({'available_user': os.path.exists(self.file_available_user)})
            self.queue_manager.publish(self.message)
            return True

        except Exception as er:
            # generate a error log
            self._log.error("message check - {} - {}".format(self.__class__.__name__, er))
            return False
