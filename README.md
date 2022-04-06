# InitCheck

## A must have repository for every penetration tester!
With the help of this script you can automate every pentest initial check such as reachability or ssh connection to host.

> NB: More checks will be added asap. 

## Running the code:

```bash
$ python3 initcheck.py
[!] Checking arguments..
[E] Missing arguments!
[E] Leaving..
```

```bash
$ python3 initcheck.py output.xlsx
[!] Checking arguments..
[!] Checking arguments..
[!] Loading Config YAML..
[+] Loaded Config YAML!
[!] Starting Checks..
[!] Starting Pinging..
[+] Finished Pinging!
[!] Starting Ssh-ing..
[+] Finished Ssh-ing!
[!] Generating output.xlsx..
[+] Generated output.xlsx!
```

## Yaml config file:

```yaml
hosts: #edit (-host or -host:port(for ssh))
  - 127.0.0.1
  - 127.0.0.2:1111
credentials: #edit
  - ['user', 'resu']
checks: #edit (possible values: ping, ssh, http)
  - ping
  - ssh
```

## Output file sample:

![test](output.JPG)