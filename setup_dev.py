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
from setuptools import setup


setup(
    name="Migration Automation",
    version="1.0b",
    packages=["migration_automation_zencheck"],
    include_package_data=True,
    entry_points={ "console_scripts": ["migration_automation_zencheck = migration_automation_zencheck.migration_zencheck_dev:main"]},
    install_requires=['configparser==3.7.1', 'mysql-connector-python==8.0.17', 'pika==1.1.0', 'ansible==2.8.3', 'zenpy==2.0.8', 'sgqlc==7.0', 'dnspython==2.0.0'],
    data_files=[('/opt/migration', []), ('/opt/migration/logs', []), ('/home/migration/reports', []), ('/opt/migration/files', []),
                ('/opt/migration/bin', ['migration_automation_zencheck/migration_zencheck_dev.py']), ('/opt/migration/logs/zencheck', [])],
    platforms="linux",
    zip_safe=False,
    author="Elliann Marks",
    author_email="elian.markes@gmail.com",
    description="Migration Automation Zencheck",
    license="BSD",
    keywords="migration, automation, zencheck",
    url="https://git.example.com.br/elsilva/migration_automation",
)

setup(
    name="Migration Automation Compare",
    version="1.0b",
    packages=["migration_automation_compare"],
    include_package_data=True,
    entry_points={"console_scripts": ["migration_automation_compare = migration_automation_compare.migration_compare_dev:main"]},
    data_files=[('/opt/migration/bin', ['migration_automation_compare/migration_compare_dev.py']), ('/opt/migration/logs/compare', [])],
    platforms="linux",
    zip_safe=False,
    author="Elliann Marks",
    author_email="elian.markes@gmail.com",
    description="Migration Automation Compare",
    license="BSD",
    keywords="migration, automation, compare",
    url="https://git.example.com.br/elsilva/migration_automation",
)

setup(
    name="Migration Automation Retry",
    version="1.0b",
    packages=["migration_automation_retry"],
    include_package_data=True,
    entry_points={"console_scripts": ["migration_automation_retry = migration_automation_retry.migration_retry_dev:main"]},
    data_files=[('/opt/migration/bin', ['migration_automation_retry/migration_retry_dev.py']), ('/opt/migration/logs/retry', [])],
    platforms="linux",
    zip_safe=False,
    author="Elliann Marks",
    author_email="elian.markes@gmail.com",
    description="Migration Automation Retry",
    license="BSD",
    keywords="migration, automation, retry",
    url="https://git.example.com.br/elsilva/migration_automation",
)

setup(
    name="Migration Automation Dbcheck",
    version="1.0b",
    packages=["migration_automation_dbcheck"],
    include_package_data=True,
    entry_points={"console_scripts": ["migration_automation_dbcheck = migration_automation_dbcheck.migration_dbcheck_dev:main"]},
    data_files=[('/opt/migration/bin', ['migration_automation_dbcheck/migration_dbcheck_dev.py']), ('/opt/migration/logs/dbcheck', [])],
    platforms="linux",
    zip_safe=False,
    author="Elliann Marks",
    author_email="elian.markes@gmail.com",
    description="Migration Automation Dbcheck",
    license="BSD",
    keywords="migration, automation, dbcheck",
    url="https://git.example.com.br/elsilva/migration_automation",
)

setup(
    name="Migration Automation Check",
    version="1.0b",
    packages=["migration_automation_check"],
    include_package_data=True,
    entry_points={"console_scripts": ["migration_automation_check = migration_automation_check.migration_check_dev:main"]},
    data_files=[('/opt/migration/bin', ['migration_automation_check/migration_check_dev.py']), ('/opt/migration/logs/check', [])],
    platforms="linux",
    zip_safe=False,
    author="Elliann Marks",
    author_email="elian.markes@gmail.com",
    description="Migration Automation Check",
    license="BSD",
    keywords="migration, automation, check",
    url="https://git.example.com.br/elsilva/migration_automation",
)

setup(
    name="Migration Automation Handle Account",
    version="1.0b",
    packages=["migration_automation_handle_report"],
    include_package_data=True,
    entry_points={"console_scripts": ["migration_automation_handle_report = migration_automation_handle_report.migration_automation_handle_report_dev:main"]},
    data_files=[('/opt/migration/bin', ['migration_automation_handle_report/migration_automation_handle_report_dev.py']), ('/opt/migration/logs/handle_report', [])],
    platforms="linux",
    zip_safe=False,
    author="Elliann Marks",
    author_email="elian.markes@gmail.com",
    description="Migration Automation Handle Report",
    license="BSD",
    keywords="migration, automation, handle, report",
    url="https://git.example.com.br/elsilva/migration_automation",
)

setup(
    name="Migration Automation Handle PHP",
    version="1.0b",
    packages=["migration_automation_handle_php"],
    include_package_data=True,
    entry_points={"console_scripts": ["migration_automation_handle_php = migration_automation_handle_php.migration_handle_php_dev:main"]},
    data_files=[('/opt/migration/bin', ['migration_automation_handle_php/migration_handle_php_dev.py']), ('/opt/migration/logs/handle_php', [])],
    platforms="linux",
    zip_safe=False,
    author="Elliann Marks",
    author_email="elian.markes@gmail.com",
    description="Migration Automation Handle PHP",
    license="BSD",
    keywords="migration, automation, handle, php",
    url="https://git.example.com.br/elsilva/migration_automation",
)

setup(
    name="Migration Automation Handle DNS",
    version="1.0b",
    packages=["migration_automation_handle_dns"],
    include_package_data=True,
    entry_points={"console_scripts": ["migration_automation_handle_dns = migration_automation_handle_dns.migration_handle_dns_dev:main"]},
    data_files=[('/opt/migration/bin', ['migration_automation_handle_dns/migration_handle_dns_dev.py']), ('/opt/migration/logs/handle_dns', [])],
    platforms="linux",
    zip_safe=False,
    author="Elliann Marks",
    author_email="elian.markes@gmail.com",
    description="Migration Automation Handle DNS",
    license="BSD",
    keywords="migration, automation, handle, dns",
    url="https://git.example.com.br/elsilva/migration_automation",
)

setup(
    name="Migration Automation Check End",
    version="1.0b",
    packages=["migration_automation_check_end"],
    include_package_data=True,
    entry_points={"console_scripts": ["migration_automation_check_end = migration_automation_check_end.migration_check_end_dev:main"]},
    data_files=[('/opt/migration/bin', ['migration_automation_check_end/migration_check_end_dev.py']), ('/opt/migration/logs/check_end', [])],
    platforms="linux",
    zip_safe=False,
    author="Elliann Marks",
    author_email="elian.markes@gmail.com",
    description="Migration Automation Check End",
    license="BSD",
    keywords="migration, automation, check, end",
    url="https://git.example.com.br/elsilva/migration_automation",
)

setup(
    name="Migration Automation CPanel",
    version="1.0b",
    packages=["migration_automation_cpanel"],
    include_package_data=True,
    entry_points={"console_scripts": ["migration_automation_cpanel = migration_automation_cpanel.migration_cpanel_dev:main"]},
    data_files=[('/opt/migration/bin', ['migration_automation_cpanel/migration_cpanel_dev.py']), ('/opt/migration/logs/cpanel', [])],
    platforms="linux",
    zip_safe=False,
    author="Elliann Marks",
    author_email="elian.markes@gmail.com",
    description="Migration Automation CPanel",
    license="BSD",
    keywords="migration, automation, cpanel",
    url="https://git.example.com.br/elsilva/migration_automation",
)

setup(
    name="Migration Automation Rsync",
    version="1.0b",
    packages=["migration_automation_rsync"],
    include_package_data=True,
    entry_points={"console_scripts": ["migration_automation_rsync = migration_automation_rsync.migration_rsync_dev:main",
                                      "migration_automation_rsync_last = migration_automation_rsync.migration_rsync_last_dev:main"]},
    data_files=[('/opt/migration/bin', ['migration_automation_rsync/migration_rsync_dev.py']), ('/opt/migration/logs/rsync', []),
                ('/opt/migration/bin', ['migration_automation_rsync/migration_rsync_last_dev.py']), ('/opt/migration/logs/rsync_last', [])],
    platforms="linux",
    zip_safe=False,
    author="Elliann Marks",
    author_email="elian.markes@gmail.com",
    description="Migration Automation Rsync",
    license="BSD",
    keywords="migration, automation, rsync",
    url="https://git.example.com.br/elsilva/migration_automation",
)

setup(
    name="Migration Automation Manager",
    version="1.0b",
    packages=["migration_automation_manager"],
    include_package_data=True,
    entry_points={"console_scripts": ["migration_automation_manager = migration_automation_manager.migration_manager_dev:main"]},
    data_files=[('/opt/migration/bin', ['migration_automation_manager/migration_manager_dev.py']), ('/opt/migration/logs/manager', [])],
    platforms="linux",
    zip_safe=False,
    author="Elliann Marks",
    author_email="elian.markes@gmail.com",
    description="Migration Automation Manager",
    license="BSD",
    keywords="migration, automation, manager",
    url="https://git.example.com.br/elsilva/migration_automation",
)
