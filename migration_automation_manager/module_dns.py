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
import dns.resolver
import ipaddress


class ModuleDNS:

    def __init__(self, module_log, module_configuration):
        self.module_configuration = module_configuration
        self._log = module_log
        # instance Resolver class
        self._dns_resolver = dns.resolver.Resolver()
        # set timeout and lifetime for query
        self._dns_resolver.timeout = 5
        self._dns_resolver.lifetime = 5
        self.domain_value = None
        self.type_record = None
        self.ip_resolver = None
        self.ip_value = None
        self.result_query = None

    def check_ip(self, ip_value):
        """
        Check if a string is a valid IP.
        :param ip_value: value of a IP address
        :type ip_value: string
        :return: IPAdress object with value of the string received on success,
            None on string not is a IP valid, False on failure
        :rtype: object or bool
        """
        try:
            self.ip_value = ip_value
            return ipaddress.ip_address(self.ip_value)

        except ValueError as er:
            # generate a error log
            self._log.debug("{} - {}".format(self.__class__.__name__, er))
            return None

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def dns_resolver(self, domain_value, type_record="A"):
        """
        Execute a resolution of a DNS, any record in query.
        :param domain_value: Value of the a domain valid
        :param domain_value: string
        :param type_record: Value of the record for query DNS, default value is A
        :type type_record: string
        :return: DNS object on success, False on failure
        :rtype: object or bool
        """
        try:
            # check if domain_value is IPv4Address object
            if isinstance(domain_value, ipaddress.IPv4Address):
                self.domain_value = domain_value
            else:
                self.domain_value = str(domain_value)
            # transform record to upper
            self.type_record = type_record.upper()
            # check record type
            if self.type_record == "PTR":
                # execute query
                self.ip_resolver = self.check_ip(self.domain_value)
                if self.ip_resolver is not False and self.ip_resolver is not None:
                    self.result_query = self._dns_resolver.query(self.ip_resolver._reverse_pointer(), self.type_record)
                    return str(self.result_query[0])
                else:
                    return False
            else:
                # execute query
                self.result_query = self._dns_resolver.query(self.domain_value, self.type_record)

            if self.type_record == "MX":
                # format result if type record is MX and return
                return self.result_query[0].exchange.to_text()
            else:
                return self.result_query[0].to_text()

        except dns.exception.DNSException as er:
            # generate a debug log
            self._log.debug("{} - {}".format(self.__class__.__name__, er))
            return False

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False
