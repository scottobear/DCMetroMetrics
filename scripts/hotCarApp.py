
# TEST CODE
if __name__ == "__main__":
    import test_setup

import gevent
from restartingGreenlet import RestartingGreenlet
import hotCars
import dbUtils
import dbGlobals
import os
import sys
from datetime import datetime

OUTPUT_DIR = os.environ['OPENSHIFT_DATA_DIR']
REPO_DIR = os.environ['OPENSHIFT_REPO_DIR']
SCRIPT_DIR = os.path.join(REPO_DIR, 'scripts')

class HotCarApp(RestartingGreenlet):

    def __init__(self, LIVE=False):
        RestartingGreenlet.__init__(self, LIVE=LIVE)
        self.SLEEP = 40 # Run every 10 seconds
        self.LIVE = LIVE
        self.dbg = dbGlobals.DBGlobals()
        self.db = self.dbg.getDB()

    # Run forever
    def _run(self):

        while True:
            try:
                self.tick()
            except Exception as e:
                import traceback
                logFileName = os.path.join(OUTPUT_DIR, 'runHotCarApp.log')
                logFile = open(logFileName, 'a')
                logFile.write('HotCarApp: Caught Exception! %s\n'%str(e))
                tb = traceback.format_exc()
                logFile.write('Traceback:\n%s\n\n'%tb)
                logFile.close()
            gevent.sleep(self.SLEEP)

    def tick(self):

        logFileName = os.path.join(OUTPUT_DIR, 'runHotCarApp.log')

        with open(logFileName, 'a') as logFile:
            n = datetime.now()
            timeStr = n.strftime('%d-%B-%Y %H:%M:%S')
            msg = '*'*50 + '\n'
            msg += '%s Running Hot Car App\n'%timeStr
            logFile.write(msg)
            logFile.flush()

            # Run the tick
            self.runOnce(tweetLive=self.LIVE, log=logFile)

            logFile.close()

    def runOnce(self, tweetLive=False, log=sys.stdout):
        # Establish connection with the database
        # Run one cycle of the hotcar app
        hotCars.tick(self.db, tweetLive=tweetLive, log=log)

if __name__ == '__main__':
    from time import sleep
    app = HotCarApp(LIVE=False)
    while True:
        app.runOnce(tweetLive=False, log=sys.stdout)
        sleep(40)
