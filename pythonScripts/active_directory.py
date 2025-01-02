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
"""

import subprocess
import os
import time

# Install Active Directory ADUC, DHCP, DNS
def install_tools():
    pass

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

def main():
    pass


if __name__ == "__main__":
    main()