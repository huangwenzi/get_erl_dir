
%%%-------------------------------------------------------------------
%%% @author hw
%%% @copyright (C) 2021, <COMPANY>
%%% @doc
%%%
%%% @end
%%% Created : 8. 3月 2021 20:21
%%%-------------------------------------------------------------------

-module(bargain_rpc).
-author("hw").

-include("erl_protocol_record.hrl").

%% API
-export([handle/2]).
    
%% 请求砍价礼包信息
handle(#bargain_info_request{}, Player) ->
    case bargain_lib:info(Player) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #bargain_info_reply{code = Code}}
    end;

%% 请求帮助砍价
handle(#bargain_help_request{friend_id = FriendId, gift_id = GiftId}, Player) ->
    case bargain_lib:help(Player, FriendId, GiftId) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #bargain_help_reply{code = Code}}
    end.