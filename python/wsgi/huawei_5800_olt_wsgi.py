from bottle import route, run, template, request
from bottle import response
import sys
sys.path.append('/data/ops/python/lib')
import runcmd
import re
import base64
import json

@route('/huawei_5800_olt_snapshot')
def device_snapshot():
  passwords = {}
  try:
    with open("/data/ops/python/wsgi/.runcmd.passwd.json", "r") as f:
      passwords = json.load(f)
    username = passwords["autouser"]
    password = passwords["autopass"].decode('base64')
    enable = passwords["accessenable"].decode('base64')
  except Exception as e:
    print device, " open password file failed!\n", e.message
    result['error'] = device + " open password file failed!\n" + e.message
    return result
  response.set_header('Cache-Control', 'no-cache, no-store, max-age=0, must-revalidate')
  response.set_header('Pragma', 'no-cache')
  #return request.query_string
  device = request.query.device
  result = {}
  #result['result']={}
  
  try:
    session = runcmd.runcmd(device, username, password)
  except Exception as e:
    print device, " open ssh session failed!\n" , e.message
    result['error'] = device + " open ssh session failed!\n" + e.message
    return result
  print device, " open ssh session successful!\n"
  try:  
    sessionoutput = session.run_cmd('undo smart')
    sessionoutput += session.run_cmd('scroll')
    sessionoutput += session.run_cmd('undo interactive')
    sessionoutput += session.run_cmd('enable')
    sessionoutput += session.enable_cmd(enable, 'super')
    sessionoutput += session.run_cmd('display time')
    sessionoutput += session.run_cmd('display sysuptime')
    output = session.run_cmd ('display board 0')
    sessionoutput += output
    outputs = output.splitlines()
    check = True
    for line in outputs:
      searchObj = re.search(r'^ +(\d+) +(\w+) +(\S+)', line)
      if searchObj:
        slot = searchObj.group(1)
        boardName = searchObj.group(2)
        status = searchObj.group(3)
        if 'ormal' in status:
          pass
        else:
          error += "  slot " + slot + " BoardName " + boardName + ": " + status + "\n"
          check = False
    if check:
      result['result'] = "board 0 : ok\n"
    else:
      result['result'] = "board 0 : <em style='color: red;'>nok</em>\n"   
      result['result'] += error

    output = session.run_cmd ('display alarm active alarmlevel critical')
    sessionoutput += output
    outputs = output.splitlines()
    check = False
    for line in outputs:
      searchObj = re.search(r'No alarm record', line)
      if searchObj:
        check = True
    if check:
      result['result'] += "alarm active critical : ok\n"
    else:
      result['result'] += "alarm active critical : <em style='color: red;'>nok</em>\n"

    output = session.run_cmd ('display alarm active alarmlevel major')
    sessionoutput += output
    outputs = output.splitlines()
    check = False
    for line in outputs:
      searchObj = re.search(r'No alarm record', line)
      if searchObj:
        check = True
    if check:
      result['result'] += "alarm active major : ok\n"
    else:
      result['result'] += "alarm active major : <em style='color: red;'>nok</em>\n"

    output = session.run_cmd ('display alarm active alarmlevel minor')
    sessionoutput += output
    outputs = output.splitlines()
    check = False
    for line in outputs:
      searchObj = re.search(r'No alarm record', line)
      if searchObj:
        check = True
    if check:
      result['result'] += "alarm active minor : ok\n"
    else:
      result['result'] += "alarm active minor : <em style='color: red;'>nok</em>\n"

    output = session.run_cmd ('display alarm active alarmlevel warning')
    sessionoutput += output
    outputs = output.splitlines()
    check = False
    for line in outputs:
      searchObj = re.search(r'No alarm record', line)
      if searchObj:
        check = True
    if check:
      result['result'] += "alarm active warning : ok\n"
    else:
      result['result'] += "alarm active warning : <em style='color: red;'>nok</em>\n"


  except Exception as e:
    session.close()
    print device, " ssh session running command failed!\n" , str(e) 
    result['error'] = device + " ssh session running command failed!\n" + e.message + sessionoutput
    result['raw']=sessionoutput
    return result
  session.close()
  print device, " ssh session running command successful.\n"
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

