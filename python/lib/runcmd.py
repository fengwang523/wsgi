#!/usr/local/bin/python2.7
import paramiko
import time
from datetime import datetime
import re
import sys
import getopt
import os
import socket
import traceback
from os.path import expanduser

#import user defined module readpass.py
home = expanduser("~")
sys.path.append("data/ops/python/lib")
import readpass
import read_args

class runcmd:

    def __init__(self, device, username, password):
        self.device=device
        self.username=username
        self.password=password
        self.promptregex = "^\S*" + device.upper() + "\S*$"
        self.max_buffer = 65535

        try:
            # Create instance of SSHClient object
            client = paramiko.SSHClient()
            # Automatically add untrusted hosts
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # initiate SSH connection
            client.connect(device, username=self.username, password=self.password, look_for_keys=False)
            # Use invoke_shell to establish an 'interactive session'
            self.shell = client.invoke_shell()
        except (paramiko.AuthenticationException,socket.error,paramiko.SSHException,Exception) as e:
            self.close()
            raise Exception( device + " open ssh session failed!\n" + "reason: " + e.strerror)
        except:
            self.close()
            raise Exception( device + " open ssh session failed!\n" + str(sys.exc_info()) )
        else:
            self.shell.keep_this = client
            print device , " open ssh session successful.\n"


    def __del__(self):
        self.close()

    def close(self):
        try:
            if (self.shell != None):
                self.shell.close()
            #if (self.client != None):
            #    self.transport.close()
            #    self.client.close()
        except Exception as e:
            #print traceback.format_exc()
            print str(e)
            pass

    def enable_cmd (self, enable, enable_cmd='enable'):
        #for Huawei GPON OLT
        if enable_cmd == 'super':
            self.shell.send('undo smart')
            self.shell.send("\n")
        self.shell.send(enable_cmd)
        self.shell.send("\n")
        time.sleep (0.5)
        total_output = ''
        output = self.shell.recv(self.max_buffer)
        total_output += output
        self.shell.send(enable)
        self.shell.send("\n")
        time.sleep (0.5)
        output = self.shell.recv(self.max_buffer)
        total_output += output
        outputs = output.splitlines()
        lastline = outputs[-1].strip()
        if re.search(self.promptregex, lastline, re.I|re.M):
            self.prompt = lastline
        else:
            raise Exception( self.device + " enable failed, can not find cli prompt.\n"  + total_output + "\n" )
        for line in outputs:
            if re.search("(failed|sorry|denied|password|error|invalid)", line, re.I):
                raise Exception( self.device + " enable failed, cli returned error!\n" + total_output + "\n" )
        print self.device , " entered enable mode.\n"
        return total_output

    def run_cmd (self, cmd, timeout=120):
        max_loop = 30000
        sleep = 0.1
        total_output = ''
        waited = 0
        waitfor = True
        output = ""
        i = 1
        self.shell.send(cmd)
        self.shell.send("\n")
        # Wait for the command to complete
        while (waitfor and i<=max_loop):
            if self.shell.recv_ready():
                output =  self.shell.recv(self.max_buffer)
                total_output += output
                outputs = output.splitlines()
                lastline = outputs[-1].strip()
                if re.search(self.promptregex, lastline, re.M|re.I):
                    waitfor = False
                    self.prompt = lastline
                    break
                output = ''
            elif waited >= timeout:
                waitfor = False
                raise Exception( device + " : " + cmd +  " : timed out!!\n" )
            else:
                time.sleep(sleep)
                waited += sleep
                i += 1
        #print self.device, " cmd: ", cmd, " successful.\n"
        return (total_output)


if __name__ == '__main__':

    passwords = readpass.get_user_pass()
    username = passwords['default_user']
    password = passwords['default_pass']

    optdict = read_args.read()

    for device in optdict['devices']:
        try:
            session = runcmd(device, username, password)
        except Exception as e:
            print e.message
            continue

        if optdict['log']:
            now = datetime.now().strftime('%Y%m%d%H%M%S')
            sessionlog = home + "/log/" + device + "_" + now + ".log"
            logfile = open(sessionlog, 'wb')
        else:
            logfile = None
        if 'enable_mode' in optdict:
            enable =  passwords[optdict['enable_mode']]
            try:
                output = session.enable_cmd(enable, optdict['enable_cmd'])
            except Exception as e:
                print e.message
                session.close()
                continue
            if optdict['prnt']:
                print output,
            if logfile:
                logfile.write(output)
        for cmd in optdict['cmds']:
            cmd = cmd.replace ("<HOSTNAME>", device)
            try:
                output = session.run_cmd (cmd)
            except Exception as e:
                print e.message
                session.close()
            else: 
                if optdict['prnt']:  
                    print output,
                if logfile:
                    logfile.write(output)
        print "\n"
        if optdict['log']:
            logfile.close()
        session.close()

    print "\n\n******************** Script Complete !*******************"
