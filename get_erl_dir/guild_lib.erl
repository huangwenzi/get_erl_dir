
%%%-------------------------------------------------------------------
%%% @author hw
%%% @copyright (C) 2021, <COMPANY>
%%% @doc
%%%
%%% @end
%%% Created : 8. 3月 2021 20:26
%%%-------------------------------------------------------------------

-module(guild_lib).
-author("hw").

-include("guild.hrl").
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
	player_info/1,
	list/1,
	view/2,
	create/4,
	apply_join/2,
	info/1,
	member_list/1,
	apply_join_list/1,
	approve_join/3,
	set_auto_apply/1,
	set_join_cond/3,
	modify_name/2,
	modify_icon/2,
	modify_notice/2,
	appoint/3,
	kick/2,
	transfer/2,
	disband/1,
	quit/1,
	donate_info/1,
	donate/2,
	donate_receive/2,
	skill_info/1,
	skill_lv_up/2,
	warehouse_info/1,
	warehouse_sell/4,
	warehouse_buy/4,
	warehouse_clear/3,
	hunting_info/1,
	hunting_inspire/1,
	hunting_challenge/3,
	hunting_blocking_list/1,
	hunting_blocking/4,
	hunting_blocking_rec/1,
	hunting_blocking_lineup/2,
	hunting_log/1,
	hunting_rank_inside/1,
	hunting_receive/1
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


%% @doc 请求玩家的部族数据
player_info(Player) ->
	try check_player_info(Player) of
		{ok} ->
			P1 = do_player_info(Player),
			{ok, P1, #guild_player_info_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 请求部族列表
list(Player) ->
	try check_list(Player) of
		{ok} ->
			P1 = do_list(Player),
			{ok, P1, #guild_list_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 查看部族信息（公共）
view(Player, Id) ->
	try check_view(Player, Id) of
		{ok} ->
			P1 = do_view(Player, Id),
			{ok, P1, #guild_view_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 创建部族
create(Player, Name, Icon, Notice) ->
	try check_create(Player, Name, Icon, Notice) of
		{ok} ->
			P1 = do_create(Player, Name, Icon, Notice),
			{ok, P1, #guild_create_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 申请加入部族
apply_join(Player, Id) ->
	try check_apply_join(Player, Id) of
		{ok} ->
			P1 = do_apply_join(Player, Id),
			{ok, P1, #guild_apply_join_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 请求玩家所在的部族信息
info(Player) ->
	try check_info(Player) of
		{ok} ->
			P1 = do_info(Player),
			{ok, P1, #guild_info_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 请求部族成员列表
member_list(Player) ->
	try check_member_list(Player) of
		{ok} ->
			P1 = do_member_list(Player),
			{ok, P1, #guild_member_list_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 请求部族申请列表
apply_join_list(Player) ->
	try check_apply_join_list(Player) of
		{ok} ->
			P1 = do_apply_join_list(Player),
			{ok, P1, #guild_apply_join_list_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 审批申请加入部族的玩家
approve_join(Player, ApplyPlayerId, IsAgree) ->
	try check_approve_join(Player, ApplyPlayerId, IsAgree) of
		{ok} ->
			P1 = do_approve_join(Player, ApplyPlayerId, IsAgree),
			{ok, P1, #guild_approve_join_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 设置自动审批
set_auto_apply(Player) ->
	try check_set_auto_apply(Player) of
		{ok} ->
			P1 = do_set_auto_apply(Player),
			{ok, P1, #guild_set_auto_apply_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 设置加入条件
set_join_cond(Player, LevelId, PowerId) ->
	try check_set_join_cond(Player, LevelId, PowerId) of
		{ok} ->
			P1 = do_set_join_cond(Player, LevelId, PowerId),
			{ok, P1, #guild_set_join_cond_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 修改部族名字
modify_name(Player, NewName) ->
	try check_modify_name(Player, NewName) of
		{ok} ->
			P1 = do_modify_name(Player, NewName),
			{ok, P1, #guild_modify_name_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 修改部族旗帜
modify_icon(Player, NewIcon) ->
	try check_modify_icon(Player, NewIcon) of
		{ok} ->
			P1 = do_modify_icon(Player, NewIcon),
			{ok, P1, #guild_modify_icon_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 修改部族公告
modify_notice(Player, NewNotice) ->
	try check_modify_notice(Player, NewNotice) of
		{ok} ->
			P1 = do_modify_notice(Player, NewNotice),
			{ok, P1, #guild_modify_notice_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 任命职位
appoint(Player, PlayerId, Position) ->
	try check_appoint(Player, PlayerId, Position) of
		{ok} ->
			P1 = do_appoint(Player, PlayerId, Position),
			{ok, P1, #guild_appoint_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 踢人
kick(Player, PlayerId) ->
	try check_kick(Player, PlayerId) of
		{ok} ->
			P1 = do_kick(Player, PlayerId),
			{ok, P1, #guild_kick_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 族长转让
transfer(Player, PlayerId) ->
	try check_transfer(Player, PlayerId) of
		{ok} ->
			P1 = do_transfer(Player, PlayerId),
			{ok, P1, #guild_transfer_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 部族解散
disband(Player) ->
	try check_disband(Player) of
		{ok} ->
			P1 = do_disband(Player),
			{ok, P1, #guild_disband_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 退出部族
quit(Player) ->
	try check_quit(Player) of
		{ok} ->
			P1 = do_quit(Player),
			{ok, P1, #guild_quit_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 祭祀信息
donate_info(Player) ->
	try check_donate_info(Player) of
		{ok} ->
			P1 = do_donate_info(Player),
			{ok, P1, #guild_donate_info_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 进行祭祀
donate(Player, Type) ->
	try check_donate(Player, Type) of
		{ok} ->
			P1 = do_donate(Player, Type),
			{ok, P1, #guild_donate_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 请求领取祭祀进度奖励
donate_receive(Player, Id) ->
	try check_donate_receive(Player, Id) of
		{ok} ->
			P1 = do_donate_receive(Player, Id),
			{ok, P1, #guild_donate_receive_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 请求部族技能信息
skill_info(Player) ->
	try check_skill_info(Player) of
		{ok} ->
			P1 = do_skill_info(Player),
			{ok, P1, #guild_skill_info_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 部族技能升级
skill_lv_up(Player, Type) ->
	try check_skill_lv_up(Player, Type) of
		{ok} ->
			P1 = do_skill_lv_up(Player, Type),
			{ok, P1, #guild_skill_lv_up_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 请求部族仓库信息
warehouse_info(Player) ->
	try check_warehouse_info(Player) of
		{ok} ->
			P1 = do_warehouse_info(Player),
			{ok, P1, #guild_warehouse_info_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 部族仓库存物品
warehouse_sell(Player, Type, ItemId, ItemGroup) ->
	try check_warehouse_sell(Player, Type, ItemId, ItemGroup) of
		{ok} ->
			P1 = do_warehouse_sell(Player, Type, ItemId, ItemGroup),
			{ok, P1, #guild_warehouse_sell_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 部族仓库兑换物品
warehouse_buy(Player, Type, Id, ItemGroup) ->
	try check_warehouse_buy(Player, Type, Id, ItemGroup) of
		{ok} ->
			P1 = do_warehouse_buy(Player, Type, Id, ItemGroup),
			{ok, P1, #guild_warehouse_buy_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 部族仓库清理物品
warehouse_clear(Player, ItemId, ItemGroup) ->
	try check_warehouse_clear(Player, ItemId, ItemGroup) of
		{ok} ->
			P1 = do_warehouse_clear(Player, ItemId, ItemGroup),
			{ok, P1, #guild_warehouse_clear_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 请求部族狩猎的信息
hunting_info(Player) ->
	try check_hunting_info(Player) of
		{ok} ->
			P1 = do_hunting_info(Player),
			{ok, P1, #guild_hunting_info_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 请求部族狩猎鼓舞
hunting_inspire(Player) ->
	try check_hunting_inspire(Player) of
		{ok} ->
			P1 = do_hunting_inspire(Player),
			{ok, P1, #guild_hunting_inspire_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 请求部族狩猎挑战
hunting_challenge(Player, InBattle, Formation) ->
	try check_hunting_challenge(Player, InBattle, Formation) of
		{ok} ->
			P1 = do_hunting_challenge(Player, InBattle, Formation),
			{ok, P1, #guild_hunting_challenge_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 请求部族狩猎阻击列表
hunting_blocking_list(Player) ->
	try check_hunting_blocking_list(Player) of
		{ok} ->
			P1 = do_hunting_blocking_list(Player),
			{ok, P1, #guild_hunting_blocking_list_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 请求部族狩猎阻击
hunting_blocking(Player, ToPlayerId, InBattle, Formation) ->
	try check_hunting_blocking(Player, ToPlayerId, InBattle, Formation) of
		{ok} ->
			P1 = do_hunting_blocking(Player, ToPlayerId, InBattle, Formation),
			{ok, P1, #guild_hunting_blocking_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 请求部族狩猎阻击记录
hunting_blocking_rec(Player) ->
	try check_hunting_blocking_rec(Player) of
		{ok} ->
			P1 = do_hunting_blocking_rec(Player),
			{ok, P1, #guild_hunting_blocking_rec_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 请求部族狩猎阻击阵容
hunting_blocking_lineup(Player, ToPlayerId) ->
	try check_hunting_blocking_lineup(Player, ToPlayerId) of
		{ok} ->
			P1 = do_hunting_blocking_lineup(Player, ToPlayerId),
			{ok, P1, #guild_hunting_blocking_lineup_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 请求部族狩猎日志
hunting_log(Player) ->
	try check_hunting_log(Player) of
		{ok} ->
			P1 = do_hunting_log(Player),
			{ok, P1, #guild_hunting_log_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 请求部族狩猎族内排行信息
hunting_rank_inside(Player) ->
	try check_hunting_rank_inside(Player) of
		{ok} ->
			P1 = do_hunting_rank_inside(Player),
			{ok, P1, #guild_hunting_rank_inside_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    
%% @doc 部族狩猎领取奖励
hunting_receive(Player) ->
	try check_hunting_receive(Player) of
		{ok} ->
			P1 = do_hunting_receive(Player),
			{ok, P1, #guild_hunting_receive_reply{}}
	catch throw : Code ->
		{false, Code}
	end.

    