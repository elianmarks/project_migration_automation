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


class ModuleCheckEnd:

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
            self.playbook_check = self.module_configuration.playbook_check
            # get values collected
            self.server = None
            self.values_ticket = None
            self.src_server = None
            self.dst_server = None
            self.src_type = None
            self.dst_type = None
            self.main_domain = None
            self.ticket_id = None
            self.thread_id = None
            self.type_task = None
            self.values_database = None
            self.report_dir = self.module_configuration.report_dir
            self.summary_ansible = None
            self.module_ansible = None
            self.vars_ansible = None
            self.message = None
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
            self.type_task = None
            self.main_domain = None
            self.ticket_id = None
            self.thread_id = None
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
            self.type_task = "destination_end"
            # get values in database
            if self.ticket_id is not None and self.ticket_id is not False and \
                    self.type_task is not None and self.type_task is not False and \
                    self.thread_id is not None and self.thread_id is not False:
                self.values_database = self.module_database.get_values(self.ticket_id, self.thread_id, "check")
                if self.values_database is not False and self.values_database is not None and len(self.values_database) == 8:
                    self.src_server = self.values_database[0]
                    self.dst_server = self.values_database[1]
                    self.src_type = self.values_database[2]
                    self.dst_type = self.values_database[3]
                    self.main_domain = self.values_database[4]
                    self.src_ip = self.values_database[5]
                    self.dst_ip = self.values_database[6]
                    self.connect_ip = self.values_database[7]
                    # instance ansible module to all servers
                    self.module_ansible = ModuleAnsible(module_log=self._log, module_configuration=self.module_configuration)
                    self.vars_ansible = {
                        "domain": self.main_domain,
                        "ticketID": self.ticket_id,
                        "threadID": self.thread_id,
                        "type": self.type_task,
                        "src_type": self.src_type,
                        "dst_type": self.dst_type,
                    }
                    if self.connect_ip == 1 and self.dst_ip is not None:
                        self.server = self.dst_ip
                    else:
                        self.server = self.dst_server
                    return True
                else:
                    self.general_error = True
                    self._log.error("Failed check end get values in database - {}".format(self.values_ticket))
                    return False
            else:
                self.general_error = True
                self._log.error("Failed check end get values in message - {}".format(self.values_ticket))
                return False

        except Exception as er:
            # generate a error log
            self._log.error("initialize check end - {} - {}".format(self.__class__.__name__, er))
            self.general_error = True
            return False

    def process(self):
        try:
            if self.general_error is False:
                # mark start ansible rsync, 1 - start, 2 - failed, 3 - completed
                self.module_database.update_analyzing("check_" + self.type_task, 1, self.thread_id)
                # debug log
                self._log.debug(self.vars_ansible)
                # execute playbook and get summary result
                self.summary_ansible = self.module_ansible.execute(self.playbook_check, self.vars_ansible, self.server)
                # check end if execution completed with success
                if self.summary_ansible is False or self.summary_ansible is None:
                    # update check end type with failed
                    self.module_database.update_analyzing("check_" + self.type_task, 2, self.thread_id)
                    self.vars_ansible = None
                    self.summary_ansible = False
                    # error log
                    self._log.error("Ansible check end failed - {} - {}".format(self.type_task, self.values_ticket))
                    if self.message_manager():
                        self._log.info("Send manager {}".format(self.message))
                    else:
                        self._log.info("Failed send manager {}".format(self.message))
                else:
                    # set completed with success in check end type
                    self.module_database.update_analyzing("check_" + self.type_task, 3, self.thread_id)
                    self.vars_ansible = None
                    self.summary_ansible = False
                    # debug log
                    self._log.debug("Ansible check end completed - {} - {}".format(self.type_task, self.values_ticket))
                    if self.message_manager():
                        self._log.info("Send manager {}".format(self.message))
                    else:
                        self._log.info("Failed send manager {}".format(self.message))
            else:
                # critical log
                self._log.critical("Error check end - generalError {} - values {}".format(self.general_error, self.values_ticket))
                return False

        except Exception as er:
            # generate a error log
            self._log.error("process check end - {} - {}".format(self.__class__.__name__, er))
            return False

    def message_manager(self):
        try:
            self.message = dict()
            self.message.update({'sender': 'check_end'})
            self.message.update({'id': self.ticket_id})
            self.message.update({'thread_id': self.thread_id})
            self.queue_manager.publish(self.message)
            return True

        except Exception as er:
            # generate a error log
            self._log.error("message check end - {} - {}".format(self.__class__.__name__, er))
            return False
