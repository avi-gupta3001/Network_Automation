#!/bin/python3

#!Author: [Avinash Gupta]!
#!Date: [26/08/2019]!

# Read device info from Excel and fetch device data via Netmiko | Python3
# Must install Netmiko and xlrd before run the Script


import xlrd
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import AuthenticationException


workbook = xlrd.open_workbook(r"devices_details.xlsx")

sheet = workbook.sheet_by_index(0)

for index in range(1, sheet.nrows):
    hostname = sheet.row(index)[0].value
    ipaddr = sheet.row(index)[1].value
    username = sheet.row(index)[2].value
    password = sheet.row(index)[3].value
    enable_password = sheet.row(index)[4].value
    vendor = sheet.row(index)[5].value

    device = {
        'device_type': vendor,
        'ip': ipaddr,
        'username': username,
        'password': password,
        'secret': enable_password }

    print ("Connecting to Device: " + ipaddr)
    try:
        net_connect = ConnectHandler(**device)
        #net_connect.enable()

        print (">> show ip configuration of device <<")
        output = net_connect.send_command("show ip int br")
        print (output, "\n")

        net_connect.disconnect()
        continue

    except (AuthenticationException):
        print ('Authentication failure: ' + ipaddr)
        continue
    except (NetMikoTimeoutException):
        print ('Timeout to device: ' + ipaddr)
        continue
    except (EOFError):
        print ('End of file while attempting device: ' + ipaddr)
        continue
    except (SSHException):
        print ('SSH Issue. Are you sure SSH is enabled? ' + ipaddr)
        continue
    except Exception as unknown_error:
        print ('Some other error: ' + str(unknown_error))
        continue
