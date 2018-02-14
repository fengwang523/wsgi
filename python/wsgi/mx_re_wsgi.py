from bottle import route, run, template, request
from bottle import response
import sys
sys.path.append('/data/ops/python/lib')
import runcmd
import re
import base64
import json

@route('/mx_re_snapshot')
def device_snapshot():
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
  result['result']=''
  
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
    sessionoutput += session.run_cmd('show system uptime')
    output = session.run_cmd ('show chassis routing-engine 0')
    sessionoutput += output
    outputs = output.splitlines()
    check = True
    info = ''
    error = ''
    count = 0
    for line in outputs:
      searchObj = re.search(r'^ +Current state +(\S+)', line)
      if searchObj:
        count += 1
        state = searchObj.group(1)
        if 'Backup' in state or 'Master' in state:
          info += "  state: " +  state + "\n"
        else:
          error += "  state: " + state + "\n"
          check = False

      searchObj = re.search(r'^ +Memory utilization +(\d+) +percent', line)
      if searchObj:
        count += 1
        memorypercent = searchObj.group(1)
        if int(memorypercent) <= 70:
          info += "  Memory utilization %: " + memorypercent + "\n"
        else:
          error += "  Memory utilization %: " + memorypercent + "\n"
          check = False
    if count < 2:
      check = False
      error += "  error: regex match line count is only: " + str(count) +"\n"
    if check:
      result['result'] += "routing-engine 0: ok\n"
      result['result'] += info
    else:
      result['result'] += "routing-engine 0 : <em style='color: red;'>nok</em>\n"   
      result['result'] += error

    output = session.run_cmd ('show chassis routing-engine 1')
    sessionoutput += output
    outputs = output.splitlines()
    check = True
    info = ''
    error = ''
    count = 0
    for line in outputs:
      searchObj = re.search(r'^ +Current state +(\S+)', line)
      if searchObj:
        count += 1
        state = searchObj.group(1)
        if 'Backup' in state or 'Master' in state:
          info += "  state: " +  state + "\n"
        else:
          error = "  state: " + state + "\n"
          check = False

      searchObj = re.search(r'^ +Memory utilization +(\d+) +percent', line)
      if searchObj:
        count += 1
        memorypercent = searchObj.group(1)
        if int(memorypercent) <= 70:
          info += "  Memory utilization %: " + memorypercent + "\n"
        else:
          error += "  Memory utilization %: " + memorypercent + "\n"
          check = False
    if count < 2:
      check = False
      error += "  error: regex match line count is only: " + str(count) +"\n"
    if check:
      result['result'] += "routing-engine 1: ok\n"
      result['result'] += info
    else:
      result['result'] += "routing-engine 1 : <em style='color: red;'>nok</em>\n"
      result['result'] += error

    output = session.run_cmd ('show chassis alarms')
    sessionoutput += output
    outputs = output.splitlines()
    check = False
    info = ''
    error = ''
    for line in outputs:
      searchObj = re.search(r'No alarms currently active', line)
      if searchObj:
        check = True
        continue
      else:
        pass

    output = session.run_cmd ('show chassis fpc')
    sessionoutput += output
    outputs = output.splitlines()
    check = True
    info = ''
    error = ''
    count = 0
    for line in outputs:
      searchObj = re.search(r'^ +(\d+) +(\S+)', line)
      if searchObj:
        count += 1
        slot = searchObj.group(1)
        state = searchObj.group(2)
        if state not in ['Online', 'Empty']:
          check = False
          error += "  FPC " + slot + " state: " + state +"\n"
      searchObj = re.search(r'^ +(\d+) +(\S+) +(\d+) +(\d+)', line)
      if searchObj:
        count += 1
        slot = searchObj.group(1)
        state = searchObj.group(2)
        temp = searchObj.group(3)
        cpu = searchObj.group(4)
        if int(temp) > 50:
          check = False
          error += "  FPC " + slot + " temperature: " + temp +"\n"
        if int(cpu) > 60:
          check = False
          error += "  FPC " + slot + " cpu %: " + cpu +"\n"
    if count < 6:
      check = False
      error += "  error: regex match line count is only: " + str(count) +"\n"
    if check:
      result['result'] += "chassis fpc: ok\n"
    else:
      result['result'] += "chassis fpc : <em style='color: red;'>nok</em>\n"
      result['result'] += error

    output = session.run_cmd ('show chassis fpc pic-status')
    sessionoutput += output
    outputs = output.splitlines()
    check = True
    info = ''
    error = ''
    count = 0
    for line in outputs:
      searchObj = re.search(r'^(Slot) +(\d+)', line)
      if searchObj:
        count += 1
        slot = searchObj.group(1)
      searchObj = re.search(r'^ +PIC +(\d+) +(\S+)', line)
      if searchObj:
        count += 1
        pic = searchObj.group(1)
        state = searchObj.group(2)
        if state != 'Online':
          check = False
          error += "  FPC " + slot + " PIC " + pic + " state: "+ state +"\n"
    if count < 8:
      check = False
      error += "  error: regex match line count is only: " + str(count) +"\n"
    if check:
      result['result'] += "chassis pic: ok\n"
    else:
      result['result'] += "chassis pic : <em style='color: red;'>nok</em>\n"
      result['result'] += error

    output = session.run_cmd ('show chassis ambient-temperature')
    sessionoutput += output
    outputs = output.splitlines()
    check = True
    info = ''
    error = ''
    count = 0
    for line in outputs:
      searchObj = re.search(r'^Ambient Temperature: +(\d+)', line)
      if searchObj:
        count += 1
        temp = searchObj.group(1)
        if int(temp) > 50:
          check = False
          error += "  Chassis Ambient Temperature C: " + temp +"\n"
        else:
          check = True
    if count < 1:
      check = False
      error += "  error: regex match line count is only: " + str(count) +"\n"
    if check:
      result['result'] += "chassis Ambient Temperature ok\n"
      result['result'] += info
    else:
      result['result'] += "chassis Ambient Temperature : <em style='color: red;'>nok</em>\n"
      result['result'] += error

    output = session.run_cmd ('show chassis fabric summary extended')
    sessionoutput += output
    outputs = output.splitlines()
    check = True
    info = ''
    error = ''
    count = 0
    for line in outputs:
      searchObj = re.search(r'^ +(\d+) +(\w+) +(\S.+?\S) +\d', line)
      if searchObj:
        count += 1
        plane = searchObj.group(1)
        state = searchObj.group(2)
        errors = searchObj.group(3)
        if state not in ['Online', 'Spare'] or errors != "NO     NO        NO/  NO":
          check = False
          error += "  chassis fabric summary: " +  plane + " " + state + " " + errors + "\n"
    if count < 6:
      check = False
      error += "  error: regex match line count is only: " + str(count) +"\n"
    if check:
      result['result'] += "chassis fabric summary ok\n"
      result['result'] += info
    else:
      result['result'] += "chassis fabric summary : <em style='color: red;'>nok</em>\n"
      result['result'] += error


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

