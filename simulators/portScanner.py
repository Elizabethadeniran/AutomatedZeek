import threading
import nmap



def simulate_port_scanning():
    
    ip_addr = input("Enter the IP address you want to scan: ")
    
    if ip_addr:
        portScanner(ip=ip_addr, protocol='tcp')
        portScanner(ip=ip_addr, protocol='udp')

    print("port scanning completed")

def portScanner(ip, protocol):
    scanner = nmap.PortScanner()
    if protocol == "tcp":
        scanner.scan(ip, '1-9000', '-v', 'sS')
        print("Ip status: ", scanner[ip].state())
        print("Open Ports: ", scanner[ip][protocol].keys())
    
    else:
        scanner.scan(ip, '1-9000', '-v', 'sU')
        print("Ip status: ", scanner[ip].state())
        print("Open Ports: ", scanner[ip][protocol].keys())


if __name__ == "__main__":
    simulate_port_scanning()