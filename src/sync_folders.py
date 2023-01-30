import schedule
import time
import argparse
from folder_logger import logger
from classes.sync import Sync
#import sys
#sys.path.append("/src/classes/sync.py")

parser = argparse.ArgumentParser(description='Synchronize source and replica folders')
parser.add_argument('--source', '-s', dest='source', type=str, required=True, help='Path to the source folder')
parser.add_argument('--replica', '-r', dest='replica', type=str, required=True, help='Path to the replica folder')
parser.add_argument('--interval', '-i', dest='interval', type=int, required=True, help='Synchronization interval in seconds')
parser.add_argument('--log', '-l', dest='log', type=str, required=True, help='Path to the log file')

args = parser.parse_args()
source = args.source
replica = args.replica
interval = args.interval   
log = args.log

logger(log, "Starting script!\n \nSync executed every:        {0} seconds.".format(interval))
logger(log, "Log file location:         {0}".format(log))
logger(log, "Source folder location:    {0}".format(source))
logger(log, "Replica folder location:   {0}\n".format(replica))

sync = Sync(source, replica, log)
sync.run()

schedule.every(interval).seconds.do(sync.run)
while True:
    schedule.run_pending()
    time.sleep(interval) 