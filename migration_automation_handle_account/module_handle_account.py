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
import datetime
import uuid
import os
from contextlib import closing


class ModuleHandleAccount:

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
            self.playbook_account = self.module_configuration.playbook_account
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
            self.message = None
            self.thread_id = None
            self.type_task = None
            self.values_database = None
            self.check_source = None
            self.check_destination = None
            self.cpanel_pkgacct = None
            self.cpanel_restore = None
            self.mysql_restore = None
            self.mysql_dump = None
            self.rsync = None
            self.all_users = None
            self.handle_dns_date = None
            self.home = None
            self.handled = None
            self.status = None
            self.today = None
            self.check_destination_end = None
            self.compare = None
            self.handle_dns_source = None
            self.handle_dns_destination_end = None
            self.difference_suspended = None
            self.rsync_last = None
            self.suspend = None
            self.remove = None
            self.suspend_date = None
            self.remove_date = None
            self.request_type = None
            self.report_dir = self.module_configuration.report_dir
            self.summary_ansible = None
            self.module_ansible = None
            self.vars_ansible = None
            self.report_casepath = None
            self.check_uuid_suspend = None
            self.check_uuid_remove = None
            self.save_remove_uuid = None
            self.open_check_uuid = None
            self.file_check_uuid = None
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
            self.report_casepath = None
            self.src_server = None
            self.dst_server = None
            self.src_type = None
            self.dst_type = None
            self.main_domain = None
            self.ticket_id = None
            self.check_source = None
            self.open_check_uuid = None
            self.file_check_uuid = None
            self.today = None
            self.check_destination = None
            self.cpanel_pkgacct = None
            self.cpanel_restore = None
            self.mysql_restore = None
            self.difference_suspended = None
            self.mysql_dump = None
            self.rsync = None
            self.all_users = None
            self.check_uuid_suspend = None
            self.check_uuid_remove = None
            self.save_remove_uuid = None
            self.home = None
            self.handled = None
            self.status = None
            self.handle_dns_date = None
            self.check_destination_end = None
            self.compare = None
            self.handle_dns_source = None
            self.handle_dns_destination_end = None
            self.rsync_last = None
            self.suspend = None
            self.remove = None
            self.suspend_date = None
            self.remove_date = None
            self.user = None
            self.thread_id = None
            self.type_task = None
            self.request_type = None
            self.values_database = None
            self.module_ansible = None
            self.vars_ansible = None
            self.src_ip = None
            self.dst_ip = None
            self.connect_ip = None
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
                self.values_database = self.module_database.get_values(self.ticket_id, self.thread_id, "handle_account")
                if self.values_database is not False and self.values_database is not None and len(self.values_database) == 29:
                    self.src_server = self.values_database[0]
                    self.dst_server = self.values_database[1]
                    self.src_type = self.values_database[2]
                    self.dst_type = self.values_database[3]
                    self.main_domain = self.values_database[4]
                    self.user = self.values_database[5]
                    self.check_source = int(self.values_database[6])
                    self.check_destination = int(self.values_database[7])
                    self.cpanel_pkgacct = int(self.values_database[8])
                    self.cpanel_restore = int(self.values_database[9])
                    self.request_type = int(self.values_database[10])
                    self.handle_dns_date = self.values_database[11]
                    self.rsync = int(self.values_database[12])
                    self.all_users = int(self.values_database[13])
                    self.home = self.values_database[14]
                    self.handled = int(self.values_database[15])
                    self.status = int(self.values_database[16])
                    self.check_destination_end = int(self.values_database[17])
                    self.compare = int(self.values_database[18])
                    self.handle_dns_source = int(self.values_database[19])
                    self.handle_dns_destination_end = int(self.values_database[20])
                    self.rsync_last = int(self.values_database[21])
                    self.suspend = int(self.values_database[22])
                    self.remove = int(self.values_database[23])
                    self.suspend_date = self.values_database[24]
                    self.remove_date = self.values_database[25]
                    self.src_ip = self.values_database[26]
                    self.dst_ip = self.values_database[27]
                    self.connect_ip = self.values_database[28]
                    self.today = datetime.datetime.now()
                    if self.suspend_date is not None:
                        self.difference_suspended = (self.today - self.suspend_date).days
                    self.report_casepath = os.path.join(self.report_dir, str(self.main_domain) + "_" + str(self.ticket_id) + "_" + str(self.thread_id))
                    # instance ansible module to all servers
                    self.module_ansible = ModuleAnsible(module_log=self._log, module_configuration=self.module_configuration)
                    if self.type_task == "suspend" and self.suspend == 0 and self.status == 3:
                        self.save_remove_uuid = str(uuid.uuid4())
                        self.check_uuid_suspend = self.get_check_uuid()
                        if self.check_uuid_suspend is not None and self.check_uuid_suspend is not False:
                            # set ansible variables
                            self.vars_ansible = {
                                "user": self.user,
                                "type": self.type_task,
                                "src_type": self.src_type,
                                "domain": self.main_domain,
                                "threadID": self.thread_id,
                                "ticketID": self.ticket_id,
                                "checkUUID": self.check_uuid_suspend,
                                "saveRemoveUUID": self.save_remove_uuid,
                            }
                            if self.connect_ip == 1 and self.src_ip is not None:
                                self.server = self.src_ip
                            else:
                                self.server = self.src_server
                            return True
                        else:
                            self.general_error = True
                            self._log.error("Invalid src type or uuid handle account - {}".format(self.values_ticket))
                            return False
                    elif self.type_task == "remove" and self.suspend == 3 and self.remove == 0 and self.status == 3:
                        if self.difference_suspended >= 15:
                            self.check_uuid_remove = self.get_check_uuid()
                            if self.check_uuid_remove is not None and self.check_uuid_remove is not False:
                                # set ansible variables
                                self.vars_ansible = {
                                    "user": self.user,
                                    "type": self.type_task,
                                    "src_type": self.src_type,
                                    "domain": self.main_domain,
                                    "threadID": self.thread_id,
                                    "ticketID": self.ticket_id,
                                    "checkUUID": self.check_uuid_remove,
                                }
                                if self.connect_ip == 1 and self.src_ip is not None:
                                    self.server = self.src_ip
                                else:
                                    self.server = self.src_server
                                return True
                            else:
                                self.general_error = True
                                self._log.error("Invalid src type or uuid handle account - {}".format(self.values_ticket))
                                return False
                        else:
                            self._log.info("Invalid difference date between suspended and now for removed")
                            return False
                    else:
                        self.general_error = True
                        self._log.error("Invalid type or status in handle account - {}".format(self.values_ticket))
                        return False
                else:
                    self.general_error = True
                    self._log.error("Failed handle account get values in database - {}".format(self.values_ticket))
                    return False
            else:
                self.general_error = True
                self._log.error("Failed handle account get values in message - {}".format(self.values_ticket))
                return False

        except Exception as er:
            # generate a error log
            self._log.error("initialize handle account - {} - {}".format(self.__class__.__name__, er))
            self.general_error = True
            return False

    def process(self):
        try:
            if self.general_error is False:
                # mark start ansible handle account, 1 - start, 2 - failed, 3 - completed
                self.module_database.update_analyzing(self.type_task, 1, self.thread_id)
                # debug log
                self._log.debug(self.vars_ansible)
                # execute playbook and get summary result
                self.summary_ansible = self.module_ansible.execute(self.playbook_account, self.vars_ansible, self.server)
                # check if execution completed with success
                if self.summary_ansible is False or self.summary_ansible is None:
                    # update cpanel type with failed
                    self.module_database.update_analyzing(self.type_task, 2, self.thread_id)
                    self.vars_ansible = None
                    self.summary_ansible = False
                    # update date
                    self.module_database.update_analyzing(self.type_task + "_date", datetime.datetime.now(), self.thread_id)
                    # error log
                    self._log.error("Ansible handle account failed - {} - {}".format(self.type_task, self.values_ticket))
                    if self.message_manager():
                        self._log.info("Send manager {}".format(self.message))
                    else:
                        self._log.info("Failed send manager {}".format(self.message))
                else:
                    # set completed with success in handle account
                    self.module_database.update_analyzing(self.type_task, 3, self.thread_id)
                    self.vars_ansible = None
                    self.summary_ansible = False
                    # update date
                    self.module_database.update_analyzing(self.type_task + "_date", datetime.datetime.now(), self.thread_id)
                    # debug log
                    self._log.debug("Ansible handle account completed - {} - {}".format(self.type_task, self.values_ticket))
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
            self._log.error("process handle dns - {} - {}".format(self.__class__.__name__, er))
            return False

    def message_manager(self):
        try:
            self.message = dict()
            self.message.update({'sender': 'handle_account'})
            self.message.update({'id': self.ticket_id})
            self.message.update({'thread_id': self.thread_id})
            self.message.update({'type_task': self.type_task})
            self.queue_manager.publish(self.message)
            return True

        except Exception as er:
            # generate a error log
            self._log.error("message handle account - {} - {}".format(self.__class__.__name__, er))
            return False

    def get_check_uuid(self):
        try:
            self.file_check_uuid = os.path.join(self.report_casepath, "source", self.type_task + "_uuid")
            # check if file exists
            if os.path.exists(self.file_check_uuid):
                # open file and store in variable
                with closing(open(self.file_check_uuid)) as self.open_check_uuid:
                    return self.open_check_uuid.read().replace("\n", "")
            else:
                return False

        except Exception as er:
            # generate a error log
            self._log.error("get check uuid failed - {} - {}".format(self.__class__.__name__, er))
            return False
