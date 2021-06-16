
%%%%%%-------------------------------------------------------------------
%%%%%% @author hw
%%%%%% @copyright (C) 2021, <COMPANY>
%%%%%% @doc
%%%%%%
%%%%%% @end
%%%%%% Created : 16. 6月 2021 20:44
%%%%%%-------------------------------------------------------------------

-module(bargain_lib).
-author("hw").

-include("bargain.hrl").
-include("player.hrl").
-include("event.hrl").
-include("task.hrl").
-include("common.hrl").
-include("erl_protocol_record.hrl").


%% API
-export([
    first_init/0,
    on_first_login_event/2,
    on_login_event/2,
    on_zero_timer_event/2,


	info/1,
	help/3,
	help_a/3,
	help_b/3
]).

%% gm
-export([
]).



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




%% @doc 协议函数
%% @doc 请求砍价礼包信息
info() ->
	try check_info() of
		ok ->
			do_info()
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 请求帮助砍价
help(FriendId, GiftId) ->
	try check_help(FriendId, GiftId) of
		ok ->
			do_help(FriendId, GiftId)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 请求帮助砍价
help_a(FriendId, GiftId) ->
	try check_help_a(FriendId, GiftId) of
		ok ->
			do_help_a(FriendId, GiftId)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 请求帮助砍价
help_b(FriendId, GiftId) ->
	try check_help_b(FriendId, GiftId) of
		ok ->
			do_help_b(FriendId, GiftId)
	catch throw : Code ->
		{false, Code}
	end.
    




%% @doc 获取函数
%% @doc 获取数据
-spec lookup(PlayerId :: integer()) -> #player_bargain{}.
lookup(PlayerId) when is_integer(PlayerId) ->
	case cache_unit:lookup(cache_player_bargain, PlayerId) of
		undefined ->
			#player_bargain{
				player_id = PlayerId
			};
		Bargain -> Bargain
	end;
lookup(Player) ->
	lookup(player_lib:player_id(Player)).

%% @doc 保存数据
save_info(Bargain) ->
	cache_unit:insert(cache_player_bargain, Bargain).
    
%% @doc 
to_bargain_gift_p(#bargain_gift{id = Id, help_list = HelpList, buy_count = BuyCount}) ->
	#bargain_gift_p{
		id = Id
		, help_list = HelpList
		, buy_count = BuyCount
	}.
to_bargain_gift_p([], List) -> List;
to_bargain_gift_p([BargainGift | T], List) ->
	to_bargain_gift_p(T, [to_bargain_gift_p(BargainGift) | List]).
    


%% @doc 检查函数
%% @doc 检查砍价礼包信息
check_info() ->
	ok.
    
%% @doc 检查帮助砍价
check_help(FriendId, GiftId) ->
	ok.
    
%% @doc 检查帮助砍价
check_help_a(FriendId, GiftId) ->
	ok.
    
%% @doc 检查帮助砍价
check_help_b(FriendId, GiftId) ->
	ok.
    


%% @doc 修改函数
%% @doc 砍价礼包信息
do_info() ->
	{ok, #bargain_info_reply{}}.
    
%% @doc 帮助砍价
do_help(FriendId, GiftId) ->
	{ok, #bargain_help_reply{}}.
    
%% @doc 帮助砍价
do_help_a(FriendId, GiftId) ->
	{ok, #bargain_help_a_reply{}}.
    
%% @doc 帮助砍价
do_help_b(FriendId, GiftId) ->
	{ok, #bargain_help_b_reply{}}.
    