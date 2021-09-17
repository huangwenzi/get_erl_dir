import os
import re


import jx_erl.help_lib as HelpLib
import jx_erl.cfg as CfgLib

# 负责internal文件


# 生成internal文件
def create_file(mod_name, records, protocols):
    # internal文件名
    file_name = "{0}/{1}_internal.erl".format(CfgLib.out_path, mod_name)
    str = ""
    # 文件是否存在
    if os.path.exists(file_name):
        # 存在文件
        with open(file_name, 'r', encoding = "utf-8") as f:
            str = f.read()
        # # 遍历协议
        # mod_pro = protocols[mod_name]
        # for protocol_key in mod_pro.protocol:
        #     protocol = mod_pro.protocol[protocol_key]
        #     # 替换已存在的函数参数
        #     str,ret = replace_lib_fun_param(str, protocol)
        #     # 添加不存在的函数
        #     if not ret:
        #         str = add_lib_fun_param(str, protocol)
            
        # # 遍历结构
        # for record_obj in pro_mod.mod.record_define:
        #     # 添加不存在的结构转换函数
        #     str = add_record_p_str(str, pro_mod, record_obj)
    else:
        # 不存在文件
        # 创建新的internal文件
        str = create_internal_file(mod_name, records, protocols)
        
    # 写到文件
    with open(file_name, 'w', encoding = "utf-8") as f:
        f.write(str)

# 创建新的rpc文件
def create_internal_file(mod_name, records, protocols):
    mod_pro = protocols[mod_name]
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

    

# 获取 获取字符串
def get_internal_file_get_str(pro_mod):
    get_str = """
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
    record_list = get_record_list(mod_pro)
    # 是否也在别的协议里
    for protocol_key in protocols:
        tmp_mod_pro = protocols[protocol_key]
        if tmp_mod_pro.name == mod_pro.name:
            continue
        tmp_record_list = get_record_list(tmp_mod_pro)
        sub_record_list = []
        for item in record_list:
            if item not in tmp_record_list:
                sub_record_list.append(item)
        record_list = sub_record_list
    # 生成字符串
    str = ""
    for record in record_list:
        str += get_record_p_str_1(records[record])
    return str 
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

# 获取 check字符串
def get_internal_file_check_str(pro_mod):
    str = "\n\n\n%% @doc 检查函数"
    for protocol_key in pro_mod.request_key:
        str += get_internal_file_check_str_1(pro_mod, protocol_key)
    return str

def get_internal_file_check_str_1(pro_mod, protocol_key):
    check_fun = """
%%%% @doc 检查%s
check_%s(%s) ->
	ok.
    """
    protocol_obj = pro_mod.protocol_map[protocol_key]
    tmp_check_fun = check_fun%(
        protocol_obj.desc[2:]
        , HelpLib.get_fun_name(pro_mod, protocol_key)
        , HelpLib.get_fun_param(protocol_obj)
    )
    return tmp_check_fun

# 获取 do字符串
def get_internal_file_do_str(pro_mod):
    str = "\n\n\n%% @doc 修改函数"
    for protocol_key in pro_mod.request_key:
        str += get_internal_file_do_str_1(pro_mod, protocol_key)
    return str

def get_internal_file_do_str_1(pro_mod, protocol_key):
    do_fun = """
%%%% @doc %s
do_%s(%s) ->
	{ok, #%s{}}.
    """
    protocol_obj = pro_mod.protocol_map[protocol_key]
    tmp_do_fun = do_fun%(
        protocol_obj.desc[2:]
        , HelpLib.get_fun_name(pro_mod, protocol_key)
        , HelpLib.get_fun_param(protocol_obj)
        , protocol_key.replace("request", "reply")
    )
    return tmp_do_fun


# 替换已存在的函数参数
def replace_lib_fun_param(str, pro_mod, protocol_obj):
    protocol_key = protocol_obj.protocol_key
    # api_str是否存在
    api_str = get_internal_file_api_str(pro_mod, protocol_key)[:-4]
    if str.find(api_str) == -1:
        return str,False
    
    # 替换rpc接口函数参数
    fun_name = HelpLib.get_fun_name(pro_mod, protocol_key)
    begin_str = "\n%s"%(fun_name)
    # 正则匹配函数
    a = r"(.*)" + begin_str + "\((.*?)\) ->(.*)"
    matchObj = re.match(a, str, re.M|re.S)
    if matchObj:
        str = "{0}{1}({2}) ->{3}".format(
                matchObj.group(1)
                , begin_str
                , HelpLib.get_fun_param(protocol_obj)
                , matchObj.group(3)
            )
    else:
        # 匹配不到
        print("替换rpc接口函数参数 err : %s"%(protocol_key))
        
    return str,True
    

    
# 添加不存在的函数
def add_lib_fun_param(str, pro_mod, protocol_obj):
    protocol_key = protocol_obj.protocol_key
    last_protocol_key = HelpLib.get_last_protocol_key(pro_mod, protocol_key)
    # 添加api_str
    # 上一个函数所在的位置
    last_fun_name = HelpLib.get_fun_name(pro_mod, last_protocol_key)
    api_str = get_internal_file_api_str(pro_mod, last_protocol_key)[:-2]
    last_fun_name_pos = str.find(api_str)
    # 上个函数下方函数的位置
    end_fun_pos = last_fun_name_pos + len(api_str)
    api_str = get_internal_file_api_str(pro_mod, protocol_key)[:-2]
    str = str[:end_fun_pos] + ",\n" + api_str +  str[end_fun_pos:]
    
    # 添加lib_fun
    # 上一个函数所在的位置
    last_fun_name = HelpLib.get_fun_name(pro_mod, last_protocol_key)
    find_str = "\n%s("%(last_fun_name)
    last_fun_name_pos = str.find(find_str)
    # 上个函数下方函数的位置
    end_fun_pos = str.find("\n%%", last_fun_name_pos)
    lib_fun_str = get_internal_file_mod_str(pro_mod, protocol_key)
    str = str[:end_fun_pos] + lib_fun_str + "\n" +  str[end_fun_pos:]
    
    # 添加check_fun
    # 上一个函数所在的位置
    find_str = "\ncheck_%s("%(last_fun_name)
    last_fun_name_pos = str.find(find_str)
    # 上个函数下方函数的位置
    end_fun_pos = str.find("\n%%", last_fun_name_pos)
    check_fun_str = get_internal_file_check_str_1(pro_mod, protocol_key)
    str = str[:end_fun_pos] + check_fun_str + "\n" +  str[end_fun_pos:]
    
    # 添加do_fun
    # 上一个函数所在的位置
    find_str = "\ndo_%s("%(last_fun_name)
    last_fun_name_pos = str.find(find_str)
    # 上个函数下方函数的位置
    end_fun_pos = str.find("\n%%", last_fun_name_pos)
    do_fun_str = get_internal_file_do_str_1(pro_mod, protocol_key)
    str = str[:end_fun_pos] + do_fun_str + "\n" +  str[end_fun_pos:]
    
    return str

# 添加结构转换函数
def add_record_p_str(str, pro_mod, record_obj):
    # 结构转换函数是否存在
    record_name = record_obj[0]
    find_str = "\nto_%s("%(record_name)
    if str.find(find_str) >= 0:
        return str
    
    # 上一个函数所在位置
    last_record_key = HelpLib.get_last_record_key(pro_mod, record_obj[0])
    find_str = "\nto_%s("%(last_record_key)
    last_fun_name_pos = str.find(find_str)
    # 是否存在上一个的位置
    if last_fun_name_pos == -1:
        # 获取save_info的位置
        find_str = "\nsave_info("
        last_fun_name_pos = str.find(find_str)
    # 上个函数下方函数的位置
    end_fun_pos = str.find("\n%%", last_fun_name_pos)
    record_p_str = get_record_p_str_1(record_obj)
    str = str[:end_fun_pos] + record_p_str + "\n" +  str[end_fun_pos:]
    return str