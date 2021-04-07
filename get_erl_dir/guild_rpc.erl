
%%%-------------------------------------------------------------------
%%% @author hw
%%% @copyright (C) 2021, <COMPANY>
%%% @doc
%%%
%%% @end
%%% Created : 7. 4月 2021 10:51
%%%-------------------------------------------------------------------

-module(guild_rpc).
-author("hw").

-include("erl_protocol_record.hrl").

% API
-export([handle/2]).
    
%% 请求玩家的部族数据
handle(#guild_player_info_request{}, Player) ->
    case guild_lib:player_info(Player) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_player_info_reply{code = Code}}
    end;

%% 请求部族列表
handle(#guild_list_request{}, Player) ->
    case guild_lib:list(Player) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_list_reply{code = Code}}
    end;

%% 查看部族信息（公共）
handle(#guild_view_request{id = Id}, Player) ->
    case guild_lib:view(Player, Id) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_view_reply{code = Code}}
    end;

%% 创建部族
handle(#guild_create_request{name = Name, icon = Icon, notice = Notice}, Player) ->
    case guild_lib:create(Player, Name, Icon, Notice) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_create_reply{code = Code}}
    end;

%% 申请加入部族
handle(#guild_apply_join_request{id = Id}, Player) ->
    case guild_lib:apply_join(Player, Id) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_apply_join_reply{code = Code}}
    end;

%% 请求玩家所在的部族信息
handle(#guild_info_request{}, Player) ->
    case guild_lib:info(Player) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_info_reply{code = Code}}
    end;

%% 请求部族成员列表
handle(#guild_member_list_request{}, Player) ->
    case guild_lib:member_list(Player) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_member_list_reply{code = Code}}
    end;

%% 请求部族申请列表
handle(#guild_apply_join_list_request{}, Player) ->
    case guild_lib:apply_join_list(Player) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_apply_join_list_reply{code = Code}}
    end;

%% 审批申请加入部族的玩家
handle(#guild_approve_join_request{apply_player_id = ApplyPlayerId, is_agree = IsAgree}, Player) ->
    case guild_lib:approve_join(Player, ApplyPlayerId, IsAgree) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_approve_join_reply{code = Code}}
    end;

%% 设置自动审批
handle(#guild_set_auto_apply_request{}, Player) ->
    case guild_lib:set_auto_apply(Player) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_set_auto_apply_reply{code = Code}}
    end;

%% 设置加入条件
handle(#guild_set_join_cond_request{level_id = LevelId, power_id = PowerId}, Player) ->
    case guild_lib:set_join_cond(Player, LevelId, PowerId) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_set_join_cond_reply{code = Code}}
    end;

%% 修改部族名字
handle(#guild_modify_name_request{new_name = NewName}, Player) ->
    case guild_lib:modify_name(Player, NewName) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_modify_name_reply{code = Code}}
    end;

%% 修改部族旗帜
handle(#guild_modify_icon_request{new_icon = NewIcon}, Player) ->
    case guild_lib:modify_icon(Player, NewIcon) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_modify_icon_reply{code = Code}}
    end;

%% 修改部族公告
handle(#guild_modify_notice_request{new_notice = NewNotice}, Player) ->
    case guild_lib:modify_notice(Player, NewNotice) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_modify_notice_reply{code = Code}}
    end;

%% 任命职位
handle(#guild_appoint_request{player_id = PlayerId, position = Position}, Player) ->
    case guild_lib:appoint(Player, PlayerId, Position) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_appoint_reply{code = Code}}
    end;

%% 踢人
handle(#guild_kick_request{player_id = PlayerId}, Player) ->
    case guild_lib:kick(Player, PlayerId) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_kick_reply{code = Code}}
    end;

%% 族长转让
handle(#guild_transfer_request{player_id = PlayerId}, Player) ->
    case guild_lib:transfer(Player, PlayerId) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_transfer_reply{code = Code}}
    end;

%% 部族解散
handle(#guild_disband_request{}, Player) ->
    case guild_lib:disband(Player) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_disband_reply{code = Code}}
    end;

%% 退出部族
handle(#guild_quit_request{}, Player) ->
    case guild_lib:quit(Player) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_quit_reply{code = Code}}
    end;

%% 祭祀信息
handle(#guild_donate_info_request{}, Player) ->
    case guild_lib:donate_info(Player) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_donate_info_reply{code = Code}}
    end;

%% 进行祭祀
handle(#guild_donate_request{type = Type}, Player) ->
    case guild_lib:donate(Player, Type) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_donate_reply{code = Code}}
    end;

%% 请求领取祭祀进度奖励
handle(#guild_donate_receive_request{id = Id}, Player) ->
    case guild_lib:donate_receive(Player, Id) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_donate_receive_reply{code = Code}}
    end;

%% 请求部族技能信息
handle(#guild_skill_info_request{}, Player) ->
    case guild_lib:skill_info(Player) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_skill_info_reply{code = Code}}
    end;

%% 部族技能升级
handle(#guild_skill_lv_up_request{type = Type}, Player) ->
    case guild_lib:skill_lv_up(Player, Type) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_skill_lv_up_reply{code = Code}}
    end;

%% 请求部族仓库信息
handle(#guild_warehouse_info_request{}, Player) ->
    case guild_lib:warehouse_info(Player) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_warehouse_info_reply{code = Code}}
    end;

%% 部族仓库存物品
handle(#guild_warehouse_sell_request{type = Type, item_id = ItemId, item_group = ItemGroup}, Player) ->
    case guild_lib:warehouse_sell(Player, Type, ItemId, ItemGroup) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_warehouse_sell_reply{code = Code}}
    end;

%% 部族仓库兑换物品
handle(#guild_warehouse_buy_request{type = Type, id = Id, item_group = ItemGroup}, Player) ->
    case guild_lib:warehouse_buy(Player, Type, Id, ItemGroup) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_warehouse_buy_reply{code = Code}}
    end;

%% 部族仓库清理物品
handle(#guild_warehouse_clear_request{item_id = ItemId, item_group = ItemGroup}, Player) ->
    case guild_lib:warehouse_clear(Player, ItemId, ItemGroup) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_warehouse_clear_reply{code = Code}}
    end;

%% 请求部族狩猎的信息
handle(#guild_hunting_info_request{}, Player) ->
    case guild_lib:hunting_info(Player) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_hunting_info_reply{code = Code}}
    end;

%% 请求部族狩猎鼓舞
handle(#guild_hunting_inspire_request{}, Player) ->
    case guild_lib:hunting_inspire(Player) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_hunting_inspire_reply{code = Code}}
    end;

%% 请求部族狩猎挑战
handle(#guild_hunting_challenge_request{in_battle = InBattle, formation = Formation}, Player) ->
    case guild_lib:hunting_challenge(Player, InBattle, Formation) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_hunting_challenge_reply{code = Code}}
    end;

%% 请求部族狩猎阻击列表
handle(#guild_hunting_blocking_list_request{}, Player) ->
    case guild_lib:hunting_blocking_list(Player) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_hunting_blocking_list_reply{code = Code}}
    end;

%% 请求部族狩猎阻击
handle(#guild_hunting_blocking_request{to_player_id = ToPlayerId, in_battle = InBattle, formation = Formation}, Player) ->
    case guild_lib:hunting_blocking(Player, ToPlayerId, InBattle, Formation) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_hunting_blocking_reply{code = Code}}
    end;

%% 请求部族狩猎阻击记录
handle(#guild_hunting_blocking_rec_request{}, Player) ->
    case guild_lib:hunting_blocking_rec(Player) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_hunting_blocking_rec_reply{code = Code}}
    end;

%% 请求部族狩猎阻击阵容
handle(#guild_hunting_blocking_lineup_request{to_player_id = ToPlayerId}, Player) ->
    case guild_lib:hunting_blocking_lineup(Player, ToPlayerId) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_hunting_blocking_lineup_reply{code = Code}}
    end;

%% 请求部族狩猎日志
handle(#guild_hunting_log_request{}, Player) ->
    case guild_lib:hunting_log(Player) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_hunting_log_reply{code = Code}}
    end;

%% 请求部族狩猎族内排行信息
handle(#guild_hunting_rank_inside_request{}, Player) ->
    case guild_lib:hunting_rank_inside(Player) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_hunting_rank_inside_reply{code = Code}}
    end;

%% 部族狩猎领取奖励
handle(#guild_hunting_receive_request{}, Player) ->
    case guild_lib:hunting_receive(Player) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_hunting_receive_reply{code = Code}}
    end;

%% 部族狩猎新的被阻击日志（只显示新被阻击的日志）
handle(#guild_hunting_blocking_rec_new_request{}, Player) ->
    case guild_lib:hunting_blocking_rec_new(Player) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #guild_hunting_blocking_rec_new_reply{code = Code}}
    end.