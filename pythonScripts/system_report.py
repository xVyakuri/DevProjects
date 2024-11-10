import subprocess
import os
import platform
import re

# Andrew Xie, Written 10/3/2024
# Program Objective - Produce a clear and organized report of the device's system
# This should include Device Info, Network Info, OS Info, Storage Info, Processor Info, and Memory Info

# print out System Report and the date that this program was called
def get_date():
    try:
    	date = subprocess.check_output(["date"], text=True).strip()
    	print("\n\t\tSystem Report " + date + "\n")
    except subprocess.CalledProcessError as e:
    	print("\n\t\tSystem Report\n")

# print hostname and domain
def get_device():
    try:
        # If the device does not have a domain name, then the domain will end up being empty
        hostname = subprocess.check_output(["hostname"], text=True).strip()
        domain = subprocess.check_output(["hostname", "-d"], text=True).strip()
        print("\nDevice Information")
        print("Hostname: \t\t\t" + hostname + "\nDomain: \t\t\t" + domain)
    except subprocess.CalledProcessError:
        print("Failed to get Device Information")


# print out IP addr, Gateway Addr, Network mask, DNS1, and DNS2
def get_network():
    try:
        system = platform.system()
        
        if system == "Windows":
            # If I ever gotta come back and make a windows version
            pass
        else:
            # ifconfig for the ip addr and network mask
            ifconfig = subprocess.check_output(["ifconfig"], text=True)
            ip_addr = re.search(r"inet\s([0-9.]+)", ifconfig)
            net_mask = re.search(r"netmask\s([0-9.]+)", ifconfig)
            
            # iproute for gateway
            iproute = subprocess.check_output(["ip", "route"], text=True)
            gateway = re.search(r"default via ([0-9.]+)", iproute)
            
            # /etc/resolve.conf file for DNS
            dns_servers = []
            with open("/etc/resolv.conf", "r") as f:
                for line in f:
                    if line.startswith("nameserver"):
                        dns_servers.append(line.split()[1])
            
            # print out all of the information gathered and check if the variables were able to be found or not  
            print("\nNetwork Information")
            if ip_addr:
                print("IP Address: \t\t\t" + ip_addr.group(1))
            else:
                print("IP Address: Not Found")
        
            if gateway:
                print("Gateway: \t\t\t" + gateway.group(1))
            else:
                print("Gateway not Found")
                
            if net_mask:
                print("Network mask: \t\t\t" + net_mask.group(1))
            else:
                print("Network Mask not Found")
                
            if dns_servers:
                print("DNS1: \t\t\t\t" + dns_servers[0])
                print("DNS2: \t\t\t\t" + dns_servers[1])
            else:
                print("DNS1 and DNS 2 not Found")
                    
    except subprocess.CalledProcessError as e:
        return "Failed to get Network Information"


# print out operating system and version, and kernel version
def get_OS():
    osys = platform.system()
    overs = platform.version()
    
    # Use uname -r to find the kernel version
    kernvers = ""
    try:
        if osys == "Windows":
            pass
        else:
            kernvers = subprocess.check_output(["uname", "-r"], text=True).strip()
    except subprocess.CalledProcessError as e:
        kernvers = "not Found"
        
    print("\nOS Information")
    print("Operating System: \t\t" + osys)
    print("Operating Version: \t\t" + overs)
    print("Kernel Version: \t\t" + kernvers)


# print out hard drive capacity and available space
def get_storage():
    sys = platform.system()
    
    try: 
        if sys == "Windows":
            pass
        else:
            df = subprocess.check_output(["df", "-h"], text=True)
            # For multiple drives data, have tuples for the data for each specific drive
            drives = []
            for line in df.splitlines()[1:]:
                parts = line.split()
                if len(parts) >= 6:
                    # index 0, 1, 3 is drive, total space, free space
                    drives.append((parts[0], parts[1], parts[3]))
                 
            # Print out all of the drives that this device has
            print("\nStorage Information")
            for drive in drives:
                print("Drive: \t\t\t\t" + drive[0]
                      + "\nHard Drive Capacity: \t\t" + drive[1]
                      + "\nFree Space: \t\t\t" + drive[2])
            
            
    except subprocess.CalledProcessError as e:
        print("Failed to get Drive space")


# print out CPU model and # of processors and cores
def get_processor():
    sys = platform.system()
    
    try:
        if sys == "Windows":
            pass
        else:
            # use lscpu to find the CPU model and # of proc and cores
            lscpu = subprocess.check_output(["lscpu"], text=True)
            model = re.search(r"Model name:\s+(.+)", lscpu).group(1).strip()
            processors = re.search(r"CPU\(s\):\s+(\d+)", lscpu).group(1).strip()
            cores = re.search(r"Core\(s\) per socket:\s+(\d+)", lscpu).group(1).strip()
        
            print("\nProcessor Information")
            print("CPU Model: \t\t\t" + model
                  + "\nNumber of Processors: \t\t" + processors
                  + "\nNumber of Cores: \t\t" + cores)
        
    except subprocess.CalledProcessError as e:
        print("Failed to get Processor Info")


# print out total and available ram
def get_memory():
    sys = platform.system()
    
    try:
        if sys == "Windows":
            pass
        else:
            # use free command to find RAM
            free = subprocess.check_output(["free", "-m"], text=True)
            total_ram = re.search(r"Mem:\s+(\d+)", free).group(1)
            available_ram = re.search(r"Mem:\s+\d+\s+\d+\s+(\d+)", free).group(1)
            
            print("\nMemory Information")
            print("Total RAM: \t\t\t" + total_ram
                  + "\nAvailable RAM: \t\t\t" + available_ram)
            
            
    except subprocess.CalledProcessError as e:
        print("Failed to get Memory Info")


def main():
    get_date()
    get_device()
    get_network()
    get_OS()
    get_storage()
    get_processor()
    get_memory()
    
    
main()
