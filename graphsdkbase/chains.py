default_prefix = "COCOS"

known_chains = {
    "prod": {
        "chain_id": "6057d856c398875cac2650fe33caef3d5f6b403d184c5154abbff526ec1143c4",
        "core_symbol": "COCOS",
        "prefix": "COCOS"
    },
    "testnet": {
        "chain_id": "1ae3653a3105800f5722c5bda2b55530d0e9e8654314e2f3dc6d2b010da641c5",
        "core_symbol": "COCOS",
        "prefix": "COCOS"
    },
    "local": {
        "chain_id": "179db3c6a2e08d610f718f05e9cc2aabad62aff80305b9621b162b8b6f2fd79f",
        "core_symbol": "COCOS",
        "prefix": "COCOS"
    }
}

env = [ "prod", "testnet", "customize"] #主网 | 测试网(默认) | 自定义
nodeAddresses = {
    env[0]: "wss://api.cocosbcx.net",
    env[1]: "wss://test.cocosbcx.net",
    env[2]: "ws://127.0.0.1:8049"
}

g_current_chain = env[1]
