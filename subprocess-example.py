import requests
from subprocess import Popen, PIPE
import os
import sys

# longpoll to get filename of new stream
r = requests.get('http://bithose.bitantics.com/u/tester/incoming')

# create download stream
r = requests.get('http://bithose.bitantics.com/u/tester/{}'.format(r.text), stream=True)

# stream data to subprocess
while True:
    data = r.raw.read(10000)
    sys.stdout.buffer.write(data)
    sys.stdout.flush()
