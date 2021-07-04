'''
telnet ip config automation
'''
import sys
import telnetlib
import os
import getpass
import json

#PASS1 = input("Enter the Password:")
#PASS2 = input("Enter password:")#displays typed password

#try:
hosts = input("Enter inventory Host file containing lists of devices to be configure:")
    #capture file error to be added
'''    if hosts != "":
        print("please enter hostfile name")
    elif hosts !="":
        print(f"host file {hosts} doesnt exist")
#except Exception as err:
except:
    print("err file not exiat")
'''
with open(f"{hosts}","r") as fi:
    devices = fi.readline()
    total_numberOf_devices = len(str(devices))

    USERNAME = input("Enter username:")
    print("enable mode")
    PASS1 = getpass.getpass()
    print("privileged mode")
    PASS2 = getpass.getpass()

    deviceList = json.dumps(devices)

    #server_consele-start
    print(f"\n**Names of Devices configured\n{deviceList}\n**\nTotal number: {total_numberOf_devices} devices\n**\n")


    #server_console-end

    tn = telnetlib.Telnet(devices)

    '''
    password and username check will be configured here in the next new Telnet version
    '''

    for line in devices:

        line+=1
        tn.read("username:")
        tn.write(f"{USERNAME}\n")
        tn.write(f"{PASS1}\n")
        tn.write("# you're in disabled mode>\n")
        tn.write("show version\n")
        tn.write("enable\n")
        tn.read("Enter privileged config mode password:")
        tn.write(f"{PASS2}\n")
        tn.write("show run\n")
        tn.write("configure terminal\n")

        #decision before effecting changes to Network devices

        tn.read(f"You're about to make changes to {total_numberOf_devices} devices in the network.These devices  may stop routing packets! Do you want to proceed?\n")

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
                    tn.read(f"configuration file for {total_numberOf_devices} devices saved successfully")

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
