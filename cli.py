#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from core.interface import get_active_interfaces
from core.router import clear_custom_routing_tables, check_existing_routing_tables

def run_cmd(cmd):
    """Helper function to run a shell command."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        stderr = result.stderr.strip()
        if result.returncode != 0 and "Cannot find device" not in stderr and "No such file or directory" not in stderr:
            print(f"[!] {cmd}\n    -> {stderr}")
        return result.stdout.strip()
    except Exception as e:
        print(f"[X] Exception while running '{cmd}': {e}")
        return None

def list_interfaces():
    """Lists all active network interfaces."""
    print("--- Active Network Interfaces ---")
    interfaces = get_active_interfaces()
    if not interfaces:
        print("No active network interfaces found.")
        return

    for iface in interfaces:
        if iface['flag'] == 'UP' and iface['ip_addresses']:
            print(f"\nInterface: {iface['name']}")
            print(f"  Status: {iface['flag']}")
            print(f"  Type: {iface['type']}")
            print(f"  IP Addresses: {', '.join(iface['ip_addresses'])}")
            print(f"  Gateways: {', '.join(iface['gateways'] if iface['gateways'] else ['N/A'])}")

def assign_app(app, iface):
    """Assigns an application to a specific network interface."""
    if "chromium" in app.lower():
        print("[X] Error: Chromium is not supported due to its sandboxing architecture, which conflicts with network namespacing.")
        return

    if not os.path.exists(app):
        print(f"[X] Error: Application path not found: {app}")
        return

    print(f"[+] Assigning '{app}' to interface '{iface}'...")
    
    ns = f"ns_{iface}"
    run_cmd(f"ip netns add {ns}")
    run_cmd("ip link add veth0 type veth peer name veth1")
    run_cmd(f"ip link set veth1 netns {ns}")
    run_cmd("ip addr add 10.0.0.1/24 dev veth0")
    run_cmd("ip link set veth0 up")
    run_cmd(f"mkdir -p /etc/netns/{ns}/tmp")

    print(f"[+] Starting application in network namespace '{ns}'...")
    # Note: This command runs in the background.
    subprocess.Popen(
        f"sudo ip netns exec {ns} env DISPLAY=$DISPLAY XAUTHORITY=$HOME/.Xauthority {app}",
        shell=True
    )
    print(f"[✓] Application '{app}' is running through '{iface}'.")

def clear_all_paths():
    """Clears all custom routing tables."""
    if not check_existing_routing_tables():
        print("[i] No custom routing tables found to clear.")
        return
    
    print("[+] Clearing all custom routing tables...")
    clear_custom_routing_tables()
    print("[✓] All paths cleared successfully.")

def reset_system():
    """Resets the system by removing all created network resources."""
    print("[+] Resetting system to defaults...")

    # Clear custom routing tables
    clear_custom_routing_tables()

    # Remove veth interface
    run_cmd("ip link del veth0 2>/dev/null")

    # Remove network namespaces
    interfaces = get_active_interfaces()
    if interfaces:
        for iface in interfaces:
            ns = f"ns_{iface['name']}"
            run_cmd(f"ip netns del {ns} 2>/dev/null")

    print("[✓] System has been reset.")

def main():
    """Main function to parse arguments and execute commands."""
    if os.geteuid() != 0:
        print("[X] This script must be run as root.")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="CLI for network interface binding.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 'list' command
    parser_list = subparsers.add_parser("list", help="List active network interfaces.")
    parser_list.set_defaults(func=list_interfaces)

    # 'assign' command
    parser_assign = subparsers.add_parser("assign", help="Assign an application to an interface.")
    parser_assign.add_argument("--app", required=True, help="Path to the application.")
    parser_assign.add_argument("--iface", required=True, help="Name of the interface.")
    parser_assign.set_defaults(func=lambda args: assign_app(args.app, args.iface))

    # 'clear' command
    parser_clear = subparsers.add_parser("clear", help="Clear all assigned paths and routing tables.")
    parser_clear.set_defaults(func=clear_all_paths)

    # 'reset' command
    parser_reset = subparsers.add_parser("reset", help="Reset everything to system defaults.")
    parser_reset.set_defaults(func=reset_system)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args) if 'app' in args or 'iface' in args else args.func()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
