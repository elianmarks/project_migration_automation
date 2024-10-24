# Migration Automation - Bifrost

---

## Table of Contents <a name="table_of_contents"></a>
* [What you need](#prerequisites)
* [Installation](#installation)
    * [All environment](#installation_all)
    * [Process](#process_application)
    * [Configuration of the environment](#conf_environment)
        * [Config section](#config_section)
        * [Logger section](#logger_section)
        * [Environment section](#environment_section)
* [Directory structure](#structure)
* [Working diagram](#working_diagram)
* [Microservices](#microservices)
    * [Manager](#manager_service)
    * [Check](#check_service)
    * [Check End](#check_end_service)
    * [Compare](#compare_service)
    * [cPanel](#cpanel_service)
    * [DBCheck](#dbcheck_service)
    * [Handle Account](#handle_account_service)
    * [Handle DNS](#handle_dns_service)
    * [Retry](#retry_service)
    * [RSync](#rsync_service)
    * [Zencheck](#zencheck_service)
* [Ansible Roles](#ansibleroles)

## What you need [[Back to contents]](#table_of_contents) <a name="prerequisites"></a>
- Python 3.7
- MySQL >= 5.7
- Docker Image RabbitMQ >= 3.7
- Libraries
    * [Zenpy](https://github.com/facetoe/zenpy) >= 2.0.8
    * [Ansible](https://www.ansible.com/) >= 2.8.3
    * Pika >= 1.1.0
    * Mysql-connector-python >= 8.0.17
    * [DNS Python](https://github.com/rthalley/dnspython) >= 2.0
    * Configparser => 3.7.1
    * [SGQLC](https://github.com/profusion/sgqlc) >= 7.0

## Installation [[Back to contents]](#table_of_contents) <a name="installation"></a>
The installation process is the same for any environment, but python file development or production are different.

### All environment [[Back to contents]](#table_of_contents) <a name="installation_all"></a>
```
# Create user
useradd migration

# Create virtualenv
virtualenv /home/migration/venv_migration

# Activate virtualenv
source /home/migration/venv_migration/bin/activate

# Enter in migration home
cd /home/migration

# Clone the repository
git clone https://stash.example.com/scm/lespo/migration_automation.git

# Clone library DNS Python
git clone https://github.com/rthalley/dnspython.git

# Install DNS Python
cd dnspython && python setup.py install

# Install migration automation
cd migration_automation && python setup.py install

# Configure permissions in /opt/migration
chown -R migration.migration /opt/migration

# Copy playbooks
cp migration_automation_playbooks/*.yaml /etc/ansible/playbooks

# Copy roles
cp -r migration_automation_playbooks/check_ssh /etc/ansible/roles
cp -r migration_automation_playbooks/cpanel_backup /etc/ansible/roles
cp -r migration_automation_playbooks/domain_info /etc/ansible/roles
cp -r migration_automation_playbooks/handle_account /etc/ansible/roles
cp -r migration_automation_playbooks/handle_dns /etc/ansible/roles
cp -r migration_automation_playbooks/handle_php /etc/ansible/roles
cp -r migration_automation_playbooks/rsync_backup /etc/ansible/roles

# Create symbolic link of the migration/bin/python in /opt/migration/bin/pythonMigration
ln -s /home/migration/venv_migration/bin/python3.7 /opt/migration/bin/pythonMigration

# Copy the services and targets
cp migration_systemd_services/migration_check* /usr/lib/systemd/system
cp migration_systemd_services/migration_check_end* /usr/lib/systemd/system
cp migration_systemd_services/migration_compare.service /usr/lib/systemd/system
cp migration_systemd_services/migration_cpanel.service /usr/lib/systemd/system
cp migration_systemd_services/migration_dbcheck.service /usr/lib/systemd/system
cp migration_systemd_services/migration_handle_account.service /usr/lib/systemd/system
cp migration_systemd_services/migration_handle_dns* /usr/lib/systemd/system
cp migration_systemd_services/migration_handle_php.service /usr/lib/systemd/system
cp migration_systemd_services/migration_manger.service /usr/lib/systemd/system
cp migration_systemd_services/migration_retry.service /usr/lib/systemd/system
cp migration_systemd_services/migration_rsync* /usr/lib/systemd/system
cp migration_systemd_services/migration_rsync_last* /usr/lib/systemd/system
cp migration_systemd_services/migration_zencheck.service /usr/lib/systemd/system

# Reload in systemctl
systemctl daemon-reload

```

### Process [[Back to contents]](#table_of_contents) <a name="process_application"></a>
* Update environment variables in correct section
* Start processes
```
# Start services and targets
systemctl start migration_check.target
systemctl start migration_check_end.target
systemctl start migration_compare
systemctl start migration_cpanel
systemctl start migration_dbcheck
systemctl start migration_handle_account
systemctl start migration_handle_dns.target
systemctl start migration_handle_php
systemctl start migration_manger
systemctl start migration_retry
systemctl start migration_rsync.target
systemctl start migration_rsync_last.target
systemctl start migration_zencheck
```

### Configuration of the environment [[Back to contents]](#table_of_contents) <a name="conf_environment"></a>
The main application variables are set in the configuration file, this requires to be created in /opt/migration/files/migration.conf.

#### Config section [[Back to contents]](#table_of_contents) <a name="config_section"></a>
Name | Type | Description | Default | Environment
--- | --- | --- | --- | ---
hostqueue | string | DNS or IP of the RabbitMQ | localhost | All
userqueue | string | User for queue in RabbitMQ | migration_dev | All
portqueue | string | Port for queue in RabbitMQ | 5674 | All
passwordqueue | string | Password for queue in RabbitMQ | migration_dev | All
keycpanel | string | Key for cPanel queue | migration_dev | Production and Development
keyrsync | string | Key for rsync queue | migration_dev | All
keyrsynclast | string | Key for rsync last queue | migration_dev | All
keycheck | string | Key for check queue | migration_dev | Production and Development
keycheckend | string | Key for check end queue | migration_dev | Production and Development
keymanager | string | Key for manager queue | migration_dev | Production and Development
keycompare | string | Key for comapre queue | migration_dev | Production and Development
keyhandlephp | string | Key for handle php queue | migration_dev | Production and Development
keyhandledns | string | Key for handle dns queue | migration_dev | Production and Development
keyhandleaccount | string | Key for handle account queue | migration_dev | Production and Development
reportdir | string | Path of treatment reports | /opt/migration/reports | All
playbookcheck | string | Path of the check playbook | /etc/ansible/playbooks/info.yaml | Production and Development
playbookcpanel | string | Path of the cpanel playbook | /etc/ansible/playbooks/cpanel.yaml | Production and Development
playbookrsync | string | Path of the rsync report playbook | /etc/ansible/playbooks/rsync.yaml | Production
playbookphp | string | Path of the php playbook | /etc/ansible/playbooks/php.yaml | Production and Development
playbookdns | string | Path of the dns playbook | /etc/ansible/playbooks/dns.yaml | Production and Development
playbookaccount | string | Path of the account playbook | /etc/ansible/playbooks/account.yaml | Production and Development
privatekeypath | string | Path of the private key for access migration server | /home/migration/.ssh/id_rsa | Production
privatekeypathall | string | Path of the private key for access clients servers | /home/migration/.ssh/suporte-l1 | Production and Development
ansibleroles | string | Path of the Ansible roles | /etc/ansible/roles | Production and Development
ipdb | string | IP for connect in database | localhost | All
userdb | string | User for connect in database | migration_dev | All
passdb | string | Password for connect in database | migration_dev | All
database | string | Database name | migration_dev | All
token | string | Token for access Zendesk BR API | X | Production and Development
tokenes | string | Token for access Zendesk LATAM API | X | Production and Development
domain | string | Name of the domain in Zendesk for BR | examplebr | Production and Development
domaines | string | Name of the domain in Zendesk for LATAM | examplemx | Production and Development
whmcschangeserver | string | Token for access API | X | Production and Development

#### Logger section [[Back to contents]](#table_of_contents) <a name="logger_section"></a>
Name | Type | Description | Default | Environment
--- | --- | --- | --- | ---
logfilezencheck | string | Path of the log directory for migration_zencheck process | /opt/migration/logs/zencheck/migration_zencheck | All
logfiledbcheck | string | Path of the log directory for migration_dbcheck process | /opt/migration/logs/dbcheck/migration_dbcheck | All
logfileretry | string | Path of the log directory for migration_retry process | /opt/migration/logs/retry/migration_retry | All
logfilecpanel | string | Path of the log directory for migration_cpanel process | /opt/migration/logs/cpanel/migration_cpanel | All
logfilersync | string | Path of the log directory for migration_rsync process | /opt/migration/logs/rsync/migration_rsync | All
logfilecheck | string | Path of the log directory for migration_check process | /opt/migration/logs/check/migration_check | All
logfilecheckend | string | Path of the log directory for migration_check_end process | /opt/migration/logs/check_end/migration_check_end | All
logfilemanager | string | Path of the log directory for migration_manager process | /opt/migration/logs/manager/migration_manager | All
logfilecompare | string | Path of the log directory for migration_compare process | /opt/migration/logs/compare/migration_compare | All
logfilehandlephp | string | Path of the log directory for migration_handle_php process | /opt/migration/logs/handle_php/migration_handle_php | All
logfilehandledns | string | Path of the log directory for migration_handle_dns process | /opt/migration/logs/handle_dns/migration_handle_dns | All
logfilehandleaccount | string | Path of the log directory for migration_handle_account process | /opt/migration/logs/handle_account/migration_handle_account | All
loglevel | string | Log level for all services | logging.INFO | All

## Directory structure [[Back to contents]](#table_of_contents) <a name="structure"></a>
```
./
├── migration_automation_check/             # Check application
│   └── migration_check.py                  # Executable python file
│   └── migration_check_dev.py              # Executable python file for development
│   └── module_check.py                     # Main python file
│   └── module_consume.py                   # Connect and consume message in queue
├── migration_automation_check_end/         # Check application
│   └── module_connectdb.py                 # Connection in database
│   └── module_database.py                  # Functions SQL
│   └── module_dates.py                     # Handle dates format
│   └── module_dns.py                       # Functions DNS
├── migration_automation_compare/           # Check application
│   └── module_exceptions.py                # Error exceptions
│   └── module_log.py                       # Manager logs 
│   └── module_main.py                      # Main python file
│   └── module_publish.py                   # Connect and publish message in queue
├── migration_automation_cpanel/            # Check application
│   └── module_regex.py                     # Load regex file
│   └── module_zen.py                       # Functions Zendesk API
├── migration_automation_dbcheck/           # Check application
├── migration_automation_check_end/         # Check application
├── migration_automation_files/             # Additional files
│   └── migration.conf                      # Configuration file
├── migration_automation_handle_account/    # Analyze application
├── migration_automation_analyze/           # Analyze application
│   └── analyze.py                          # Executable python file
│   └── module_analyze.py                   # Main python file
│   └── module_consume.py                   # Connect and consume message in queue
├── migration_automation_ia/        # IA application
│   └── ia.py                   # Executable python file
│   └── module_ia.py            # Main python file
│   └── module_consume.py       # Connect and consume message in queue
├── migration_automation_playbooks/ # Ansible playbooks and roles
│   └── migration_upload            # Role for upload report to migration server
│   └── backup_generate         # Role for generate backup in intentional phishing
│   └── check_ssh               # Role for identify ssh port
│   └── block_execute           # Role for execute block account
│   └── domain_check            # Role for extract account infos
│   └── scan_check              # Role for execute scan
│   └── migration.yaml              # Playbook with migration_upload role
│   └── backup.yaml             # Playbook with backup_generate role
│   └── block.yaml              # Playbook with block_execute role
│   └── check.yaml              # Playbook with domain_check role
│   └── scan.yaml               # Playbook with scan_check role
├── migration_automation_vt/        # VT application
│   └── vt.py                   # Executable python file
│   └── module_vt.py            # Main python file
│   └── module_consume.py       # Connect and consume message in queue
├── migration_automation_zenapply/  # Zenapply application
│   └── zenapply.py             # Executable python file
│   └── module_zenapply.py      # Main python file
│   └── module_consume.py       # Connect and consume message in queue
├── migration_scan_sigs/            # Scan files
│   └── clamav-64bit.tar.gz     # Clamav files for execution
│   └── malware.ndb             # Malware sigs
│   └── phishing.nd             # Phishing sigs
├── migration_systemd_services/     # Scan files
│   └── migration.service           # Systemd file to main service
│   └── analyze.service         # Systemd file to analyze service
│   └── ia.service              # Systemd file to ia service
│   └── vt.service              # Systemd file to vt service
├── deploy.sh                   # Script for deploy, not use to install
├── setup.py                    # Setup to install modules python
```

## Flow process [[Back to contents]](#table_of_contents) <a name="flow_process"></a>
The automation identifies the domains hosted on our infrastructure and handles all reporting, gathering information, 
locking the account and notify the customer.

## Working diagram [[Back to contents]](#table_of_contents) <a name="working_diagram"></a>

## Microservices [[Back to contents]](#table_of_contents) <a name="microservices"></a>
In this section we will describe the structure of the automation, the microservices created, the way it works and the sequence of execution.

#### Main [[Back to contents]](#table_of_contents) <a name="main_service"></a>
This service is responsible for checking tickets in Zendesk and extracting ticket information, identifying domains and IPs in the ticket 
description or subject using regex. After this information is extracted, the service identifies whether the domain is valid and is hosted on our infrastructure.
For domains not hosted on company, a comment is made and the ticket is terminated;
For domains that are hosted on company, a comment is made on the ticket and messages are sent to the other services to continue treatment;
This service sends messages to VirusTotal and Analyze service.

#### Analyze [[Back to contents]](#table_of_contents) <a name="analyze_service"></a>
This service is responsible for accessing the server where the domain is hosted to collect user account information. Information is 
accessed and collected using Ansible, the playbooks have several commands from whmapi and uapi.
This service sends messages to the Artificial Intelligence service.

#### IA [[Back to contents]](#table_of_contents) <a name="ia_service"></a>
This service is responsible for transforming the data collected by Analyze, after normalization it is predicted whether the account is 
intentional or unintentional phishing using machine learning with KNN (K-Nearest Neighbors) algorithm.
This service sends messages to Zenapply service.

#### VT [[Back to contents]](#table_of_contents) <a name="vt_service"></a>
This service is responsible for verifying that the domain is marked as malicious in the VirusTotal framework.

#### Zenapply [[Back to contents]](#table_of_contents) <a name="zenapply_service"></a>
This service is responsible for conducting final dealings with Zendesk, notifying customers 
of unintentional phishing or forcing the customer to terminate their account.

## Ansible Roles [[Back to contents]](#table_of_contents) <a name="ansibleroles"></a>
In this section we will describe the structure of the roles that automation use.

#### migration_upload [[Back to contents]](#table_of_contents) <a name="migration_uplaod_role"></a>
- This role is responsible by send the report data for VPS Support (migration Server), only execute copy module with source in /opt/migration/reports/ID_REPORT and destination /opt/migration/reports/ (migration Server - Support);
- Not access client or shared servers;

#### backup_generate [[Back to contents]](#table_of_contents) <a name="backup_generate_role"></a>
- This role is responsible for generating an account backup when the IA predicts that the account is phishing intentionally and the disk used is less than 500MB, after sending a ticket for check and confirmation Financial Department. If the disk used is greater than 500MB, the ticket is sended for check in the Support Department;
- When the account is less than 500MB, this execute suspendacct in account too;
- Not delete account or data, only create a backup and copy for Jigsaw Server;

#### block_execute [[Back to contents]](#table_of_contents) <a name="block_execute_role"></a>
- This role is responsible by execute a pwrestrict command in user account;
- Not delete account or data, only execute a pwrestrict in account;

#### check_ssh [[Back to contents]](#table_of_contents) <a name="check_ssh_role"></a>
- This role is responsible by identify the listening ssh port;
- Not access client or shared servers;

#### domain_check [[Back to contents]](#table_of_contents) <a name="domain_check_role"></a>
- This role is response by get account information, use only uapi, whamp1, hf, hostname and vdetect commands;
- Not delete account or data, only get informations;
- Commands list
    - uapi --user="USER" Email list_pops_with_disk --output=json
    - uapi --user="USER" Email get_main_account_disk_usage_bytes --output=json
    - whmapi1 accountsummary user="USER" --output=json
    - whmapi1 accountsummary user="OWNER_USER" --output=json
    - whmapi1 list_mysql_databases_and_users user="USER" --output=json
    - uapi --user="USER" Email list_mxs --output=json
    - whmapi1 accountsummary user="USER" --output=json
    - vdetect --user "USER" --json
    - hostname
    - uapi --user="USER" DomainInfo domains_data format=hash return_https_redirect_status=1 --output=json
    - uapi --user="USER" Bandwidth query grouping=domain%7Cyear_month_day%7Cprotocol protocols=http%7Cftp timezone=America%2FSao_Paulo --output=json
    - whmapi1 showbw searchtype=user search=^"USER"$ --output=json
    - uapi --user="USER" LastLogin get_last_or_current_logged_in_ip --output=json
    - whmapi1 domainuserdata domain="DOMAIN" --output=json
    - uapi --user="USER" Ftp list_ftp_with_disk include_acct_types=main --output=json
    - uapi --user="USER" DomainInfo list_domains --output=json
    - hf -r 120 -n 10 -u "USER" -j "PATH"

#### scan_check [[Back to contents]](#table_of_contents) <a name="scan_check_role"></a>
- This role is responsible by execute a scan in specific path, does not delete any malicious files found;
- Scan parameters
    - -i -r --no-summary --max-recursion=10 --max-dir-recursion=10 --exclude='(error_log|access_log)' --exclude-dir='(access-logs|mail|awstats|webalizer|analog|.security|cpbandwidth|webalizerftp|MYSQL_DATA|cpeasyapache|virtfs|.trash)' --max-filesize=3M --scan-mail=no --scan-pe=no --scan-archive=no --cross-fs=no --bytecode-timeout=5 --phishing-sigs=no --phishing-scan-urls=no --scan-ole2=no --scan-pdf=no --block-encrypted=yes
- Not delete account or data, only execute a scan.
