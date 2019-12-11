#-*- coding: utf-8  -*-

import json
import requests

local_rpc_url = "http://192.168.192.148:8049"
node_rpc_url = "http://test.cocosbcx.net"
headers = {"content-type": "application/json"}

def request_post(url, req_data={}):
    response = json.loads(requests.post(url, data = json.dumps(req_data), headers = headers).text)
    print('>> {} {}\n{}\n'.format(req_data['method'], req_data['params'], response))
    return json_dumps(response['result'])

def json_dumps(json_data):
    return json.dumps(json_data, indent=4)

'''
curl http://test.cocosbcx.net -d '{"jsonrpc": "2.0", "method": "get_dynamic_global_properties", "params": [], "id": 1}'
'''