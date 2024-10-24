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
import time


class ModuleRsync:

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
            self.playbook_rsync = self.module_configuration.playbook_rsync
            # get values collected
            self.retry = None
            self.server = None
            self.values_ticket = None
            self.src_server = None
            self.dst_server = None
            self.src_type = None
            self.dst_type = None
            self.main_domain = None
            self.ticket_id = None
            self.user = None
            self.home = None
            self.thread_id = None
            self.values_database = None
            self.report_dir = self.module_configuration.report_dir
            self.summary_ansible = None
            self.module_ansible = None
            self.vars_ansible = None
            self.home_destination = None
            self.message = None
            self.report_casepath = None
            self.src_server_delegate = None
            self.file_available_user = None
            self.file_flag_rsync_error = None
            self.src_ip = None
            self.dst_ip = None
            self.connect_ip = None
            self.file_flag_rsync_reseller_error = None
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
            self.src_server_delegate = None
            self.main_domain = None
            self.user = None
            self.ticket_id = None
            self.home = None
            self.thread_id = None
            self.home_destination = None
            self.values_database = None
            self.report_casepath = None
            self.file_available_user = None
            self.file_flag_rsync_error = None
            self.file_flag_rsync_reseller_error = None
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
            self.retry = 0
            # get values in database
            if self.ticket_id is not None and self.ticket_id is not False and \
                    self.thread_id is not None and self.thread_id is not False:
                self.values_database = self.module_database.get_values(self.ticket_id, self.thread_id, "rsync")
                if self.values_database is not False and self.values_database is not None and len(self.values_database) == 11:
                    self.src_server = self.values_database[0]
                    self.dst_server = self.values_database[1]
                    self.src_type = self.values_database[2]
                    self.dst_type = self.values_database[3]
                    self.main_domain = self.values_database[4]
                    self.home = self.values_database[5]
                    self.home_destination = self.values_database[6]
                    self.user = self.values_database[7]
                    self.src_ip = self.values_database[8]
                    self.dst_ip = self.values_database[9]
                    self.connect_ip = self.values_database[10]
                    self.report_casepath = os.path.join(self.report_dir, str(self.main_domain) + "_" + str(self.ticket_id) + "_" + str(self.thread_id))
                    self.file_flag_rsync_error = os.path.join(self.report_casepath, "rsync_error.flag")
                    self.file_flag_rsync_reseller_error = os.path.join(self.report_casepath, "rsync_reseller_error.flag")
                    self.file_available_user = os.path.join(self.report_casepath, "destination/user_available.flag")
                    # instance ansible module to all servers
                    self.module_ansible = ModuleAnsible(module_log=self._log, module_configuration=self.module_configuration)
                    if self.connect_ip == 1 and self.dst_ip is not None:
                        self.server = self.dst_ip
                    else:
                        self.server = self.dst_server
                    if self.connect_ip and self.src_ip is not None:
                        self.src_server_delegate = self.src_ip
                    else:
                        self.src_server_delegate = self.src_server
                    self.vars_ansible = {
                        "domain": self.main_domain,
                        "ticketID": self.ticket_id,
                        "threadID": self.thread_id,
                        "home_destination": self.home_destination,
                        "home": self.home,
                        "src_type": self.src_type,
                        "dst_type": self.dst_type,
                        "user": self.user,
                        "src_server": self.src_server_delegate,
                        "dst_server": self.server,
                    }
                    return True
                else:
                    self.general_error = True
                    self._log.error("Failed rsync get values in database - {}".format(self.values_ticket))
                    return False
            else:
                self.general_error = True
                self._log.error("Failed rsync get values in message - {}".format(self.values_ticket))
                return False

        except Exception as er:
            # generate a error log
            self._log.error("initialize rsync - {} - {}".format(self.__class__.__name__, er))
            self.general_error = True
            return False

    def process(self):
        try:
            if self.general_error is False:
                if os.path.exists(self.file_flag_rsync_error):
                    os.remove(self.file_flag_rsync_error)
                if os.path.exists(self.file_flag_rsync_reseller_error):
                    os.remove(self.file_flag_rsync_reseller_error)
                # mark start ansible rsync, 1 - start, 2 - failed, 3 - completed
                self.module_database.update_analyzing("rsync", 1, self.thread_id)
                # debug log
                self._log.debug(self.vars_ansible)
                # execute playbook and get summary result
                self.summary_ansible = self.module_ansible.execute(self.playbook_rsync, self.vars_ansible, self.server)
                if self.summary_ansible is False or self.summary_ansible is None or \
                        os.path.exists(self.file_flag_rsync_error) or os.path.exists(self.file_flag_rsync_reseller_error) or self.summary_ansible['rescued'] > 0:
                    if self.retry <= 3:
                        self.retry += 1
                        self._log.info("Retry rsync - {} - {}".format(self.retry, self.vars_ansible))
                        time.sleep(120)
                        self.process()
                    else:
                        # update rsync type with failed
                        self.module_database.update_analyzing("rsync", 2, self.thread_id)
                        self.vars_ansible = None
                        self.summary_ansible = False
                        # error log
                        self._log.error("Ansible rsync failed - {}".format(self.values_ticket))
                        if self.message_manager():
                            self._log.info("Send manager {}".format(self.message))
                        else:
                            self._log.info("Failed send manager {}".format(self.message))
                else:
                    # set completed with success in rsync type
                    self.module_database.update_analyzing("rsync", 3, self.thread_id)
                    self.vars_ansible = None
                    self.summary_ansible = False
                    # debug log
                    self._log.debug("Ansible rsync completed - {}".format(self.values_ticket))
                    if self.message_manager():
                        self._log.info("Send manager {}".format(self.message))
                    else:
                        self._log.info("Failed send manager {}".format(self.message))
                return True
            else:
                # critical log
                self._log.critical("Error rsync - generalError {} - values {}".format(self.general_error, self.values_ticket))
                return False

        except Exception as er:
            # generate a error log
            self._log.error("process rsync - {} - {}".format(self.__class__.__name__, er))
            return False

    def message_manager(self):
        try:
            self.message = dict()
            self.message.update({'sender': 'rsync'})
            self.message.update({'id': self.ticket_id})
            self.message.update({'thread_id': self.thread_id})
            self.queue_manager.publish(self.message)
            return True

        except Exception as er:
            # generate a error log
            self._log.error("message check - {} - {}".format(self.__class__.__name__, er))
            return False
