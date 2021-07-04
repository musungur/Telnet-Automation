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
    total_numberOf_devices = len(str(devices))

#server_consele-start
    print(f"**\n{devices}**\n**{total_numberOf_devices)**\n")
#server_console-end

    tn = telnetlib.Telnet(devices)

    for line in devices:
        line+=1
        tn.read("Enter username:")
        tn.write(f"{USERNAME}\n")
        tn.write("# you're in enable mode>\n")
        tn.write("show version\n")
        tn.write("enable\n")
        tn.read("Enter privileged config mode password:")
        tn.write(f"{PASS1}\n")
        tn.write("show run\n")
        tn.write("configure terminal\n")

        #decision before effecting changes to Network devices

        tn.read("You're about to make changes to {total_numberOf_devices} devices in the network.,These devices  may stop routing packets! Do you want to proceed?\n")
        deside = input("y/yes or n/no:")

        tn.write(f"{deside}\n")

        if deside == "y" or deside == "yes":
            for ip in range(1,20,2):
                mask = "255.255.255.0"
                ip+=1
                tn.write("banner motd #Do not make any changes to this device unless authorised by Eng.Robert")
                tn.write(f"hostname {line}")
                tn.write(f"int loopback {ip}\n")
                tn.write(f"description {line}\n")
                tn.write(f"ip add 192.168.51.{ip} {mask}")
                tn.write("\nip ospf 1 area 0\n")
                tn.write("do wr\n")
                tn.write("end\n")
                tn.write("logout\n")

#saving configarations
                with open("running_config","w") as sav:
                    devices_cfgs = tn.read_all()
                    sav.write(devices_cfgs)
                    tn.read("configuration file saved successfully")
        elif deside == "n" or deside == "no":
#device console
            tn.read("you stopped to push new cofigurations to {total_numberOf_devices} devices")
            tn.close()
#server/admin console
            print("you did not accept to make changes. Major Configuration changes were stopped by you. Script ended")
        elif deside == "":
#device console
            tn.read("you did not make choise. telnet script will close. please try again later\n")
            tn.close()
#server/admin console
            print("you didnt deside. please run script again\n")
