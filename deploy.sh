#!/bin/bash

# roles
ansible_roles="/etc/ansible/roles/"
r_cpanel_backup="cpanel_backup"
r_domain_info="domain_info"
r_handle_account="handle_account"
r_handle_dns="handle_dns"
r_handle_php="handle_php"
r_check_ssh="check_ssh"

# playbooks
ansible_playbooks="/etc/ansible/playbooks/"
p_account="account.yaml"
p_cpanel="cpanel.yaml"
p_dns="dns.yaml"
p_info="info.yaml"
p_php="php.yaml"

# variables
venv_path="/home/migration/venv_migration/bin/activate"
app_path="/home/migration/migration_automation"
playbooks_path="/home/migration/migration_automation/migration_automation_playbooks"

_git_pull() {
  echo "[INFO] Executing pull..."
  cd $app_path
  git pull
  _check_execution $?
  echo "[INFO] Executing install..."
  # active venv
  source $venv_path
  _check_execution $?
  # execute two install
  python3.7 setup.py install
  _check_execution $?
  python3.7 setup.py install
}

_copy_roles() {
  echo "[INFO] Executing copy roles..."
  cd $playbooks_path
  # delete all roles
  rm -rf $ansible_roles$r_cpanel_backup
  rm -rf $ansible_roles$r_domain_info
  rm -rf $ansible_roles$r_handle_account
  rm -rf $ansible_roles$r_handle_dns
  rm -rf $ansible_roles$r_handle_php
  # copy all roles
  cp -r $r_cpanel_backup $ansible_roles
  _check_execution $?
  cp -r $r_domain_info $ansible_roles
  _check_execution $?
  cp -r $r_handle_account $ansible_roles
  _check_execution $?
  cp -r $r_handle_dns $ansible_roles
  _check_execution $?
  cp -r $r_handle_php $ansible_roles
  _check_execution $?
  if [ -d "$ansible_roles$r_check_ssh" ]; then
    cp -r $r_check_ssh $ansible_roles
  fi
}

_copy_playbooks() {
  echo "[INFO] Executing copy playbooks..."
  cd $playbooks_path
  # delete all playbooks
  rm -rf $ansible_playbooks$p_account
  rm -rf $ansible_playbooks$p_cpanel
  rm -rf $ansible_playbooks$p_dns
  rm -rf $ansible_playbooks$p_info
  rm -rf $ansible_playbooks$p_php
  # copy all playbooks
  cp $p_account $ansible_playbooks
  _check_execution $?
  cp $p_cpanel $ansible_playbooks
  _check_execution $?
  cp $p_dns $ansible_playbooks
  _check_execution $?
  cp $p_info $ansible_playbooks
  _check_execution $?
  cp $p_php $ansible_playbooks
  _check_execution $?
}

_check_execution() {
    if [ "$1" != "0" ]
    then
        echo -e "[ERROR] :: Require checking..."
        exit 1
    fi
}

_services() {
  service migration_check.target $1
  service migration_check_end.target $1
  service migration_compare $1
  service migration_cpanel $1
  service migration_dbcheck $1
  service migration_handle_account $1
  service migration_handle_dns.target $1
  service migration_handle_php $1
  service migration_rsync.target $1
  service migration_rsync_last.taget $1
}

echo "Initializing deploy..."
_services "stop"
_git_pull
_copy_roles
_copy_playbooks
_services "start"
echo "Deploy completed..."