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
hosts = input("\nEnter inventory file name of devices to be configured:")
if hosts != "":
#        try:
    with open(f"{hosts}","r") as fi:
        devices = fi.readline()
        total_numberOf_devices = len(str(devices))
        print("disabled mode credentials")
        USERNAME = input("Enter username:")
        PASS1 = getpass.getpass()
        print("privileged enable mode credentials")
        prv_USERNAME = input("Enter username:")
        PASS2 = getpass.getpass()
        deviceList = json.dumps(devices)

        #server_consele-start

        print(f"\n**Names of Devices\n{deviceList}\n**\nTotal number: {total_numberOf_devices} devices\n**\n")

        #server_console-end

        tn = telnetlib.Telnet(devices)

        for line in devices:
            line+=1
            tn.read("username:")
            tn.write(f"{USERNAME}\n")
            tn.read("password")
            tn.write(f"{PASS1}\n")
            tn.write("# you're in disabled mode>\n")
            tn.write("show version\n")
            tn.write("enable\n")
            tn.read("username")
            tn.write(f"{prv_USERNAME}\n")
            tn.read("password")
            tn.write(f"{PASS2}\n")
            tn.write("show run\n")
            tn.write("configure terminal\n")
                #decision before effecting changes to Network devices
            tn.read(f"You're about to make changes to {total_numberOf_devices} devices in the network.These devices  may stop routing packets! Do you want to proceed?\n")

            deside = input("y/yes or n/no:")

            tn.write(f"{deside}\n")

            if deside == "y" or deside == "yes" and deside != "":
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
                    #tn.write("logout\n")

                    #saving configarations
                    with open("running_config","w") as sav:
                        devices_cfgs = tn.read_all()
                        sav.write(devices_cfgs)
                        tn.read(f"configuration file for {total_numberOf_devices} devices saved successfully")
                        print(f"config files for {total_numberOf_devices} devices successfully saved!")
                    tn.write("logout\n")

            elif deside == "n" or deside == "no" and deside != "":
                #device console
                 tn.read(f"you declined to push new cofigurations to {total_numberOf_devices} devices")
                 tn.close()
                 #server/admin console
                 print(f"you declined to push new cofigurations to {total_numberOf_devices} devices.")
            else:
                #device console
                tn.read(f"'{deside}' not recognised. You can only put 'y' or 'yes' to accept,'n' or 'no' to decline \n")
                tn.close()
                #server/admin console
                print(f"'{deside}' not recognised. You can only put 'y' or 'yes' to accept,'n' or 'no' to decline")
#        except Exception as error:                            print(f"{error}")
                
else:
    print(f"\nYou didnt specify inventory host file of hosts to be configured.")

#except Exception as err:
#   print(f"\n{err}")

#except:
#    print(f"\nInventory file name '{hosts}' does not exist in your directory.")
