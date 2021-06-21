import os


import src.hrl_mod as HrlMod
import src.rpc_mod as RpcMod
import src.lib_mod as LibMod
import src.help_mod as HelpMod
import src.cfg as CfgMod


# 功能协议类
class ProMod(object):
    # 协议模块
    mod = None
    # 模块名
    mod_name = ""
    # 目录地址
    dir_path = ""
    # 为了协议顺序
    request_key = []    # 请求协议  ["protocol_key",...]
    reply_key = []      # 返回协议
    
    protocol_map = {}   # 新协议对象
    
    def __init__(self):
        self.mod = None
        self.mod_name = ""
        self.dir_path = ""
        self.request_key = []
        self.reply_key = []
        self.protocol_map = {}

# 单个协议类
class Protocol(object):
    protocol_key = ""           # 协议key
    param = []                  # 参数
    erl_param = []              # erl参数,参数转格式
    desc = ""                   # 协议注释
    
    def __init__(self):
        self.protocol_key = ""
        self.param = []
        self.erl_param = []
        self.desc = ""

    # 初始化参数字符串
    def init_param(self):
        pass
        

# 创建文件
def create_file(mod, mod_name):
    # 解析协议
    pro_mod = analysis_protocol(mod, mod_name)
    # 目录是否存在
    dir_path = CfgMod.out_path + "/" + mod_name
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    pro_mod.dir_path = dir_path
    # 生成hrl文件
    HrlMod.create_hrl_file(pro_mod)
    # 生成rpc文件
    RpcMod.create_rpc_file(pro_mod)
    # 生成lib文件
    LibMod.create_lib_file(pro_mod)
    
   

# 解析协议
def analysis_protocol(mod, mod_name):
    pro_mod = ProMod()
    pro_mod.mod = mod
    pro_mod.mod_name = mod_name
    # 解析请求协议
    request_key_list = get_protocol_key(mod, ["_request"])
    pro_mod.request_key = request_key_list
    # 解析返回协议
    reply_key_list = get_protocol_key(mod, ["_reply"])
    pro_mod.reply_key = reply_key_list
    analysis_protocol_obj(pro_mod)
    return pro_mod

# 解析协议对象
def analysis_protocol_obj(pro_mod):
    mod = pro_mod.mod
    key_list = pro_mod.request_key + pro_mod.reply_key
    for protocol_key in key_list:
        protocol = Protocol()
        protocol.protocol_key = protocol_key
        # 获取参数
        mod_protocol = mod.protocol_define[protocol_key]
        analysis_protocol_param(protocol, mod_protocol)
        pro_mod.protocol_map[protocol_key] = protocol

#  解析协议参数
def analysis_protocol_param(protocol, obj):
    list = []   # 参数
    list_1 = [] # 参数转erl变量格式
    for tmp_param in obj["payload"]:
        param = tmp_param[0]
        list.append(param)
        list_1.append(HelpMod.get_erl_val_name(param))
    protocol.param = list
    protocol.erl_param = list_1
    protocol.desc = obj["desc"]
    
# 获取包含list的协议
def get_protocol_key(mod, list):
    key_list = []
    for protocol_key in mod.protocol_define:
        for item in list:
            if protocol_key.find(item) > 0:
                key_list.append(protocol_key)
                break
    return key_list  
    
    

    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    