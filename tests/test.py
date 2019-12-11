from utils import *

req_data = {
    "method": "get_dynamic_global_properties",
    "params": [],
    "id":1
}
status, result = request_post(req_data)
print('status: {}, result: {}'.format(status, result))

