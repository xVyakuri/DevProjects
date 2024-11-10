import subprocess

def find_gateway():
    # This only works on linux cuz windows ipconfig is all too much
    # Test all of this on rocky 9
    try:
        result = subprocess.check_output("ip route", shell=True).decode()
        
        for line in result.splitlines():
            if "default" in line:
                # IP address is in the 3rd slot where it says "default via IP BLA BLA BLA"
                gateway = line.split()[2]
                return str(gateway)
            
    except subprocess.CalledProcessError:
        print("Error: Unable to retrieve the default gateway.")


def ping(ip):
    try:
        # -n for windows, -c for Linux
        # Just gonna test all of the pings with windows first as I'm coding
        # Switch it to -c when testing on Rocky 9
        output = subprocess.check_output(['ping', '-c', '4', ip], stderr=subprocess.STDOUT, universal_newlines=True)
        print(f"Ping results for {ip}:\n{output}")
        
    except subprocess.CalledProcessError:
        print("Failed to ping " + str(ip))
        
        
def check_dns_res(domain_name):
    try:
        # use nslookup
        result = subprocess.run(['nslookup', domain_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Print the results of the nslookup
        print(f"DNS resolution for {domain_name} using nslookup:")
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        print(f"Error executing nslookup: {e}")

def main():
    # Introduce the Script
    print("HELLO! This is a Ping Test for Your Device...")

    userInput = ""
    iteration = 0
    while (iteration == 0):
        print("\n\n\t1. Display Default Gateway\n" +
            "\t2. Test Local Connectivity\n" +
            "\t3. Test Remote Connectivity\n" +
            "\t4. Test DNS Resolution\n")
        
        userInput = input("Please Enter from (1 - 4) or 'Q/q' to quit this script...\n\n")
        # If Q, then close while loop
        if (userInput == "q"):
            print("Bye Bye Now...")
            subprocess.run("clear")
            iteration = iteration + 1
        
        # If 1, find default gateway and print it out
        elif (userInput == "1"):
            print("Default Gateway is " + find_gateway())
            
        # If 2, Ping the default gateway to check local connectivity
        elif (userInput == "2"):
            print("Pinging Default Gateway")
            ping(find_gateway())
        
        # If 3, Ping RIT's DNS Server IP address which is 129.21.3.17
        elif (userInput == "3"):
            print("Pinging RIT's DNS Server")
            ping("129.21.3.17")
        
        # If 4, nslookup google name
        elif (userInput == "4"):
            check_dns_res("www.google.com")
            
        else:
            print("Please Enter a Valid input...")
            
main()
