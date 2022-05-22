#!/usr/bin/python3

import os, errno
import sys
import pwd
import grp
import string
import random
import logging
import requests
import tarfile

## Logging ##
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def password_generator(size=10, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def recursive_chown(path, uid, gid):
    for dirpath, dirnames, filenames in os.walk(path):
        logger.info("Change ownership of: {}".format(dirpath))
        os.chown(dirpath, uid, gid)
        for filename in filenames:
            logger.info("Change ownership of: {}".format(filename))
            os.chown(os.path.join(dirpath, filename), uid, gid)

def remove_directory(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            logger.info("Removing file: {}".format(name))
            os.remove(os.path.join(root, name))
        for name in dirs:
            logger.info("Removing folder: {}".format(name))
            os.rmdir(os.path.join(root, name))
    logger.info("Removing folder: {}".format(path))
    os.rmdir(path)

## PREPARATIONS ##
os.system("useradd splunk")

## General Settings ##
uid = pwd.getpwnam("splunk").pw_uid
gid = grp.getgrnam("splunk").gr_gid

BASE_DIR = "/tmp/splunk/"
BASE_APP_URL = "https://attack-range-appbinaries.s3-us-west-2.amazonaws.com/"

BASE_SPLUNK_URL = "https://download.splunk.com/products/splunk/releases/8.2.1/linux/splunk-8.2.1-ddff1c41e5cf-Linux-x86_64.tgz"
SPLUNK_BINARY = BASE_SPLUNK_URL.split('/')[8]

SPLUNK_HOME = "/opt/splunk/"
SPLUNK_APP_HOME = SPLUNK_HOME+"etc/apps/"
SPLUNK_PASSWORD = password_generator()

with open("/home/ec2-user/splunk_password","w") as f: # Write Splunk password to file
    logger.info("Writing Splunk credentials to: /home/ec2-user/splunk_password")
    f.write("Username: admin\nPassword: {}".format(SPLUNK_PASSWORD))

APPS = [
    {"name": "splunk_windows_ta", "file_name": "splunk-add-on-for-microsoft-windows_812.tgz"},
    {"name": "splunk_cim_app", "file_name": "splunk-common-information-model-cim_4200.tgz"},
    {"name": "splunk_python_app", "file_name": "python-for-scientific-computing-for-linux-64-bit_202.tgz"},
    {"name": "splunk_mltk_app ", "file_name": "splunk-machine-learning-toolkit_521.tgz"},
    {"name": "splunk_dashboard_beta", "file_name": "splunk-dashboards-app-beta_090.tgz"}
]

def main():
    if not os.path.exists(BASE_DIR):
        try:
            os.makedirs(BASE_DIR)
            print("folder created: {}".format(BASE_DIR))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    ## Download and Install Splunk ##
    logger.info("Downloading Splunk TAR from: {}".format(BASE_SPLUNK_URL))
    req = requests.get(BASE_SPLUNK_URL)
    resp = req.content
    with open(BASE_DIR+SPLUNK_BINARY,'wb') as f:
        f.write(resp)
    
    logger.info("Extracting Splunk to: {}".format(BASE_DIR))
    tar = tarfile.open(BASE_DIR+SPLUNK_BINARY)
    for item in tar:
        tar.extract(item, "/opt/")
    tar.close()

    ## Download and Install Apps ##
    for app in APPS:
        name = app['name']
        fn = app['file_name']

        with open(BASE_DIR+fn, 'wb') as f:
            logger.info("Downloading app: {}".format(name))
            req = requests.get(BASE_APP_URL+fn)
            resp = req.content
            f.write(resp)
            logger.info("Successfully downloaded: {}".format(name))

        ## Untar apps ##
        tar = tarfile.open(BASE_DIR+fn)
        for item in tar:
            logger.info("Extracting Splunk App to: {}".format(item))
            tar.extract(item, SPLUNK_APP_HOME)
        tar.close()

    ## Start Splunk ##
    logger.info("Starting Splunk")
    os.system("/opt/splunk/bin/splunk start --accept-license --answer-yes --no-prompt --seed-passwd {}".format(SPLUNK_PASSWORD))
    os.system("/opt/splunk/bin/splunk stop")
    logger.info("Enabling Splunk SSL")
    os.system("/opt/splunk/bin/splunk enable web-ssl -auth 'admin:{}'".format(SPLUNK_PASSWORD))
    logger.info("Setting webport to 8443")
    os.system("/opt/splunk/bin/splunk set web-port 8443")
    logger.info("Set SPLUNK_OS_USER variable")
    with open('/opt/splunk/etc/splunk-launch.conf','a') as f:
        f.write('\nSPLUNK_OS_USER=splunk')
    logger.info("Changing $SPUNK_HOME ownership")
    recursive_chown(SPLUNK_HOME, uid, gid)
    logger.info("Restarting Splunk")
    os.system("/opt/splunk/bin/splunk restart")

    ## Cleanup ##
    logger.info("Removing: {}".format(BASE_DIR))
    remove_directory(BASE_DIR)
    print("Splunk username: Admin\nSplunk Password: {}".format(SPLUNK_PASSWORD))

    return 0

if __name__ == "__main__":
    sys.exit(main())