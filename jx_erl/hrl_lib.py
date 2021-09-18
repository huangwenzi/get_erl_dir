
import os


import jx_erl.help_lib as HelpLib
import jx_erl.cfg as CfgLib

# 负责hrl文件




# 生成hrl文件
def create_file(mod_name):
    # hrl文件名
    file_name = "{0}/{1}.hrl".format(CfgLib.hrl_path, mod_name)
    # 目录不存在就创建
    HelpLib.create_dir(CfgLib.hrl_path)
    str = ""
    # 文件是否存在
    if not os.path.exists(file_name):
        # 不存在文件
        # 创建新的hrl文件
        str = create_hrl_file(mod_name)
        # 写到文件
        with open(file_name, 'w', encoding = "utf-8") as f:
            f.write(str)
        
    
# 创建新的hrl文件
def create_hrl_file(mod_name):
    # 文件开头
    str = HelpLib.get_file_head_str()
    # 宏定义文件
    str += get_def_str(mod_name)
    str += "\n-endif.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
    return str

# 获取宏定义字符串
def get_def_str(mod_name):
    str = """

-ifndef({0}_HRL).
-define({0}_HRL, true).

    """
    mod_name_1 = mod_name.upper()
    str = str.format(mod_name_1)
    return str 

