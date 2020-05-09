**pwallet**

----------------------

__WARNING__: *This is experimental software. Use at your own risk*

## 概述

一款使用wxPython实现的Cocos-BCX链跨平台图形化桌面钱包。

基于[python-sdk](https://github.com/Cocos-BCX/Python-Middleware)和链进行交互。对python-sdk进行重新封装，有如下补充：

* 不需要安装，支持多链。
* 数据存储优化。

## 功能：

* 支持主网、测试网和自定义网络python-sdk功能。

* 支持主网、测试网、自定义水龙头账户注册功能。

* 新增接口，只需修改[配置](config.py),格式如下：

  ``` python
  # 新增接口分类 API_CLASS
  "name" : {
      "name": "",                 # string; 分类名
      "enable": True/False,       # bool; 是否可用
      "isExpand": True/False      # bool; 是否展开
      "desc":""                   # string; 分类描述
  }
  
  # 新增接口 API_LIST
  "name": {
      "name": "";       # string; 接口名; "get_account"
      "class": "";      # string; 接口分类; "account"
      "params": [[]];   # [["label"; "input_tip"]; ...]; 参数列表(若使用默认按钮单击事件，label需要和sdk.api参数名相同且顺序一致); [["Account name"; "1.2."]] 
      "enable": false;  # bool; 是否可用; True
      "sdk_name": [];   # [int,string]; int -- 索引[0:"" 默认，1:"sdk.api", 2:"sdk.wallet.api", 3:"sdk.rpc.api"], string -- sdk对应的接口名，为空表示和“name”相同
      "desc": ""        # string; 接口描述
  }
  ```

* 支持重写api执行按钮绑定function的重写


## 说明：

该程序，目前处于开发测试中，部分接口暂时可能会调用失败，主网环境中，请谨慎使用涉及operation的操作，避免资金损失。


## 运行环境：

* python 3.5+
* wxPython 4.0+
* 其他依赖参考requirements.txt安装



## 待完成:

* API Config中参数增加类型，支持参数输入根据类型转换
* 水龙头注册账户导入到钱包中。
* 打包成可安装文件

