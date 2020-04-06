env = [ "mainnet", "testnet", "customize"]
node_addresses = {
    env[0]: "wss://api.cocosbcx.net",
    env[1]: "wss://test.cocosbcx.net", 
    env[2]: "ws://127.0.0.1:8049"
}

wallet_wallet_commands = ['lock', 'unlock', 'set_password', 'list_my_accounts', 'suggest_brain_key']
