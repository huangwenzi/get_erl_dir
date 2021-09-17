%%% @author hw
%%% @date 2021.08.05
%%% @doc 奖池抽奖

-module(mod_luck_draw).

-behaviour(gen_mod).

-include("common.hrl").
-include("role.hrl").
-include("proto_luck_draw_pb.hrl").

%% @doc gen_mod回调函数
-export([i/1, p/1, init/0, register_event/0, init_role/1, send_info/1, on_timer/2, terminate_role/1, delete_role/1, clear_daily/2,
    handle_c2s/2, handle_timeout/2, handle_s2s_call/2, handle_s2s_cast/2, is_handle_c2s/2,
    is_handle_s2s_cast/2]).
-export([gm/3]).

%% @doc 运行信息
i(#role{}) ->
    [].

%% @doc 打印信息
p(_Info) ->
    "".

%% @doc 初始化
init() ->
    ?MOD_INIT().

%% @doc 关心的事件
register_event() ->
    [].

%% @doc 玩家进程初始化
init_role(_RoleId) ->
    ok.

%% @doc 玩家登录或重登后发送数据
send_info(_RoleId) ->
    ok.

%% @doc 定时执行
on_timer(_RoleId,_LoopCount) ->
	ok.

%% @doc 玩家结束
terminate_role(_RoleId) ->
    ok.

%% @doc 数据清理
delete_role(_RoleId) ->
    ok.

%% @doc 清除daily
clear_daily(_RoleId, _IsLogin) ->
    ok.

%% @doc 检测c2s处理条件
is_handle_c2s(_Req, #role_state{type = ?STATE_TYPE_ROLE}) ->
    true.

%% @doc 检测s2s_cast处理条件
is_handle_s2s_cast(_Req, #role_state{type = ?STATE_TYPE_ROLE}) ->
    true.

%% 协议
handle_c2s(Proto, #role_state{id = RoleId}) ->
    case handle_c2s_1(Proto, RoleId) of
        {false, Code} -> role_notice:send_self_one_msg(Code);
        Rec -> game_send:role(RoleId, Rec)
    end.

%% 奖池信息
handle_c2s_1(#luck_draw_recruit_info_c2s{}, RoleId) ->
    luck_draw_internal:recruit_info(RoleId);

%% 招聘单次
handle_c2s_1(#luck_draw_recruit_one_c2s{type = Type}, RoleId) ->
    luck_draw_internal:recruit_one(RoleId, Type);

%% 招聘十连
handle_c2s_1(#luck_draw_recruit_ten_c2s{type = Type}, RoleId) ->
    luck_draw_internal:recruit_ten(RoleId, Type);

%% 人脉兑换
handle_c2s_1(#luck_draw_contacts_c2s{type = Type}, RoleId) ->
    luck_draw_internal:contacts(RoleId, Type);

%% 修改动画状态
handle_c2s_1(#luck_draw_change_state_c2s{type = Type}, RoleId) ->
    luck_draw_internal:change_state(RoleId, Type);


%% @doc 其他未知协议
handle_c2s_1(_Req, _State) ->
    ?WARN("收到未知c2s消息:~p", [_Req]),
    {error, unknow_proto}.

handle_timeout(_Event, State) ->
    ?ERROR("收到未知timeout事件:~p", [_Event]),
    {ok, State}.

%% @doc 处理来自其它服务的call
handle_s2s_call(_Req, RoleState) ->
    ?ERROR("未知的s2s_call请求: ~p", [_Req]),
    {ok, RoleState}.


%% @doc 处理来自其它服务的cast
handle_s2s_cast(_Req, _RoleState) ->
    ?ERROR("未知的s2s_cast请求: ~p", [_Req]),
    ok.

%% ====================================================================
%% External functions
%% ====================================================================


%% ====================================================================
%% Internal functions
%% ====================================================================

%% gm Args 非int的参数需要单独匹配
gm(GmId, RoleId, List) ->
    List1 = [erlang:list_to_integer(Num) || Num <- List],
    gm_1(GmId, RoleId, List1).

gm_1(reset, RoleId, []) ->
    luck_draw_internal:gm_reset(RoleId),
    ?INFO("luck_draw_internal reset", []),
    ok;
gm_1(GmId, _RoleId, Args) ->
    ?INFO("不存在GmId:~p, Args:~p", [GmId, Args]),
    ok.