#!/usr/bin/env python3

import sys, os, threading

def usage():
    print("Usage: " + sys.argv[0] + " <Host> <Command>\n\n\
        \"Host\" is a hostname, IP or a file containing a list of IPs\n\
        Use single quotes (\') to enclose your command, and double quotes (\")\n\
        inside for any quoted arguments on the target host.\n\
        If you pass a filter, only the output matching the given string \n\
        will be returned.\n\n\
        Example_1: " + sys.argv[0] + " TargetList.txt 'arp -a'\n\
        Example_2: " + sys.argv[0] + " 192.168.0.1 'echo \"Example\"'\n")
    exit()

if len(sys.argv) != 3:
    usage()

username = "Administrator"
password = "P@55w0rd"
cmd = sys.argv[2]
lock = threading.Lock()
threads = []

def exec_on_host(host, command, user, password):
    cmd = "pth-winexe -U {0}%{1} //{2} 'cmd.exe /c \"{3}\"'".format(username, password, host, command)
    print(cmd)
    os.system(cmd)

def get_hosts_from_file(path):
    f = open(path, "r")
    hosts = f.readlines()
    return [(lambda h: h.strip())(h) for h in hosts]

def execute(host, cmd):
    response = exec_on_host(host, cmd, username, password)
    try:
        lock.acquire()
        print(response)
    finally:
        lock.release()

if os.path.isfile(sys.argv[1]):
    hosts = get_hosts_from_file(sys.argv[1])
else:
    hosts = [sys.argv[1]]

for host in hosts:
    t = threading.Thread(target = execute, args = (host, cmd))
    t.start()
    threads.append(t)
    [(lambda t: t.join())(t) for t in threads]
