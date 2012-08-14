# import fabric
from fabric.api import *
# import colors (for pretty output)
from fabric.colors import green as _green, yellow as _yellow
# import boto and the ec2 api
import boto
import boto.ec2
# import the AWS config file and the software download list
#from aws_config import *
from secret_config import *
from services import service_list
# import os, time, sys for utilities
import os
import time
import sys

env.user = SERVER_USERNAME
env.key_filename = SSH_PRIVATE_KEY_PATH
env.host_string = 'ec2-50-112-40-82.us-west-2.compute.amazonaws.com'

def roBoto():
    print(_green("Konnichiwa, human!"))
    # check_env_vars("AWS_KEYPAIR", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY")
    # the host string is the return value of server, which is the public DNS
    # env.host_string = server()
    # print(_green("Waiting for server to boot..."))
    # time.sleep(30)
    download_services()
    print(_green("Domo arigato, human!"))

def check_env_vars(*args):
    """
    Check if the boto environment variables have been defined
    if they have, use them instead of the config values
    """
    for var in args:
        if var in os.environ:
            aws_config[var] = os.environ[var]

def server():
    """
    Creates an EC2 Instance
    """
    print(_yellow("Creating EC2 instance..."))
    
    conn = boto.ec2.connect_to_region(AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, 
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY) 
    image = conn.get_all_images(AWS_AMIS)
    group = conn.get_all_security_groups(groupnames=[AWS_SECURITY])[0]
    reservation = image[0].run(1, 1, key_name=AWS_KEYPAIR, security_groups=AWS_SECURITY,
        instance_type=AWS_INSTANCE_TYPE)
    instance = reservation.instances[0]
    conn.create_tags([instance.id], {"Name":INSTANCE_NAME_TAG})

    while instance.state == u'pending':
        print(_yellow("Instance state: %s" % instance.state))
        time.sleep(10)
        instance.update()

    print(_green("Instance state: %s" % instance.state))
    print(_green("Public dns: %s" % instance.public_dns_name))

    return instance.public_dns_name  

def download_services():
    """
    Downloads the software you want on your instance
    """
    print(_yellow('Installing services...'))

    for item in service_list:
        try:
            print(_yellow(item['message']))
        except KeyError:
            pass
        globals()[item['action']](item['params'])
        
        for pkg in params:
            _sudo("apt-get install -qq %s" % pkg)

# Install packages
# Create virtualenv
# Install django in virtualenv
# Install gunicorn in virtualenv
# Setup and run supervisor    