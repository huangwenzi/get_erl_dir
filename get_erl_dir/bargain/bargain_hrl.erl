
%%%%%%-------------------------------------------------------------------
%%%%%% @author hw
%%%%%% @copyright (C) 2021, <COMPANY>
%%%%%% @doc
%%%%%%
%%%%%% @end
%%%%%% Created : 17. 6月 2021 14:30
%%%%%%-------------------------------------------------------------------


-ifndef(BARGAIN_H_H_).
-define(BARGAIN_H_H_, 1).

    
%% 
-record(bargain_gift, {
	id = 0,						%% 礼包id
	help_list = [],				%% 已砍价玩家, [[玩家id, 砍价金额]]
	buy_count = 0				%% 已购买次数
}).

%% 
-record(bargain_gift_a, {
	id = 0,						%% 礼包id
	help_list = [],				%% 已砍价玩家, [[玩家id, 砍价金额]]
	buy_count = 0				%% 已购买次数
}).


%% 
-record(player_bargain, {
	player_id = 0, 
	help_conut = 0,				%% 已帮助砍价次数
	help_list = [],				%% 已帮助好友 [[玩家id, 礼包id]]
	gift_list = []				%% 礼包列表
}).

-endif.

















