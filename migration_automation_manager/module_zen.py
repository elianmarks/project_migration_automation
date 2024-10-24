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
from zenpy import Zenpy
from zenpy.lib.api_objects import Ticket, Comment, User


class ModuleZen:

    def __init__(self, module_log, module_configuration):
        """
        :param module_log: Instance of the log class
        :type module_log: object
        """
        self._log = module_log
        self.module_configuration = module_configuration
        self._domain = self.module_configuration.domain
        self._token = self.module_configuration.token
        self._domain_es = self.module_configuration.domain_es
        self._token_es = self.module_configuration.token_es
        # values in zendesk
        self.tag_search = "migration_automation_not_checked"
        self.tag_search_retry = "migration_automation_retry"
        if self.module_configuration.production:
            self.group_migration = 11111111111
            self.group_migration_es = 11111111111
        else:
            self.group_migration = 11111111111
            self.group_migration_es = 11111111111
        self.status_search = "hold"
        self.tag_error = "migration_automation_error"
        self.tag_ns_not = "migration_automation_ns_not"
        self.tag_handled = "migration_automation_handled"
        self.tag_completed = "migration_automation_completed"
        self.tag_force_ns = "migration_automation_force_ns"
        self._email = "apizendesk@example.com"
        self._credentials = None
        self.update_object = None
        self.ticket_id = None
        self.type_macro = None
        self.body = None
        self.public = None
        self.macro_id = None
        self.current_tags = None
        self.add_tag = None
        self.remove_tag = None
        self.brand = None
        # if self.module_configuration.production:
        #    self.macro_finish_shared_id = 11111111111
        #    self.macro_finish_reseller_id = 11111111111
        #    self.macro_start_id = 11111111111
        # else:
        #    self.macro_finish_shared_id = 11111111111
        #    self.macro_start_id = 11111111111
        self.comment_value = None
        self.comment_id = None
        self.mysql_version_src = None
        self.mysql_version_dst = None

    @property
    def connect_zen(self):
        """
        Return object with connection of the zendesk
        """
        try:
            if self.brand == "br":
                self._credentials = {
                    "email": self._email,
                    "token": self._token,
                    "subdomain": self._domain
                }
                return Zenpy(**self._credentials)
            elif self.brand == "es":
                self._credentials = {
                    "email": self._email,
                    "token": self._token_es,
                    "subdomain": self._domain_es
                }
                return Zenpy(**self._credentials)
            else:
                return False

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def get_group_id(self, brand="br"):
        try:
            self.brand = brand
            if self.brand == "es":
                return self.group_migration_es
            else:
                return self.group_migration

        except Exception as er:
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def search_migration(self, brand="br"):
        try:
            self.brand = brand
            return self.connect_zen.search(type="ticket", status=self.status_search, tags=self.tag_search, group_id=self.get_group_id(brand=self.brand))

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def search_migration_retry(self, brand="br"):
        try:
            self.brand = brand
            return self.connect_zen.search(type="ticket", status=self.status_search, tags=self.tag_search_retry, group_id=self.get_group_id(brand=self.brand))

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def search_id(self, ticket_id, brand="br"):
        """
        Search for ID of the ticket
        """
        try:
            self.brand = brand
            self.ticket_id = ticket_id
            return self.connect_zen.tickets(id=self.ticket_id)

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def handle_tag(self, current_tags, add_tag, remove_tag=None):
        try:
            self.current_tags = current_tags
            self.remove_tag = remove_tag
            self.add_tag = add_tag
            if isinstance(self.current_tags, list) and len(self.current_tags) > 0 and self.remove_tag is not None:
                if self.remove_tag in self.current_tags:
                    self.current_tags.remove(self.remove_tag)
            if isinstance(self.current_tags, list):
                self.current_tags.append(self.add_tag)
            else:
                self.current_tags = self.add_tag
            return self.current_tags

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def comment_mysql_version(self, mysql_version_src, mysql_version_dst):
        try:
            self.mysql_version_src = mysql_version_src
            self.mysql_version_dst = mysql_version_dst
            return "Mysql source server: {}\n\nMysql destination server: {}\n\nRequire checking databases.".format(self.mysql_version_src, self.mysql_version_dst)

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def comment_error(self, comment_value, comment_id):
        try:
            self.comment_value = comment_value
            self.comment_id = comment_id
            return "Error in migration, require checking.\n\nMessage - {}\n\nID - {}".format(self.comment_value, self.comment_id)

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def macro(self, ticket_id, macro_id, brand="br"):
        try:
            self.brand = brand
            self.macro_id = macro_id
            self.ticket_id = ticket_id
            return self.connect_zen.tickets.show_macro_effect(self.ticket_id, self.macro_id)

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def comment_ticket(self, ticket_id, body, public=True, brand="br"):
        try:
            self.brand = brand
            self.ticket_id = ticket_id
            self.body = body
            self.public = public
            self.update_object = self.search_id(self.ticket_id, brand=self.brand)
            if self.update_object is not False:
                self.update_object.comment = Comment(body=self.body, public=self.public)
                self.update_ticket(self.update_object, brand=self.brand)
                return True
            else:
                return False

        except Exception as er:
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def update_ticket(self, update_object, type_macro=None, brand="br"):
        """
        Update a ticket
        """
        try:
            self.brand = brand
            self.type_macro = type_macro
            if self.type_macro:
                self.update_object = update_object.ticket
            else:
                self.update_object = update_object
            return self.connect_zen.tickets.update(self.update_object)

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False
