import re
import ssl
import websocket
import json
import time
import logging
from itertools import cycle

log = logging.getLogger(__name__)

class wallet_rpc(object):
    def __init__(self, urls, user="", password="", **kwargs):
        self._request_id = 0
        if isinstance(urls, list):
            self.urls = cycle(urls)
        else:
            self.urls = cycle([urls])
        self.user = user
        self.password = password
        self.num_retries = kwargs.get("num_retries", -1)

        self.wsconnect()

    def get_request_id(self):
        self._request_id += 1
        return self._request_id

    def wsconnect(self):
        cnt = 0
        while True:
            cnt += 1
            self.url = next(self.urls)
            log.debug("Trying to connect to node %s" % self.url)
            if self.url[:3] == "wss":
                sslopt_ca_certs = {'cert_reqs': ssl.CERT_NONE}
                self.ws = websocket.WebSocket(sslopt=sslopt_ca_certs)
            else:
                self.ws = websocket.WebSocket()
            try:
                self.ws.connect(self.url)
                break
            except KeyboardInterrupt:
                raise
            except:
                if (self.num_retries >= 0 and cnt > self.num_retries):
                    raise 

                sleeptime = (cnt - 1) * 2 if cnt < 10 else 10
                if sleeptime:
                    log.warning(
                        "Lost connection to node during wsconnect(): %s (%d/%d) "
                        % (self.url, cnt, self.num_retries) +
                        "Retrying in %d seconds" % sleeptime
                    )
                    time.sleep(sleeptime)


    """ RPC Calls
    """
    def rpc_exec(self, payload):
        """ Execute a call by sending the payload
            :param json payload: Payload data
        """
        log.debug(json.dumps(payload))
        cnt = 0
        while True:
            cnt += 1

            try:
                self.ws.send(json.dumps(payload, ensure_ascii=False).encode('utf8'))
                reply = self.ws.recv()
                break
            except KeyboardInterrupt:
                raise
            except:
                if (self.num_retries > -1 and
                        cnt > self.num_retries):
                    raise 
                sleeptime = (cnt - 1) * 2 if cnt < 10 else 10
                if sleeptime:
                    log.warning(
                        "Lost connection to node during rpc_exec(): %s (%d/%d) "
                        % (self.url, cnt, self.num_retries) +
                        "Retrying in %d seconds" % sleeptime
                    )
                    time.sleep(sleeptime)

                try:
                    self.ws.close()
                    time.sleep(sleeptime)
                    self.wsconnect()
                    self.register_apis()
                except:
                    pass

        ret = {}
        try:
            ret = json.loads(reply, strict=False)
        except ValueError:
            raise ValueError("Client returned invalid format. Expected JSON!")

        if 'error' in ret:
            raise Exception(ret["error"])
        else:
            return ret["result"]

    def __getattr__(self, name):
        """ Map all methods to RPC calls and pass through the arguments
        """
        def method(*args, **kwargs):

            query = {"method": name,
                     "params": list(args),
                     "jsonrpc": "2.0",
                     "id": self.get_request_id()}
            r = self.rpc_exec(query)
            print('>>>> {} {} \n {}'.format(query['method'], query['params'], r))
            return r
        return method

def test_wallet_api():
    # ws = "ws://127.0.0.1:8048" # 单节点
    ws = ["ws://127.0.0.1:8048"] # 多节点
    wallet_rpc_instance = wallet_rpc(ws)

    result = wallet_rpc_instance.info()
    print('info: {}\n'.format(result))

    result = wallet_rpc_instance.list_account_balances('nicotest')
    print('list_account_balances: {}\n'.format(result))

    result = wallet_rpc_instance.transfer('nicotest', 'test1', "100", "COCOS", ["test memo", 'false'], 'true')
    print('transfer: {}\n'.format(result))

    result = wallet_rpc_instance.get_account_history('nicotest', 3)
    print('get_account_history: {}\n'.format(result))
    
test_wallet_api()

