
%%%%%%-------------------------------------------------------------------
%%%%%% @author hw
%%%%%% @copyright (C) 2021, <COMPANY>
%%%%%% @doc
%%%%%%
%%%%%% @end
%%%%%% Created : 17. 6月 2021 14:30
%%%%%%-------------------------------------------------------------------

-module(bargain_rpc).
-author("hw").

-include("erl_protocol_record.hrl").
-include("logger.hrl").

%% API
-export([handle/2]).
    
%%%% 请求砍价礼包信息
handle(#bargain_info_request{}, Player) ->
    case bargain_lib:info() of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #bargain_info_reply{code = Code}}
    end;

%%%% 请求帮助砍价
handle(#bargain_help_request{friend_id = FriendId, gift_id = GiftId}, Player) ->
    case bargain_lib:help(FriendId, GiftId) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #bargain_help_reply{code = Code}}
    end;
 
%%%% 请求帮助砍价
handle(#bargain_help_a_request{friend_id = FriendId, gift_id = GiftId}, Player) ->
    case bargain_lib:help_a(FriendId, GiftId) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #bargain_help_a_reply{code = Code}}
    end;

%%%% 请求帮助砍价
handle(#bargain_help_b_request{friend_id = FriendId, gift_id = GiftId}, Player) ->
    case bargain_lib:help_b(FriendId, GiftId) of
        {ok, Notify} ->
            {reply, Notify};
        {false, Code} ->
            {reply, #bargain_help_b_reply{code = Code}}
    end;

handle(Msg, _Player) ->
    ?ERROR("module:[~p] handle msg error:[~p]", [?MODULE, Msg]),
    ok.
    