import os
import sys
import getpass
from crontab import CronTab


currdirec = os.getcwd()
username = getpass.getuser()

job_comment = "buzzbang scraper schedule"
cron = CronTab(user=username)
for job in cron:
    if job.comment == job_comment:
        print("Scheduler already working")
        sys.exit()
    else:
        job = cron.new(command= '/usr/bin/python ' + currdirec + '/bioschemas_scraper/test.py', comment=job_comment)
        job.minute.every(1)
        cron.write()
        print("Scheduler already working")
        sys.exit()

job = cron.new(command= 'bash ' + currdirec + '/bioschemas_scraper/scheduler.sh', comment=job_comment)
job.minute.every(3)
cron.write()
