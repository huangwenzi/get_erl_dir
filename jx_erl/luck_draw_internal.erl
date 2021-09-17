%% @date 2020-08-05
%% @doc 奖池抽奖

-module(luck_draw_internal).

%% ====================================================================
%% includes
%% ====================================================================
-include("common.hrl").
-include("counter.hrl").
-include("role.hrl").
-include("sys_staff_lv.hrl").
-include("sys_staff_lv_consume.hrl").
-include("sys_staff_quality_type.hrl").
-include("sys_staff_quality.hrl").
-include("sys_staff.hrl").
-include("sys_staff_star.hrl").
-include("proto_luck_draw_pb.hrl").
-include("staff.hrl").
-include("fight.hrl").
-include("sys_recruit_type.hrl").
-include("sys_recruit_pool.hrl").
-include("role_daily.hrl").


%% ====================================================================
%% API functions
%% ====================================================================
%% 协议接口
-export([
    recruit_info/1
    , recruit_one/2
    , recruit_ten/2
    , contacts/2
    , change_state/2
]).

%% 外部接口
-export([
    get_all_pool_info/0
]).

%% 获取函数

%% 修改函数

%% 结构转换

%% gm
-export([
    gm_reset/1
]).


%% ====================================================================
%% External functions
%% ====================================================================


%%========================================协议函数
%% 奖池信息
recruit_info(RoleId) ->
    #recruit{contacts = Contacts} = get_recruit_info(RoleId),
    AllPoolInfo = get_all_pool_info(),
    #luck_draw_recruit_info_s2c{
        contacts = util:to_p_key_value(Contacts, [])
        , info_list = to_p_recruit_pool(AllPoolInfo, [])
    }.

%% 招聘单次
recruit_one(RoleId, Type) ->
    case check_recruit_one(RoleId, Type) of
        {false, []} -> {false, ?E_ITEM_NOT_ENOUGH};
        {HasFree, ConsumeItem} ->
            %% 扣除消耗
            CostRet = case HasFree of
                          true ->
                              %% 添加今日抽奖次数
                              add_pool_daily_count(RoleId, Type),
                              true;
                          false ->
                              case item_bag:try_cost_item(RoleId, ConsumeItem, ?LOG_COST_TYPE_STAFF_RECRUIT) of
                                  true -> true;
                                  Err -> Err
                              end
                      end,
            case CostRet of
                {error, Code} -> {false, Code};
                true ->
                    #sys_recruit_type{
                        contact = Contact
                        , reward_num = RewardNum
                    } = sys_recruit_type:get(Type),
                    %% 抽取奖励
                    PoolList = sys_recruit_pool:get_recruit_pool(Type),
                    List = util:select_pick_by_prob(PoolList, RewardNum, false),
                    {StaffList, ItemList} = pool_list_to_reward(List, {[],[]}),
                    %% 先添加人才
                    {NewStaffList, NewItemList} = staff_internal:add_list_staff(RoleId, StaffList),
                    item_bag:add_bag_by_cid(RoleId, ItemList, ?LOG_GAIN_TYPE_STAFF_RECRUIT),
                    %% 添加人脉值
                    Contacts = add_contact(RoleId, Type, Contact),
                    #luck_draw_recruit_one_s2c{
                        contacts = util:to_p_key_value(Contacts, [])
                        , staff_list = [StaffId || #staff{staff_id = StaffId} <- NewStaffList]
                        , reward_item = util:to_p_key_value(NewItemList ++ ItemList, [])
                    }
            end
    end.
%% 检查招聘单次
check_recruit_one(RoleId, Type) ->
    #sys_recruit_type{
        free_type = FreeType
        , cooling = Cooling
        , free_param = FreeParam
        , consume = Consume
        , diamond = Diamond
    } = sys_recruit_type:get(Type),
    #recruit_pool{
        luck_draw_time = LuckDrawTime
    } = get_pool_info(RoleId, Type),
    %% 是否有免费次数
    %% 检查冷却时间
    Now = util:now_sec(),
    HasFree = case LuckDrawTime + Cooling < Now of
                  false -> false;
                  true ->
                      %% 检查次数
                      case FreeType of
                          ?RECRUIT_FREE_TYPE_DAY ->
                              %% 检查今日次数
                              DailyCount = get_pool_daily_count(Type),
                              %% ps 暂时设为1
                              _CfgDailyCount = get_cfg_pool_daily_count(FreeParam, RoleId, 0),
                              CfgDailyCount1 = 1,
                              DailyCount < CfgDailyCount1;
                          ?RECRUIT_FREE_TYPE_COUNT -> true
                      end
              end,
    %% 道具消耗
    ConsumeItem = case HasFree of
                      true -> [];
                      false ->
                          %% 道具是否满足
                          case item_bag:is_cost_enough(RoleId, Consume) of
                              true -> Consume;
                              _ ->
                                  %% 钻石是否满足
                                  case item_bag:is_cost_enough(RoleId, Diamond) of
                                      true -> Diamond;
                                      _ -> []
                                  end
                          end
                  end,
    {HasFree, ConsumeItem}.

%% 招聘十连
recruit_ten(RoleId, Type) ->
    case check_recruit_ten(RoleId, Type) of
        false -> {false, ?E_ITEM_NOT_ENOUGH};
        ConsumeItem ->
            %% 扣除消耗
            CostRet = case item_bag:try_cost_item(RoleId, ConsumeItem, ?LOG_COST_TYPE_STAFF_RECRUIT) of
                          true -> true;
                          Err -> Err
                      end,
            case CostRet of
                {error, Code} -> {false, Code};
                true ->
                    #sys_recruit_type{
                        contact = Contact
                        , reward_num = RewardNum
                    } = sys_recruit_type:get(Type),
                    %% 抽取奖励
                    PoolList = sys_recruit_pool:get_recruit_pool(Type),
                    List = util:select_pick_by_prob(PoolList, RewardNum*?RECRUIT_TEN, false),
                    {StaffList, ItemList} = pool_list_to_reward(List, {[],[]}),
                    %% 先添加人才
                    {NewStaffList, NewItemList} = staff_internal:add_list_staff(RoleId, StaffList),
                    item_bag:add_bag_by_cid(RoleId, ItemList, ?LOG_GAIN_TYPE_STAFF_RECRUIT),
                    %% 添加人脉值
                    Contacts = add_contact(RoleId, Type, Contact*?RECRUIT_TEN),
                    #luck_draw_recruit_ten_s2c{
                        contacts = util:to_p_key_value(Contacts, [])
                        , staff_list = [StaffId || #staff{staff_id = StaffId} <- NewStaffList]
                        , reward_item = util:to_p_key_value(NewItemList ++ ItemList, [])
                    }
            end
    end.
%% 检查招聘十连
check_recruit_ten(RoleId, Type) ->
    #sys_recruit_type{
        consume = Consume
        , diamond = Diamond
    } = sys_recruit_type:get(Type),
    %% 道具消耗
    %% 道具是否满足
    ConsumeCount = item_bag:can_cost_count(Consume, RoleId),
    case ConsumeCount >= ?RECRUIT_TEN of
        true -> item_util:item_num_rate(Consume, ?RECRUIT_TEN, []);
        _ ->
            %% 钻石是否满足
            DiamondCount = ?RECRUIT_TEN - ConsumeCount,
            Diamond1 = item_util:item_num_rate(Diamond, DiamondCount, []),
            case item_bag:is_cost_enough(RoleId, Diamond1) of
                true -> Diamond1 ++ item_util:item_num_rate(Consume, ?RECRUIT_TEN, []);
                _ -> false
            end
    end.

%% 人脉兑换
contacts(RoleId, Type) ->
    case check_contacts(RoleId, Type) of
        {false, _} -> {false, ?E_ITEM_NOT_ENOUGH};
        {true, #sys_recruit_type{
            contact_consume = ContactConsume
            , contacts_pool = ContactsPool
            , reward_num = RewardNum
        }} ->
            %% 扣除人脉值
            Contacts = add_contact(RoleId, Type, -ContactConsume),
            %% 人脉抽奖
            PoolList = sys_recruit_pool:get_recruit_pool(ContactsPool),
            List = util:select_pick_by_prob(PoolList, RewardNum, false),
            {StaffList, ItemList} = pool_list_to_reward(List, {[],[]}),
            %% 先添加人才
            {NewStaffList, NewItemList} = staff_internal:add_list_staff(RoleId, StaffList),
            item_bag:add_bag_by_cid(RoleId, ItemList, ?LOG_GAIN_TYPE_STAFF_RECRUIT),
            #luck_draw_contacts_s2c{
                contacts = util:to_p_key_value(Contacts, [])
                , staff_list = [StaffId || #staff{staff_id = StaffId} <- NewStaffList]
                , reward_item = util:to_p_key_value(NewItemList ++ ItemList, [])
            }
    end.
%% 检查人脉兑换
check_contacts(RoleId, Type) ->
    %% 人脉消耗是否满足要求
    RecruitTypeCfg = #sys_recruit_type{
        contact_consume = ContactConsume
    } = sys_recruit_type:get(Type),
    #recruit{
       contacts = Contacts
    }=  get_recruit_info(RoleId),
    ContactVal = get_contact(Contacts, Type),
    {ContactConsume >= ContactVal, RecruitTypeCfg}.

%% 修改动画状态
change_state(RoleId, Type) ->
    PoolInfo = get_pool_info(RoleId, Type),
    set_pool_info(PoolInfo#recruit_pool{act_state = 1}),
    #luck_draw_change_state_s2c{type = Type}.


%%========================================辅助函数
%% 获取全部奖池信息
get_all_pool_info() ->
    cache:list(?TABLE_RECRUIT_POOL).

%% 获取奖池信息
get_pool_info(RoleId, Type) ->
    case cache:key_find(?TABLE_RECRUIT_POOL, Type, #recruit_pool.type) of
        false ->
            {ok, Id} = serv_id:new(?TABLE_RECRUIT_POOL),
            % 新数据
            RecruitPool = #recruit_pool{
                id = Id
                , role_id = RoleId
                , type = Type
                , luck_draw_time = 0
                , act_state = 0
            },
            cache:add(RecruitPool),
            RecruitPool;
        RecruitPool -> RecruitPool
    end.

%% 保存抽奖信息
set_pool_info(RecruitPool) ->
    cache:update(RecruitPool).

%% 获取抽奖信息
get_recruit_info(RoleId) ->
    case cache:get(?TABLE_RECRUIT, RoleId) of
        false ->
            % 新数据
            RecruitInfo = #recruit{
                id = RoleId
                , contacts = []
            },
            cache:add(RecruitInfo),
            RecruitInfo;
        RecruitInfo -> RecruitInfo
    end.

%% 保存抽奖信息
set_recruit_info(RecruitInfo) ->
    cache:update(RecruitInfo).

%% 获取奖池今天免费抽奖次数
get_pool_daily_count(Type) ->
    List = role_daily:get(?ROLE_DAILY_TYPE_RECRUIT, []),
    case lists:keyfind(Type, 1, List) of
        false -> 0;
        {_, Count} -> Count
    end.
%% 添加奖池今天免费抽奖次数
add_pool_daily_count(RoleId, Type) ->
    List = role_daily:get(?ROLE_DAILY_TYPE_RECRUIT, []),
    List1 = case lists:keyfind(Type, 1, List) of
        false -> [{Type, 1} | List];
        {_, Count} -> lists:keystore(Type, 1, List, {Type, Count + 1})
    end,
    %% 免费抽奖修改抽奖时间
    PoolInfo = get_pool_info(RoleId, Type),
    set_pool_info(PoolInfo#recruit_pool{luck_draw_time = util:now_sec()}),
    role_daily:set(?ROLE_DAILY_TYPE_RECRUIT, List1).

%% 获取对应次数
get_cfg_pool_daily_count([], _RoleId, Count) -> Count;
get_cfg_pool_daily_count([{DepartmentId, DepartmentLv, CfgCount} | T], RoleId, Count) ->
    DepartmentLv1 = enterprise_internal:get_department_lv(RoleId, DepartmentId),
    Count1 = ?IF(DepartmentLv1 >= DepartmentLv, erlang:max(CfgCount, Count), Count),
    get_cfg_pool_daily_count(T, RoleId, Count1).

%% 添加人脉值
add_contact(RoleId, Type, Contact) ->
    RecruitType = Type div ?RECRUIT_TYPE_BASE,
    RecruitInfo = #recruit{
        contacts = Contacts
    } = get_recruit_info(RoleId),
    OldVal = get_contact(Contacts, Type),
    %% 替换旧值
    Contacts1 = lists:keystore(RecruitType, 1, Contacts, {RecruitType, OldVal + Contact}),
    RecruitInfo1 = RecruitInfo#recruit{contacts = Contacts1},
    set_recruit_info(RecruitInfo1),
    Contacts1.

%% 获取人脉值
get_contact(Contacts, Type) ->
    RecruitType = Type div ?RECRUIT_TYPE_BASE,
    case lists:keyfind(RecruitType, 1, Contacts) of
        false -> 0;
        {_, Val} -> Val
    end.

%% 权重列表转奖励列表
pool_list_to_reward([], List) -> List;
pool_list_to_reward([{PoolId} | T], {StaffList, ItemList}) ->
    #sys_recruit_pool{
        reward_type = RewardType
        , reward = Reward
    } = sys_recruit_pool:get(PoolId),
    case RewardType of
        ?RECRUIT_POOL_REWARD_STAFF -> pool_list_to_reward(T, {Reward ++ StaffList, ItemList});
        ?RECRUIT_POOL_REWARD_ITEM -> pool_list_to_reward(T, {StaffList, Reward ++ ItemList})
    end.


%%========================================结构转换函数
to_p_recruit_pool([], List) -> List;
to_p_recruit_pool([
    #recruit_pool{
        type = Type
        , luck_draw_time = LuckDrawTime
        , act_state = ActState
    } | T], List) ->
    Add = #p_recruit_pool{
        type = Type
        , luck_draw_time = LuckDrawTime
        , day_count = get_pool_daily_count(Type)
        , act_state = ActState
    },
    to_p_recruit_pool(T, [Add | List]).




%%========================================gm
%% 重置数据
gm_reset(RoleId) ->
    cache:delete(get_recruit_info(RoleId)),
    [cache:delete(Rec) || Rec <- get_all_pool_info()],
    role_daily:set(?ROLE_DAILY_TYPE_RECRUIT, []).