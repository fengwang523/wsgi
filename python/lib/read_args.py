#!/usr/local/bin/python2.7
import re
import sys
import getopt
import os
import json
libdir=os.path.dirname(os.path.realpath(__file__))
sys.path.append(libdir)

script_name =  os.path.basename(sys.argv[0])

def print_help():
    print "Usage: %s <options> <device list file or name> <cmds list file or cmds seperated by ;>" %(script_name)
    print "\t options:"
    print "\t\t -e    <edge|core|embargo|access> : use edge or core or embargo enable password"
    print "\t\t -c    <enable|enable_admin|super> : enable command, default is enable"
    print "\t\t -l    log ssh session output to file as ~/log/<device>.log"
    print "\t\t -s    suppress ssh session output"
    print "\t\t -h    print this help"
    print "\t examples:"
    print "\t\t runcmd.py EDTNAB02CS17 cisco.cmds"
    print "\t\t runcmd.py -s EDTNAB02CS17 cisco.cmds"
    print "\t\t runcmd.py -e edge cisco.list cisco.cmds"
    print "\t\t runcmd.py -e edge -l cisco.list cisco.cmds"
    return

def read():
    devices = []
    cmds = []
    optdict = {}
    optdict['prnt'] = True
    optdict['log'] = False
    optdict['enable_cmd'] = 'enable'
    try:
        opts, args = getopt.getopt(sys.argv[1:],"he:c:ls", ["enable="])
    except getopt.GetoptError as e:
        print(str(e))
        print_help()
        sys.exit(2)
    for opt, value in opts:
        if opt in ('-h', '--help'):
            print_help()
            sys.exit()
        elif opt in ("-e", "--enable"):
            searched = re.search(r"^(?:edge|core|embargo|access)$", value)
            if searched:
                optdict['enable_mode'] = value+"_enable"
            else:
                print "!!!! enable mode can only be edge, core, or embargo!"
                sys.exit(2)
        elif opt in ("-c"):
            searched = re.search(r"^(?:enable|enable_admin|super)$", value)
            if searched:
                optdict['enable_cmd'] = value
            else:
                print "!!!! enable cmd can only be enable, enable_admin or super!"
                sys.exit(2)
        elif opt in ("-l", "--log"):
            optdict['log'] = True
        elif opt in ("-s", "--suppress"):
            optdict['prnt'] = False

    if len(args) != 2 :
        print "!!!! %s requires two arguments!" %(script_name)
        print_help()
        sys.exit(2)

    if os.path.isfile(args[0]):
        myfile = open(args[0], 'r')
        for line in myfile.readlines():
            searched = re.search(r"^(\w{10}\d{2})", line)
            if searched:
                devices.append(searched.group(1).upper())
        myfile.close

    else:
        searched = re.search(r"^(\w{10}\d{2})", args[0])
        if searched:
            devices.append(searched.group(1).upper())
        else:
            print "!!!! devic name :" , args[0], " is invalid!"
            sys.exit(2)
    if devices:
        pass
    else:
        print "!!!! no device name parsed out from argument!"

    if os.path.isfile(args[1]):
      cmdsfile = open(args[1], 'r')
      for line in cmdsfile.readlines():
          searched = re.search(r"^ *\w", line)
          if searched:
            cmds.append(line.strip())
      cmdsfile.close()
    else:
      for cmd in args[1].split(';'):
        searched = re.search(r"^ *\w", cmd)
        if searched:
          cmds.append(cmd.strip())
    if not cmds:
        print "!!!! file : " , args[1], " did not parse out any cmd to run!"
        sys.exit(2)
    optdict['cmds'] = cmds
    optdict['devices'] = devices
    return optdict

if __name__ == '__main__':
  print "lib dir is: ", libdir
  optdict = read()
  print "command line arguments passed out:"
  print (json.dumps(optdict, indent=2))
