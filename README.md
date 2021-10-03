# Zabbix-agent2

![Build Status](https://github.com/1mr/ansible-role-zabbix_agent2/actions/workflows/ci.yaml/badge.svg)

This role helps to install and configure zabbix-agent2.

## Requirements

This role requires ansible 2.5 or higher.

## Role Variables

The variables that can be passed to this role and a brief description about them are as follows:

    zabbix_agent_server: zabbix.lcl
    zabbix_agent_mysql_user: zbx_monitor
    zabbix_agent_mysql_passwd: zbx_pass
    zabbix_agemt_psk_secret: secret

## Dependencies

None

## Example Playbook

    - hosts: servers
      roles:
         - { role: 1mr.zabbix-agent2, tags: zabbix-agent2 }

## License

BSD

## Author Information

This role was created by Stas Stavnichuk.
