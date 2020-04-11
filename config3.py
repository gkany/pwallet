env = [ "mainnet", "testnet", "customize"]
node_addresses = {
    env[0]: "wss://api.cocosbcx.net",
    env[1]: "wss://test.cocosbcx.net", 
    env[2]: "ws://127.0.0.1:8049"
}

faucet_urls = {
    env[0]: "https://api-faucet.cocosbcx.net/api/v1/accounts",
    env[1]: "https://test-faucet.cocosbcx.net/api/v1/accounts", 
    env[2]: "http://127.0.0.1:8041/api/v1/accounts"
}

API_CLASS = {
                "faucet" : True, 
                "wallet" : True, 
                "chain" : True, 
                "account" : True, 
                "asset" : True, 
                "contract" : True, 
                "transaction" : False, 
                "file" : False
            }

## wallet api tree list  
faucet_api = ["faucet_register_account"]
wallet_api = ["new_wallet", "lock", "unlock", "set_password", "import_key", "suggest_key", "getAccounts", "getPrivateKeyForPublicKey", "getAccountFromPublicKey"]
chain_api = ["info", "get_object", "get_block", "get_config", "get_chain_id", "get_chain_properties", "get_global_properties", "get_dynamic_global_properties"]
account_api = ["get_account", "account_balances", "transfer", "create_account", "update_account", "get_account_history", "update_collateral_for_gas"]
asset_api = ["get_asset", "create_asset"]
contract_api = ["get_contract", "create_contract", "revise_contract", "call_contract"]
transaction_api = ["sign", "broadcast", "get_transaction_by_id", "get_transaction_in_block_info"]
file_api = ["get_file", "create_file", "file_signature", "add_file_relate_account", "relate_parent_file"]

API_PARAM_LIST = {
    "faucet_register_account": [["new account name", ""]],
    "new_wallet": [["wallet password", ""]],
    "unlock": [["password", ""]],
    "set_password": [["new_password", ""]],
    "import_key": [["private_key", ""]],
    "getPrivateKeyForPublicKey": [["public key", ""]],
    "getAccountFromPublicKey": [["public key", ""]],
    "get_account": [["account name or ID", "1.2."]],
    "list_account_balances": [["account name or ID", "1.2."]],
    "get_asset": [["asset symbol or ID", "1.3."]],
    "get_contract": [["contract name or ID", "1.16."]],
    "get_object": [["object ID", ""]],
    "get_file": [["file name or ID", ""]],
    "get_block": [["block number", ""]],
    "create_file": [
        ["file_owner", ""],
        ["file_name", ""],
        ["file_content", ""],
    ],
    "add_file_relate_account": [
        ["file_owner", ""],
        ["file_id", ""],
        ["relate_account", ""],
    ],
    "file_signature": [
        ["signature_account", ""],
        ["file_id", ""],
        ["signature", ""],
    ],
    "transfer": [
                    ["from_account", "1.2."], 
                    ["to_account", "1.2."],
                    ["amount", ""],
                    ["asset", "COCOS"],
                    ["memo", ""]
                ],
    "create_account": [
                    ["account_name", ""], 
                    ["owner_key", ""],
                    ["active_key", "可选"],
                    ["memo_key", "可选"],
                    ["register", "1.2."]
                ],
    "get_account_history": [
                    ["account_name", "1.2."], 
                    ["limit", "10"]
                ],
    "update_collateral_for_gas": [
                ["mortgager", "1.2."], 
                ["beneficiary", "1.2."],
                ["collateral", "带精度"]
    ],
    "get_transaction_by_id": [ "transaction ID", ""],
    "get_transaction_in_block_info": ["transaction ID", ""],
    "broadcast": ["transaction", ""],
    "sign": [
        ["transaction", ""],
        ["wifs", ""]
    ]
}

api_empty_param = ["lock", "getAccounts", "suggest_key", "info", "get_chain_properties", "get_global_properties", "get_config", "get_chain_id", "get_dynamic_global_properties"]
api_one_param = ["faucet_register_account", "new_wallet", "getAccountFromPublicKey", "import_key", "getPrivateKeyForPublicKey", "unlock", "set_password", "get_object", "get_account", "get_asset", "list_account_balances", "get_contract", "get_file", "broadcast", "get_transaction_by_id", "get_transaction_in_block_info", "get_block"]
api_two_params = ["get_account_history", "sign"]
api_three_params = ["update_collateral_for_gas", "create_file", "add_file_relate_account", "file_signature"]
api_four_params = []
api_five_params = ["transfer", "create_account"]
api_six_params = []
api_seven_params = []


headers = {"content-type": "application/json"}
faucet_headers = {
        "content-type": "application/json",
        "authorization": "YnVmZW5nQDIwMThidWZlbmc="
}

API_BUTTON_CLICK_EVENT_PREFIX_ = "api_button_on_click_"

