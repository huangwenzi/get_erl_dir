
%%%-------------------------------------------------------------------
%%% @author hw
%%% @copyright (C) 2021, <COMPANY>
%%% @doc
%%%
%%% @end
%%% Created : 8. 3月 2021 20:21
%%%-------------------------------------------------------------------

-module(bargain_lib).
-author("hw").

-include("bargain.hrl").
-include("player.hrl").
-include("event.hrl").
-include("task.hrl").
-include("common.hrl").
-include("erl_protocol_record.hrl").


%%%% API
-export([
    first_init/0,
    on_first_login_event/2,
    on_login_event/2,
    on_zero_timer_event/2,
	info/1,
	help/3
]).

%%%% gm
-export([
]).



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


%% @doc 请求砍价礼包信息
info(Player) ->
	try check_info(Player) of
		{ok} ->
			P1 = do_info(Player),
			{ok, P1, #bargain_info_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 请求帮助砍价
help(Player, FriendId, GiftId) ->
	try check_help(Player, FriendId, GiftId) of
		{ok} ->
			P1 = do_help(Player, FriendId, GiftId),
			{ok, P1, #bargain_help_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    