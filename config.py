APP_CONFIRM_EXIT = False
FRAME_CLOSE_HIDE = True

MAINNET_CHAIN = "mainnet"
TESTNET_CHAIN = "testnet"
CUSTOMIZE_CHAIN = "customize"

CHAIN_CONFIG = {
    MAINNET_CHAIN: {
        "name": MAINNET_CHAIN,
        "zh": "主网",
        "address":"wss://api.cocosbcx.net"
    },
    TESTNET_CHAIN: {
        "name": TESTNET_CHAIN,
        "zh": "测试网",
        "address":"wss://test.cocosbcx.net"
    },
    CUSTOMIZE_CHAIN: {
        "name": CUSTOMIZE_CHAIN,
        "zh": "自定义",
        "address":"ws://127.0.0.1:8049"
    },
}

FAUCET_ROUTE = "/api/v1/accounts"
FAUCET_CONFIG = {
    MAINNET_CHAIN: "https://api-faucet.cocosbcx.net",
    TESTNET_CHAIN: "https://test-faucet.cocosbcx.net", 
    CUSTOMIZE_CHAIN: "http://127.0.0.1:8041"
}

headers = {"content-type": "application/json"}
faucet_headers = {
    "content-type": "application/json",
    "authorization": "YnVmZW5nQDIwMThidWZlbmc="
}

# >>> API
'''
API_CLASS:
    name : {
        "name": "",                 # string; 分类名
        "enable": True/False,       # bool; 是否可用
        "isExpand": True/False      # bool; 是否展开
        "desc":""                   # string; 分类描述
    }
'''
API_CLASS = {
    "faucet": {
        "name": "faucet",
        "enable": True,
        "isExpand": True,
        "desc": "faucet"
    },
    "wallet": {
        "name": "wallet",
        "enable": True,
        "isExpand": False,
        "desc": "wallet"
    },
    "chain": {
        "name": "chain",
        "enable": True,
        "isExpand": True,
        "desc": "chain"
    },
    "account": {
        "name": "account",
        "enable": True,
        "isExpand": True,
        "desc": "account"
    },
    "asset": {
        "name": "asset",
        "enable": True,
        "isExpand": False,
        "desc": "asset"
    },
    "contract": {
        "name": "contract",
        "enable": True,
        "isExpand": True,
        "desc": "contract"
    },
    "transaction": {
        "name": "transaction",
        "enable": True,
        "isExpand": False,
        "desc": "transaction"
    },
    "file": {
        "name": "file",
        "enable": True,
        "isExpand": False,
        "desc": "file"
    },
    "committee_vesting": {
        "name": "committee_vesting",
        "enable": True,
        "isExpand": False,
        "desc": "committee witness and vesting"
    }
}

API_EMPTY_PARAM = []

'''
API_LIST:
    {
        "name": "";       # string; 接口名; "get_account"
        "class": "";      # string; 接口分类; "account"
        "params": [[]];   # [["label"; "input_tip"]; ...]; 参数列表(若使用默认按钮单击事件，label需要和sdk.api参数名相同且顺序一致); [["Account name"; "1.2."]] 
        "enable": false;  # bool; 是否可用; True
        "sdk_name": [];   # [int,string]; int -- 索引[0:"" 默认，1:"sdk.api", 2:"sdk.wallet.api", 3:"sdk.rpc.api"], string -- sdk对应的接口名，为空表示和“name”相同
        "desc": ""        # string; 接口描述
    },
'''
API_LIST = {
    "faucet_register_account": {
        "name": "faucet_register_account",
        "class": "faucet",
        "params": [
            [
                "new account name",
                ""
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "new_wallet": {
        "name": "new_wallet",
        "class": "wallet",
        "params": [
            [
                "wallet password",
                ""
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "lock": {
        "name": "lock",
        "class": "wallet",
        "params": [],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "unlock": {
        "name": "unlock",
        "class": "wallet",
        "params": [
            [
                "password",
                ""
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "set_password": {
        "name": "set_password",
        "class": "wallet",
        "params": [
            [
                "new_password",
                ""
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "import_key": {
        "name": "import_key",
        "class": "wallet",
        "params": [
            [
                "private_key",
                ""
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "suggest_key": {
        "name": "suggest_key",
        "class": "wallet",
        "params": [],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "getAccounts": {
        "name": "getAccounts",
        "class": "wallet",
        "params": [],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "getPrivateKeyForPublicKey": {
        "name": "getPrivateKeyForPublicKey",
        "class": "wallet",
        "params": [
            [
                "public key",
                ""
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "getAccountFromPublicKey": {
        "name": "getAccountFromPublicKey",
        "class": "wallet",
        "params": [
            [
                "public key",
                ""
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "info": {
        "name": "info",
        "class": "chain",
        "params": [],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "get_object": {
        "name": "get_object",
        "class": "chain",
        "params": [
            [
                "object ID",
                ""
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "get_block": {
        "name": "get_block",
        "class": "chain",
        "params": [
            [
                "block number",
                ""
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "get_config": {
        "name": "get_config",
        "class": "chain",
        "params": [],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "get_chain_id": {
        "name": "get_chain_id",
        "class": "chain",
        "params": [],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "get_chain_properties": {
        "name": "get_chain_properties",
        "class": "chain",
        "params": [],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "get_global_properties": {
        "name": "get_global_properties",
        "class": "chain",
        "params": [],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "get_dynamic_global_properties": {
        "name": "get_dynamic_global_properties",
        "class": "chain",
        "params": [],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "get_account": {
        "name": "get_account",
        "class": "account",
        "params": [
            [
                "Account name",
                "1.2."
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "account_balances": {
        "name": "account_balances",
        "class": "account",
        "params": [["Account name", ""]],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "transfer": {
        "name": "transfer",
        "class": "account",
        "params": [
            [
                "from_account",
                "1.2."
            ],
            [
                "to_account",
                "1.2."
            ],
            [
                "amount",
                ""
            ],
            [
                "asset",
                "COCOS"
            ],
            [
                "memo",
                ""
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "create_account": {
        "name": "create_account",
        "class": "account",
        "params": [
            [
                "account_name",
                ""
            ],
            [
                "owner_key",
                ""
            ],
            [
                "active_key",
                "\u53ef\u9009"
            ],
            [
                "memo_key",
                "\u53ef\u9009"
            ],
            [
                "register",
                "1.2."
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "update_account": {
        "name": "update_account",
        "class": "account",
        "params": [["Account name", "1.2."], ["Args", ""]],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "get_account_history": {
        "name": "get_account_history",
        "class": "account",
        "params": [
            [
                "account_name",
                "1.2."
            ],
            [
                "limit",
                "10"
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "update_collateral_for_gas": {
        "name": "update_collateral_for_gas",
        "class": "account",
        "params": [
            [
                "mortgager",
                "1.2."
            ],
            [
                "beneficiary",
                "1.2."
            ],
            [
                "collateral",
                "\u5e26\u7cbe\u5ea6"
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "get_asset": {
        "name": "get_asset",
        "class": "asset",
        "params": [
            [
                "asset symbol or ID",
                "1.3."
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "asset_create": {
        "name": "asset_create",
        "class": "asset",
        "params": [
            [
                "Symbol",
                ""
            ],
            [
                "Precision",
                ""
            ],
            [
                "Common options",
                "[]"
            ],
            [
                "Bitasset opts",
                ""
            ],
            [
                "Account",
                "1.2."
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "asset_issue": {
        "name": "asset_issue",
        "class": "asset",
        "params": [
            [
                "Amount",
                ""
            ],
            [
                "Asset",
                "1.3."
            ],
            [
                "issue_to_account",
                "1.2."
            ],
            [
                "memo",
                ""
            ],
            [
                "Account",
                "1.2."
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "asset_update": {
        "name": "asset_update",
        "class": "asset",
        "params": [
            [
                "Asset",
                "1.3."
            ],
            [
                "new_options",
                ""
            ],
            [
                "Issuer",
                "1.2."
            ],
            [
                "Account",
                "1.2."
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "asset_update_bitasset": {
        "name": "asset_update_bitasset",
        "class": "asset",
        "params": [
            [
                "Asset",
                "1.3."
            ],
            [
                "new_options",
                "[]"
            ],
            [
                "Account",
                "1.2."
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "asset_update_feed_producers": {
        "name": "asset_update_feed_producers",
        "class": "asset",
        "params": [
            [
                "Asset",
                "1.3."
            ],
            [
                "feed_producers",
                "逗号分隔"
            ],
            [
                "Account",
                "1.2."
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "asset_settle": {
        "name": "asset_settle",
        "class": "asset",
        "params": [
            [
                "Amount",
                ""
            ],
            [
                "Asset",
                "1.3."
            ],
            [
                "Account",
                "1.2."
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "asset_settle_cancel": {
        "name": "asset_settle_cancel",
        "class": "asset",
        "params": [
            [
                "Settlement",
                ""
            ],
            [
                "Amount",
                ""
            ],
            [
                "Asset",
                "1.3."
            ],
            [
                "Account",
                "1.2."
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "asset_global_settle": {
        "name": "asset_global_settle",
        "class": "asset",
        "params": [
            [
                "asset_to_settle",
                "1.3."
            ],
            [
                "settle_price",
                ""
            ],
            [
                "Account",
                "1.2."
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "get_contract": {
        "name": "get_contract",
        "class": "contract",
        "params": [
            [
                "contract name or ID",
                "1.16."
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "create_contract": {
        "name": "create_contract",
        "class": "contract",
        "params": [
            [
                "Contract name",
                "contract."
            ],
            [
                "Contract data",
                ""
            ],
            [
                "Contract authority",
                "公钥"
            ],
            [
                "Account",
                "1.2."
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "revise_contract": {
        "name": "revise_contract",
        "class": "contract",
        "params": [
            [
                "Contract",
                "1.16."
            ],
            [
                "Contract data",
                ""
            ],
            [
                "Account",
                "1.2."
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "call_contract": {
        "name": "call_contract",
        "class": "contract",
        "params": [
            [
                "Contract",
                "contract."
            ],
            [
                "Function",
                ""
            ],
            [
                "Value list",
                "[]"
            ],
            [
                "Account",
                "1.2."
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "sign": {
        "name": "sign",
        "class": "transaction",
        "params": [
            [
                "transaction",
                ""
            ],
            [
                "wifs",
                ""
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "broadcast": {
        "name": "broadcast",
        "class": "transaction",
        "params": [
            "transaction",
            ""
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "get_transaction_by_id": {
        "name": "get_transaction_by_id",
        "class": "transaction",
        "params": [
            [
                "transaction ID",
                ""
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "get_transaction_in_block_info": {
        "name": "get_transaction_in_block_info",
        "class": "transaction",
        "params": [
            [
                "transaction ID",
                ""
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "get_file": {
        "name": "get_file",
        "class": "file",
        "params": [
            [
                "file name or ID",
                ""
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "create_file": {
        "name": "create_file",
        "class": "file",
        "params": [
            [
                "file_owner",
                ""
            ],
            [
                "file_name",
                ""
            ],
            [
                "file_content",
                ""
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "file_signature": {
        "name": "file_signature",
        "class": "file",
        "params": [
            [
                "signature_account",
                ""
            ],
            [
                "file_id",
                ""
            ],
            [
                "signature",
                ""
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "add_file_relate_account": {
        "name": "add_file_relate_account",
        "class": "file",
        "params": [
            [
                "file_owner",
                ""
            ],
            [
                "file_id",
                ""
            ],
            [
                "relate_account",
                ""
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "relate_parent_file": {
        "name": "relate_parent_file",
        "class": "file",
        "params": [],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "get_vesting_balances": {
        "name": "get_vesting_balances",
        "class": "committee_vesting",
        "params": [
            [
                "account_id_or_name",
                "1.2."
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "vesting_balance_create": {
        "name": "vesting_balance_create",
        "class": "committee_vesting",
        "params": [
            [
                "Owner",
                "1.2."
            ],
            [
                "Amount",
                ""
            ],
            [
                "Asset",
                "1.3."
            ],
            [
                "start",
                ""
            ],
            [
                "_type",
                "linear or cdd"
            ],
            [
                "vesting_cliff_seconds",
                "0"
            ],
            [
                "vesting_duration_seconds",
                "0"
            ],
            [
                "vesting_seconds",
                "0"
            ],
            [
                "Account",
                "1.2."
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    },
    "vesting_balance_withdraw": {
        "name": "vesting_balance_withdraw",
        "class": "committee_vesting",
        "params": [
            [
                "vesting_id",
                ""
            ],
            [
                "Amount",
                ""
            ],
            [
                "Asset",
                "1.3."
            ],
            [
                "Account",
                "1.2."
            ]
        ],
        "enable": True,
        "sdk_name": [],
        "desc": ""
    }
}


