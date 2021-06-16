# -*- coding: utf-8 -*-

# 根据协议生成erl文件
import datetime

## 加一层rpc匹配容错
# 容错匹配
# handle(Msg, _Player) ->
# 	?ERROR("module:[~p] handle msg error:[~p]", [?MODULE, Msg]),
# 	ok.


import mod_protocol.bargain as mod
_g_mod_name = "bargain"


# record字段长度
_g_record_len = 32


## 获取函数
# 获取协议对应的函数名
def get_fun_name(protocol_key):
    tmp_str = protocol_key[len(_g_mod_name):]
    begin = tmp_str.find("_")
    end = tmp_str.rfind("_")
    return tmp_str[begin+1 : end]

# 获取请求协议
def get_request_key():
    # 遍历协议
    protocol_list = mod.protocol_define.keys()
    key_list = []
    for protocol_key in protocol_list:
        # 只提取请求
        if protocol_key.find("_request") > 0:
            key_list.append(protocol_key)
    return key_list

# 获取协议参数 首字母 下划线后一个替换大写
def get_param_name(param):
    while True:
        idx = param.find("_")
        # 替换完退出
        if idx < 0:
            # 首字母替换大写
            param = param[:1].upper() + param[1:]
            return param
        # 下划线去掉，后一个替换大写
        tmp_1 = param[idx+1]
        tmp_1 = tmp_1.upper()
        param = param[:idx] + tmp_1 + param[idx+2:]

# 获取函数参数
def get_param_str(protocol_obj):
    # 遍历参数
    param_str = ""              # 获取协议参数
    param_str_1 = "Player, "    # lib函数参数
    for tmp_param in protocol_obj["payload"]:
        tmp_param_1 = get_param_name(tmp_param[0])
        param_str += "%s = %s, "%(tmp_param[0], tmp_param_1)
        param_str_1 += "%s, "%(tmp_param_1)
    if len(param_str) > 0:
        param_str = param_str[:-2]
    param_str_1 = param_str_1[:-2]
    return param_str,param_str_1

# 获取结构参数
def get_record_param_str(record_param):
    # 遍历参数
    param_str = ""
    for tmp_param in record_param:
        tmp_param_1 = get_param_name(tmp_param[0])
        param_str += "%s = %s, "%(tmp_param[0], tmp_param_1)
    if len(param_str) > 0:
        param_str = param_str[:-2]
    # ，号换行
    param_str_1 = param_str.replace(",", "\n\t\t,")
    return param_str,param_str_1

# 获取开头
def get_file_head_str():
    # 时间
    i = datetime.datetime.now()
    str = """
%%%%%%-------------------------------------------------------------------
%%%%%% @author hw
%%%%%% @copyright (C) %s, <COMPANY>
%%%%%% @doc
%%%%%%
%%%%%% @end
%%%%%% Created : %s. %s月 %s %s:%s
%%%%%%-------------------------------------------------------------------
"""""
    str = str%(i.year, i.day, i.month, i.year, i.hour, i.minute)
    return str

# 获取rpc mod字符串
def get_rpc_file_mod_str():
    # 模块名
    str = """
-module(%s_rpc).
-author("hw").

-include("erl_protocol_record.hrl").

%% API
-export([handle/2]).
    """%(_g_mod_name)
    return str

# 获取rpc 协议函数字符串
def get_rpc_file_protocol_fun_str(protocol_key):
    # 协议函数结构
    protocol_fun ="""
%%%% %s
handle(#%s{%s}, Player) ->
    case %s_lib:%s(%s) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #%s{code = Code}}
    end;\n"""
    # lib函数名
    fun_name = get_fun_name(protocol_key)
    protocol_obj = mod.protocol_define[protocol_key]
    # 函数参数
    param_str,param_str_1 = get_param_str(protocol_obj)
    # 生成协议函数
    tmp_protocol_fun = protocol_fun%(
        protocol_obj["desc"]
        , protocol_key
        , param_str
        , _g_mod_name
        , fun_name
        , param_str_1
        , protocol_key.replace("request", "reply")
    )
    return tmp_protocol_fun

# 获取lib mod字符串
def get_lib_file_mod_str():
    # 模块名
    str = """
-module(%s_lib).
-author("hw").

-include("%s.hrl").
-include("player.hrl").
-include("event.hrl").
-include("task.hrl").
-include("common.hrl").
-include("erl_protocol_record.hrl").\n\n"""%(_g_mod_name, _g_mod_name)
    return str

# 获取lib api字符串
def get_lib_file_api_str(request_list):
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
    for protocol_key in request_list:
        protocol_obj = mod.protocol_define[protocol_key]
        fun_name = get_fun_name(protocol_key)
        param_num = len(protocol_obj["payload"])
        tmp_api_str = "\t%s/%s,\n"%(fun_name, param_num + 1)
        api_str += tmp_api_str
    if len(protocol_key) > 0:
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
def get_lib_file_lib_fun_str(request_list):
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
    for protocol_key in request_list:
        protocol_obj = mod.protocol_define[protocol_key]
        fun_name = get_fun_name(protocol_key)
        # 函数参数
        param_str,param_str_1 = get_param_str(protocol_obj)

        tmp_lib_fun = lib_fun.format(
            protocol_obj["desc"]
            , fun_name
            , param_str_1
        )
        str += tmp_lib_fun
    return str

# 获取lib 获取字符串
def get_lib_file_get_str():
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
    mod_name_1 = get_param_name(_g_mod_name)
    str = str.format(
        _g_mod_name
        , mod_name_1

    )
    return str

# 获取lib check字符串
def get_lib_file_check_str(request_list):
    str = "\n\n\n%% @doc 检查函数"
    check_fun = """
%%%% @doc 检查%s
check_%s(%s) ->
	ok.
    """
    for protocol_key in request_list:
        protocol_obj = mod.protocol_define[protocol_key]
        fun_name = get_fun_name(protocol_key)
        # 函数参数
        param_str,param_str_1 = get_param_str(protocol_obj)

        tmp_check_fun = check_fun%(
            protocol_obj["desc"][2:]
            , fun_name
            , param_str_1
        )
        str += tmp_check_fun
    return str

# 获取lib do字符串
def get_lib_file_do_str(request_list):
    str = "\n\n\n%% @doc 修改函数"
    do_fun = """
%%%% @doc %s
do_%s(%s) ->
	{ok, #%s{}}.
    """
    for protocol_key in request_list:
        protocol_obj = mod.protocol_define[protocol_key]
        fun_name = get_fun_name(protocol_key)
        # 函数参数
        param_str,param_str_1 = get_param_str(protocol_obj)

        tmp_do_fun = do_fun%(
            protocol_obj["desc"][2:]
            , fun_name
            , param_str_1
            , protocol_key.replace("request", "reply")
        )
        str += tmp_do_fun
    return str

# 获取宏定义字符串
def get_def_str():
    str = """

-ifndef(%s_H_H_).
-define(%s_H_H_, 1).

    """
    mod_name_1 = _g_mod_name.upper()
    str = str%(mod_name_1, mod_name_1)
    return str 

# 玩法数据结构
def get_record_str():
    # 遍历协议
    str = ""
    for record_obj in mod.record_define:
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

# 结构转换函数
def get_record_p_str():
    # 遍历协议
    str = ""
    for record_obj in mod.record_define:
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
    record_name_upper = get_param_name(record_name)
    fun_name = "to_%s_p"%(record_name)
    record_param_str,record_param_str_1 = get_record_param_str(record_obj[1])

    str = str.format(
        fun_name
        , record_name
        , record_name_upper
        , record_param_str
        , record_param_str_1
    )
    return str 
# 获取record字段
def get_record_p_param(record_param_list):
    str = ""
    param_len = len(record_param_list)
    param_idx = 0
    # 遍历字段
    for tmp_param in record_param_list:
        # 参数
        param_idx += 1
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




# 获取rpc文件
def get_rpc_file():
    # 文件开头
    str = get_file_head_str()
    # mod字符串
    str += get_rpc_file_mod_str()

    # 遍历协议
    request_list = get_request_key()
    for protocol_key in request_list:
        # 协议函数
        protocol_fun = get_rpc_file_protocol_fun_str(protocol_key)
        str += protocol_fun
    # 替换最后的;
    str = str[: -2] + "."

    # 写到文件
    file_path = 'get_erl_dir/%s_rpc.erl'%(_g_mod_name)
    with open(file_path, 'w', encoding = "utf-8") as f:
        f.write(str)

# 获取lib文件
def get_lib_file():
    # 文件开头
    str = get_file_head_str()
    # mod字符串
    str += get_lib_file_mod_str()
    # API字符串
    request_list = get_request_key()
    str += get_lib_file_api_str(request_list)
    # init字符串
    str += get_lib_file_init_str()
    # lib_fun字符串
    str += get_lib_file_lib_fun_str(request_list)
    # 获取函数
    str += get_lib_file_get_str()
    # 结构转换函数
    str += get_record_p_str()
    # 检查函数
    str += get_lib_file_check_str(request_list)
    # 修改函数
    str += get_lib_file_do_str(request_list)

    # 写到文件
    file_path = 'get_erl_dir/%s_lib.erl'%(_g_mod_name)
    with open(file_path, 'w', encoding = "utf-8") as f:
        f.write(str)

# 获取hrl文件
def get_hrl_file():
    # 文件开头
    str = get_file_head_str()
    # 宏定义文件
    str += get_def_str()
    # 玩法数据结构
    str += get_record_str()
    # 玩家数据结构
    str += get_player_record_str()
    str += "\n-endif.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"

    # 写到文件
    file_path = 'get_erl_dir/%s.hrl'%(_g_mod_name)
    with open(file_path, 'w', encoding = "utf-8") as f:
        f.write(str)


def main():
    # 生成rpc文件
    get_rpc_file()
    # 生成lib文件
    get_lib_file()
    # 生成hrl文件
    get_hrl_file()
    # # 生成server文件
    # get_server_file()
    
main()




