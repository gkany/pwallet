
# from pyGraphSDK.graphsdk import *


from graphsdk.graphene import Graphene
from graphsdk.instance import set_shared_graphene_instance
from graphsdk.storage import configStorage as config
# from pprint import pprint

nodeAddress = "wss://test.cocosbcx.net" # 所需要连接的RPC节点
gph = Graphene(node=nodeAddress, blocking=True) # 实例化对象
set_shared_graphene_instance(gph) # 将gph设置为共享的全局实例

# if gph.wallet.created() is False: # 创建本地钱包数据库，如果没有，则创建一个新的钱包数据库
#     gph.newWallet("xxxxxx")
# gph.wallet.unlock("xxxxxx") # 解锁钱包，若后续操作需要与钱包交互，则需要解锁钱包

# config["default_prefix"] = gph.rpc.chain_params["prefix"] # 向钱包数据库中添加默认信息
# gph.wallet.addPrivateKey(privateKey) # 向钱包中添加私钥
# config["default_account"] = yourname # 向钱包数据库中添加默认信息
