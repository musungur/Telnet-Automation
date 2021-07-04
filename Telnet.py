'''
telnet ip config automation
'''
import sys
import telnetlib
import os
import getpass

USERNAME = input("Enter username:")
#PASS1 = input("Enter the Password:")
PASS1 = getpass.getpass()#doesnt show typed pswrd
#PASS2 = input("Enter password:")#displays typed pswrd
PASS2 = getpass.getpass()
hosts = input("Enter inventory file containing lists of devices to be configure:")

with open(f"{hosts}","r") as fi:
    devices = fi.readline()
    print(devices)
    tn = telnetlib.Telnet(devices)

    for line in devices:
        tn.read("Enter username:")
        tn.write(f"{USERNAME}\n")
        tn.write("# you're in enable mode>\n")
        tn.write("show version\n")
        tn.write("enable\n")
        tn.read("Enter privileged config mode password:")
        tn.write(f"{PASS1}\n")
        tn.write("show run\n")
        tn.write("configure terminal\n")

        for ip in range(1,20,2):
            mask = "255.255.255.0"
            ip+=1
            tn.write(f"int loopback {ip}\n")
            tn.write(f"description {line}\n") 
            tn.write(f"ip add 192.168.51.{ip} {mask}")
            tn.write("\nip osp 1 area 0\n")
            tn.write("do wr\n")
            tn.write("end\n")
            tn.write("logout\n")
