# -*- coding: utf-8 -*-

# 根据协议生成erl文件
import datetime



import mod_protocol.guild as mod



# 获取协议对应的函数名
def get_fun_name(protocol_key):
    begin = protocol_key.find("_")
    end = protocol_key.rfind("_")
    return protocol_key[begin+1 : end]

# 获取协议参数
def get_param_name(param):
    while True:
        idx = param.find("_")
        # 替换完退出
        if idx < 0:
            param = param[:1].upper() + param[1:]
            return param
        # 替换大写
        tmp_1 = param[idx+1]
        tmp_1 = tmp_1.upper()
        param = param[:idx] + tmp_1 + param[idx+2:]


# 获取rpc文件
def get_rpc_file(mod_name):
    # 时间
    i = datetime.datetime.now()
    str = ""
    str += """
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

    # 模块名
    str += """
-module(%s_rpc).
-author("hw").

-include("erl_protocol_record.hrl").

%%%% API
-export([handle/2]).
    """%(mod_name)

    # 函数结构
    protocol_fun ="""
%%%% %s
handle(#%s{%s}, Player) ->
    case %s_lib:%s(%s) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #%s{code = Code}}
    end;\n"""
    protocol_list = mod.protocol_define.keys()
    for protocol_key in protocol_list:
        if protocol_key.find("_notify") > 0 or protocol_key.find("_reply") > 0:
            continue
        protocol_obj = mod.protocol_define[protocol_key]
        # 函数参数
        param_str = ""
        param_str_1 = "Player, "
        for tmp_param in protocol_obj["payload"]:
            tmp_param_1 = get_param_name(tmp_param[0])
            param_str += "%s = %s, "%(tmp_param[0], tmp_param_1)
            param_str_1 += "%s, "%(tmp_param_1)
        if len(param_str) > 0:
            param_str = param_str[:-2]
        param_str_1 = param_str_1[:-2]

        # lib函数名
        fun_name = get_fun_name(protocol_key)
        tmp_protocol_fun = protocol_fun%(
            protocol_obj["desc"]
            , protocol_key
            , param_str
            , mod_name
            , fun_name
            , param_str_1
            , protocol_key.replace("request", "reply")
        )
        str += tmp_protocol_fun

    # 替换最后的;
    str = str[: -2] + "."

    # 写到文件
    file_path = 'get_erl_dir/%s_rpc.erl'%(mod_name)
    with open(file_path, 'w', encoding = "utf-8") as f:
        f.write(str)


# 获取lib文件
def get_lib_file(mod_name):
    # 时间
    i = datetime.datetime.now()
    str = ""
    str += """
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

    # 模块名
    str += """
-module(%s_lib).
-author("hw").

-include("%s.hrl").
-include("player.hrl").
-include("event.hrl").
-include("task.hrl").
-include("common.hrl").
-include("erl_protocol_record.hrl").\n\n"""%(mod_name, mod_name)

    # API
    api_str = """
%%%% API
-export([
    first_init/0,
    on_first_login_event/2,
    on_login_event/2,
    on_zero_timer_event/2,
"""
    protocol_list = mod.protocol_define.keys()
    for protocol_key in protocol_list:
        if protocol_key.find("_notify") > 0 or protocol_key.find("_reply") > 0:
            continue
        protocol_obj = mod.protocol_define[protocol_key]
        fun_name = get_fun_name(protocol_key)
        param_num = len(protocol_obj["payload"])
        tmp_api_str = "\t%s/%s,\n"%(fun_name, param_num + 1)
        api_str += tmp_api_str
    if len(protocol_key) > 0:
        api_str = api_str[:-2]
    api_str += "\n]).\n"
    str += api_str

    # gm
    gm_str = """
%%%% gm
-export([
]).\n\n
"""
    str += gm_str



    # 函数结构
    init_fun ="""
%%%% 初始化模块
first_init() ->
	event_dispatcher:add_event_listener_once(?EVENT_AFTER_FIRST_INIT, ?MODULE, on_first_login_event),
	event_dispatcher:add_event_listener(?EVENT_PLAYER_LOGIN, ?MODULE, on_login_event),
	event_dispatcher:add_event_listener(?EVENT_ZERO_TIMER, ?MODULE, on_zero_timer_event).

%%%% 登录初始化
on_first_login_event(Player, _Param) ->
	ok.

%%%% 登录事件
on_login_event(Player, _Param) ->
	ok.

%%%% 零点事件
on_zero_timer_event(Player, _Param) ->
	ok.

"""
    str += init_fun


    lib_fun = """
%%%% @doc %s
%s(%s) ->
	try check_%s(%s) of
		{ok} ->
			P1 = do_%s(%s),
			{ok, P1, #%s{}}
	catch throw : Code ->
		{false, Code}
	end.

    """
    protocol_list = mod.protocol_define.keys()
    for protocol_key in protocol_list:
        if protocol_key.find("_notify") > 0 or protocol_key.find("_reply") > 0:
            continue
        protocol_obj = mod.protocol_define[protocol_key]
        fun_name = get_fun_name(protocol_key)
        # 函数参数
        param_str = "Player, "
        for tmp_param in protocol_obj["payload"]:
            tmp_param_1 = get_param_name(tmp_param[0])
            param_str += "%s, "%(tmp_param_1)
        param_str = param_str[:-2]

        tmp_lib_fun = lib_fun%(
            protocol_obj["desc"]
            , fun_name
            , param_str
            , fun_name
            , param_str
            , fun_name
            , param_str
            , protocol_key.replace("request", "reply")
        )
        str += tmp_lib_fun

    # 写到文件
    file_path = 'get_erl_dir/%s_lib.erl'%(mod_name)
    with open(file_path, 'w', encoding = "utf-8") as f:
        f.write(str)






def main():
    mod_name = "guild"
    # 生成rpc文件
    get_rpc_file(mod_name)
    # 生成lib文件
    get_lib_file(mod_name)
    
main()




