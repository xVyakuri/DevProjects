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

# Install Active Directory ADUC, DHCP, DNS given a Domain Name to Promote Server to a Domain Controller
def install_tools(dm):
    try:
        aduc = subprocess.run(["powershell", "-Command", "Install-WindowsFeature RSAT-ADDS"], capture_output=True, text=True, check=True)
        dhcp = subprocess.run(["powershell", "-Command", "Install-WindowsFeature DHCP -IncludeManagementTools"], capture_output=True, text=True, check=True)
        dns = subprocess.run(["powershell", "-Command", "Install-WindowsFeature DNS -IncludeManagementTools"], capture_output=True, text=True, check=True)
        
        print(aduc.stdout)
        print(dhcp.stdout)
        print(dns.stdout)
        
        # Assume Active Directory is the DNS Server for this program
        ipconf = subprocess.check_output(["ipconfig", "/all"], text=True)
        ip_addr = re.search(r"IPv4 Address\s*.*:\s*([\d\.]+)", ipconf)
        
        # Promote to Domain Controller
        temp_command = f'Install-ADDSForest -DomainName "{dm}" -InstallDNS -Force'
        promote = subprocess.run(["powershell", "-Command", temp_command], capture_output=True, text=True, check=True)
        print(promote.stdout)
        
        # Authorize DHCP Server
        temp_command = f'Add-DhcpServerInDC -DnsName "{dm}" -IpAddress {ip_addr}'
        auth = subprocess.run(["powershell", "-Command", temp_command], capture_output=True, text=True, check=True)
        print(auth.stdout)
        
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