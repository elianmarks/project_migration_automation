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
import re


class ModuleRegex:

    def __init__(self, module_log, module_configuration):
        self.module_configuration = module_configuration
        self._log = module_log
        # regex variables
        self.regex_domain = "Domínio: .*"
        self.regex_src = "Servidor (atual|actual): .*"
        self.regex_dst = "Servidor destino: .*"
        if self.module_configuration.production:
            self.regex_shared = "(br|bz|mx|shared)[0-9]{1,4}\.example\.(com\.br|com\.mx|mx|com\.cl|cl|com\.co|co)"
            self.regex_reseller = "((srv|server)\.example02\.com\.br)|((srv|reseller)[0-9]{1,4}\.example02\.(com\.br|com\.mx|mx|com\.cl|cl|com\.co|co))"
        else:
            self.regex_shared = "(brdev|br|bz|mx|shared)[0-9]{1,4}\.example\.(com\.br|com\.mx|mx|com\.cl|cl|com\.co|co)"
            self.regex_reseller = "((srv|server)\.example02\.com\.br)|((srvdev|srv|reseller)[0-9]{1,4}\.example02\.(com\.br|com\.mx|mx|com\.cl|cl|com\.co|co))"
        self.regex = "server[0-9]{1,4}\.example\.(com\.br|com\.mx|mx|com\.cl|cl|com\.co|co)"
        self.regex_wp = "wp[0-9]{1,4}\.example\.com\.br"
        self.regex_vps = "(vps-[0-9]+|vps)\..*"
        self.regex_dedi = "(server[0-9]{1,2}|dedi-[0-9]+)\..*"
        self.regex_company = "(example|example02)\.(com\.br|com\.mx|mx|com\.cl|cl|com\.co|co)"
        # requests type
        self.request_regex = "para servidor"
        self.request_regex_monitoring = "para novo servidor"
        self.request_regex_shared = "conta compartilhada"
        self.request_regex_vps_dedi = "servidor dedicado e vps"
        self.request_regex_reseller = "de revenda"
        # variables
        self.description = None
        self.src_server = None
        self.dst_server = None
        self.main_domain = None
        self.list_data = None
        self.value_type = None
        self.value_ns = None

    def get_data(self, description):
        try:
            self.description = description
            self.list_data = list()
            self.src_server = re.search(self.regex_src, self.description, flags=re.IGNORECASE)
            self.dst_server = re.search(self.regex_dst, self.description, flags=re.IGNORECASE)
            self.main_domain = re.search(self.regex_domain, self.description, flags=re.IGNORECASE)
            if self.src_server is not None and self.dst_server is not None and self.main_domain is not None:
                self.list_data.append(str(self.main_domain.group()).split(":")[1].replace(" ", ""))
                self.list_data.append(str(self.src_server.group()).split(":")[1].replace(" ", ""))
                self.list_data.append(str(self.dst_server.group()).split(":")[1].replace(" ", ""))
                return self.list_data
            else:
                return False

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def check_ns(self, value_ns):
        try:
            self.value_ns = value_ns
            # check if match
            if re.search(self.regex_company, self.value_ns, flags=re.IGNORECASE):
                return True
            else:
                return False

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def check_type(self, value_type):
        try:
            self.value_type = value_type
            if re.search(self.regex_shared, self.value_type, flags=re.IGNORECASE) is not None:
                return "shared"
            if re.search(self.regex_reseller, self.value_type, flags=re.IGNORECASE) is not None:
                return "reseller"
            if re.search(self.regex_wp, self.value_type, flags=re.IGNORECASE) is not None:
                return "wp"
            if re.search(self.regex_dedi, self.value_type, flags=re.IGNORECASE) is not None:
                return "dedi"
            if re.search(self.regex_vps, self.value_type, flags=re.IGNORECASE) is not None:
                return "vps"
            if re.search(self.regex, self.value_type, flags=re.IGNORECASE) is not None:
                return "server"
            return False

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def check_request_type(self, value_type):
        try:
            self.value_type = value_type
            if re.search(self.request_regex, self.value_type, flags=re.IGNORECASE) is not None:
                return 1
            if re.search(self.request_regex_monitoring, self.value_type, flags=re.IGNORECASE) is not None:
                return 2
            if re.search(self.request_regex_shared, self.value_type, flags=re.IGNORECASE) is not None:
                return 3
            if re.search(self.request_regex_vps_dedi, self.value_type, flags=re.IGNORECASE) is not None:
                return 4
            if re.search(self.request_regex_reseller, self.value_type, flags=re.IGNORECASE) is not None:
                return 5
            return 0

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False
