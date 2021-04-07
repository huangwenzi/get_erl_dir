# get_erl_dir

## 作用
根据协议自动生成hrl，rpc，lib文件

## 用法
协议文件放在mod_protocol目录下

修改get_erl.py  
import mod_protocol.你的协议文件名 as mod  
_g_mod_name = "你的协议文件名"

命令行运行 py get_erl.py

## 注意
这里的协议文件格式和生成的代码都是示例，需要根据你自己的工程文件修改使用

