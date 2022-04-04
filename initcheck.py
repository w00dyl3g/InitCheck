import os, yaml, pprint, paramiko
#support old or unsafe ciphers
paramiko.Transport._preferred_kex = ('diffie-hellman-group-exchange-sha256','diffie-hellman-group14-sha256','diffie-hellman-group-exchange-sha1',
'diffie-hellman-group14-sha1','diffie-hellman-group1-sha1')
#init ssh
_ssh = paramiko.SSHClient()
_ssh.load_system_host_keys()
_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#global config
config = {}
output = {}

def check_ssh(hostname, username, password):
    if ":" in hostname:
        hostname,port = hostname.split(":")[0],hostname.split(":")[1]
        #print(hostname, port)
        try:
            _ssh.connect(hostname=hostname, port=port, username=username, password=password)
            return True
        except:        
            return False
    else:
        try:
            _ssh.connect(hostname=hostname, username=username, password=password)
            return True
        except:        
            return False        

"""
def ssh():
    print("[!] Starting Ssh-ing..")
    global output
    output['ssh'] = {}
    for host in config['hosts']:
        #for username,password in config['credentials'].items():
        for cred in config['credentials']:
            username = cred[0] #new with tuple
            password = cred[1] #new with tuple
            output['ssh'][host+" ("+username+":"+password+")"] = check_ssh(host,username,password)
    print("[+] Finished Ssh-ing!")
"""
def ssh():
    print("[!] Starting Ssh-ing..")
    global output
    output['ssh'] = {}
    for cred in config['credentials']:
        username = cred[0] #new with tuple
        password = cred[1] #new with tuple
        output['ssh']["("+username+":"+password+")"] = dict()
        for host in config['hosts']:
            output['ssh']["("+username+":"+password+")"][host] = check_ssh(host,username,password)
    print("[+] Finished Ssh-ing!")


def check_ping(hostname):
    hostname = hostname.split(":")[0]
    response = os.system("ping -c 1 " + hostname + " > /dev/null 2>&1")
    if response == 0:
        return True
    else:
        return False

def ping():
    print("[!] Starting Pinging..")
    global output
    output['ping'] = {}
    for host in config['hosts']:
        output['ping'][host.split(":")[0]] = check_ping(host)
    print("[+] Finished Pinging!")

def do_checks():
    for check in config['checks']:
        globals()[check]()

def parse_yaml(filename):
    with open(filename, "r") as stream:
        try:
            global config
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

def print2screen():
    global output
    print("[!] Printing ping..")
    for host in output['ping']:
        print(output['ping'][host])
    print("[!] Printing ssh..")
    for cred in output['ssh']:
        print(cred)
        for host in output['ssh'][cred]:
            print(output['ssh'][cred][host])

def main():
    print("[!] Loading Config YAML..")
    parse_yaml("config.yaml")
    print("[+] Loaded Config YAML!")
    
    #debug
    #pprint.pprint(config)
    
    print("[!] Starting Checks..")
    do_checks()
    
    #debug
    #pprint.pprint(output)
    
    print("[+] Ended Checks!")
    print("[BETA] Printing to Screen..")
    print2screen()
    print("[BETA] Printed to Screen!")
    
    print("[END] Copy it to excel file!")

    #todo...

    #print("[!] Generating output.csv..")
    #export2csv()
    #print("[+] Generated output.csv!")



if __name__ == "__main__":
    main()