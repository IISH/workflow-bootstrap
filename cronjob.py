# https://apscheduler.readthedocs.io/en/3.x/userguide.html
import subprocess
import os
import time
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

CERTS_DIR = os.environ.get('CERTS_DIR', './certs')
CERTS_EXPIRE = os.environ.get('CERTS_EXPIRE', 3600)


@scheduler.scheduled_job(trigger='cron', minute='*')
def my_scheduled_job():
    for file in os.listdir(CERTS_DIR):
        if file.endswith('.csr') or file.endswith('.pem'):
            file_part = file.split('/')[-1].split('.')[0]
            filename = CERTS_DIR + '/' + file
            if os.path.exists(filename):
                mtime = os.path.getmtime(filename)
                now = time.time()
                timespan = (now - mtime)
                if timespan > CERTS_EXPIRE:
                    os.remove(filename)
                return

            run = [
                '/usr/bin/openssl',
                'x509',
                '-req',
                '-in',
                filename,
                '-CA',
                CERTS_DIR + '/ca.cert',
                '-CAkey',
                CERTS_DIR + '/ca.key',
                '-CAcreateserial',
                '-out',
                CERTS_DIR + '/' + file_part + '.pem',
                '-days',
                '365',
                '-sha256',
                '-extfile',
                CERTS_DIR + '/client-cert.conf',
                '-extensions',
                'req_ext']
            subprocess.run(run)
