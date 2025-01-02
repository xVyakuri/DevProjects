# Author: Andrew Xie, Date: 12/17/2024

# Purpose of Program: Have basic details of the network and device
# Be able to use tools through the command prompt in order to troubleshoot for specific connectivity issues
# Will find default gateway connectivity, DNS connectivity, etc.

import subprocess
import platform
import os
import re
import time

def clear_terminal(operating_system):
    if operating_system == "Windows":
        os.system("cls")
    elif operating_system == "Linux":
        os.system("clear")

def operating_system():
    # find the specific operating system: Windows, Linux,
    return platform.system()

# Linux Side
def get_l_hostname():
    try:
        hostname = subprocess.check_output(["hostname", "-f"], text=True).strip(".")
        return hostname[0], hostname[1]
    
    except subprocess.CalledProcessError as e:
        print(f"Failed to get Device Information: {e}")

def get_l_network():
    # ip addr, gateway, network mask, and DNS
    try:
        ifconfig = subprocess.check_output(["ifconfig"], text=True)
        ip_addr = re.search(r"inet\s([0-9.]+)", ifconfig)
        net_mask = re.search(r"netmask\s([0-9.]+)", ifconfig)
        
        iproute = subprocess.check_output(["ip", "route"], text=True)
        gateway = re.serach(r"default via ([0-9.]+)", iproute)
        
        dns_servers = []
        with open("/etc/resolv.conf", "r") as f:
            for line in f:
                if line.startswith("nameserver"):
                    dns_servers.append(line.split()[1])
        
        return_line = []
        
        if ip_addr:
            return_line.append(ip_addr.group(1))
        else:
            return_line.append("IP Address Not Found or Not Properly Configured")
        
        if gateway:
            return_line.append(gateway.group(1))
        else:
            return_line.append("Default Gateway not Found or Not Properly Configured")
        
        if net_mask:
            return_line.append(net_mask.group(1))
        else:
            return_line.append("Network Mask Not Found or Not Properly Configured")
        
        if dns_servers:
            temp = []
            for i in range(len(dns_servers)):
                temp.append(dns_servers[i])
            return_line.append(temp)
        else:
            return_line.append("Primary DNS Not Found or Properly Configured")
            return_line.append("Secondary DNS Not Found or Properly Configured")
        
        return return_line
        
    except subprocess.CalledProcessError as e:
        print(f"Failed to get Network Information: {e}")

def get_l_Storage():
    try:
        df = subprocess.check_output(["df", "-h"], text=True)
        drives = []
        for line in df.splitlines()[1:]:
            parts = line.split()
            if len(parts) >= 6:
                # index 0, 1, 3 is drive, total space, and free space respectively
                drives.append((parts[0], parts[1], parts[3]))
                
        return drives
    except subprocess.CalledProcessError as e:
        print(f"Failed to get Drives: {e}")

def get_l_processors():
    try:
        lscpu = subprocess.check_output(["lscpu"], text=True)
        model = re.search(r"Model name:\s+(.+)", lscpu).group(1).strip()
        processors = re.search(r"CPU\(s\):\s+(\d+)", lscpu).group(1).strip()
        cores = re.search(r"Core\(s\) per socket:\s+(\d+)", lscpu).group(1).strip()
        
        return (model, processors, cores)
    except subprocess.CalledProcessError as e:
        print(f"Failed to get Processor Info: {e}")

def l_ping_test(ip):
    try:
        output = subprocess.check_output(['ping', '-c', '4', ip], stderr=subprocess.STDOUT, universal_newlines=True)
        print(f"Ping results for {ip}:\n{output}")
    except subprocess.CalledProcessError:
        print("Failed to ping " + str(ip))
        
def l_resolve_DNS(domain_name):
    try:
        result = subprocess.run(['nslookup', domain_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"DNS resolution for {domain_name} using nslookup:")
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        print(f"Error executing nslookup: {e}")

#  Windows Side
def get_w_network():
    # ip addr, gateway, network mask, and DNS
    try:
        ipconf = subprocess.check_output(["ipconfig", "/all"], text=True)
        
        hostname = re.search(r"Host Name\s*:?\s*(.+)", ipconf)
        domain = re.search(r"Primary DNS Suffix\s*:?\s*(.+)", ipconf)
        ip_addr = re.search(r"IPv4 Address\s*.*:\s*([\d\.]+)", ipconf)
        gateway = re.search(r"Default Gateway\s*.*:\s*([\d\.]+)", ipconf)
        net_mask = re.search(r"Subnet Mask\s*.*:\s*([\d\.]+)", ipconf)
        # There could be multiple DNS servers, this only takes one for now
        dns_server = re.search(r"DNS Servers\s*.*:\s*([\d\.]+)", ipconf)
        
        return_line = []
        if hostname:
            return_line.append(hostname.group(1))
        else:
            return_line.append("Hostname Not Found")
        
        if domain:
            return_line.append(domain.group(1))
        else:
            return_line.append("Domain Not Found")
            
        if ip_addr:
            return_line.append(ip_addr.group(1))
        else:
            return_line.append("IP Address Not Found")
            
        if gateway:
            return_line.append(gateway.group(1))
        else:
            return_line.append("Default Gateway Not Found")
            
        if net_mask:
            return_line.append(net_mask.group(1))
        else:
            return_line.append("Network/Subnet Mask Not Found")
            
        if dns_server:
            return_line.append([dns_server.group(1)])
        else:
            return_line.append(["DNS Servers Not Found"])
            
        return return_line
        
    except subprocess.CalledProcessError as e:
        print(f"Failed to get Network Configurations: {e}")
    
def get_w_Storage():
    try:
        result = subprocess.check_output(["wmic", "logicaldisk", "get", "name,size,freespace"], text=True)
        lines = result.strip().splitlines()
        
        drives = []
        # Skip the header when looping through the drives
        for l in lines[1:]:
            parts = l.split()
            if (len(parts) == 3):
                drives.append((parts[0], parts[1], parts[2]))
        
        return drives
    except subprocess.CalledProcessError as e:
        print(f"Failed to get Storage: {e}")

def get_w_processors():
    try:
        result = subprocess.check_output(["wmic", "cpu", "get", "name,", "NumberOfCores,", "NumberOfLogicalProcessors"], text=True)
        lines = result.strip().splitlines()
        
        processors = []
        for l in lines[1:]:
            parts = l.split()
            if len(parts) >= 3:
                name = " ".join(parts[:-2])
                cores = parts[-2]
                logical_proc = parts[-1]
                
                processors.append((name, cores, logical_proc))
        
        return processors
    except subprocess.CalledProcessError as e:
        print(f"Failed to get Processors: {e}")

def w_ping_test(ip):
    try:
        output = subprocess.check_output(['ping', '-n', '4', ip], stderr=subprocess.STDOUT, universal_newlines=True)
        print(f"Ping results for {ip}:\n{output}")
        
    except subprocess.CalledProcessError:
        print("Failed to ping " + str(ip))
        
def w_resolve_DNS(domain_name):
    try:
        result = subprocess.run(['nslookup', domain_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"DNS resolution for {domain_name} using nslookup:")
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        print(f"Error executing nslookup: {e}")

def main_menu(operating_system):
    iteration = 1
    while iteration == 1:
        clear_terminal(operating_system)
        print("Welcome to Basic Connectivity Troubleshooter")
        
        choice = str(input("\n\t1.\tNetwork Configuration Settings" +
                            "\n\t2.\tDevice Storage Information" +
                            "\n\t3.\tDevice Processor Information" +
                            "\n\t4.\tRun Ping Tests" +
                            "\n\t5.\tRun NSlookup Tests" +
                            "\n\t6.\tQuit Troubleshooter" +
                            "\nPlease Select an input from 1 - 6:\t\t\t"))
        
        # First check if the user input is proper
        if choice == "6":
            iteration += 1
        elif choice == "1" or choice == "2" or choice == "3" or choice == "4" or choice == "5":
            # Check if the current operating system is linux or Windows, run the separate functions
            clear_terminal(operating_system)
            if operating_system == "Linux":
                if choice == "1":
                    # Network Configs
                    hostname, domain = get_l_hostname()
                    ip_addr, gateway, netmask, dns_servers = get_l_network()
                    print_network(hostname, domain, ip_addr, gateway, netmask, dns_servers)
                elif choice == "2":
                    # Storage Info
                    print_storage(get_l_Storage())
                elif choice == "3":
                    # Processor Info
                    print_processors(get_l_processors())
                elif choice == "4":
                    # Ping tests
                    c = str(input("Please Input the target IP Address:\t"))
                    l_ping_test(c)
                else:
                    # NSlookup tests
                    c = str(input("Please Input the target Domain Name:\t"))
                    l_resolve_DNS(c)
                    
                for i in range(6):
                    print(f"...Returning to Main Screen in {5 - i} Seconds...")
                    time.sleep(1)
            elif operating_system == "Windows":
                if choice == "1":
                    # Network Configs
                    hostname, domain, ip_addr, gateway, netmask, dns_servers = get_w_network()
                    print_network(hostname, domain, ip_addr, gateway, netmask, dns_servers)
                elif choice == "2":
                    # Storage Info
                    print_storage(get_w_Storage())
                    pass
                elif choice == "3":
                    # Processor Info
                    print_processors(get_w_processors())
                elif choice == "4":
                    # Ping tests
                    c = str(input("Please Input the target IP Address:\t"))
                    w_ping_test(c)
                else:
                    # NSlookup tests
                    c = str(input("Please Input the target Domain Name:\t"))
                    w_resolve_DNS(c)
                
                for i in range(6):
                    print(f"...Returning to Main Screen in {5 - i} Seconds...")
                    time.sleep(1)
        else:
            print("Please Enter a Valid input from 1 - 6")
    
    print("...Exiting...")
    time.sleep(2)

def print_network(hostname, domain, ip_addr, gateway, netmask, dns_servers):
    print(f"Hostname\t\t:\t\t{hostname}" +
          f"\nDomain\t\t\t:\t\t{domain}" +
          f"\nIP Address\t\t:\t\t{ip_addr}" +
          f"\nDefault Gateway\t\t:\t\t{gateway}" +
          f"\nNetwork/Subnet Mask\t:\t\t{netmask}")
    
    temp_string = ""
    for server in dns_servers:
        temp_string += server + "\n\t\t\t\t"
        
    print(f"DNS Servers\t\t:\t\t{temp_string}")

def print_storage(drives):
    print("Device\t\tTotal Size\t\tFree Space")
    for drive in drives:
        print(f"{drive[0]}\t\t\t{drive[1]}\t\t\t{drive[2]}")
        
def print_processors(processors):
    print("Model Name\t\t\t\t\t\tNumber of Cores\t\tNumber of Logical Processors")
    for proc in processors:
        print(f"{proc[0]}\t\t\t\t{proc[1]}\t\t\t{proc[2]}")

def main():
    system = operating_system()
    
    main_menu(system)

    print("GoodBye")

if __name__ == "__main__":
    main()