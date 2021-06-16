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
        protocol_obj = pro_mod.protocol_map[protocol_key]
        fun_name = HelpMod.get_fun_name(pro_mod, protocol_key)
        param_num = len(protocol_obj.param)
        tmp_api_str = "\t%s/%s,\n"%(fun_name, param_num+1)
        api_str += tmp_api_str
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
    for protocol_key in pro_mod.request_key:
        protocol_obj = pro_mod.protocol_map[protocol_key]
        # 函数参数
        tmp_lib_fun = lib_fun.format(
            protocol_obj.desc
            , HelpMod.get_fun_name(pro_mod, protocol_key)
            , HelpMod.get_fun_param(protocol_obj)
        )
        str += tmp_lib_fun
    return str

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
    # 首字母大写
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
    check_fun = """
%%%% @doc 检查%s
check_%s(%s) ->
	ok.
    """
    for protocol_key in pro_mod.request_key:
        protocol_obj = pro_mod.protocol_map[protocol_key]
        tmp_check_fun = check_fun%(
            protocol_obj.desc[2:]
            , HelpMod.get_fun_name(pro_mod, protocol_key)
            , HelpMod.get_fun_param(protocol_obj)
        )
        str += tmp_check_fun
    return str

# 获取lib do字符串
def get_lib_file_do_str(pro_mod):
    str = "\n\n\n%% @doc 修改函数"
    do_fun = """
%%%% @doc %s
do_%s(%s) ->
	{ok, #%s{}}.
    """
    for protocol_key in pro_mod.request_key:
        protocol_obj = pro_mod.protocol_map[protocol_key]
        tmp_do_fun = do_fun%(
            protocol_obj.desc[2:]
            , HelpMod.get_fun_name(pro_mod, protocol_key)
            , HelpMod.get_fun_param(protocol_obj)
            , protocol_key.replace("request", "reply")
        )
        str += tmp_do_fun
    return str

# 替换已存在的函数参数
def replace_lib_fun_param(str, pro_mod, protocol_obj):
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
    fun_name = HelpMod.get_fun_name(pro_mod, protocol_key)
    begin_str = "%s_lib:%s\("%(mod_name, fun_name)
    begin_str_1 = "case %s_lib:%s("%(mod_name, fun_name)
    a = r"(.*)case " + begin_str + "(.*?) of(.*)"
    matchObj = re.match(a, str, re.M|re.S)
    if matchObj:
        str = matchObj.group(1) + begin_str_1 + HelpMod.get_fun_param(protocol_obj) + ") of" + matchObj.group(3)
    return str,True
    
# 添加不存在的函数
def add_lib_fun_param(str, pro_mod, protocol_obj):
    a = r"(.*)\nhandle\(Msg, _Player\)(.*)"
    matchObj = re.match(a, str, re.M|re.S)
    if matchObj:
        rpc_fun = HelpMod.get_rpc_file_protocol_fun_str(pro_mod, protocol_obj.protocol_key)
        str = matchObj.group(1) + rpc_fun + "\nhandle(Msg, _Player)" + matchObj.group(2)
    return str


