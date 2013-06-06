import os
import sys
import subprocess
from datetime import datetime
from gevent import Greenlet

OUTPUT_DIR = os.environ.get('OPENSHIFT_DATA_DIR', None)
if OUTPUT_DIR is None:
    OUTPUT_DIR = os.getcwd()

REPO_DIR = os.environ.get('OPENSHIFT_REPO_DIR', None)
if REPO_DIR is None:
    SCRIPT_DIR = os.getcwd()
else:
    SCRIPT_DIR = os.path.join(REPO_DIR, 'scripts')

SLEEP = 30

def runOnce(LIVE=False):

    logFileName = os.path.join(OUTPUT_DIR, 'runTwitterApp.log')
    logFile = open(logFileName, 'a')

    n = datetime.now()
    timeStr = n.strftime('%d-%B-%Y %H:%M:%S')

    msg = '*'*50 + '\n'
    msg += '%s Running Twitter App\n'%timeStr
    msg += 'Mode: %s\n'%('LIVE' if LIVE else 'NOT LIVE')

    logFile.write(msg)
    logFile.flush()

    twitterApp = os.path.join(SCRIPT_DIR, 'twitterApp.py')
    if LIVE:
        cmd = ['python', twitterApp]
    else:
        cmd = ['python', twitterApp, '--test']

    p = subprocess.Popen(cmd, stdout = logFile, stderr = logFile)
    ret = p.wait()

    logFile.flush()
    logFile.write('App exited with return code: %i\n\n'%ret)

##########################################
# Run the Twitter App as a Greenlet. This allows
# us to run the app concurrently with the WSGI server.
class TwitterApp(Greenlet):

    def __init__(self, SLEEP=SLEEP, LIVE=False):
        Greenlet.__init__(self)
        self.LIVE = LIVE # Tweet if True
        self.SLEEP = SLEEP

    def _run(self):
        while True:
            runOnce(LIVE=self.LIVE)
            gevent.sleep(self.SLEEP)
