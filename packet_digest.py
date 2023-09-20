import subprocess
import os

# path definitions for logs and packets 
zeek_logs = 'dlogs'#"logs"
pcap_path = os.path.join("packets", "test_packets.pcap")

#bash script to run zeek
bash_script = f"""
#!/bin/bash
cd {zeek_logs}
zeek -C -r {pcap_path}
"""

# write script to temp file
bash_script_file = "digest.sh"
with open(bash_script_file, "w") as script:
    script.write(bash_script)

# make the temp script an executable
subprocess.run(["chmod", "+x", bash_script_file])

# run the bash script
subprocess.run(["./" + bash_script_file])

# delete the temporary script file
os.remove(bash_script_file)

print("Zeek packet digest completed.")