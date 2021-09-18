import datetime
import os


import jx_erl.cfg as CfgMod




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

## 获取record参数
def get_record_param(record):
    str = ""
    for key_name in record.keys:
        tmp_key = record.keys[key_name]
        str += "{0} = {1}, ".format(tmp_key.name, get_erl_val_name(tmp_key.name))
    # 去掉尾部", "
    if len(record.keys) > 0:
        str = str[: -2]
    return str

## 获取fun参数
def get_fun_param(record):
    str = ", "
    for key_name in record.keys:
        tmp_key = record.keys[key_name]
        str += "{0}, ".format(get_erl_val_name(tmp_key.name))
    if len(record.keys) > 0:
        str = str[: -2]
    else:
        str = str[2:]
    return str

## 创建目录
def create_dir(dir):
    # 目录是否存在
    if dir != "" and not os.path.exists(dir):
        os.makedirs(dir)
    