#!/usr/bin/env python

from __future__ import with_statement
import os, sys, argparse

#DEV_NULL = open(os.devnull, 'w')
#STDOUT_ORIG = sys.stdout
#STDERR_ORIG = sys.stderr

#sys.stderr = DEV_NULL

# Import Fabric's API module
from fabric.api import *
from fabric.tasks import execute
from fabric.contrib.console import confirm

#sys.stderr = STDERR_ORIG

def hello(name="Abhishek"):
    print >>sys.stdout, "Hello {name}!\n".format(name=name)

# Fabfile to:
#    - update the remote system(s) 
#    - download and install an application

env.skip_bad_hosts = True
env.eagerly_disconnect = True
env.colorize_errors = True
env.forward_agent = True
#env.abort_on_prompts = True

'''
env.hosts = [
    '172.16.15.201',
    '172.16.15.202',
    '172.16.15.203',
    '172.16.15.204',
    '172.16.15.205',
    '172.16.15.206',
    '172.16.15.207',
    '172.16.15.208',
    '172.16.15.209',
    '172.16.15.210',
    '172.16.15.211',
    '172.16.15.212',
    '172.16.15.213',
]
'''

all_hosts = {
'172.16.15.201' : 'junaid',
'172.16.15.202' : 'mayur',
'172.16.15.203' : 'tabrez',
'172.16.15.204' : 'ravi',
'172.16.15.205' : 'ronak',
'172.16.15.206' : 'inki',
'172.16.15.207' : 'ashish',
'172.16.15.208' : 'midhun',
'172.16.15.209' : 'ramesh',
'172.16.15.210' : 'hassan',
'172.16.15.211' : 'ashwin',
'172.16.15.212' : 'subash',
'172.16.15.213' : 'yugandhar',
'172.16.15.246' : 'abhishek',
#    '172.16.15.214',
#    '172.16.15.215',
  # 'ip.add.rr.ess
  # 'server2.domain.tld',
}

# Set the username
env.user   = "root"
#env.user   = "abhishek"

# Set the password [NOT RECOMMENDED]
env.password = "centos6"
#env.password = "qwerty"


'''
env.passwords = {
    'root@172.16.15.202': 'centos6',
}
'''
'''
(Pdb) dir(result)
['__add__', '__class__', '__contains__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__getslice__', '__gt__', '__hash__', '__init__', '__le__', '__len__', '__lt__', '__mod__', '__module__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', '__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '_formatter_field_name_split', '_formatter_parser', 'capitalize', 'center', 'command', 'count', 'decode', 'encode', 'endswith', 'expandtabs', 'failed', 'find', 'format', 'index', 'isalnum', 'isalpha', 'isdigit', 'islower', 'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'partition', 'real_command', 'replace', 'return_code', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'stderr', 'stdout', 'strip', 'succeeded', 'swapcase', 'title', 'translate', 'upper', 'zfill']
'''

notify_hosts = []
notify_users = []

def notify_all():
    with settings(warn_only=True):
        result = run("DISPLAY=:0 notify-send --expire-time=0 'Test' ")
        print >>sys.stderr, result

def users_to_notify(users):
    global notify_hosts, notify_users
    if users == 'all':
        notify_users=all_hosts.values()
        notify_hosts=all_hosts
    else:
        notify_users=filter(lambda x: x in users,  all_hosts.values())
        notify_hosts=[host for host in all_hosts if all_hosts[host] in notify_users]

    print >>sys.stderr, notify_hosts, notify_users
    env.hosts = notify_hosts
        
def notify(message):
    current_host = env.host_string
    current_user = all_hosts[current_host]
    
    #cmd = "su {0} -c 'DISPLAY=:0 notify-send --expire-time=0 \"Test\"'".format(current_user)
    cmd = "su {0} -c 'DISPLAY=:0 kdialog --title \"Attention\" --sorry \"{1}\" &'".format(current_user, message)
    print >>sys.stderr, current_host, current_user, cmd

    with settings(warn_only=True):
        result = run(cmd)
        print >>sys.stderr, result

def get_user():
    with settings(warn_only=True):
        result = run("w")
        print >>sys.stderr, result

def main(argv):
    users = ''
    message = ''

    parser = argparse.ArgumentParser(description='Notify users')
    parser.add_argument('-u', action="store", dest="users", default='all', type=str)    
    parser.add_argument('-m', action="store", dest="message", default='Test', type=str)

    results = parser.parse_args()

    users = results.users
    message = results.message

    ''' 
    try:
        opts, args = getopt.getopt(argv,"hu:m:",["users=","message="])
    except getopt.GetoptError:
        print 'notify -u <users> -m <message>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'notify -u <users> -m <message>'
            sys.exit()
        elif opt in ("-u", "--users"):
            users = arg
        elif opt in ("-m", "--message"):
           message = arg
    '''

    print 'Users are ', users
    print 'Message is ', message
    
    sys.exit(0)

    execute(users_to_notify, users)
    execute(notify, message)

if __name__ == '__main__':
    main(sys.argv[1:])
