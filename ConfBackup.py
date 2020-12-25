#!/usr/bin/env python
"""
This script is meant to be ran to conduct regular daily backups of Cisco devices.
It first checks for a backup directory and if one does not exist it creates it.
It opens a devices file to get a full list of devices that need to be backed up.
Fill the devices file with the IP address of the device you want to back up.
The script logs into the device and retrieves the hostname.  It uses the hostname to
look for a directory in the backup directory with named the hostname of the device.
If the directory does not exist it will create the directory for the device.  It
logs in to the device to grab a copy of the running config and creates the backup
file using the hostname and todays date. Finally it writes the running config
to startup config.

"""
import os
from pathlib import Path
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

#Checks if the backup directory exists
backupDirectory = Path('C:/DeviceBackups/CiscoBackups')
checkDir = backupDirectory.exists()
newDirectory = 'C:\\DeviceBackups\\CiscoBackups'

#If the directory does not exist it creates the directory
if checkDir == False:
    print('Creating Backup Directorys')
    os.makedirs(newDirectory)
    print('Backup Directory Created in ' + str(backupDirectory))
else:
    print('Backup Directory Validated!')

#Opens the devices file and reads each device that will be backed up
with open('devices_file') as f:
    devices_list = f.read().splitlines()

#Starts the for loop to backup each device
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

    cliHostname = net_connect.send_command('show run | i hostname')
    splitHostname = cliHostname.split()
    hostname = splitHostname[1]

    deviceDir = Path(hostname)
    fullPath = backupDirectory / deviceDir
    checkDevDir = fullPath.exists()
    newDevDir = '\\'.join([str(backupDirectory), hostname])

    if checkDevDir == False:
        print('Creating Device Backup Directorys')
        os.makedirs(newDevDir)
        print('Backup Directory Created in ' + str(fullPath))
        os.chdir(newDevDir)
    else:
        print('Backup Directory Validated!')
        os.chdir(newDevDir)

    cliConfig = net_connect.send_command('show run')
    today = str(date.today())
    backupFile = open(hostname + "-" + today, 'w')
    backupFile.write(cliConfig)
    backupFile.close()
    saveConfig = net_connect.send_command('copy running-config startup-config')
    print("Backup of " + hostname + " complete!")
