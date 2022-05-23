#before running the code, you should run these three commands from the console
#import upip
#upip.install('picoweb')
#upip.install('pycopy-ulogging')
import picoweb
import network
import json

from time import sleep

wlan = network.WLAN(network.STA_IF)       # create station interface
wlan.active(True)                         # activate the interface
wlan.scan()                               # scan for access points
print('conntected: ',wlan.isconnected())
if not wlan.isconnected():                # check if the station is connected to an AP
  print('connecting..')
  wlan.connect('Ubicomp', 'Ubicomp_Test') # connect to an AP
  sleep(3)
print('conntected: ',wlan.isconnected())
print(wlan.ifconfig())                    # get the interface's IP/netmask/gw/DNS addresses

ip = wlan.ifconfig()[0]                   # store the IP address 
sleep(1)
dist = 5
j_data = {'type':'distance','value':dist} # JSON contains some arbitrary key-value pairs
sleep(1)
app = picoweb.WebApp(__name__)            # create server

@app.route('/')                           
def index(req, resp):
  method = req.method                     # get type of request (GET, PUT, POST, etc..)
  
  if method == 'GET':
    encoded = json.dumps(j_data)          # get the data in the appropriate format
    yield from picoweb.start_response(resp, content_type = "application/json") # update the header with the appropriate content type
    yield from resp.awrite(encoded)       # write the response
  
  elif method == 'POST':
    yield from req.read_form_data()       # obtaining the request body contents
    body = req.form
    print(body)                           # print statements for debugging - the body is formed of a dict with our payload as the first and only key
    print(type(body))
    sleep(0.5)
    print(body.keys())
    sleep(0.5)
    for key, value in body.items():       # extract the key - this is the JSON in the request
      tmp = key
    tmp = "".join(tmp.split()).replace(" ","") # remove extra spaces and line breaks 
    body_parsed = json.loads(tmp)         # parse the JSON
    j_data["new_val"] = body_parsed['key']
    j_data['type'] = 'temp'
    yield from picoweb.start_response(resp,content_type = "application/json")
    yield from resp.awrite(json.dumps(j_data))
app.run(debug=True, host =ip)             # start the server at the ip address we obtained in the beginning 

