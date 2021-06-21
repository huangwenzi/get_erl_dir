import os
import re


import src.help_mod as HelpMod
import src.cfg as CfgMod

# 负责rpc文件




# 生成rpc文件
def create_rpc_file(pro_mod):
    # rpc文件名
    file_name = "{0}/{1}_rpc.erl".format(pro_mod.dir_path, pro_mod.mod_name)
    str = ""
    # 文件是否存在
    if os.path.exists(file_name):
        # 存在文件
        with open(file_name, 'r', encoding = "utf-8") as f:
            str = f.read()
        # 遍历协议
        for tmp_key in pro_mod.request_key:
            protocol_obj = pro_mod.protocol_map[tmp_key]
            # 替换已存在的函数参数
            str,ret = replace_rpc_fun_param(str, pro_mod, protocol_obj)
            # 添加不存在的函数
            if not ret:
                str = add_rpc_fun_param(str, pro_mod, protocol_obj)
    else:
        # 不存在文件
        # 创建新的rpc文件
        str = create_rpc_file_1(pro_mod)
        
    # 写到文件
    with open(file_name, 'w', encoding = "utf-8") as f:
        f.write(str)
        
    
# 创建新的rpc文件
def create_rpc_file_1(pro_mod):
    # 文件开头
    str = HelpMod.get_file_head_str()
    # mod字符串
    str += get_rpc_file_mod_str(pro_mod.mod_name)

    # 遍历协议
    for protocol_key in pro_mod.request_key:
        # 协议函数
        str += get_rpc_file_protocol_fun_str(pro_mod, protocol_key)
    ## 加一层rpc匹配容错
    str += """ 
handle(Msg, _Player) ->
    ?ERROR("module:[~p] handle msg error:[~p]", [?MODULE, Msg]),
    ok.
    """
    # # 替换最后的;
    # str = str[: -2] + "."
    return str

# 替换rpc函数参数
def replace_rpc_fun_param(str, pro_mod, protocol_obj):
    protocol_key = protocol_obj.protocol_key
    mod_name = pro_mod.mod_name
    # 替换record参数
    # 注意()前面的\,会影响正则匹配
    begin_str = "\nhandle\(#%s{"%(protocol_key)
    begin_str_1 = "\nhandle(#%s{"%(protocol_key)
    # 正则匹配函数
    a = r"(.*)" + begin_str + "(.*?)}, Player(.*)"
    matchObj = re.match(a, str, re.M|re.S)
    if matchObj:
        str = matchObj.group(1) + begin_str_1 + HelpMod.get_rpc_record_param(protocol_obj) + "}, Player" + matchObj.group(3)
    else:
        # 匹配不到，说明没有这个函数
        return str,False
    
    # 替换lib参数
    "case memory_lib:video(Player, Type) of"
    fun_name =  HelpMod.get_fun_name(pro_mod, protocol_key)
    begin_str = "%s_lib:%s\("%(mod_name, fun_name)
    begin_str_1 = "case %s_lib:%s("%(mod_name, fun_name)
    a = r"(.*)case " + begin_str + "(.*?) of(.*)"
    matchObj = re.match(a, str, re.M|re.S)
    if matchObj:
        str = matchObj.group(1) + begin_str_1 +  HelpMod.get_fun_param(protocol_obj) + ") of" + matchObj.group(3)
    return str,True
    
# 添加rpc函数参数
def add_rpc_fun_param(str, pro_mod, protocol_obj):
    a = r"(.*)\nhandle\(Msg, _Player\)(.*)"
    matchObj = re.match(a, str, re.M|re.S)
    if matchObj:
        rpc_fun = get_rpc_file_protocol_fun_str(pro_mod, protocol_obj.protocol_key)
        str = matchObj.group(1) + rpc_fun + "\nhandle(Msg, _Player)" + matchObj.group(2)
    return str

# 获取rpc mod字符串
def get_rpc_file_mod_str(mod_name):
    # 模块名
    str = """
-module({0}_rpc).
-author("{1}").

-include("erl_protocol_record.hrl").
-include("logger.hrl").

%% API
-export([handle/2]).
    """.format(mod_name, CfgMod.author_name)
    return str

# 获取rpc 协议函数字符串
def get_rpc_file_protocol_fun_str(pro_mod, protocol_key):
    # 协议函数结构
    protocol_fun ="""
%%%% {0}
handle(#{1}{{{2}}}, Player) ->
    case {3}_lib:{4}({5}) of
        {{ok, Reply}} ->
            {{reply, Reply}};
        {{false, Code}} ->
            {{reply, #{6}{{code = Code}}}}
    end;\n"""
    protocol_obj = pro_mod.protocol_map[protocol_key]
    # 生成协议函数
    tmp_protocol_fun = protocol_fun.format(
        protocol_obj.desc
        , protocol_key
        , HelpMod.get_rpc_record_param(protocol_obj)    # rpc参数
        , pro_mod.mod_name
        , HelpMod.get_fun_name(pro_mod, protocol_key)   # 函数名
        , HelpMod.get_fun_param(protocol_obj)           # 函数参数
        , protocol_key.replace("request", "reply")
    )
    return tmp_protocol_fun