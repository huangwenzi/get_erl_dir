import os
import re


import src.help_mod as HelpMod
import src.cfg as CfgMod

# 负责lib文件


# 生成lib文件
def create_lib_file(pro_mod):
    # lib文件名
    file_name = "{0}/{1}_lib.erl".format(pro_mod.dir_path, pro_mod.mod_name)
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
            str,ret = replace_lib_fun_param(str, pro_mod, protocol_obj)
            # 添加不存在的函数
            if not ret:
                str = add_lib_fun_param(str, pro_mod, protocol_obj)
            
        # 遍历结构
        for record_obj in pro_mod.mod.record_define:
            # 添加不存在的结构转换函数
            str = add_record_p_str(str, pro_mod, record_obj)
    else:
        # 不存在文件
        # 创建新的lib文件
        str = create_lib_file_1(pro_mod)
        
    # 写到文件
    with open(file_name, 'w', encoding = "utf-8") as f:
        f.write(str)

# 创建新的rpc文件
def create_lib_file_1(pro_mod):
    # 文件开头
    str = HelpMod.get_file_head_str()
    # mod字符串
    str += get_lib_file_mod_str(pro_mod)
    # API字符串
    str += get_lib_file_api_str(pro_mod)
    # init字符串
    str += get_lib_file_init_str()
    # lib_fun字符串
    str += get_lib_file_lib_fun_str(pro_mod)
    # 获取函数
    str += get_lib_file_get_str(pro_mod)
    # 结构转换函数
    str += get_record_p_str(pro_mod)
    # 检查函数
    str += get_lib_file_check_str(pro_mod)
    # 修改函数
    str += get_lib_file_do_str(pro_mod)
    return str
    



    
# lib文件
# 获取lib mod字符串
def get_lib_file_mod_str(pro_mod):
    # 模块名
    str = """
-module({0}_lib).
-author("{1}").

-include("{0}.hrl").
-include("player.hrl").
-include("event.hrl").
-include("task.hrl").
-include("common.hrl").
-include("erl_protocol_record.hrl").\n\n""".format(pro_mod.mod_name, CfgMod.author_name)
    return str

# 获取lib api字符串
def get_lib_file_api_str(pro_mod):
    # API
    api_str = """
%% API
-export([
    first_init/0,
    on_first_login_event/2,
    on_login_event/2,
    on_zero_timer_event/2,


"""
    # 遍历协议
    for protocol_key in pro_mod.request_key:
        api_str += get_api_str_1(pro_mod, protocol_key)
    if len(pro_mod.request_key) > 0:
        api_str = api_str[:-2]
    api_str += "\n]).\n"

    # gm
    gm_str = """
%% gm
-export([
]).\n\n
"""
    api_str += gm_str
    return api_str

def get_api_str_1(pro_mod, protocol_key):
    protocol_obj = pro_mod.protocol_map[protocol_key]
    fun_name = HelpMod.get_fun_name(pro_mod, protocol_key)
    param_num = len(protocol_obj.param)
    return "\t%s/%s,\n"%(fun_name, param_num+1)

# 获取lib init字符串
def get_lib_file_init_str():
    # 函数结构
    init_fun ="""
%% 初始化模块
first_init() ->
	event_dispatcher:add_event_listener_once(?EVENT_AFTER_FIRST_INIT, ?MODULE, on_first_login_event),
	event_dispatcher:add_event_listener(?EVENT_PLAYER_LOGIN, ?MODULE, on_login_event),
	event_dispatcher:add_event_listener(?EVENT_ZERO_TIMER, ?MODULE, on_zero_timer_event).

%% 登录初始化
on_first_login_event(_Player, _Param) ->
	ok.

%% 登录事件
on_login_event(_Player, _Param) ->
	ok.

%% 零点事件
on_zero_timer_event(_Player, _Param) ->
	ok.

"""
    return init_fun

# 获取lib lib_fun字符串
def get_lib_file_lib_fun_str(pro_mod):
    str = "\n\n\n%% @doc 协议函数"
    for protocol_key in pro_mod.request_key:
        tmp_lib_fun = get_lib_file_lib_fun_str_1(pro_mod, protocol_key)
        str += tmp_lib_fun
    return str

def get_lib_file_lib_fun_str_1(pro_mod, protocol_key):
    lib_fun = """
%% @doc {0}
{1}({2}) ->
	try check_{1}({2}) of
		ok ->
			do_{1}({2})
	catch throw : Code ->
		{{false, Code}}
	end.
    """
    protocol_obj = pro_mod.protocol_map[protocol_key]
    # 函数参数
    tmp_lib_fun = lib_fun.format(
        protocol_obj.desc
        , HelpMod.get_fun_name(pro_mod, protocol_key)
        , HelpMod.get_fun_param(protocol_obj)
    )
    return tmp_lib_fun
    

# 获取lib 获取字符串
def get_lib_file_get_str(pro_mod):
    str = """
\n\n\n
%% @doc 获取函数
%% @doc 获取数据
-spec lookup(PlayerId :: integer()) -> #player_{0}{{}}.
lookup(PlayerId) when is_integer(PlayerId) ->
	case cache_unit:lookup(cache_player_{0}, PlayerId) of
		undefined ->
			#player_{0}{{
				player_id = PlayerId
			}};
		{1} -> {1}
	end;
lookup(Player) ->
	lookup(player_lib:player_id(Player)).

%% @doc 保存数据
save_info({1}) ->
	cache_unit:insert(cache_player_{0}, {1}).
    """
    str = str.format(
        pro_mod.mod_name
        , HelpMod.get_erl_val_name(pro_mod.mod_name)
    )
    return str

# 结构转换函数
def get_record_p_str(pro_mod):
    # 遍历协议
    str = ""
    for record_obj in pro_mod.mod.record_define:
        str += get_record_p_str_1(record_obj)
    return str 

# 玩法数据结构
def get_record_p_str_1(record_obj):
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
    record_name = record_obj[0][:-2]
    record_param_str,record_param_str_1 = HelpMod.get_record_param_str(record_obj[1])

    str = str.format(
        "to_%s_p"%(record_name)
        , record_name
        , HelpMod.get_erl_val_name(record_name)
        , record_param_str
        , record_param_str_1
    )
    return str 

# 获取lib check字符串
def get_lib_file_check_str(pro_mod):
    str = "\n\n\n%% @doc 检查函数"
    for protocol_key in pro_mod.request_key:
        str += get_lib_file_check_str_1(pro_mod, protocol_key)
    return str

def get_lib_file_check_str_1(pro_mod, protocol_key):
    check_fun = """
%%%% @doc 检查%s
check_%s(%s) ->
	ok.
    """
    protocol_obj = pro_mod.protocol_map[protocol_key]
    tmp_check_fun = check_fun%(
        protocol_obj.desc[2:]
        , HelpMod.get_fun_name(pro_mod, protocol_key)
        , HelpMod.get_fun_param(protocol_obj)
    )
    return tmp_check_fun

# 获取lib do字符串
def get_lib_file_do_str(pro_mod):
    str = "\n\n\n%% @doc 修改函数"
    for protocol_key in pro_mod.request_key:
        str += get_lib_file_do_str_1(pro_mod, protocol_key)
    return str

def get_lib_file_do_str_1(pro_mod, protocol_key):
    do_fun = """
%%%% @doc %s
do_%s(%s) ->
	{ok, #%s{}}.
    """
    protocol_obj = pro_mod.protocol_map[protocol_key]
    tmp_do_fun = do_fun%(
        protocol_obj.desc[2:]
        , HelpMod.get_fun_name(pro_mod, protocol_key)
        , HelpMod.get_fun_param(protocol_obj)
        , protocol_key.replace("request", "reply")
    )
    return tmp_do_fun


# 替换已存在的函数参数
def replace_lib_fun_param(str, pro_mod, protocol_obj):
    protocol_key = protocol_obj.protocol_key
    # api_str是否存在
    api_str = get_api_str_1(pro_mod, protocol_key)[:-2]
    if str.find(api_str) == -1:
        return str,False
    
    # 替换rpc接口函数参数
    fun_name = HelpMod.get_fun_name(pro_mod, protocol_key)
    begin_str = "\n%s"%(fun_name)
    # 正则匹配函数
    a = r"(.*)" + begin_str + "\((.*?)\) ->(.*)"
    matchObj = re.match(a, str, re.M|re.S)
    if matchObj:
        str = "{0}{1}({2}) ->{3}".format(
                matchObj.group(1)
                , begin_str
                , HelpMod.get_fun_param(protocol_obj)
                , matchObj.group(3)
            )
    else:
        # 匹配不到
        print("替换rpc接口函数参数 err : %s"%(protocol_key))
        
    return str,True
    

    
# 添加不存在的函数
def add_lib_fun_param(str, pro_mod, protocol_obj):
    protocol_key = protocol_obj.protocol_key
    last_protocol_key = HelpMod.get_last_protocol_key(pro_mod, protocol_key)
    # 添加api_str
    # 上一个函数所在的位置
    last_fun_name = HelpMod.get_fun_name(pro_mod, last_protocol_key)
    api_str = get_api_str_1(pro_mod, last_protocol_key)[:-2]
    last_fun_name_pos = str.find(api_str)
    # 上个函数下方函数的位置
    end_fun_pos = last_fun_name_pos + len(api_str)
    api_str = get_api_str_1(pro_mod, protocol_key)[:-2]
    str = str[:end_fun_pos] + ",\n" + api_str +  str[end_fun_pos:]
    
    # 添加lib_fun
    # 上一个函数所在的位置
    last_fun_name = HelpMod.get_fun_name(pro_mod, last_protocol_key)
    find_str = "\n%s("%(last_fun_name)
    last_fun_name_pos = str.find(find_str)
    # 上个函数下方函数的位置
    end_fun_pos = str.find("\n%%", last_fun_name_pos)
    lib_fun_str = get_lib_file_lib_fun_str_1(pro_mod, protocol_key)
    str = str[:end_fun_pos] + lib_fun_str + "\n" +  str[end_fun_pos:]
    
    # 添加check_fun
    # 上一个函数所在的位置
    find_str = "\ncheck_%s("%(last_fun_name)
    last_fun_name_pos = str.find(find_str)
    # 上个函数下方函数的位置
    end_fun_pos = str.find("\n%%", last_fun_name_pos)
    check_fun_str = get_lib_file_check_str_1(pro_mod, protocol_key)
    str = str[:end_fun_pos] + check_fun_str + "\n" +  str[end_fun_pos:]
    
    # 添加do_fun
    # 上一个函数所在的位置
    find_str = "\ndo_%s("%(last_fun_name)
    last_fun_name_pos = str.find(find_str)
    # 上个函数下方函数的位置
    end_fun_pos = str.find("\n%%", last_fun_name_pos)
    do_fun_str = get_lib_file_do_str_1(pro_mod, protocol_key)
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
    last_record_key = HelpMod.get_last_record_key(pro_mod, record_obj[0])
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