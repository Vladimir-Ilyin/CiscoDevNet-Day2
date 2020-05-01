#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml
import argparse

from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result

from prettytable import PrettyTable

os.environ['NET_TEXTFSM'] = os.path.dirname(os.path.abspath(__file__)) + '\\ntc-template\\templates\\'

def find_mac(ft, val, mode='access'):
    # Поиск заданного MAC в полной таблице, возврат всех найденных записей MAC удовлетворяющих условию поиска
    result = []
    for record in ft:
        if record['destination_address'].lower() == val.lower() and (mode in record.get('mode', 'UNDEFINED')):
            result.append(record)
    return result

def find_interface(interface_table, val):
    # Вспомогательная функция для формирования списка словарей
    for interface in interface_table:
        if val == interface['interface']:
            return interface
    return {}

def gather_info():
    # Сбор информации по mac адресам и интерфейсам в сети
    with InitNornir(config_file="config.yaml") as nr:

        mac_table = nr.run(netmiko_send_command, command_string="show mac address-table", use_textfsm=True)
        int_table  = nr.run(netmiko_send_command, command_string="show interface switchport", use_textfsm=True)

        # Формируем плоский список словарей { MAC, интерфейс, режим интерфейса и т.п. (все данные из шаблонов) }
        full_table = []
        for host in nr.inventory.hosts.keys():
            for mac in mac_table[host][0].result:
                full_table.append( { 'host': host, **mac, **find_interface(int_table[host][0].result, mac['destination_port']) })

        return full_table

def main():
    parser, args = get_args()

    if args.mode:
        mode=args.mode
    else:
        mode=''
    if args.mac:
        macs_list = args.mac
    else:
        macs_list = None

    # Сбор информации по mac адресам и интерфейсам в сети
    full_table = gather_info()

    # Поиск заданного MAC (или списка MAC) в сформированном списке с заданным условием mode (по умолчанию mode='access')
    # Если список адресов не задан в командной строке, просмотр всей таблицы адресов
    result = []
    if macs_list:
        for mac in macs_list:
            res = find_mac(full_table, mac, mode)
            if res:
                result.extend(res)
    else:
        result = full_table

    # Инициализируем таблицу для вывода данных и заполняем выводимые значениями
    table = PrettyTable(['SwitchName','Port','Mode','Vlan','MAC'])
    for row in result:
        table.add_row([row['host'],row['destination_port'],row.get('mode', 'UNDEFINED'),row['vlan'],row['destination_address']])
    # Выводим результат
    print(table)

    return

def get_args():
    # Парсер аргументов командной строки
    parser = argparse.ArgumentParser(description="Поиск MAC адресов на оборудовании")

    parser.add_argument(
        "--mac",
        action='store',
        nargs='+',
        help="Поиск заданного MAC на устройствах"
    )

    parser.add_argument(
        "--mode",
        action='store',
        choices=['access','trunk'],
        help="Режим интерфейса при поиске - access или trunk, по умолчанию поиск всех"
    )

    return parser, parser.parse_args()

if __name__ == '__main__':
    main()