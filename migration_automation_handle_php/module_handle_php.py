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


class ModuleHandlePHP:

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
            self.playbook_php = self.module_configuration.playbook_php
            # get values collected
            self.server = None
            self.values_ticket = None
            self.dst_server = None
            self.dst_type = None
            self.main_domain = None
            self.set_domain = None
            self.ticket_id = None
            self.thread_id = None
            self.type_task = None
            self.set_version_php = None
            self.set_value_php = None
            self.set_variable_php = None
            self.values_database = None
            self.report_dir = self.module_configuration.report_dir
            self.summary_ansible = None
            self.module_ansible = None
            self.vars_ansible = None
            self.user_destination = None
            self.src_ip = None
            self.dst_ip = None
            self.connect_ip = None

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            self.general_error = True

    def initialize(self, values_ticket):
        try:
            # get values collected
            self.server = None
            self.user_destination = None
            self.values_ticket = None
            self.dst_server = None
            self.dst_type = None
            self.set_domain = None
            self.main_domain = None
            self.ticket_id = None
            self.thread_id = None
            self.type_task = None
            self.set_version_php = None
            self.set_value_php = None
            self.set_variable_php = None
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
            self.set_domain = self.values_ticket.get('set_domain')
            if self.type_task is not False and self.type_task is not None and self.type_task == "phpversion":
                self.set_version_php = self.values_ticket.get('set_version_php')
            elif self.type_task == "phpini":
                self.set_variable_php = self.values_ticket.get('set_variable_php')
                self.set_value_php = self.values_ticket.get('set_value_php')
            else:
                self._log.error("Invalid type handle php - {}".format(self.values_ticket))
                self.general_error = True
                return False
            # get values in database
            if self.ticket_id is not None and self.ticket_id is not False and \
                    self.thread_id is not None and self.thread_id is not False and \
                    ((self.set_version_php is not False and self.set_version_php is not None) or
                     (self.set_value_php is not False and self.set_value_php is not None and
                     self.set_variable_php is not False and self.set_variable_php is not None)):
                self.values_database = self.module_database.get_values(self.ticket_id, self.thread_id, "handle_php")
                if self.values_database is not False and self.values_database is not None and len(self.values_database) == 9:
                    self.dst_server = self.values_database[1]
                    self.dst_type = self.values_database[3]
                    self.main_domain = self.values_database[4]
                    self.user_destination = self.values_database[5]
                    self.src_ip = self.values_database[6]
                    self.dst_ip = self.values_database[7]
                    self.connect_ip = self.values_database[8]
                    if self.type_task == "phpversion":
                        self.module_ansible = ModuleAnsible(module_log=self._log, module_configuration=self.module_configuration)
                        self.vars_ansible = {
                            "domain": self.set_domain,
                            "ticketID": self.ticket_id,
                            "threadID": self.thread_id,
                            "type": self.type_task,
                            "user": self.user_destination,
                            "version_php": self.set_version_php,
                        }
                        if self.connect_ip == 1 and self.dst_ip is not None:
                            self.server = self.dst_ip
                        else:
                            self.server = self.dst_server
                        return True
                    elif self.type_task == "phpini":
                        self.module_ansible = ModuleAnsible(module_log=self._log, module_configuration=self.module_configuration)
                        self.vars_ansible = {
                            "domain": self.set_domain,
                            "ticketID": self.ticket_id,
                            "threadID": self.thread_id,
                            "type": self.type_task,
                            "user": self.user_destination,
                            "value_php": self.set_value_php,
                            "variable_php": self.set_variable_php,
                        }
                        if self.connect_ip == 1 and self.dst_ip is not None:
                            self.server = self.dst_ip
                        else:
                            self.server = self.dst_server
                        return True
                    else:
                        self.general_error = True
                        self._log.error("Invalid type handle php - {}".format(self.values_ticket))
                        return False
                else:
                    self.general_error = True
                    self._log.error("Failed handle php get values in database - {}".format(self.values_ticket))
                    return False
            else:
                self.general_error = True
                self._log.error("Failed handle php get values in message - {}".format(self.values_ticket))
                return False

        except Exception as er:
            # generate a error log
            self._log.error("initialize handle php - {} - {}".format(self.__class__.__name__, er))
            self.general_error = True
            return False

    def process(self):
        try:
            if self.general_error is False:
                # debug log
                self._log.debug(self.vars_ansible)
                # execute playbook and get summary result
                self.summary_ansible = self.module_ansible.execute(self.playbook_php, self.vars_ansible, self.server)
                # check if execution completed with success
                if self.summary_ansible is False or self.summary_ansible is None:
                    # update check type with failed
                    self.vars_ansible = None
                    self.summary_ansible = False
                    # error log
                    self._log.error("Ansible handle php failed - {} - {}".format(self.type_task, self.values_ticket))
                else:
                    self.vars_ansible = None
                    self.summary_ansible = False
                    # debug log
                    self._log.debug("Ansible handle php completed - {} - {}".format(self.type_task, self.values_ticket))
            else:
                # critical log
                self._log.critical("Error handle php - generalError {} - values {}".format(self.general_error, self.values_ticket))
                return False

        except Exception as er:
            # generate a error log
            self._log.error("process handle php - {} - {}".format(self.__class__.__name__, er))
            return False
