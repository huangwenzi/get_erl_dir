import os
import re


import src.help_mod as HelpMod
import src.cfg as CfgMod

# 负责hrl文件




# 生成hrl文件
def create_hrl_file(pro_mod):
    # hrl文件名
    file_name = "{0}/{1}_hrl.erl".format(pro_mod.dir_path, pro_mod.mod_name)
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
            str,ret = replace_hrl_fun_param(str, pro_mod, protocol_obj)
            # 添加不存在的函数
            if not ret:
                str = add_hrl_fun_param(str, pro_mod, protocol_obj)
    else:
        # 不存在文件
        # 创建新的hrl文件
        str = create_hrl_file_1(pro_mod)
        
    # 写到文件
    with open(file_name, 'w', encoding = "utf-8") as f:
        f.write(str)
        
    
# 创建新的hrl文件
def create_hrl_file_1(pro_mod):
    # 文件开头
    str = HelpMod.get_file_head_str()
    # 宏定义文件
    str += get_def_str()
    # 玩法数据结构
    str += get_record_str()
    # 玩家数据结构
    str += get_player_record_str()
    str += "\n-endif.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
    return str

# 获取宏定义字符串
def get_def_str(pro_mod):
    str = """

-ifndef(%s_H_H_).
-define(%s_H_H_, 1).

    """
    mod_name_1 = pro_mod.mod_name.upper()
    str = str%(mod_name_1, mod_name_1)
    return str 

# 玩法数据结构
def get_record_str(pro_mod):
    # 遍历结构
    str = ""
    for record_obj in pro_mod.mod.record_define:
        str += get_record_str_1(record_obj)
    return str 

# 玩法数据结构
def get_record_str_1(record_obj):
    str = """
%%%% 
-record(%s, {\n"""%(record_obj[0][:-2])
    str += get_record_param(record_obj[1])
    str += "}).\n"
    return str 

# 获取record字段
def get_record_param(record_param_list):
    str = ""
    param_len = len(record_param_list)
    param_idx = 0
    # 遍历字段
    for tmp_param in record_param_list:
        # 参数
        param_idx += 1
        # 跳过code
        if tmp_param[0] == "code":
            continue
        param_str = ""
        if tmp_param[1] == "int":
            param_str = "\t%s = 0"%(tmp_param[0])
        else:
            param_str = "\t%s = []"%(tmp_param[0])
        param_str_len = len(param_str)
        # 加，
        if param_idx != param_len:
            param_str += ","
        # 对齐的\t
        if _g_record_len > param_str_len:
            t_num = int((_g_record_len - param_str_len)/4)
            param_str += "\t"*t_num
        # 注释
        param_str += "%%%% %s\n"%(tmp_param[2])
        str += param_str
    return str

# 玩家数据结构
def get_player_record_str():
    # 协议是否存在
    reply_name = _g_mod_name + "_info_reply"
    if reply_name not in mod.protocol_define:
        return ""
    
    str = """
%%%% 
-record(player_%s, {\n"""%(_g_mod_name)
    reply_obj = mod.protocol_define[reply_name]
    str += "\tplayer_id = 0, \n" + get_record_param(reply_obj["payload"])
    str += "}).\n"
    return str