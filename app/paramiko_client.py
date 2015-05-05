#!/usr/bin/env python

import socket
import sys
import traceback
import json

import paramiko


# setup logging
paramiko.util.log_to_file('demo_client.log')
# Paramiko client configuration
UseGSSAPI = True             # enable GSS-API / SSPI authentication
DoGSSAPIKeyExchange = True

with open('cred.json', 'r') as credential_file:
    credentials = json.loads(credential_file.read())

port = credentials['port']
hostname = credentials['hostname']
username = credentials['username']
password = credentials['password']

# now, connect and use paramiko Client to negotiate SSH2 across the connection
try:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    print('*** Connecting...')
    if not UseGSSAPI or (not UseGSSAPI and not DoGSSAPIKeyExchange):
        client.connect(hostname, port, username, password)
    else:
        # SSPI works only with the FQDN of the target host
        hostname = socket.getfqdn(hostname)
        try:
            client.connect(hostname, port, username, gss_auth=UseGSSAPI,
                           gss_kex=DoGSSAPIKeyExchange)
        except Exception:
            # password = getpass.getpass('Password for %s@%s: ' % (username, hostname))
            client.connect(hostname, port, username, password)

    command2 = "r:self.VS1_GT1.temp"
    stdin, stdout, stderr = client.exec_command("python3 ~/Projects/HAMC/connect_to_socket.py {}".format(command2))
    print(stdout.readlines())
    client.close()

except Exception as e:
    print('*** Caught exception: %s: %s' % (e.__class__, e))
    traceback.print_exc()
    try:
        client.close()
    except:
        pass
    sys.exit(1)
