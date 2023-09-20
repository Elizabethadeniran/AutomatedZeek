# Overview
PacketWarden is an interactive terminal application that accepts user inputs as configuration settings for network monitoring and analysis with Zeek

## setup
- navigate to the project folder(root directory)

- initialize a virtual environment:
  ```bash  python -m venv env```  

- navigate to the bin directory within the env folder created
  for Windows : ```cmd cd env\Scripts```
  for Linux/Mac : ```bash cd env/bin```

- activate the virtual environment
  for Windows :  ```cmd activate```
  for Linux/Mac : ```bash source activate```

- install required packages (libraries)
    sample command pip3 install requests
    paxkage list include :

    - requests
    - flask
    - pynmap
    - tqdm
    - 


## Running the Script
the script warden.py is the main zeek rule generating script. run the script using the command :
```bash python warden.py``` from the terminal.

once started, you will need to provide answers to some network monitoring configuration prompts and then appropriate zeek rules will be written to a file warden.zeek within the zeek_scripts directory



## starting the zeek engine
- copy the generated warden.zeek script into the path where zeek is installed in your machine. i.e /opt/zeek/share/zeek/site

- open a new terminal window, navigate to /opt/zeek/share/zeek/site and confirm that warden.zeek was copied.

- in the same terminal window navigate into /opt/zeek/etc

- run the command ```bash nano node.cfg```

- look for a line with type=standalone directly below [zeek]. if the value is cluster, change to standalone

- ctrl+ O save, Hit Enter to confirm and ctrl + x to exit

- run the command ```bash nano zeekctl.cfg```

- look for the line with SitePolicyScripts = local.zeek

- duplicate the line but with value set to warden.zeek and comment the original setting

- ctrl+ O save, Hit Enter to confirm and ctrl + x to exit

- navigate back to home ```bash cd ~```


- run the following commands
  - ```bash zeek install``` to activate the changes made
  - ```bash zeek start``` to start zeek engine


## run network simulators
note for better experince run all simulators in seperate terminal windows as outlined below:

### to simulate large file transfer anomaly check 
  - copy a file of size >10MB into the simulators directory
  - rename the file as 'largeFile' (pdf)
  - run the ftpReceiver.py script first and then ftpSender.py in 2 seperate terminals

### to simulate http brute force attack
- start the server.py script

- run the bruteForce.py script

- run the userAgent.py to simulate http request with varying user_agents header property

- run portScanner.py for port scanning using python-nmap library

- run dns.py which is a simple dns server cretaed for the purpose to performing dns request with suspicious TLDs and multiple subdomains. (run as a privilege user i.e sudo python3 dns.py)

- once the dns server is running, open new terminal, navigate to simulators directory and run the command ```bash chmod +x dns.sh``` to make the script an executable

- now run the script ```bash dns.sh``` to start the dns lookpup. this essentially sends a dns request with randomly select subdomain string for "packetwarden.<suspicious tld here>" @127.0.0.1 using the "dig" command

DNS COMMANDS

a. to start the server = sudo python3 dns.py

b. to run the dns bash script = ./dns.sh


Note: these commands are to be run on 2 seperate terminal windows and the environment (env) activated

dns.py requires priviledge access hence the "sudo" keyword, as the python script will be attempting to open up a socket port.


- run all scripts in seperate terminals.