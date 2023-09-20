# import argparse
# from zat.log_to_dataframe import LogToDataFrame
# from zat import zeek_log_reader
import os

# zeek rule generator
zscript_path = os.path.join("zeek_scripts", "warden.zeek")


def create_zeek_rule(threshold, queryLength, portScanLimit):

    rule = f'''
    
    @load base/protocols/conn
    @load base/protocols/http
    @load base/protocols/ftp
    @load base/protocols/smtp
    @load base/frameworks/notice
    @load base/frameworks/files


    # Define a set of suspicious User-Agent strings associated with port scanning tools
    global suspicious_user_agents: set[string] = {{
        "Nmap", "Masscan", "ZMap", "NetCat", "nc", "hping3", "Hunt", "MyCustomUserAgent/1.0"
    }};

    # table of IPs hitting bruteforce limit 
    global failed_IPS : table[addr] of count = {{
        [127.0.0.1] = 1
    }};

    # table of primary domains with tld length greater than limit
    global primary_domains : table[string] of count = {{["test"]=1}};

    # incremental id for randomly generated file name during file analysis extraction
    global idx: count = 0;

    # http based events
    event http_header(c: connection, is_orig: bool, original_name:string, name:string, value:string) 
        {{
        # Check if the User-Agent matches any of the suspicious strings
        if (original_name == "User-Agent" ) 
            {{
            for ( agent in suspicious_user_agents )
                {{
                if (value == agent ) 
                    {{
                    NOTICE([$note=Notice::ACTION_LOG, $msg="Untrusted User-Agent detected in HTTP request",
                            $conn=c ]);
                    }}
                }}            
            }}    
        }}

    # brute force event handler
    event http_reply(c: connection, version: string, code: count, reason: string) 
        {{
        
        # Check if the response code indicates a failed login attempt (customize response code)
        if (code == 401) 
            {{
                # Extract relevant information from the connection and response
                const source_ip = c$id$orig_h;

                if (source_ip !in failed_IPS)
                    {{
                        failed_IPS[source_ip] = 1;
                    }}
                
                if (source_ip in failed_IPS)
                    {{
                        failed_IPS[source_ip] += 1;
                        local failed_attempts: count = failed_IPS[source_ip];
                    
                    if (failed_attempts >= {threshold}) 
                        {{
                        NOTICE([$note=Notice::ACTION_LOG, $msg="Potential Brute force Attack detected",
                                $conn=c ]);
                        }}
                    
                    }}
            }} 

        }}
        


    # dns events
    event dns_request(c: connection, msg: dns_msg, query: string, qtype: count, qclass: count) 
        {{
        if ( c$id$resp_p == 53/udp && query != "" )
            {{
            # Extract the TLD (Top-Level Domain)
            local domain_parts = split_string(query, /(\.)/)[1];

            if (|domain_parts[1]| > {queryLength} && domain_parts[0] !in primary_domains)
                {{
                    primary_domains[domain_parts[0]] = 1;
                }}

            if (|domain_parts[1]| > {queryLength} && domain_parts[0] in primary_domains) 
                {{
                    primary_domains[domain_parts[0]] += 1;

                    # Count subdomain requests with the primary domain name
                    local domain_request_count = |primary_domains|;

                if (domain_request_count > 5) 
                    {{
                    NOTICE([$note=Notice::ACTION_LOG, $msg="Suspicious dsn lookup",
                        $conn=c ]);
                    }}
                }}
        
            }}
        
        }}


    # ftp protocol events
    event file_new(f: fa_file)
        {{
        Files::add_analyzer(f, Files::ANALYZER_EXTRACT,
                        [$extract_filename=fmt("file-%04d", ++idx)]);
        }}    
    '''
    with open(zscript_path, "w") as zscript:
        zscript.write(rule)
    print("zeek script with customized rule written to warden.zeek")
    #return rule
    




def generate_rule():
    
    
    print("Anomalies detected for include:\n 'brute force',\n 'dns query length',\n 'port scanning',\n 'user_agents',\n 'malicious mail attachemnts'")
    
    queryLimit = int(input("Set the max length for safe dns query : "))
    threshold = int(input("Enter the threshold for potential brute force attack : "))
    portScanLimit = int(input("Enter the limit for potential port scanning : "))
    create_zeek_rule(threshold=threshold, queryLength=queryLimit, portScanLimit=portScanLimit)
        



if __name__ == "__main__":
    generate_rule()