import os, yaml, pprint, paramiko, sys, datetime, xlsxwriter

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
            _ssh.connect(hostname=hostname, port=port, username=username, password=password,timeout=10)
            return "OK"
        except:        
            return "NO"
    else:
        try:
            _ssh.connect(hostname=hostname, username=username, password=password, timeout=10)
            return "OK"
        except:        
            return "NO"        

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
        return "OK"
    else:
        return "NO"

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

def export2xlsx():
    filename = sys.argv[1]
    sheetname = datetime.datetime.now().strftime("%d-%m-%Y")

    #init xlsx
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet(sheetname)
    
    row = 1
    col = 0
    worksheet.write(0, 0, "Host")
    worksheet.write(0, 1, "Result")

    #ping
    for host in output['ping']:
        worksheet.write(row, 0, host)
        worksheet.write(row, 1, output['ping'][host])
        row += 1
    
    #ssh
    col += 2 #blankspaces
    for cred in output['ssh']:
        worksheet.write(0, col, cred)
        row = 1  
        for host in output['ssh'][cred]:
            worksheet.write(row, col, output['ssh'][cred][host])
            row += 1
        col += 1
    workbook.close()   

def safe_checks():
    if len(sys.argv) != 2:
        print("[E] Missing arguments!")
        print("[E] Leaving..")
        sys.exit(1)

def main():

    print("[!] Checking arguments..")
    safe_checks()
    print("[!] Checking arguments..")

    print("[!] Loading Config YAML..")
    parse_yaml("config.yaml")
    print("[+] Loaded Config YAML!")
    
    print("[!] Starting Checks..")
    do_checks()
    
    print("[!] Generating output.xlsx..")
    export2xlsx()
    print("[+] Generated output.xlsx!")



if __name__ == "__main__":
    main()