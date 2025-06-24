#!/usr/bin/env python3

import os
import subprocess
import re
import ipaddress
from interface import get_active_interfaces

RT_TABLES_PATH = "/etc/iproute2/rt_tables"
BASE_TABLE_ID = 100
BASE_PRIORITY = 1000



def get_network(ip_with_cidr):
    net = ipaddress.ip_interface(ip_with_cidr).network
    return str(net)

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stderr and not result.returncode == 0:
        print(f"[!] {cmd} -> {result.stderr.strip()}")
    return result.stdout.strip()



def extract_ip_and_prefix(ip_with_cidr):
    if '/' in ip_with_cidr:
        return ip_with_cidr.split('/')
    return ip_with_cidr, '24'

def ensure_routing_table(table_id, name):
    with open(RT_TABLES_PATH, 'r+') as f:
        lines = f.read().splitlines()
        entry = f"{table_id} {name}"
        if entry not in lines:
            f.write(f"\n{entry}\n")
            print(f"[+] Added routing table entry: {entry}")
    return True

# def setup_interface_routing(name, ip_with_cidr, gateway, table_id):
#     ip, prefix = extract_ip_and_prefix(ip_with_cidr)
#     table_name = f"{name}_rt"

#     ensure_routing_table(table_id, table_name)

#     run_cmd(f"ip route flush table {table_id}")
#     run_cmd(f"ip rule del from {ip} table {table_id} priority {BASE_PRIORITY + table_id} 2>/dev/null")

#     run_cmd(f"ip route add {ip}/{prefix} dev {name} scope link table {table_id}")
#     run_cmd(f"ip route add default via {gateway} dev {name} table {table_id}")
#     run_cmd(f"ip rule add from {ip} table {table_id} priority {BASE_PRIORITY + table_id}")

#     print(f"[✓] Routing set for {name} ({ip}/{prefix}) via {gateway} [table {table_id}]")

def setup_interface_routing(name, ip_with_cidr, gateway, table_id):
    ip, prefix = extract_ip_and_prefix(ip_with_cidr)
    table_name = f"{name}_rt"

    ensure_routing_table(table_id, table_name)

    run_cmd(f"ip route flush table {table_id}")
    run_cmd(f"ip rule del from {ip} table {table_id} priority {BASE_PRIORITY + table_id} 2>/dev/null")

    network = get_network(ip_with_cidr)
    run_cmd(f"ip route add {network} dev {name} scope link table {table_id}")

    run_cmd(f"ip route add default via {gateway} dev {name} table {table_id}")
    run_cmd(f"ip rule add from {ip} table {table_id} priority {BASE_PRIORITY + table_id}")

    print(f"[✓] Routing set for {name} ({ip}/{prefix}) via {gateway} [table {table_id}]")

def main():
    if os.geteuid() != 0:
        print("[X] Run this script as root.")
        return

    interfaces = get_active_interfaces()
    table_id = BASE_TABLE_ID

    for iface in interfaces:
        if iface['flag'] != 'UP':
            continue

        ipv4s = [ip for ip in iface['ip_addresses'] if ':' not in ip]
        if not ipv4s or not iface['gateways']:
            continue

        ip_with_cidr = ipv4s[0]
        gateway = iface['gateways'][0]

        setup_interface_routing(iface['name'], ip_with_cidr, gateway, table_id)
        table_id += 1

if __name__ == "__main__":
    main()
