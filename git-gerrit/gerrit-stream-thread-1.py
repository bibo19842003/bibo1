import configparser
import queue
import json
import logging
import threading
import time
import subprocess
import os

import paramiko


queue = queue.Queue()

# Logging

logging.basicConfig(level=logging.INFO)
logger = paramiko.util.logging.getLogger()
logger.setLevel(logging.INFO)

# Config

cf = configparser.ConfigParser()
cf.read('gerrit-stream.config')

options = dict(timeout=60)
options.update(cf.items('Gerrit'))
options['port'] = int(options['port'])


class GerritStream(threading.Thread):
    """Threaded job; listens for Gerrit events and puts them in a queue."""

    def run(self):
        while 1:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
               # client.connect(**options)
                private_key = paramiko.RSAKey.from_private_key_file(options['key_filename'])
                client.connect(hostname=options['hostname'], port=int(options['port']), username=options['username'], pkey=private_key)
                client.get_transport().set_keepalive(60)
                _, stdout, _ = client.exec_command('gerrit stream-events')
                for line in stdout:
                    queue.put(json.loads(line))
            except:
                logging.exception('Gerrit error')
            finally:
                client.close()
            time.sleep(5)


gerrit = GerritStream()
gerrit.daemon = True
gerrit.start()


while 1:
    event = queue.get()
    if (event['type'] == 'ref-updated'):
        print('111111111', event)
        gerrit_project = event['refUpdate']['project']
        gerrit_ref = event['refUpdate']['refName']
        local_git_project_path = options['localprojectpath'] + "/" + gerrit_project + ".git"
        print(local_git_project_path)
        
        if not os.path.exists(local_git_project_path):
            subprocess.run(['git', 'init', '--bare', local_git_project_path])

        server_git_project_path = "ssh://" + options['username'] + "@" + options['hostname'] + ":" + str(options['port']) + "/" + gerrit_project
        os.chdir(local_git_project_path)
        fetch_ref = gerrit_ref + ":" + gerrit_ref

        if ( options['branch_name'] == "allrefs" ):
            subprocess.run(['git', 'fetch', '-f', server_git_project_path, fetch_ref])
        else:
            branches_name = options['branch_name'].replace(' ','')
            if gerrit_ref.replace('refs/heads/','') in branches_name.split(','):
                subprocess.run(['git', 'fetch', '-f', server_git_project_path, fetch_ref])

    time.sleep(10)


gerrit.join()


