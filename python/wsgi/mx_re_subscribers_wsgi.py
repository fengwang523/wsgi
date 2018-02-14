from bottle import route, run, template, request
from bottle import response
import sys
sys.path.append('/data/ops/python/lib')
import runcmd
import re
import base64
import json

#https://www.toptal.com/bottle/building-a-rest-api-with-bottle-framework

@route('/hello')
def hello():
  return "Hello you!"

@route('/mx_re_sub_summary')
def mx_re_sub_summary():
  passwords = {}
  try:
    with open("/data/ops/python/wsgi/.runcmd.passwd.json", "r") as f:
      passwords = json.load(f)
    username = passwords["autouser"]
    password = passwords["autopass"].decode('base64')
  except Exception as e:
    print device, " open password file failed!\n", e.message
    result['error'] = device + " open password file failed!\n" + e.message
    return result
  response.set_header('Cache-Control', 'no-cache, no-store, max-age=0, must-revalidate')
  response.set_header('Pragma', 'no-cache')
  #return request.query_string
  device = request.query.device
  result = {}
  try:
    session = runcmd.runcmd(device, username, password)
  except Exception as e:
    print device, " open ssh session failed!\n" , e.message
    result['error'] = device + " open ssh session failed!\n" + e.message
    return result
  print device, " open ssh session successful!\n"
  try:  
    sessionoutput = session.run_cmd('set cli screen-width 300')
    sessionoutput += session.run_cmd('set cli screen-length 0')
    sessionoutput += session.run_cmd ('show system uptime')
    output = session.run_cmd ('show subscribers summary')
    sessionoutput += output
    outputs = output.splitlines()
    result['result'] = "Subscribers Summary:\n"
    for line in outputs:
      searchObj = re.search(r'DHCP: +(\d+)', line)
      if searchObj:
        result['result'] += "  DHCP: " + searchObj.group(1) + "\n"
      searchObj = re.search(r'VLAN: +(\d+)', line)
      if searchObj:
        result['result'] += "  VLAN: " + searchObj.group(1) + "\n"
  except Exception as e:
    session.close()
    print device, " ssh session running command failed!\n" , str(e) 
    result['error'] = device + " ssh session running command failed!\n" + e.message + sessionoutput
    result['raw']=sessionoutput
    return result
  session.close()
  print device, " ssh session running command successful.\n"
  print device, " result is:\n"
  print json.dumps(result, indent=2)
  result['raw']=sessionoutput
  if 'result' in result:
    pass
  else:
    result['result'] = 'null'
  if 'raw' in result:
    pass
  else:
    result['raw'] = 'null'
  if 'error' in result:
    pass
  else:
    result['error'] = 'null'
  return result

@route('/listdevices')
def listdevices():
  listfile = "/data/ops/python/data/version.txt"
  print "listdevices called\n";
  response.set_header('Cache-Control', 'no-cache, no-store, max-age=0, must-revalidate')
  response.set_header('Pragma', 'no-cache')
  type = request.query.type
  vendor = request.query.vendor
  devices = {}
  devices['devices'] = []
  try:
    with open(listfile, 'r') as f:
      for line in f:
        columns=line.strip().split("\t")
        device = columns[0]
        if vendor == columns[8]:
          if device[8:10] == type:
            devices['devices'].append(device)
          else:
            continue
        else:
          continue
  except:
    print "listdevices() failed!"
    devices['devices'] = ["not_found"]
  return devices 

