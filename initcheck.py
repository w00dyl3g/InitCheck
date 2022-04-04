import os, yaml, pprint, paramiko

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
            _ssh.connect(hostname=hostname, port=port, username=username, password=password)
            return True
        except:        
            return False        


def ssh():
    global output
    output['ssh'] = {}
    for host in config['hosts']:
        for username,password in config['credentials'].items():
            output['ssh'][host+" ("+username+":"+password+")"] = check_ssh(host,username,password)

def check_ping(hostname):
    hostname = hostname.split(":")[0]
    response = os.system("ping -c 1 " + hostname + " > /dev/null 2>&1")
    if response == 0:
        return True
    else:
        return False

def ping():
    global output
    output['ping'] = {}
    for host in config['hosts']:
        output['ping'][host.split(":")[0]] = check_ping(host)

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

def main():
    parse_yaml("config.yaml")
    pprint.pprint(config)
    do_checks()
    pprint.pprint(output)

if __name__ == "__main__":
    main()