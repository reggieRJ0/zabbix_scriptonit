#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author: Janssen dos Reis Lima

from pyzabbix import ZabbixAPI
import csv

zapi = ZabbixAPI("http:///zabbix") # подключиться к zabbix
zapi.login(user="Admin", password="zabbix")

hosts = csv.reader(open('hosts.csv')) # скормить csv

for [hostname, port] in hosts:
    hostcriado = zapi.host.create(
        host=hostname,
        visiblename = hostname,
        status=1,
        interfaces=[{
            "type": 2,
            "main": "1",
            "useip": 1,
            "ip": '', # добавить адрес
            "port": 161
        }],
        groups=[{
            "groupid": # добавить группу
        }],
        templates=[{
            "templateid": # добавить ID шаблона
        }],
        macros = [{
            "macro": "{$TEST1}", # указать макрос
            "value": port # значение макроса
        }]
    )7






