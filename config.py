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

faucet_commands = ["faucet_register_account"]
wallet_wallet_commands = ["new_wallet", "lock", "unlock", "set_password", "import_key", "list_my_accounts", "suggest_brain_key", "getPrivateKeyForPublicKey", "getAccountFromPublicKey"]
wallet_chain_commands = ["info", "get_object", "get_block", "get_config", "get_chain_id", "get_chain_properties", "get_global_properties", "get_dynamic_global_properties"]
wallet_account_commands = ["get_account",  "transfer", "list_account_balances", "create_account", "update_account", "get_account_history", "update_collateral_for_gas"]
wallet_asset_commands = ["get_asset", "create_asset"]
wallet_contract_commands = ["get_contract", "create_contract", "revise_contract", "call_contract"]
wallet_transaction_commands = ["sign", "broadcast", "get_transaction_by_id", "get_transaction_in_block_info"]
wallet_file_commands = ["get_file", "create_file", "file_signature", "add_file_relate_account", "relate_parent_file"]

cmd_param_notes = {
    "faucet_register_account": ["new account name", ""],
    "new_wallet": ["wallet password", ""],
    "unlock": ["password", ""],
    "set_password": ["new_password", ""],
    "import_key": ["private_key", ""],
    "getPrivateKeyForPublicKey": ["public key", ""],
    "getAccountFromPublicKey": ["public key", ""],
    "get_account": ["account name or ID", "eg: 1.2.3 or null-account"],
    "list_account_balances": ["account name or ID", "eg: 1.2.3 or null-account"],
    "get_asset": ["asset symbol or ID", "eg: 1.3.0 or COCOS"],
    "get_contract": ["contract name or ID", ""],
    "get_object": ["object ID", "eg: 1.3.0"],
    "get_file": ["file name or ID", ""],
    "get_block": ["block number", ""],
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
                    ["from_account", ""], 
                    ["to_account", ""],
                    ["amount", ""],
                    ["asset", ""],
                    ["memo", ""]
                ],
    "create_account": [
                    ["account_name", ""], 
                    ["owner_key", ""],
                    ["active_key", "可选"],
                    ["memo_key", "可选"],
                    ["register", ""]
                ],
    "get_account_history": [
                    ["account_name", ""], 
                    ["limit", ""]
                ],
    "update_collateral_for_gas": [
                ["mortgager", ""], 
                ["beneficiary", ""],
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

no_params_commands = ["lock", "list_my_accounts", "suggest_brain_key", "info", "get_chain_properties", "get_global_properties", "get_config", "get_chain_id", "get_dynamic_global_properties"]
one_params_commands = ["faucet_register_account", "new_wallet", "getAccountFromPublicKey", "import_key", "getPrivateKeyForPublicKey", "unlock", "set_password", "get_object", "get_account", "get_asset", "list_account_balances", "get_contract", "get_file", "broadcast", "get_transaction_by_id", "get_transaction_in_block_info", "get_block"]
two_params_commands = ["get_account_history", "sign"]
three_params_commands = ["update_collateral_for_gas", "create_file", "add_file_relate_account", "file_signature"]
four_params_commands = []
five_params_commands = ["transfer", "create_account"]
six_params_commands = []
seven_params_commands = []


headers = {"content-type": "application/json"}
faucet_headers = {
        "content-type": "application/json",
        "authorization": "YnVmZW5nQDIwMThidWZlbmc="
}
