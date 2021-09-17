# -*- coding: utf-8 -*-

# 根据协议生成erl文件
import jx_erl.xml_lib as XmlLib
import jx_erl.hrl_lib as HrlLib
import jx_erl.mod_lib as ModLib
import jx_erl.erl_lib as ErlLib

mod_name = "luck_draw"

# 解析xml文件
records,protocols = XmlLib.analysis_protocol("jx_erl/protocol.xml")

HrlLib.create_file(mod_name)
ModLib.create_file(mod_name, protocols)
ErlLib.create_file(mod_name, records, protocols)


