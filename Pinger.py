#!/usr/bin/env python3

import asyncio
import os
import socket
import sys
import re
import argparse
from ping3 import ping
from statistics import mean
from colorama import init, Fore, Style

init(autoreset=True)

os.system("clear")

HELP_TEXT = """Usage:
  pinger HOST [-c COUNT] [-i INTERVAL_MS] [-t TIMEOUT_MS]
  pinger -h | --help

Flags:
  HOST                  IP address or hostname to ping
  -c,  --count COUNT    Number of pings to send (default: 10)
  -i,  --interval MS    Delay between pings in milliseconds (default: 500)
  -t,  --timeout  MS    Timeout per ping in milliseconds (default: 1000)
  -h,  --help           Show this help and exit

Examples:
  pinger google.com
  pinger 1.1.1.1 -c 5 -i 200 -t 1000
"""

def parse_args():
    p = argparse.ArgumentParser(
        prog="pinger",
        add_help=False,
        formatter_class=argparse.RawTextHelpFormatter,
        description=HELP_TEXT,
    )

    p.add_argument("host", nargs="?", help=argparse.SUPPRESS)
    p.add_argument("-c", "--count", type=int, default=10, help=argparse.SUPPRESS)
    p.add_argument("-i", "--interval", type=int, default=500, metavar="MS", help=argparse.SUPPRESS)
    p.add_argument("-t", "--timeout", type=int, default=1000, metavar="MS", help=argparse.SUPPRESS)
    p.add_argument("-h", "--help", action="store_true", help=argparse.SUPPRESS)

    return p.parse_args()

def strip_ansi(string):
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    return ansi_escape.sub('', string)

class PingStats:
    def __init__(self):
        self.latencies = []
        self.sent = 0
        self.received = 0

    def add(self, latency):
        self.sent += 1
        if latency is not None:
            self.received += 1
            self.latencies.append(latency * 1000)

    def packet_loss(self):
        return ((self.sent - self.received) / self.sent) * 100 if self.sent else 0

    def avg_latency(self):
        return mean(self.latencies) if self.latencies else 0

    def min_latency(self):
        return min(self.latencies) if self.latencies else 0

    def max_latency(self):
        return max(self.latencies) if self.latencies else 0

def is_valid_ip(host):
    ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    if re.match(ip_pattern, host):
        parts = host.split(".")
        return all(0 <= int(part) <= 255 for part in parts)
    try:
        if len(host) > 1 and "." in host:
            socket.gethostbyname(host)
            return True
        else:
            return False
    except socket.error:
        return False

COL_WIDTHS = {
    'try': 6,
    'ip': 17,
    'protocol': 10,
    'latency': 12,
    'bytes': 8,
    'status': 10
}

async def ping_target(host, count=10, interval=0.5, timeout=1.0):
    stats = PingStats()

    header = (
        f"{Fore.WHITE}"
        f"{'             TRY'.center(COL_WIDTHS['try'])}"
        f"{'     TARGET'.center(COL_WIDTHS['ip'])}"
        f"{'   PROTOCOL'.center(COL_WIDTHS['protocol'])}"
        f"{' LATENCY'.center(COL_WIDTHS['latency'])}"
        f"{'  BYTES'.center(COL_WIDTHS['bytes'])}"
        f"{'  STATUS'.center(COL_WIDTHS['status'])}"
        f"{Style.RESET_ALL}"
    )

    print(f"\n{header}")

    for i in range(count):
        latency = await asyncio.to_thread(ping, host, timeout=timeout)
        stats.add(latency)

        protocol = "ICMP"
        bytes_sent = "64"

        if latency is None:
            status = f"{Fore.RED}   Down{Style.RESET_ALL}"
            latency_display = "-"
            bytes_sent = "-"
        else:
            status = f"{Fore.WHITE}    UP{Style.RESET_ALL}"
            latency_display = f"{latency*1000:.2f} ms"

        row = (
            f"{('#' + str(i+1)).center(COL_WIDTHS['try'])}"
            f"{host.center(COL_WIDTHS['ip'])}"
            f"{protocol.center(COL_WIDTHS['protocol'])}"
            f"{latency_display.center(COL_WIDTHS['latency'])}"
            f"{bytes_sent.center(COL_WIDTHS['bytes'])}"
            f"{status.center(COL_WIDTHS['status'])}"
        )
        print(f"            {row}")

        await asyncio.sleep(interval)

    print(f" ")

    print(f"{Fore.WHITE}            {'═'*23} Ping Summary {'═'*24}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}            Packets  : {Fore.WHITE}Sent = {Fore.YELLOW}{stats.sent}{Style.RESET_ALL}, "
        f"Received = {Fore.GREEN}{stats.received}{Style.RESET_ALL}, "
        f"Lost = {Fore.RED}{stats.sent - stats.received}{Style.RESET_ALL} "
        f"({Fore.RED}{stats.packet_loss():.1f}%{Style.RESET_ALL} loss)")
    print(f"{Fore.GREEN}            Latency  : {Fore.WHITE}Avg = {Fore.YELLOW}{stats.avg_latency():.2f} ms{Style.RESET_ALL}, "
        f"Min = {Fore.GREEN}{stats.min_latency():.2f} ms{Style.RESET_ALL}, "
        f"Max = {Fore.RED}{stats.max_latency():.2f} ms{Style.RESET_ALL}")
    print(f"{Fore.WHITE}            {'═'*61}{Style.RESET_ALL}")

async def main():
    os.system("clear")
    args = parse_args()

    if args.help:
        print(HELP_TEXT)
        sys.exit(0)

    if args.host:
        host = args.host
        if not is_valid_ip(host):
            print(f"{Fore.RED}❌ Invalid host or IP provided!{Style.RESET_ALL}")
            sys.exit(1)

        if args.count <= 0 or args.interval <= 0 or args.timeout <= 0:
            print(f"{Fore.RED}❌ All numeric values must be positive!{Style.RESET_ALL}")
            sys.exit(1)

        interval_s = args.interval / 1000.0
        timeout_s  = args.timeout  / 1000.0

        await ping_target(host, count=args.count, interval=interval_s, timeout=timeout_s)
        return

    print(f"{Fore.RED}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}                    ██████╗ ██╗███╗   ██╗ ██████╗ ███████╗██████╗ {Style.RESET_ALL}")
    print(f"{Fore.WHITE}                    ██╔══██╗██║████╗  ██║██╔════╝ ██╔════╝██╔══██╗{Style.RESET_ALL}")
    print(f"{Fore.WHITE}                    ██████╔╝██║██╔██╗ ██║██║  ███╗█████╗  ██████╔╝{Style.RESET_ALL}")
    print(f"{Fore.WHITE}                    ██╔═══╝ ██║██║╚██╗██║██║   ██║██╔══╝  ██╔══██╗{Style.RESET_ALL}")
    print(f"{Fore.WHITE}                    ██║     ██║██║ ╚████║╚██████╔╝███████╗██║  ██║{Style.RESET_ALL}")
    print(f"{Fore.WHITE}                    ╚═╝     ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝{Style.RESET_ALL}")
    input(f"{Fore.WHITE}                                Press [Enter] to start              {Style.RESET_ALL}")

    while True:
        host = input(f"{Fore.WHITE}                                Enter host or IP : {Style.RESET_ALL}")
        if is_valid_ip(host):
            break
        else:
            print(f"{Fore.RED}                             ❌ Invalid host or IP{Style.RESET_ALL}")

    while True:
        count_input = input(f"{Fore.WHITE}                                Number of pings : [default 10]: {Style.RESET_ALL}")
        if count_input == "":
            count = 10
            break
        elif count_input.isdigit() and int(count_input) > 0:
            count = int(count_input)
            break
        else:
            print(f"{Fore.RED}                             ❌ Invalid number of pings!{Style.RESET_ALL}")

    while True:
        interval_input = input(f"{Fore.WHITE}                                Ping interval : [default 500]ms: {Style.RESET_ALL}")
        if interval_input == "":
            interval_ms = 500
            break
        try:
            interval_ms = int(interval_input)
            if interval_ms <= 0:
                raise ValueError
            break
        except ValueError:
            print(f"{Fore.RED}                             ❌ Invalid interval!{Style.RESET_ALL}")

    while True:
        timeout_input = input(f"{Fore.WHITE}                                Ping timeout : [default 1000]ms: {Style.RESET_ALL}")
        if timeout_input == "":
            timeout_ms = 1000
            break
        try:
            timeout_ms = int(timeout_input)
            if timeout_ms <= 0:
                raise ValueError
            break
        except ValueError:
            print(f"{Fore.RED}                             ❌ Invalid timeout value!{Style.RESET_ALL}")

    os.system("clear")
    await ping_target(host, count, interval_ms / 1000.0, timeout_ms / 1000.0)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}                             ❌ User interrupted. Exiting{Style.RESET_ALL}")
        sys.exit(0)
