# https://apscheduler.readthedocs.io/en/3.x/userguide.html
import subprocess
import os
import time
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

CSR_DIR = os.environ.get('CSR_DIR', './csr')
CERTS_DIR = os.environ.get('CERTS_DIR', './certs')
AUTOSIGN_DIR = os.environ.get('AUTOSIGN_DIR', './autosign')
SIGNED_DIR = os.environ.get('SIGNED_DIR', './signed')
KEYS_DIR = os.environ.get('KEYS_DIR', os.environ.get('PRIVATE_DIR', './private'))
CERTS_EXPIRE = os.environ.get('CERTS_EXPIRE', 3600)


@scheduler.scheduled_job(trigger='cron', minute='*')
def my_scheduled_job():
    for file in os.listdir(AUTOSIGN_DIR):
        if file.endswith('.csr'):
            file_part = file.split('/')[-1].split('.')[0]
            file_in = AUTOSIGN_DIR + '/' + file_part + '.csr'
            file_out = SIGNED_DIR + '/' + file_part + '.pem'
            extfile = CERTS_DIR + '/client-cert.conf'
            ca_file = CERTS_DIR + '/ca.cert'
            ca_key_file = KEYS_DIR + '/ca.key'

            run = [
                '/usr/bin/openssl',
                'x509',
                '-req',
                '-in',
                file_in,
                '-CA',
                ca_file,
                '-CAkey',
                ca_key_file,
                '-CAcreateserial',
                '-out',
                file_out,
                '-days',
                '365',
                '-sha256',
                '-extfile',
                extfile,
                '-extensions',
                'req_ext']
            subprocess.run(run, timeout=10)

            os.remove(file_in)
