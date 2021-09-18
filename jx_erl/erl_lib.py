import os
import re


import jx_erl.help_lib as HelpLib
import jx_erl.cfg as CfgLib

# 负责internal文件


# 生成internal文件
def create_file(mod_name, records, protocols):
    # internal文件名
    file_name = "{0}/{1}_internal.erl".format(CfgLib.internal_path, mod_name)
    # 目录不存在就创建
    HelpLib.create_dir(CfgLib.internal_path)
    mod_pro = protocols[mod_name]
    str = ""
    # 文件是否存在
    if os.path.exists(file_name):
        # 存在文件
        with open(file_name, 'r', encoding = "utf-8") as f:
            str = f.read()
        # 遍历协议
        last_protocol = None
        for protocol_key in mod_pro.protocol:
            protocol = mod_pro.protocol[protocol_key]
            # 替换已存在的函数参数
            ret,str = replace_protocol_fun_param(str, protocol)
            # 添加不存在的函数
            if not ret:
                str = add_protocol_fun_param(str, mod_name, protocol, last_protocol)
            last_protocol = protocol
            
        # 遍历结构
        record_list = get_mod_record_list(mod_pro, protocols)
        for record_key in record_list:
            # 是否在str中
            if str.find("to_p_" + record_key + "(") > 0:
                continue
            else:
                str += get_record_p_str_1(records[record_key])
    else:
        # 不存在文件
        # 创建新的internal文件
        str = create_internal_file(mod_name, records, protocols, mod_pro)
        
    # 写到文件
    with open(file_name, 'w', encoding = "utf-8") as f:
        f.write(str)

# 创建新的rpc文件
def create_internal_file(mod_name, records, protocols, mod_pro):
    # 文件开头
    str = HelpLib.get_file_head_str()
    # mod字符串
    str += get_internal_file_mod_str(mod_name)
    # API字符串
    str += get_internal_file_api_str(mod_pro)
    # protocol_fun字符串
    str += get_internal_file_protocol_fun_str(mod_name, mod_pro)
    # 获取函数
    str += get_internal_file_get_str(mod_name)
    # 结构转换函数
    str += get_record_p_str(records, mod_pro, protocols)
    return str
    



    
# internal文件
# 获取internal mod字符串
def get_internal_file_mod_str(mod_name):
    # 模块名
    str = """
-module({0}_internal).

%% ====================================================================
%% includes
%% ====================================================================
-include("common.hrl").
-include("counter.hrl").
-include("role.hrl").
-include("{0}.hrl").
-include("proto_{0}_pb.hrl").\n\n""".format(mod_name)
    return str

# 获取 api字符串
def get_internal_file_api_str(mod_pro):
    # API
    api_str = """
%%%% ====================================================================
%%%% API functions
%%%% ====================================================================
%%%% 协议接口
-export([
%s
]).

%%%% 外部接口

%%%% 获取函数

%%%% 修改函数

%%%% 结构转换

%%%% gm



"""   
    # 遍历协议
    export_str = ""
    for protocol_key in mod_pro.protocol:
        protocol = mod_pro.protocol[protocol_key]
        export_str += get_export_str(protocol.c2s)
    if len(export_str) > 0:
        export_str = "\t" + export_str[3:]
    return api_str%(export_str)
def get_export_str(c2s_record):
    fun_name = c2s_record.name
    param_num = len(c2s_record.keys)
    return "\t, %s/%s\n"%(fun_name, param_num+1)

# 获取 protocol_fun字符串
def get_internal_file_protocol_fun_str(mod_name, mod_pro):
    str = """
%% ====================================================================
%% External functions
%% ====================================================================


%%========================================协议函数
"""
    for protocol_key in mod_pro.protocol:
        protocol = mod_pro.protocol[protocol_key]
        c2s_record = protocol.c2s
        protocol_fun = get_protocol_fun_str(mod_name, c2s_record)
        check_fun = get_check_fun_str(c2s_record)
        str = str + protocol_fun + check_fun
    return str
# 协议函数
def get_protocol_fun_str(mod_name, c2s_record):
    protocol_fun_str = """
%% @doc {0}
{1}(RoleId{2}) ->
	case check_{1}(RoleId{2}) of
        {{false, Code}} -> {{false, Code}};
		ok ->
            #{3}
	end.
    """
    # 函数参数
    protocol_fun_str = protocol_fun_str.format(
        c2s_record.desc
        , c2s_record.name
        , HelpLib.get_fun_param(c2s_record)
        , mod_name + c2s_record.name + "s2c{}"
    )
    return protocol_fun_str
# 检查函数
def get_check_fun_str(c2s_record):
    protocol_fun_str = """
%% @doc 检查{0}
check_{1}(RoleId{2}) ->
	ok.
    """
    # 函数参数
    protocol_fun_str = protocol_fun_str.format(
        c2s_record.desc
        , c2s_record.name
        , HelpLib.get_fun_param(c2s_record)
    )
    return protocol_fun_str

    

# 获取 获取函数
def get_internal_file_get_str(pro_mod):
    get_str = """
%%========================================获取函数
%% 获取全部数据
get_all_info() ->
    cache:list({0}).

%% 获取数据信息
get_data_info(RoleId, Id) ->
    case cache:key_find({0}, Id, #{1}.id) of
        false ->
            {{ok, Uid}} = serv_id:new({0}),
            % 新数据
            Info = #{1}{{
                id = Uid
            }},
            cache:add(Info),
            Info;
        Info -> Info
    end.

%% 保存数据信息
set_data_info(Info) ->
    cache:update(Info).    
"""
    get_str = get_str.format(
        "?TABLE_" + pro_mod.upper()
        , pro_mod
    )
    return get_str

# 结构转换函数
def get_record_p_str(records, mod_pro, protocols):
    # 协议包含的结构体
    record_list = get_mod_record_list(mod_pro, protocols)
    # 生成字符串
    str = "%%========================================结构转换函数\n"
    for record in record_list:
        str += get_record_p_str_1(records[record])
    return str 
# 其他协议不存在的结构
def get_mod_record_list(mod_pro, protocols):
    # 协议包含的结构体
    record_list = get_record_list(mod_pro)
    # 是否也在别的协议里
    for protocol_key in protocols:
        tmp_mod_pro = protocols[protocol_key]
        # 同mod跳过
        if tmp_mod_pro.name == mod_pro.name:
            continue
        tmp_record_list = get_record_list(tmp_mod_pro)
        sub_record_list = []
        for item in record_list:
            if item not in tmp_record_list:
                sub_record_list.append(item)
        record_list = sub_record_list
    return record_list
# 协议包含的结构体
def get_record_list(mod_pro):
    base_type = ["int32", "int64", "uint32", "uint64", "string"]
    record_list = []
    for protocol_key in mod_pro.protocol:
        protocol = mod_pro.protocol[protocol_key]
        c2s_record = protocol.c2s
        for key in c2s_record.keys:
            key = c2s_record.keys[key]
            if key.type not in base_type and key.type not in record_list:
                record_list.append(key.type)
        s2c_record = protocol.s2c
        for key in s2c_record.keys:
            key = s2c_record.keys[key]
            if key.type not in base_type and key.type not in record_list:
                record_list.append(key.type)
    return record_list
# 玩法数据结构
def get_record_p_str_1(record):
    str = """
%% @doc 
{0}(#{1}{{{3}}}) ->
	#{1}_p{{
		{4}
	}}.
{0}([], List) -> List;
{0}([{2} | T], List) ->
	{0}(T, [{0}({2}) | List]).
    """
    record_param = HelpLib.get_record_param(record)
    str = str.format(
        "to_p_%s"%(record.name)
        , record.name
        , HelpLib.get_erl_val_name(record.name)
        , record_param
        , record_param.replace(", ", "\n\t\t, ")
    )
    return str 


# 替换已存在的函数参数
def replace_protocol_fun_param(str, protocol):
    # fun_str是否存在
    fun_str = "\n" + protocol.name + "("
    if str.find(fun_str) == -1:
        return False,str
    
    # 替换rpc接口函数参数
    # 正则匹配函数
    fun_str_1 = "\n" + protocol.name + "\("
    a = r"(.*)" + fun_str_1 + "RoleId(.*?)\) ->(.*)"
    matchObj = re.match(a, str, re.M|re.S)
    if matchObj:
        str = "{0}{1}RoleId{2}) ->{3}".format(
                matchObj.group(1)
                , fun_str
                , HelpLib.get_fun_param(protocol.c2s)
                , matchObj.group(3)
            )
    else:
        # 匹配不到
        print("替换rpc接口函数参数 err : %s"%(protocol.name))
        
    return True,str
    
    
# 添加不存在的函数
def add_protocol_fun_param(str, mod_name, protocol, last_protocol):
    # 添加export_str
    # 上一个函数所在的位置 不考虑不存在上一个协议
    last_export_str = get_export_str(last_protocol.c2s)
    last_export_pos = str.find(last_export_str) + len(last_export_str)
    str = str[:last_export_pos] + "\n" + get_export_str(protocol.c2s) + str[last_export_pos:]
#     if last_protocol:
#         last_export_str = get_export_str(last_protocol.c2s)
#         last_export_pos = str.find(last_export_str) + len(last_export_str)
#         str = str[:last_export_pos] + "\n" + get_export_str(protocol.c2s) + str[last_export_pos:]
#     else:
#         begin_str = """%% 协议接口
# -export(["""
#         last_export_pos = str.find(begin_str) + len(begin_str)
#         str = str[:last_export_pos] + "\n\t" + get_export_str(protocol.c2s)[2] + str[last_export_pos:]
    
    # 添加protocol_fun
    # 上一个函数所在的位置
    find_str = "\ncheck_%s("%(last_protocol.name)
    last_fun_name_pos = str.find(find_str)
    # 上个函数下方函数的位置
    end_fun_pos = str.find("\n%%", last_fun_name_pos)
    c2s_record = protocol.c2s
    protocol_fun = get_protocol_fun_str(mod_name, c2s_record)
    check_fun = get_check_fun_str(c2s_record)
    str = str[:end_fun_pos] + protocol_fun + check_fun + "\n" +  str[end_fun_pos:]
    
    return str
