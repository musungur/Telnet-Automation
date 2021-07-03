'''
telnet ip config automation
'''
import sys
import telnetlib
import os
import getpass

USERNAME = input("Enter username:")
PASS1 = input("Enter the Password:")

PASS2 = input("Enter password:")

hosts = input("Enter inventory file containing lists of devices to be configure:")

with open(f"{hosts}","r") as fi:
    devices = fi.readline()
    print(devices)
    tn = telnetlib.Telnet(devices)

    for line in devices:
        tn.read("Enter username:")
        tn.write(f"{USERNAME}\n")
        tn.read("Enter password:")
        tn.write(f"{PASS1}\n")
        tn.write("enable\n")
        tn.read("Enter password:")
        tn.write(f"{PASS2}\n")
        tn.write("show run\n")
        tn.write("configure terminal\n")

        for ip in range(1,20,2):
            mask = "255.255.255.0"
            ip+=1
            tn.write(f"int lo {ip}\n")
            tn.write(f"description {line}\n") 
            tn.write(f"ip add 192.168.51.{ip} {mask}")
            tn.write("\nip osp 1 area 0\n")
            tn.write("do wr\n")
            tn.write("end\n")
            tn.write("logout")
