
%%%-------------------------------------------------------------------
%%% @author hw
%%% @copyright (C) 2021, <COMPANY>
%%% @doc
%%%
%%% @end
%%% Created : 7. 4月 2021 10:51
%%%-------------------------------------------------------------------


-ifndef(GUILD_H_H_).
-define(GUILD_H_H_, 1).

    
%% 
-record(guild_join_condition, {
	level_id = 0,				%% 所需等级id, 配置表配的id
	power_id = 0				%% 所需战力id
}).

%% 
-record(guild_list, {
	idx = 0,						%% 排名
	id = 0,						%% 部族id
	name = [],					%% 部族名字
	icon = 0,					%% 旗帜id
	level = 0,					%% 部族等级
	num = 0,						%% 部族人数
	patriarch_pid = 0,			%% 族长的玩家id
	patriarch_name = [],			%% 族长名字
	join_cond = []				%% 加入部族的条件
}).

%% 
-record(guild_member_info, {
	player_id = 0,				%% 玩家id
	name = [],					%% 玩家名字
	level = 0,					%% 玩家等级
	power = 0,					%% 玩家战力
	position = 0,				%% 职位
	contribution = 0,			%% 历史贡献值
	status = 0					%% 玩家在线状态  在线是0，离线则是上一次离线的时间戳
}).

%% 
-record(guild_public_info, {
	id = 0,						%% 部族id
	name = [],					%% 部族名字
	icon = 0,					%% 旗帜id
	level = 0,					%% 部族等级
	num = 0,						%% 部族人数
	patriarch_pid = 0,			%% 族长的玩家id
	patriarch_name = [],			%% 族长的名字
	notice = [],					%% 部族公告
	all_power = 0,				%% 总战力
	member_list = []			%% 成员列表
}).

%% 
-record(guild_info, {
	id = 0,						%% 部族id
	name = [],					%% 部族名字
	icon = 0,					%% 旗帜id
	level = 0,					%% 部族等级
	num = 0,						%% 部族人数
	patriarch_pid = 0,			%% 族长的玩家id
	patriarch_name = [],			%% 族长的名字
	notice = [],					%% 部族公告
	prestige = 0,				%% 部族声望
	position = 0,				%% 职位
	is_new_lvup = 0				%% 是否有新的升级 0否 1是
}).

%% 
-record(guild_apply_join_info, {
	player_id = 0,				%% 玩家id
	name = [],					%% 玩家名字
	level = 0,					%% 玩家等级
	power = 0,					%% 玩家战力
	status = 0					%% 玩家在线状态  在线是0，离线则是上一次离线的时间戳
}).

%% 
-record(guild_donate_log, {
	player_id = 0,				%% 玩家id
	name = [],					%% 玩家名字
	position = 0,				%% 职位
	type = 0,					%% 祭祀类型
	time = 0					%% 祭祀时间
}).

%% 
-record(guild_skill_info, {
	type = 0,					%% 技能类型
	skills = []					%% 技能等级
}).

%% 
-record(guild_warehouse_activity_shared, {
	id = 0,						%% 唯一id
	conf_id = 0,					%% 配置表id
	item_id = 0,					%% 道具id
	item_group = 0,				%% 道具组数
	activity_id = 0,				%% 活动id
	time = 0					%% 发放时间
}).

%% 
-record(guild_warehouse_log, {
	type = 0,					%% 操作类型 1玩家存 2活动奖励存 3玩家取 4过期 5清理
	item_list = [],				%% 道具id和数量
	time = 0,					%% 操作时间
	player_id = 0,				%% 操作的玩家id
	player_name = [],			%% 操作的玩家名字
	activity_id = 0				%% 活动id
}).

%% 
-record(guild_warehouse_info, {
	sell_rec = [],				%% 今日存入次数
	buy_rec = [],				%% 今日兑换次数
	member_shared = [],			%% 成员共享的道具列表
	activity_shared = [],		%% 活动奖励的道具列表
	log = [],					%% 仓库日志
	beast_sell_count = 0,		%% 今日异兽的存入次数
	beast_buy_count = 0			%% 今日异兽的兑换次数
}).

%% 
-record(guild_hunting_log, {
	type = 0,					%% 战报类型 1挑战 2阻击
	svr_id = 0,					%% 操作的玩家所在服务器id
	player_name = [],			%% 操作的玩家名字
	to_svr_id = 0,				%% 被阻击的玩家所在服务器id
	to_player_name = [],			%% 被阻击的玩家名字
	integral = 0				%% 获得的积分
}).

%% 
-record(guild_hunting_top, {
	idx = 0,						%% 排名
	svr_id = 0,					%% 所在服务器id
	id = 0,						%% id
	name = [],					%% 名字
	integral = 0				%% 积分
}).

%% 
-record(guild_hunting_info, {
	dungeon_id = 0,				%% 副本id
	personal_integral = 0,		%% 个人积分
	personal_idx = 0,			%% 个人排名
	guild_idx = 0,				%% 部族排名
	inspire_times = 0,			%% 已鼓舞的次数
	sur_blocking_times = 0,		%% 阻击剩余次数
	sur_blocking_cd = 0,			%% 阻击剩余冷却时间
	sur_challenge_times = 0,		%% 挑战剩余次数
	sur_challenge_cd = 0,		%% 挑战剩余冷却时间
	log = [],					%% 战况广播
	top_rank = [],				%% 个人排行榜前N名信息
	top_rank_guild = [],			%% 部族排行榜前N名信息
	top_rank_guild_inside = [],	%% 族内排行榜前N名信息
	is_received = 0,				%% 奖励是否领取了 0：未领取 1：已领取
	reward = []					%% 可领取的奖励
}).

%% 
-record(guild_hunting_blocking_list, {
	idx = 0,						%% 排名
	head = [],					%% 玩家的头像信息
	integral = 0				%% 玩家的积分
}).

%% 
-record(guild_hunting_blocking_rec, {
	result = 0,					%% 结果 1阻击成功 2阻击失败 3防守成功 4防守失败
	head = [],					%% 阻击或被阻击的玩家头像
	time = 0,					%% 时间
	integral = 0,				%% 损失或获得的积分
	video_id = 0				%% 录像id
}).

%% 
-record(guild_hunting_rank, {
	player_head = [],			%% 头像信息
	idx = 0,						%% 名次
	position = 0,				%% 职位
	integral = 0				%% 玩家的积分
}).

%% 
-record(player_guild, {
	player_id = 0, 
	guild_info = []				%% 部族信息
}).

-endif.

















