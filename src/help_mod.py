import datetime



import src.cfg as CfgMod




# 公用的函数在这里


# 获取开头
def get_file_head_str():
    # 时间
    i = datetime.datetime.now()
    str = """
%%%%%%-------------------------------------------------------------------
%%%%%% @author {0}
%%%%%% @copyright (C) {1}, <COMPANY>
%%%%%% @doc
%%%%%%
%%%%%% @end
%%%%%% Created : {3}. {2}月 {1} {4}:{5}
%%%%%%-------------------------------------------------------------------
"""""
    str = str.format(CfgMod.author_name, i.year, i.month, i.day, i.hour, i.minute)
    return str

# 获取协议对应的函数名
def get_fun_name(pro_mod, protocol_key):
    tmp_str = protocol_key[len(pro_mod.mod_name):]
    begin = tmp_str.find("_")
    end = tmp_str.rfind("_")
    return tmp_str[begin+1 : end]

# 获取rpc record参数
def get_rpc_record_param(protocol_obj):
    str = ""
    param_len = len(protocol_obj.param)
    for idx in range(param_len):
        str += "%s = %s, "%(protocol_obj.param[idx], protocol_obj.erl_param[idx])
    return str[:-2]

# 获取函数参数
def get_fun_param(protocol_obj):
    str = "Player, "
    for tmp_param in protocol_obj.erl_param:
        str += "%s, "%(tmp_param)
    return str[:-2]

# 获取结构参数
def get_record_param_str(record_param):
    # 遍历参数
    param_str = ""
    for tmp_param in record_param:
        tmp_param_1 = get_erl_val_name(tmp_param[0])
        param_str += "%s = %s, "%(tmp_param[0], tmp_param_1)
    if len(param_str) > 0:
        param_str = param_str[:-2]
    # ，号换行
    param_str_1 = param_str.replace(",", "\n\t\t,")
    return param_str,param_str_1
        
# 转erl变量名格式
# 获取协议参数 首字母、下划线后一个替换大写
def get_erl_val_name(name):
    while True:
        idx = name.find("_")
        # 替换完退出
        if idx < 0:
            # 首字母替换大写
            name = name[:1].upper() + name[1:]
            return name
        # 下划线去掉，后一个替换大写
        tmp_1 = name[idx+1]
        tmp_1 = tmp_1.upper()
        name = name[:idx] + tmp_1 + name[idx+2:]

# 上一个protocol_key
def get_last_protocol_key(pro_mod, protocol_key):
    last_protocol_key = ""
    for tmp_protocol_key in pro_mod.request_key:
        if tmp_protocol_key == protocol_key:
            break
        last_protocol_key = tmp_protocol_key
    return last_protocol_key

# 上一个record_p
def get_last_record_key(pro_mod, record_key):
    last_record_key = ""
    for record_obj in pro_mod.mod.record_define:
        if record_obj[0] == record_key:
            break
        last_record_key = record_obj[0]
    return last_record_key