
%%%-------------------------------------------------------------------
%%% @author hw
%%% @copyright (C) 2021, <COMPANY>
%%% @doc
%%%
%%% @end
%%% Created : 7. 4月 2021 10:51
%%%-------------------------------------------------------------------

-module(guild_lib).
-author("hw").

-include("guild.hrl").
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
	hunting_receive/1,
	hunting_blocking_rec_new/1
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
%% @doc 请求玩家的部族数据
player_info(Player) ->
	try check_player_info(Player) of
		ok ->
			do_player_info(Player)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 请求部族列表
list(Player) ->
	try check_list(Player) of
		ok ->
			do_list(Player)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 查看部族信息（公共）
view(Player, Id) ->
	try check_view(Player, Id) of
		ok ->
			do_view(Player, Id)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 创建部族
create(Player, Name, Icon, Notice) ->
	try check_create(Player, Name, Icon, Notice) of
		ok ->
			do_create(Player, Name, Icon, Notice)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 申请加入部族
apply_join(Player, Id) ->
	try check_apply_join(Player, Id) of
		ok ->
			do_apply_join(Player, Id)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 请求玩家所在的部族信息
info(Player) ->
	try check_info(Player) of
		ok ->
			do_info(Player)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 请求部族成员列表
member_list(Player) ->
	try check_member_list(Player) of
		ok ->
			do_member_list(Player)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 请求部族申请列表
apply_join_list(Player) ->
	try check_apply_join_list(Player) of
		ok ->
			do_apply_join_list(Player)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 审批申请加入部族的玩家
approve_join(Player, ApplyPlayerId, IsAgree) ->
	try check_approve_join(Player, ApplyPlayerId, IsAgree) of
		ok ->
			do_approve_join(Player, ApplyPlayerId, IsAgree)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 设置自动审批
set_auto_apply(Player) ->
	try check_set_auto_apply(Player) of
		ok ->
			do_set_auto_apply(Player)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 设置加入条件
set_join_cond(Player, LevelId, PowerId) ->
	try check_set_join_cond(Player, LevelId, PowerId) of
		ok ->
			do_set_join_cond(Player, LevelId, PowerId)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 修改部族名字
modify_name(Player, NewName) ->
	try check_modify_name(Player, NewName) of
		ok ->
			do_modify_name(Player, NewName)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 修改部族旗帜
modify_icon(Player, NewIcon) ->
	try check_modify_icon(Player, NewIcon) of
		ok ->
			do_modify_icon(Player, NewIcon)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 修改部族公告
modify_notice(Player, NewNotice) ->
	try check_modify_notice(Player, NewNotice) of
		ok ->
			do_modify_notice(Player, NewNotice)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 任命职位
appoint(Player, PlayerId, Position) ->
	try check_appoint(Player, PlayerId, Position) of
		ok ->
			do_appoint(Player, PlayerId, Position)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 踢人
kick(Player, PlayerId) ->
	try check_kick(Player, PlayerId) of
		ok ->
			do_kick(Player, PlayerId)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 族长转让
transfer(Player, PlayerId) ->
	try check_transfer(Player, PlayerId) of
		ok ->
			do_transfer(Player, PlayerId)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 部族解散
disband(Player) ->
	try check_disband(Player) of
		ok ->
			do_disband(Player)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 退出部族
quit(Player) ->
	try check_quit(Player) of
		ok ->
			do_quit(Player)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 祭祀信息
donate_info(Player) ->
	try check_donate_info(Player) of
		ok ->
			do_donate_info(Player)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 进行祭祀
donate(Player, Type) ->
	try check_donate(Player, Type) of
		ok ->
			do_donate(Player, Type)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 请求领取祭祀进度奖励
donate_receive(Player, Id) ->
	try check_donate_receive(Player, Id) of
		ok ->
			do_donate_receive(Player, Id)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 请求部族技能信息
skill_info(Player) ->
	try check_skill_info(Player) of
		ok ->
			do_skill_info(Player)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 部族技能升级
skill_lv_up(Player, Type) ->
	try check_skill_lv_up(Player, Type) of
		ok ->
			do_skill_lv_up(Player, Type)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 请求部族仓库信息
warehouse_info(Player) ->
	try check_warehouse_info(Player) of
		ok ->
			do_warehouse_info(Player)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 部族仓库存物品
warehouse_sell(Player, Type, ItemId, ItemGroup) ->
	try check_warehouse_sell(Player, Type, ItemId, ItemGroup) of
		ok ->
			do_warehouse_sell(Player, Type, ItemId, ItemGroup)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 部族仓库兑换物品
warehouse_buy(Player, Type, Id, ItemGroup) ->
	try check_warehouse_buy(Player, Type, Id, ItemGroup) of
		ok ->
			do_warehouse_buy(Player, Type, Id, ItemGroup)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 部族仓库清理物品
warehouse_clear(Player, ItemId, ItemGroup) ->
	try check_warehouse_clear(Player, ItemId, ItemGroup) of
		ok ->
			do_warehouse_clear(Player, ItemId, ItemGroup)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 请求部族狩猎的信息
hunting_info(Player) ->
	try check_hunting_info(Player) of
		ok ->
			do_hunting_info(Player)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 请求部族狩猎鼓舞
hunting_inspire(Player) ->
	try check_hunting_inspire(Player) of
		ok ->
			do_hunting_inspire(Player)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 请求部族狩猎挑战
hunting_challenge(Player, InBattle, Formation) ->
	try check_hunting_challenge(Player, InBattle, Formation) of
		ok ->
			do_hunting_challenge(Player, InBattle, Formation)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 请求部族狩猎阻击列表
hunting_blocking_list(Player) ->
	try check_hunting_blocking_list(Player) of
		ok ->
			do_hunting_blocking_list(Player)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 请求部族狩猎阻击
hunting_blocking(Player, ToPlayerId, InBattle, Formation) ->
	try check_hunting_blocking(Player, ToPlayerId, InBattle, Formation) of
		ok ->
			do_hunting_blocking(Player, ToPlayerId, InBattle, Formation)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 请求部族狩猎阻击记录
hunting_blocking_rec(Player) ->
	try check_hunting_blocking_rec(Player) of
		ok ->
			do_hunting_blocking_rec(Player)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 请求部族狩猎阻击阵容
hunting_blocking_lineup(Player, ToPlayerId) ->
	try check_hunting_blocking_lineup(Player, ToPlayerId) of
		ok ->
			do_hunting_blocking_lineup(Player, ToPlayerId)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 请求部族狩猎日志
hunting_log(Player) ->
	try check_hunting_log(Player) of
		ok ->
			do_hunting_log(Player)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 请求部族狩猎族内排行信息
hunting_rank_inside(Player) ->
	try check_hunting_rank_inside(Player) of
		ok ->
			do_hunting_rank_inside(Player)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 部族狩猎领取奖励
hunting_receive(Player) ->
	try check_hunting_receive(Player) of
		ok ->
			do_hunting_receive(Player)
	catch throw : Code ->
		{false, Code}
	end.
    
%% @doc 部族狩猎新的被阻击日志（只显示新被阻击的日志）
hunting_blocking_rec_new(Player) ->
	try check_hunting_blocking_rec_new(Player) of
		ok ->
			do_hunting_blocking_rec_new(Player)
	catch throw : Code ->
		{false, Code}
	end.
    




%% @doc 获取函数
%% @doc 获取数据
-spec lookup(PlayerId :: integer()) -> #player_guild{}.
lookup(PlayerId) when is_integer(PlayerId) ->
	case cache_unit:lookup(cache_player_guild, PlayerId) of
		undefined ->
			#player_guild{
				player_id = PlayerId
			};
		Guild -> Guild
	end;
lookup(Player) ->
	lookup(player_lib:player_id(Player)).

%% @doc 保存数据
save_info(Guild) ->
	cache_unit:insert(cache_player_guild, Guild).
    
%% @doc 
to_guild_join_condition_p(#guild_join_condition{level_id = LevelId, power_id = PowerId}) ->
	#guild_join_condition_p{
		level_id = LevelId
		, power_id = PowerId
	}.
to_guild_join_condition_p([], List) -> List;
to_guild_join_condition_p([GuildJoinCondition | T], List) ->
	to_guild_join_condition_p(T, [to_guild_join_condition_p(GuildJoinCondition) | List]).
    
%% @doc 
to_guild_list_p(#guild_list{idx = Idx, id = Id, name = Name, icon = Icon, level = Level, num = Num, patriarch_pid = PatriarchPid, patriarch_name = PatriarchName, join_cond = JoinCond}) ->
	#guild_list_p{
		idx = Idx
		, id = Id
		, name = Name
		, icon = Icon
		, level = Level
		, num = Num
		, patriarch_pid = PatriarchPid
		, patriarch_name = PatriarchName
		, join_cond = JoinCond
	}.
to_guild_list_p([], List) -> List;
to_guild_list_p([GuildList | T], List) ->
	to_guild_list_p(T, [to_guild_list_p(GuildList) | List]).
    
%% @doc 
to_guild_member_info_p(#guild_member_info{player_id = PlayerId, name = Name, level = Level, power = Power, position = Position, contribution = Contribution, status = Status}) ->
	#guild_member_info_p{
		player_id = PlayerId
		, name = Name
		, level = Level
		, power = Power
		, position = Position
		, contribution = Contribution
		, status = Status
	}.
to_guild_member_info_p([], List) -> List;
to_guild_member_info_p([GuildMemberInfo | T], List) ->
	to_guild_member_info_p(T, [to_guild_member_info_p(GuildMemberInfo) | List]).
    
%% @doc 
to_guild_public_info_p(#guild_public_info{id = Id, name = Name, icon = Icon, level = Level, num = Num, patriarch_pid = PatriarchPid, patriarch_name = PatriarchName, notice = Notice, all_power = AllPower, member_list = MemberList}) ->
	#guild_public_info_p{
		id = Id
		, name = Name
		, icon = Icon
		, level = Level
		, num = Num
		, patriarch_pid = PatriarchPid
		, patriarch_name = PatriarchName
		, notice = Notice
		, all_power = AllPower
		, member_list = MemberList
	}.
to_guild_public_info_p([], List) -> List;
to_guild_public_info_p([GuildPublicInfo | T], List) ->
	to_guild_public_info_p(T, [to_guild_public_info_p(GuildPublicInfo) | List]).
    
%% @doc 
to_guild_info_p(#guild_info{id = Id, name = Name, icon = Icon, level = Level, num = Num, patriarch_pid = PatriarchPid, patriarch_name = PatriarchName, notice = Notice, prestige = Prestige, position = Position, is_new_lvup = IsNewLvup}) ->
	#guild_info_p{
		id = Id
		, name = Name
		, icon = Icon
		, level = Level
		, num = Num
		, patriarch_pid = PatriarchPid
		, patriarch_name = PatriarchName
		, notice = Notice
		, prestige = Prestige
		, position = Position
		, is_new_lvup = IsNewLvup
	}.
to_guild_info_p([], List) -> List;
to_guild_info_p([GuildInfo | T], List) ->
	to_guild_info_p(T, [to_guild_info_p(GuildInfo) | List]).
    
%% @doc 
to_guild_apply_join_info_p(#guild_apply_join_info{player_id = PlayerId, name = Name, level = Level, power = Power, status = Status}) ->
	#guild_apply_join_info_p{
		player_id = PlayerId
		, name = Name
		, level = Level
		, power = Power
		, status = Status
	}.
to_guild_apply_join_info_p([], List) -> List;
to_guild_apply_join_info_p([GuildApplyJoinInfo | T], List) ->
	to_guild_apply_join_info_p(T, [to_guild_apply_join_info_p(GuildApplyJoinInfo) | List]).
    
%% @doc 
to_guild_donate_log_p(#guild_donate_log{player_id = PlayerId, name = Name, position = Position, type = Type, time = Time}) ->
	#guild_donate_log_p{
		player_id = PlayerId
		, name = Name
		, position = Position
		, type = Type
		, time = Time
	}.
to_guild_donate_log_p([], List) -> List;
to_guild_donate_log_p([GuildDonateLog | T], List) ->
	to_guild_donate_log_p(T, [to_guild_donate_log_p(GuildDonateLog) | List]).
    
%% @doc 
to_guild_skill_info_p(#guild_skill_info{type = Type, skills = Skills}) ->
	#guild_skill_info_p{
		type = Type
		, skills = Skills
	}.
to_guild_skill_info_p([], List) -> List;
to_guild_skill_info_p([GuildSkillInfo | T], List) ->
	to_guild_skill_info_p(T, [to_guild_skill_info_p(GuildSkillInfo) | List]).
    
%% @doc 
to_guild_warehouse_activity_shared_p(#guild_warehouse_activity_shared{id = Id, conf_id = ConfId, item_id = ItemId, item_group = ItemGroup, activity_id = ActivityId, time = Time}) ->
	#guild_warehouse_activity_shared_p{
		id = Id
		, conf_id = ConfId
		, item_id = ItemId
		, item_group = ItemGroup
		, activity_id = ActivityId
		, time = Time
	}.
to_guild_warehouse_activity_shared_p([], List) -> List;
to_guild_warehouse_activity_shared_p([GuildWarehouseActivityShared | T], List) ->
	to_guild_warehouse_activity_shared_p(T, [to_guild_warehouse_activity_shared_p(GuildWarehouseActivityShared) | List]).
    
%% @doc 
to_guild_warehouse_log_p(#guild_warehouse_log{type = Type, item_list = ItemList, time = Time, player_id = PlayerId, player_name = PlayerName, activity_id = ActivityId}) ->
	#guild_warehouse_log_p{
		type = Type
		, item_list = ItemList
		, time = Time
		, player_id = PlayerId
		, player_name = PlayerName
		, activity_id = ActivityId
	}.
to_guild_warehouse_log_p([], List) -> List;
to_guild_warehouse_log_p([GuildWarehouseLog | T], List) ->
	to_guild_warehouse_log_p(T, [to_guild_warehouse_log_p(GuildWarehouseLog) | List]).
    
%% @doc 
to_guild_warehouse_info_p(#guild_warehouse_info{sell_rec = SellRec, buy_rec = BuyRec, member_shared = MemberShared, activity_shared = ActivityShared, log = Log, beast_sell_count = BeastSellCount, beast_buy_count = BeastBuyCount}) ->
	#guild_warehouse_info_p{
		sell_rec = SellRec
		, buy_rec = BuyRec
		, member_shared = MemberShared
		, activity_shared = ActivityShared
		, log = Log
		, beast_sell_count = BeastSellCount
		, beast_buy_count = BeastBuyCount
	}.
to_guild_warehouse_info_p([], List) -> List;
to_guild_warehouse_info_p([GuildWarehouseInfo | T], List) ->
	to_guild_warehouse_info_p(T, [to_guild_warehouse_info_p(GuildWarehouseInfo) | List]).
    
%% @doc 
to_guild_hunting_log_p(#guild_hunting_log{type = Type, svr_id = SvrId, player_name = PlayerName, to_svr_id = ToSvrId, to_player_name = ToPlayerName, integral = Integral}) ->
	#guild_hunting_log_p{
		type = Type
		, svr_id = SvrId
		, player_name = PlayerName
		, to_svr_id = ToSvrId
		, to_player_name = ToPlayerName
		, integral = Integral
	}.
to_guild_hunting_log_p([], List) -> List;
to_guild_hunting_log_p([GuildHuntingLog | T], List) ->
	to_guild_hunting_log_p(T, [to_guild_hunting_log_p(GuildHuntingLog) | List]).
    
%% @doc 
to_guild_hunting_top_p(#guild_hunting_top{idx = Idx, svr_id = SvrId, id = Id, name = Name, integral = Integral}) ->
	#guild_hunting_top_p{
		idx = Idx
		, svr_id = SvrId
		, id = Id
		, name = Name
		, integral = Integral
	}.
to_guild_hunting_top_p([], List) -> List;
to_guild_hunting_top_p([GuildHuntingTop | T], List) ->
	to_guild_hunting_top_p(T, [to_guild_hunting_top_p(GuildHuntingTop) | List]).
    
%% @doc 
to_guild_hunting_info_p(#guild_hunting_info{dungeon_id = DungeonId, personal_integral = PersonalIntegral, personal_idx = PersonalIdx, guild_idx = GuildIdx, inspire_times = InspireTimes, sur_blocking_times = SurBlockingTimes, sur_blocking_cd = SurBlockingCd, sur_challenge_times = SurChallengeTimes, sur_challenge_cd = SurChallengeCd, log = Log, top_rank = TopRank, top_rank_guild = TopRankGuild, top_rank_guild_inside = TopRankGuildInside, is_received = IsReceived, reward = Reward}) ->
	#guild_hunting_info_p{
		dungeon_id = DungeonId
		, personal_integral = PersonalIntegral
		, personal_idx = PersonalIdx
		, guild_idx = GuildIdx
		, inspire_times = InspireTimes
		, sur_blocking_times = SurBlockingTimes
		, sur_blocking_cd = SurBlockingCd
		, sur_challenge_times = SurChallengeTimes
		, sur_challenge_cd = SurChallengeCd
		, log = Log
		, top_rank = TopRank
		, top_rank_guild = TopRankGuild
		, top_rank_guild_inside = TopRankGuildInside
		, is_received = IsReceived
		, reward = Reward
	}.
to_guild_hunting_info_p([], List) -> List;
to_guild_hunting_info_p([GuildHuntingInfo | T], List) ->
	to_guild_hunting_info_p(T, [to_guild_hunting_info_p(GuildHuntingInfo) | List]).
    
%% @doc 
to_guild_hunting_blocking_list_p(#guild_hunting_blocking_list{idx = Idx, head = Head, integral = Integral}) ->
	#guild_hunting_blocking_list_p{
		idx = Idx
		, head = Head
		, integral = Integral
	}.
to_guild_hunting_blocking_list_p([], List) -> List;
to_guild_hunting_blocking_list_p([GuildHuntingBlockingList | T], List) ->
	to_guild_hunting_blocking_list_p(T, [to_guild_hunting_blocking_list_p(GuildHuntingBlockingList) | List]).
    
%% @doc 
to_guild_hunting_blocking_rec_p(#guild_hunting_blocking_rec{result = Result, head = Head, time = Time, integral = Integral, video_id = VideoId}) ->
	#guild_hunting_blocking_rec_p{
		result = Result
		, head = Head
		, time = Time
		, integral = Integral
		, video_id = VideoId
	}.
to_guild_hunting_blocking_rec_p([], List) -> List;
to_guild_hunting_blocking_rec_p([GuildHuntingBlockingRec | T], List) ->
	to_guild_hunting_blocking_rec_p(T, [to_guild_hunting_blocking_rec_p(GuildHuntingBlockingRec) | List]).
    
%% @doc 
to_guild_hunting_rank_p(#guild_hunting_rank{player_head = PlayerHead, idx = Idx, position = Position, integral = Integral}) ->
	#guild_hunting_rank_p{
		player_head = PlayerHead
		, idx = Idx
		, position = Position
		, integral = Integral
	}.
to_guild_hunting_rank_p([], List) -> List;
to_guild_hunting_rank_p([GuildHuntingRank | T], List) ->
	to_guild_hunting_rank_p(T, [to_guild_hunting_rank_p(GuildHuntingRank) | List]).
    


%% @doc 检查函数
%% @doc 检查玩家的部族数据
check_player_info(Player) ->
	ok.
    
%% @doc 检查部族列表
check_list(Player) ->
	ok.
    
%% @doc 检查部族信息（公共）
check_view(Player, Id) ->
	ok.
    
%% @doc 检查部族
check_create(Player, Name, Icon, Notice) ->
	ok.
    
%% @doc 检查加入部族
check_apply_join(Player, Id) ->
	ok.
    
%% @doc 检查玩家所在的部族信息
check_info(Player) ->
	ok.
    
%% @doc 检查部族成员列表
check_member_list(Player) ->
	ok.
    
%% @doc 检查部族申请列表
check_apply_join_list(Player) ->
	ok.
    
%% @doc 检查申请加入部族的玩家
check_approve_join(Player, ApplyPlayerId, IsAgree) ->
	ok.
    
%% @doc 检查自动审批
check_set_auto_apply(Player) ->
	ok.
    
%% @doc 检查加入条件
check_set_join_cond(Player, LevelId, PowerId) ->
	ok.
    
%% @doc 检查部族名字
check_modify_name(Player, NewName) ->
	ok.
    
%% @doc 检查部族旗帜
check_modify_icon(Player, NewIcon) ->
	ok.
    
%% @doc 检查部族公告
check_modify_notice(Player, NewNotice) ->
	ok.
    
%% @doc 检查职位
check_appoint(Player, PlayerId, Position) ->
	ok.
    
%% @doc 检查
check_kick(Player, PlayerId) ->
	ok.
    
%% @doc 检查转让
check_transfer(Player, PlayerId) ->
	ok.
    
%% @doc 检查解散
check_disband(Player) ->
	ok.
    
%% @doc 检查部族
check_quit(Player) ->
	ok.
    
%% @doc 检查信息
check_donate_info(Player) ->
	ok.
    
%% @doc 检查祭祀
check_donate(Player, Type) ->
	ok.
    
%% @doc 检查领取祭祀进度奖励
check_donate_receive(Player, Id) ->
	ok.
    
%% @doc 检查部族技能信息
check_skill_info(Player) ->
	ok.
    
%% @doc 检查技能升级
check_skill_lv_up(Player, Type) ->
	ok.
    
%% @doc 检查部族仓库信息
check_warehouse_info(Player) ->
	ok.
    
%% @doc 检查仓库存物品
check_warehouse_sell(Player, Type, ItemId, ItemGroup) ->
	ok.
    
%% @doc 检查仓库兑换物品
check_warehouse_buy(Player, Type, Id, ItemGroup) ->
	ok.
    
%% @doc 检查仓库清理物品
check_warehouse_clear(Player, ItemId, ItemGroup) ->
	ok.
    
%% @doc 检查部族狩猎的信息
check_hunting_info(Player) ->
	ok.
    
%% @doc 检查部族狩猎鼓舞
check_hunting_inspire(Player) ->
	ok.
    
%% @doc 检查部族狩猎挑战
check_hunting_challenge(Player, InBattle, Formation) ->
	ok.
    
%% @doc 检查部族狩猎阻击列表
check_hunting_blocking_list(Player) ->
	ok.
    
%% @doc 检查部族狩猎阻击
check_hunting_blocking(Player, ToPlayerId, InBattle, Formation) ->
	ok.
    
%% @doc 检查部族狩猎阻击记录
check_hunting_blocking_rec(Player) ->
	ok.
    
%% @doc 检查部族狩猎阻击阵容
check_hunting_blocking_lineup(Player, ToPlayerId) ->
	ok.
    
%% @doc 检查部族狩猎日志
check_hunting_log(Player) ->
	ok.
    
%% @doc 检查部族狩猎族内排行信息
check_hunting_rank_inside(Player) ->
	ok.
    
%% @doc 检查狩猎领取奖励
check_hunting_receive(Player) ->
	ok.
    
%% @doc 检查狩猎新的被阻击日志（只显示新被阻击的日志）
check_hunting_blocking_rec_new(Player) ->
	ok.
    


%% @doc 修改函数
%% @doc 玩家的部族数据
do_player_info(Player) ->
	{ok, #guild_player_info_reply{}}.
    
%% @doc 部族列表
do_list(Player) ->
	{ok, #guild_list_reply{}}.
    
%% @doc 部族信息（公共）
do_view(Player, Id) ->
	{ok, #guild_view_reply{}}.
    
%% @doc 部族
do_create(Player, Name, Icon, Notice) ->
	{ok, #guild_create_reply{}}.
    
%% @doc 加入部族
do_apply_join(Player, Id) ->
	{ok, #guild_apply_join_reply{}}.
    
%% @doc 玩家所在的部族信息
do_info(Player) ->
	{ok, #guild_info_reply{}}.
    
%% @doc 部族成员列表
do_member_list(Player) ->
	{ok, #guild_member_list_reply{}}.
    
%% @doc 部族申请列表
do_apply_join_list(Player) ->
	{ok, #guild_apply_join_list_reply{}}.
    
%% @doc 申请加入部族的玩家
do_approve_join(Player, ApplyPlayerId, IsAgree) ->
	{ok, #guild_approve_join_reply{}}.
    
%% @doc 自动审批
do_set_auto_apply(Player) ->
	{ok, #guild_set_auto_apply_reply{}}.
    
%% @doc 加入条件
do_set_join_cond(Player, LevelId, PowerId) ->
	{ok, #guild_set_join_cond_reply{}}.
    
%% @doc 部族名字
do_modify_name(Player, NewName) ->
	{ok, #guild_modify_name_reply{}}.
    
%% @doc 部族旗帜
do_modify_icon(Player, NewIcon) ->
	{ok, #guild_modify_icon_reply{}}.
    
%% @doc 部族公告
do_modify_notice(Player, NewNotice) ->
	{ok, #guild_modify_notice_reply{}}.
    
%% @doc 职位
do_appoint(Player, PlayerId, Position) ->
	{ok, #guild_appoint_reply{}}.
    
%% @doc 
do_kick(Player, PlayerId) ->
	{ok, #guild_kick_reply{}}.
    
%% @doc 转让
do_transfer(Player, PlayerId) ->
	{ok, #guild_transfer_reply{}}.
    
%% @doc 解散
do_disband(Player) ->
	{ok, #guild_disband_reply{}}.
    
%% @doc 部族
do_quit(Player) ->
	{ok, #guild_quit_reply{}}.
    
%% @doc 信息
do_donate_info(Player) ->
	{ok, #guild_donate_info_reply{}}.
    
%% @doc 祭祀
do_donate(Player, Type) ->
	{ok, #guild_donate_reply{}}.
    
%% @doc 领取祭祀进度奖励
do_donate_receive(Player, Id) ->
	{ok, #guild_donate_receive_reply{}}.
    
%% @doc 部族技能信息
do_skill_info(Player) ->
	{ok, #guild_skill_info_reply{}}.
    
%% @doc 技能升级
do_skill_lv_up(Player, Type) ->
	{ok, #guild_skill_lv_up_reply{}}.
    
%% @doc 部族仓库信息
do_warehouse_info(Player) ->
	{ok, #guild_warehouse_info_reply{}}.
    
%% @doc 仓库存物品
do_warehouse_sell(Player, Type, ItemId, ItemGroup) ->
	{ok, #guild_warehouse_sell_reply{}}.
    
%% @doc 仓库兑换物品
do_warehouse_buy(Player, Type, Id, ItemGroup) ->
	{ok, #guild_warehouse_buy_reply{}}.
    
%% @doc 仓库清理物品
do_warehouse_clear(Player, ItemId, ItemGroup) ->
	{ok, #guild_warehouse_clear_reply{}}.
    
%% @doc 部族狩猎的信息
do_hunting_info(Player) ->
	{ok, #guild_hunting_info_reply{}}.
    
%% @doc 部族狩猎鼓舞
do_hunting_inspire(Player) ->
	{ok, #guild_hunting_inspire_reply{}}.
    
%% @doc 部族狩猎挑战
do_hunting_challenge(Player, InBattle, Formation) ->
	{ok, #guild_hunting_challenge_reply{}}.
    
%% @doc 部族狩猎阻击列表
do_hunting_blocking_list(Player) ->
	{ok, #guild_hunting_blocking_list_reply{}}.
    
%% @doc 部族狩猎阻击
do_hunting_blocking(Player, ToPlayerId, InBattle, Formation) ->
	{ok, #guild_hunting_blocking_reply{}}.
    
%% @doc 部族狩猎阻击记录
do_hunting_blocking_rec(Player) ->
	{ok, #guild_hunting_blocking_rec_reply{}}.
    
%% @doc 部族狩猎阻击阵容
do_hunting_blocking_lineup(Player, ToPlayerId) ->
	{ok, #guild_hunting_blocking_lineup_reply{}}.
    
%% @doc 部族狩猎日志
do_hunting_log(Player) ->
	{ok, #guild_hunting_log_reply{}}.
    
%% @doc 部族狩猎族内排行信息
do_hunting_rank_inside(Player) ->
	{ok, #guild_hunting_rank_inside_reply{}}.
    
%% @doc 狩猎领取奖励
do_hunting_receive(Player) ->
	{ok, #guild_hunting_receive_reply{}}.
    
%% @doc 狩猎新的被阻击日志（只显示新被阻击的日志）
do_hunting_blocking_rec_new(Player) ->
	{ok, #guild_hunting_blocking_rec_new_reply{}}.
    