#!/usr/bin/env python
"""
This script logs into Cisco devices and saves a copy of the running configuration to a backup folder

"""
import os
from datetime import date
from getpass import getpass
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException

"""
username = input('Enter your SSH username: ')
password = getpass()
"""

with open('devices_file') as f:
    devices_list = f.read().splitlines()

def backupDevice(deviceIP):
    print ('Connecting to device" ' + devices)
    ip_address_of_device = devices
    ios_device = {
        'device_type': 'cisco_ios',
        'ip': ip_address_of_device,
        'username': "swanny",
        'password': "python123"
    }

    try:
        net_connect = ConnectHandler(**ios_device)
    except (AuthenticationException):
        print ('Authentication failure: ' + ip_address_of_device)
        continue
    except (NetMikoTimeoutException):
        print ('Timeout to device: ' + ip_address_of_device)
        continue
    except (EOFError):
        print ('End of file while attempting device ' + ip_address_of_device)
        continue
    except (SSHException):
        print ('SSH Issue. Are you sure SSH is enabled? ' + ip_address_of_device)
        continue
    except Exception as unknown_error:
        print ('Some other error: ' + str(unknown_error))
        continue

    cliConfig = net_connect.send_command('show run')

    cliHostname = net_connect.send_command('show run | i hostname')
    splitHostname = cliHostname.split()
    hostname = splitHostname[1]

    today = str(date.today())
    backupFile = open(hostname + "-" + today, 'w')
    backupFile.write(cliConfig)
    backupFile.close()
    print("Backup of " + hostname + " complete!")

for devices in device_list:
    backupDevice(device)


"""
for devices in devices_list:
    print ('Connecting to device" ' + devices)
    ip_address_of_device = devices
    ios_device = {
        'device_type': 'cisco_ios',
        'ip': ip_address_of_device,
        'username': "swanny",
        'password': "python123"
    }

    try:
        net_connect = ConnectHandler(**ios_device)
    except (AuthenticationException):
        print ('Authentication failure: ' + ip_address_of_device)
        continue
    except (NetMikoTimeoutException):
        print ('Timeout to device: ' + ip_address_of_device)
        continue
    except (EOFError):
        print ('End of file while attempting device ' + ip_address_of_device)
        continue
    except (SSHException):
        print ('SSH Issue. Are you sure SSH is enabled? ' + ip_address_of_device)
        continue
    except Exception as unknown_error:
        print ('Some other error: ' + str(unknown_error))
        continue

    cliConfig = net_connect.send_command('show run')

    cliHostname = net_connect.send_command('show run | i hostname')
    splitHostname = cliHostname.split()
    hostname = splitHostname[1]

    today = str(date.today())
    backupFile = open(hostname + "-" + today, 'w')
    backupFile.write(cliConfig)
    backupFile.close()
    print("Backup of " + hostname + " complete!")
"""
