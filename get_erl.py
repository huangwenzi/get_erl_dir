# -*- coding: utf-8 -*-

# 根据协议生成erl文件
import src.erl_lib as ErlLib


import mod_protocol.bargain as mod
mod_name = "bargain"


ErlLib.create_file(mod, mod_name)




