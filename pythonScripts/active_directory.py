# Author: Andrew Xie, Date: 01/02/2025

"""
Purpose of Program: Set up Default Active Directory Configuration Settings based on given User Inputs for Network configurations
- Sets up DHCP
- Sets up DNS reverse and forward lookup zones
- Sets up Organizational Units if prompted to
- Adds Group Policies to OU's
- Add Functionality to Group Policy (Will be updated to include more functionalities)

Some Additional Notes:
- This program assumes the DNS Server is run on the the same machine as the Active Directory Server
- Active Directory is run on Windows (duh)
- Program HEAVILY relies on proper User usage and is only supposed to be used to make the setting up process faster
"""

import subprocess
import os
import time
import re

def run_cmd(cmd):
    try:
        result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error Running the command: {cmd}\n{e}")

# Install Active Directory ADUC, DHCP, DNS given a Domain Name to Promote Server to a Domain Controller
def install_tools(dm):
    try:
        print(run_cmd("Install-WindowsFeature RSAT-ADDS"))
        print(run_cmd("Install-WindowsFeature DHCP -IncludeManagementTools"))
        print(run_cmd("Install-WindowsFeature DNS -IncludeManagementTools"))
        
        # Assume Active Directory is the DNS Server for this program
        ipconf = subprocess.check_output(["ipconfig", "/all"], text=True)
        ip_addr = re.search(r"IPv4 Address\s*.*:\s*([\d\.]+)", ipconf)
        
        # Promote to Domain Controller
        print(run_cmd(f'Install-ADDSForest -DomainName "{dm}" -InstallDNS -Force'))
        
        # Authorize DHCP Server
        print(run_cmd(f'Add-DhcpServerInDC -DnsName "{dm}" -IpAddress {ip_addr}'))
        
    except subprocess.CalledProcessError as e:
        print(f"Error in Installing ADUC, DHCP, and DNS: {e.stderr}")

# Setup DHCP scope given parameters: Default Gateway IP, IP Scope, and Excluded IP scope
def setup_dhcp(dg, ips, eips):
    pass

# Setup DNS reverse and forward lookup zones based on given IP address
def setup_DNS_zones(ip):
    pass

# Create an Organizational Unit given parameters: Name, Description
def setup_OUs(n, d):
    pass

# Create a Group Policy given an OU
def create_GPO(ou):
    pass

# Add specific functionality to a GPO
def add_GPO_function(gpo):
    pass

# Simply like having a different function for the main menu
def main_menu():
    pass

def main():
    pass


if __name__ == "__main__":
    main()