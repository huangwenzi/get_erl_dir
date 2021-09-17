import os
import re


import jx_erl.help_lib as HelpLib
import jx_erl.cfg as CfgLib

# 负责rpc文件


# 协议函数开头str
global_fun_head_str = """
%% 协议
handle_c2s(Proto, #role_state{id = RoleId}) ->
    case handle_c2s_1(Proto, RoleId) of
        {false, Code} -> role_notice:send_self_one_msg(Code);
        Rec -> game_send:role(RoleId, Rec)
    end.
"""


# 生成rpc文件
def create_file(mod_name, protocols):
    # rpc文件名
    file_name = "{0}/mod_{1}.erl".format(CfgLib.out_path, mod_name)
    str = ""
    mod_pro = protocols[mod_name]
    # 文件是否存在
    if os.path.exists(file_name):
        # 存在文件
        with open(file_name, 'r', encoding = "utf-8") as f:
            str = f.read()
        # 遍历协议
        last_protocol = None
        for protocol_name in mod_pro.protocol:
            tmp_protocol = mod_pro.protocol[protocol_name]
            # 替换已存在的函数参数
            ret,str = replace_fun_param(str, mod_name, tmp_protocol)
            # 添加不存在的函数
            if not ret:
                str = add_fun_param(str, mod_name, last_protocol, tmp_protocol)
            last_protocol = tmp_protocol
    else:
        # 不存在文件
        # 创建新的mod文件
        str = create_mod_file(mod_name, mod_pro)
        
    # 写到文件
    with open(file_name, 'w', encoding = "utf-8") as f:
        f.write(str)
        
    
# 创建新的mod文件
def create_mod_file(mod_name, mod_pro):
    # 文件开头
    str = HelpLib.get_file_head_str()
    # 遍历协议
    protocol_str = ""
    for protocol_name in mod_pro.protocol:
        tmp_protocol = mod_pro.protocol[protocol_name]
        # 协议函数
        protocol_str += get_protocol_fun_str(mod_name, tmp_protocol)
    ## 加一层rpc匹配容错
    protocol_str += """ 
handle_c2s_1(C2sRec, RoleState) ->
    ?ERROR("handle_c2s_1 err, {0}  C2sRec:[~p] RoleState:[~p]", [C2sRec, RoleState]),
    ok.
    """.format(mod_name)
    # mod字符串
    str += get_mod_str(mod_name, protocol_str)

    return str

# 替换函数参数
def replace_fun_param(str, mod_name, protocol):
    # 替换record参数
    # 注意()前面的\,会影响正则匹配
    begin_str = "\nhandle_c2s_1\(#%s{"%(mod_name + protocol.name + "c2s")
    # 正则匹配函数
    a = r"(.*)" + begin_str + "(.*?)}, RoleId(.*)"
    matchObj = re.match(a, str, re.M|re.S)
    if matchObj:
        str = matchObj.group(1) + begin_str + HelpLib.get_record_param(protocol.c2s) + "}, RoleId" + matchObj.group(3)
    else:
        # 匹配不到，说明没有这个函数
        return False,str
    
    # 替换lib参数
    "luck_draw_internal:recruit_one(RoleId, Type);"
    begin_str = "%s_internal:%s\(RoleId"%(mod_name, protocol.name)
    a = r"(.*)" + begin_str + "(.*?))(.*)"
    matchObj = re.match(a, str, re.M|re.S)
    if matchObj:
        str = matchObj.group(1) + begin_str +  HelpLib.get_fun_param(protocol.c2s) + ")" + matchObj.group(3)
    return True,str
    
# 添加函数
def add_fun_param(str, mod_name, last_protocol, tmp_protocol):
    # 是否存在上一个协议
    fun_str = get_protocol_fun_str(mod_name, tmp_protocol)
    if last_protocol:
        last_fun_str = get_protocol_fun_str(mod_name, last_protocol)
        a = r"(.*)" + last_fun_str + "(.*)"
        matchObj = re.match(a, str, re.M|re.S)
        if matchObj:
            str = matchObj.group(1) + fun_str + matchObj.group(2)
    else:
        # 这就是第一个
        a = r"(.*)" + global_fun_head_str + "\n(.*)"
        matchObj = re.match(a, str, re.M|re.S)
        if matchObj:
            str = matchObj.group(1) + global_fun_head_str + "\n\n" + fun_str + matchObj.group(2)
        pass
    return str

# 获取rpc mod字符串
def get_mod_str(mod_name, protocol_str):
    # 模块名
    str = """
-module(mod_%s).

-behaviour(gen_mod).

-include("common.hrl").
-include("role.hrl").
-include("proto_%s_pb.hrl").

%%%% @doc gen_mod回调函数
-export([i/1, p/1, init/0, register_event/0, init_role/1, send_info/1, on_timer/2, terminate_role/1, delete_role/1, clear_daily/2,
    handle_c2s/2, handle_timeout/2, handle_s2s_call/2, handle_s2s_cast/2, is_handle_c2s/2,
    is_handle_s2s_cast/2]).
-export([gm/3]).

%%%% @doc 运行信息
i(#role{}) ->
    [].

%%%% @doc 打印信息
p(_Info) ->
    "".

%%%% @doc 初始化
init() ->
    ?MOD_INIT().

%%%% @doc 关心的事件
register_event() ->
    [].

%%%% @doc 玩家进程初始化
init_role(_RoleId) ->
    ok.

%%%% @doc 玩家登录或重登后发送数据
send_info(_RoleId) ->
    ok.

%%%% @doc 定时执行
on_timer(_RoleId,_LoopCount) ->
	ok.

%%%% @doc 玩家结束
terminate_role(_RoleId) ->
    ok.

%%%% @doc 数据清理
delete_role(_RoleId) ->
    ok.

%%%% @doc 清除daily
clear_daily(_RoleId, _IsLogin) ->
    ok.

%%%% @doc 检测c2s处理条件
is_handle_c2s(_Req, #role_state{type = ?STATE_TYPE_ROLE}) ->
    true.

%%%% @doc 检测s2s_cast处理条件
is_handle_s2s_cast(_Req, #role_state{type = ?STATE_TYPE_ROLE}) ->
    true.

%s

%s

%%%% @doc 其他未知协议
handle_c2s_1(_Req, _State) ->
    ?WARN("收到未知c2s消息:~p", [_Req]),
    {error, unknow_proto}.

handle_timeout(_Event, State) ->
    ?ERROR("收到未知timeout事件:~p", [_Event]),
    {ok, State}.

%%%% @doc 处理来自其它服务的call
handle_s2s_call(_Req, RoleState) ->
    ?ERROR("未知的s2s_call请求: ~p", [_Req]),
    {ok, RoleState}.


%%%% @doc 处理来自其它服务的cast
handle_s2s_cast(_Req, _RoleState) ->
    ?ERROR("未知的s2s_cast请求: ~p", [_Req]),
    ok.

%%%% ====================================================================
%%%% External functions
%%%% ====================================================================


%%%% ====================================================================
%%%% Internal functions
%%%% ====================================================================

%%%% gm Args 非int的参数需要单独匹配
gm(GmId, RoleId, List) ->
    List1 = [erlang:list_to_integer(Num) || Num <- List],
    gm_1(GmId, RoleId, List1).

gm_1(GmId, _RoleId, Args) ->
    ?INFO("不存在GmId:~p, Args:~p", [GmId, Args]),
    ok.
    """%(mod_name, mod_name, global_fun_head_str, protocol_str)
    return str

# 获取rpc 协议函数字符串
def get_protocol_fun_str(mod_name, protocol):
    # 协议函数结构
    protocol_fun = """
%% {0}
handle_c2s_1(#{1}_{2}_c2s{{3}}, RoleId) ->
    {1}_internal:{2}(RoleId{4});
"""
    # 生成协议函数
    tmp_protocol_fun = protocol_fun.format(
        protocol.desc
        , mod_name
        , protocol.name
        , HelpLib.get_record_param(protocol.c2s)
        , HelpLib.get_fun_param(protocol.c2s)
    )
    return tmp_protocol_fun

