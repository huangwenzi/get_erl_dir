# 部族系统

record_define = [
    # 加入部族的条件
    ("guild_join_condition_p", [
        ("level_id", "int", "所需等级id, 配置表配的id"),
        ("power_id", "int", "所需战力id"),
    ], True),

    # 部族列表
    ("guild_list_p", [
        ("idx", "int", "排名"),
        ("id", "int", "部族id"),
        ("name", "string", "部族名字"),
        ("icon", "int", "旗帜id"),
        ("level", "int", "部族等级"),
        ("num", "int", "部族人数"),
        ("patriarch_pid", "int", "族长的玩家id"),
        ("patriarch_name", "string", "族长名字"),
        ("join_cond", "guild_join_condition_p", "加入部族的条件"),
    ], True),

     # 部族成员信息
    ("guild_member_info_p", [
        ("player_id", "int", "玩家id"),
        ("name", "string", "玩家名字"),
        ("level", "int", "玩家等级"),
        ("power", "int", "玩家战力"),
        ("position", "int", "职位"),
        ("contribution", "int", "历史贡献值"),
        ("status", "int", "玩家在线状态  在线是0，离线则是上一次离线的时间戳"),
    ], True),

    # 外部查看部族信息 属于开放给所有玩家看的部族信息
    ("guild_public_info_p", [
        ("id", "int", "部族id"),
        ("name", "string", "部族名字"),
        ("icon", "int", "旗帜id"),
        ("level", "int", "部族等级"),
        ("num", "int", "部族人数"),
        ("patriarch_pid", "int", "族长的玩家id"),
        ("patriarch_name", "string", "族长的名字"),
        ("notice", "string", "部族公告"),
        ("all_power", "int", "总战力"),
        ("member_list", "array of guild_member_info_p", "成员列表"),
    ], True),

    # 部族信息 属于本部族的成员才能查看的信息
    ("guild_info_p", [
        ("id", "int", "部族id"),
        ("name", "string", "部族名字"),
        ("icon", "int", "旗帜id"),
        ("level", "int", "部族等级"),
        ("num", "int", "部族人数"),
        ("patriarch_pid", "int", "族长的玩家id"),
        ("patriarch_name", "string", "族长的名字"),
        ("notice", "string", "部族公告"),
        ("prestige", "int", "部族声望"),
        ("position", "int", "职位"),
        ("is_new_lvup", "int", "是否有新的升级 0否 1是"),
    ], True),

    # 部族申请信息
    ("guild_apply_join_info_p", [
        ("player_id", "int", "玩家id"),
        ("name", "string", "玩家名字"),
        ("level", "int", "玩家等级"),
        ("power", "int", "玩家战力"),
        ("status", "int", "玩家在线状态  在线是0，离线则是上一次离线的时间戳"),
    ], True),

    # 祭祀日志
    ("guild_donate_log_p", [
        ("player_id", "int", "玩家id"),
        ("name", "string", "玩家名字"),
        ("position", "int", "职位"),
        ("type", "int", "祭祀类型"),
        ("time", "int", "祭祀时间"),
    ], True),

    # 部族技能信息
    ("guild_skill_info_p", [
        ("type", "int", "技能类型"),
        ("skills", "array of simple_list", "技能等级"),
    ], True),

    # 仓库活动奖励的道具信息
    ("guild_warehouse_activity_shared_p", [
        ("id", "int", "唯一id"),
        ("conf_id", "int", "配置表id"),
        ("item_id", "int", "道具id"),
        ("item_group", "int", "道具组数"),
        ("activity_id", "int", "活动id"),
        ("time", "int", "发放时间"),
    ], True),

    # 仓库日志
    ("guild_warehouse_log_p", [
        ("type", "int", "操作类型 1玩家存 2活动奖励存 3玩家取 4过期 5清理"),
        ("item_list", "array of simple_list", "道具id和数量"),
        ("time", "int", "操作时间"),
        ("player_id", "int", "操作的玩家id"),
        ("player_name", "string", "操作的玩家名字"),
        ("activity_id", "int", "活动id"),
    ], True),

    # 部族仓库信息
    ("guild_warehouse_info_p", [
        ("sell_rec", "array of simple_list", "今日存入次数"),
        ("buy_rec", "array of simple_list", "今日兑换次数"),
        ("member_shared", "array of simple_list", "成员共享的道具列表"),
        ("activity_shared", "array of guild_warehouse_activity_shared_p", "活动奖励的道具列表"),
        ("log", "array of guild_warehouse_log_p", "仓库日志"),
        ("beast_sell_count", "int", "今日异兽的存入次数"),
        ("beast_buy_count", "int", "今日异兽的兑换次数"),
    ], True),

    # 狩猎战报
    ("guild_hunting_log_p", [
        ("type", "int", "战报类型 1挑战 2阻击"),
        ("svr_id", "int", "操作的玩家所在服务器id"),
        ("player_name", "string", "操作的玩家名字"),
        ("to_svr_id", "int", "被阻击的玩家所在服务器id"),
        ("to_player_name", "string", "被阻击的玩家名字"),
        ("integral", "int", "获得的积分"),
    ], True),

    # 狩猎前N的信息
    ("guild_hunting_top_p", [
        ("idx", "int", "排名"),
        ("svr_id", "int", "所在服务器id"),
        ("id", "int", "id"),
        ("name", "string", "名字"),
        ("integral", "int", "积分"),
    ], True),

    # 狩猎信息
    ("guild_hunting_info_p", [
        ("dungeon_id", "int", "副本id"),
        ("personal_integral", "int", "个人积分"),
        ("personal_idx", "int", "个人排名"),
        ("guild_idx", "int", "部族排名"),
        ("inspire_times", "int", "已鼓舞的次数"),
        ("sur_blocking_times", "int", "阻击剩余次数"),
        ("sur_blocking_cd", "int", "阻击剩余冷却时间"),
        ("sur_challenge_times", "int", "挑战剩余次数"),
        ("sur_challenge_cd", "int", "挑战剩余冷却时间"),
        ("log", "array of guild_hunting_log_p", "战况广播"),
        ("top_rank", "array of guild_hunting_top_p", "个人排行榜前N名信息"),
        ("top_rank_guild", "array of guild_hunting_top_p", "部族排行榜前N名信息"),
        ("top_rank_guild_inside", "array of guild_hunting_top_p", "族内排行榜前N名信息"),
        ("is_received", "int", "奖励是否领取了 0：未领取 1：已领取"),
        ("reward", "array of simple_list", "可领取的奖励"),
    ], True),
   
    # 狩猎阻击列表
    ("guild_hunting_blocking_list_p", [
        ("idx", "int", "排名"),
        ("head", "player_head_p", "玩家的头像信息"),
        ("integral", "int", "玩家的积分"),
    ], True),

    # 狩猎阻击记录
    ("guild_hunting_blocking_rec_p", [
        ("result", "int", "结果 1阻击成功 2阻击失败 3防守成功 4防守失败"),
        ("head", "player_head_p", "阻击或被阻击的玩家头像"),
        ("time", "int", "时间"),
        ("integral", "int", "损失或获得的积分"),
    ], True),

    # 狩猎族内排名信息
    ("guild_hunting_rank_p", [
        ("player_head", "player_head_p", "头像信息"),
        ("idx", "int", "名次"),
        ("position", "int", "职位"),
        ("integral", "int", "玩家的积分"),
    ], True, "狩猎族内排名信息"),
]

protocol_define = {
    "guild_player_info_request": {
         
        "desc": "请求玩家的部族数据",
        "reply": "guild_player_info_reply",
        "payload": [
        ],
    },
    "guild_player_info_reply": {
         
        "desc": "返回玩家的部族数据",
        "payload": [
            ("guild_id", "int", "所在部族的id，未加入部族则是0"),
            ("leave_time", "int", "离开部族的时间,从未离开过部族或已加入部族则是0"),
            ("apply_list", "array of int", "玩家申请的部族列表"),
        ],
    },
    
    "guild_list_request": {
         
        "desc": "请求部族列表",
        "reply": "guild_list_reply",
        "payload": [
        ],
    },
    "guild_list_reply": {
         
        "desc": "返回部族列表",
        "payload": [
            ("guild_list", "array of guild_list_p", "部族列表"),
        ],
    },

    "guild_view_request": {
         
        "desc": "查看部族信息（公共）",
        "reply": "guild_view_reply",
        "payload": [
            ("id", "int", "部族id"),
        ],
    },
    "guild_view_reply": {
         
        "desc": "返回部族信息（公共）",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
            ("guild_info", "guild_public_info_p", "部族信息"),
        ],
    },

    "guild_create_request": {
         
        "desc": "创建部族",
        "reply": "guild_create_reply",
        "payload": [
           ("name", "string", "部族名字"),
           ("icon", "int", "旗帜id"),
           ("notice", "string", "部族公告"),
        ],
    },
    "guild_create_reply": {
         
        "desc": "创建部族返回",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
            ("guild_info", "guild_info_p", "部族信息"),
        ],
    },

    "guild_apply_join_request": {
         
        "desc": "申请加入部族",
        "reply": "guild_apply_join_reply",
        "payload": [
            ("id", "int", "部族id"),
        ],
    },
    "guild_apply_join_reply": {
         
        "desc": "申请加入部族返回",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
        ],
    },

    "guild_apply_join_notify":{
         
        "desc": "玩家申请加入部族通知 只发给有审核资格的部族成员",
        "payload": [
        ],
    },

    "guild_info_request": {
         
        "desc": "请求玩家所在的部族信息",
        "reply": "guild_info_reply",
        "payload": [
        ],
    },
    "guild_info_reply": {
         
        "desc": "返回部族信息",
        "payload": [
            ("guild_info", "guild_info_p", "部族信息"),
        ],
    },

    "guild_member_list_request": {
         
        "desc": "请求部族成员列表",
        "reply": "guild_member_list_reply",
        "payload": [
        ],
    },
    "guild_member_list_reply": {
         
        "desc": "返回部族成员列表",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
            ("member_list", "array of guild_member_info_p", "成员列表"),
        ],
    },

    "guild_apply_join_list_request": {
         
        "desc": "请求部族申请列表",
        "reply": "guild_apply_join_list_reply",
        "payload": [
        ],
    },
    "guild_apply_join_list_reply": {
         
        "desc": "返回部族申请列表",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
            ("apply_join_list", "array of guild_apply_join_info_p", "申请列表"),
            ("is_auto_apply", "int", "是否自动同意申请 0否 1是"),
            ("join_cond", "guild_join_condition_p", "加入部族的条件"),
        ],
    },

    "guild_approve_join_request": {
         
        "desc": "审批申请加入部族的玩家",
        "reply": "guild_approve_join_list_reply",
        "payload": [
             ("apply_player_id", "int", "申请加入的玩家id"),
             ("is_agree", "int", "是否同意 0拒绝 1同意"),
        ],
    },
    "guild_approve_join_list_reply": {
         
        "desc": "返回审批结果",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
            ("is_agree", "int", "是否同意 0拒绝 1同意"),
        ],
    },

    "guild_join_notify":{
         
        "desc": "加入部族通知",
        "payload": [
             ("is_auto_join", "int", "是否是由自动同意加入的部族 0否 1是"),
             ("guild_info", "guild_info_p", "部族信息"),
        ],
    },

    "guild_set_auto_apply_request": {
         
        "desc": "设置自动审批",
        "reply": "guild_set_auto_apply_reply",
        "payload": [
        ],
    },
    "guild_set_auto_apply_reply": {
         
        "desc": "返回自动审批结果",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
            ("is_auto_apply", "int", "是否自动同意申请 0否 1是"),
        ],
    },

    "guild_set_join_cond_request": {
         
        "desc": "设置加入条件",
        "reply": "guild_set_join_cond_reply",
        "payload": [
            ("level_id", "int", "所需等级id, 配置表配的id"),
            ("power_id", "int", "所需战力id"),
        ],
    },
    "guild_set_join_cond_reply": {
         
        "desc": "返回加入条件",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
            ("join_cond", "guild_join_condition_p", "加入部族的条件"),
        ],
    },

    "guild_modify_name_request": {
         
        "desc": "修改部族名字",
        "reply": "guild_modify_name_reply",
        "payload": [
            ("new_name", "string", "新的名字"),
        ],
    },
    "guild_modify_name_reply": {
         
        "desc": "返回修改结果",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
            ("new_name", "string", "新的名字"),
        ],
    },

    "guild_modify_icon_request": {
         
        "desc": "修改部族旗帜",
        "reply": "guild_modify_icon_reply",
        "payload": [
            ("new_icon", "int", "新的旗帜id"),
        ],
    },
    "guild_modify_icon_reply": {
         
        "desc": "返回修改结果",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
            ("new_icon", "int", "新的旗帜id"),
        ],
    },

    "guild_modify_notice_request": {
         
        "desc": "修改部族公告",
        "reply": "guild_modify_notice_reply",
        "payload": [
            ("new_notice", "string", "新的公告"),
        ],
    },
    "guild_modify_notice_reply": {
         
        "desc": "返回修改结果",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
            ("new_notice", "string", "新的公告"),
        ],
    },

    "guild_appoint_request": {
         
        "desc": "任命职位",
        "reply": "guild_appoint_reply",
        "payload": [
            ("player_id", "int", "被任命的玩家id"),
            ("position", "int", "职位"),
        ],
    },
    "guild_appoint_reply": {
         
        "desc": "任命职位结果",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
            ("member_list", "array of guild_member_info_p", "成员列表"),
        ],
    },

    "guild_kick_request": {
         
        "desc": "踢人",
        "reply": "guild_kick_reply",
        "payload": [
            ("player_id", "int", "被踢玩家id"),
        ],
    },
    "guild_kick_reply": {
         
        "desc": "踢人结果",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
            ("member_list", "array of guild_member_info_p", "成员列表"),
        ],
    },

    "guild_kicked_notify":{
         
        "desc": "被踢通知",
        "payload": [
        ],
    },

    "guild_transfer_request": {
         
        "desc": "族长转让",
        "reply": "guild_transfer_reply",
        "payload": [
            ("player_id", "int", "被转让的玩家id"),
        ],
    },
    "guild_transfer_reply": {
         
        "desc": "族长转让结果",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
            ("member_list", "array of guild_member_info_p", "成员列表"),
        ],
    },

    "guild_disband_request": {
         
        "desc": "部族解散",
        "reply": "guild_disband_reply",
        "payload": [
        ],
    },
    "guild_disband_reply": {
         
        "desc": "部族解散结果",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
        ],
    },

    "guild_disband_notify":{
         
        "desc": "部族解散通知",
        "payload": [
        ],
    },

    "guild_quit_request": {
         
        "desc": "退出部族",
        "reply": "guild_quit_reply",
        "payload": [
        ],
    },
    "guild_quit_reply": {
         
        "desc": "退出部族结果",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
        ],
    },

    #部族祭祀
    "guild_donate_info_request": {
         
        "desc": "祭祀信息",
        "reply": "guild_donate_info_reply",
        "payload": [
        ],
    },
    "guild_donate_info_reply": {
         
        "desc": "返回祭祀信息",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
            ("type", "int", "今日祭祀类型 0为未祭祀"),
            ("level", "int", "部族等级"),
            ("prestige", "int", "部族声望"),
            ("progress", "int", "祭祀进度"),
            ("status", "array of int", "祭祀奖励领取情况"),
            ("log", "array of guild_donate_log_p", "祭祀日志"),
        ],
    },

    "guild_donate_request": {
         
        "desc": "进行祭祀",
        "reply": "guild_donate_reply",
        "payload": [
            ("type", "int", "祭祀类型"),
        ],
    },
    "guild_donate_reply": {
         
        "desc": "祭祀结果",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
            ("level", "int", "部族等级"),
            ("prestige", "int", "部族声望"),
            ("progress", "int", "祭祀进度"),
            ("log", "array of guild_donate_log_p", "祭祀日志"),
        ],
    },

    "guild_donate_notify":{
         
        "desc": "玩家祭祀通知",
        "payload": [
            ("progress", "int", "祭祀进度"),
        ],
    },

    "guild_donate_receive_request": {
         
        "desc": "请求领取祭祀进度奖励",
        "reply": "guild_donate_receive_reply",
        "payload": [
            ("id", "int", "领取的奖励id"),
        ],
    },
    "guild_donate_receive_reply": {
         
        "desc": "领取祭祀进度奖励结果",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
            ("id", "int", "领取的奖励id"),
        ],
    },

    #部族技能
    "guild_skill_info_request": {
         
        "desc": "请求部族技能信息",
        "reply": "guild_skill_info_reply",
        "payload": [
        ],
    },
    "guild_skill_info_reply": {
         
        "desc": "返回部族技能信息",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
            ("skill_list", "array of guild_skill_info_p", "技能列表"),
        ],
    },

    "guild_skill_lv_up_request": {
         
        "desc": "部族技能升级",
        "reply": "guild_skill_lv_up_reply",
        "payload": [
            ("type", "int", "升级的技能类型"),
        ],
    },
    "guild_skill_lv_up_reply": {
         
        "desc": "部族技能升级返回",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
            ("skill_id", "int", "升级的技能id"),
            ("skill_info", "guild_skill_info_p", "技能信息"),
        ],
    },

    #部族仓库
    "guild_warehouse_info_request": {
         
        "desc": "请求部族仓库信息",
        "reply": "guild_warehouse_info_reply",
        "payload": [
        ],
    },
    "guild_warehouse_info_reply": {
         
        "desc": "返回部族仓库信息",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
            ("info", "guild_warehouse_info_p", "仓库信息"),
        ],
    },

    "guild_warehouse_sell_request": {
         
        "desc": "部族仓库存物品",
        "reply": "guild_warehouse_sell_reply",
        "payload": [
            ("type", "int", "存入类型 跟配置表对应"),
            ("item_id", "int", "物品id或异兽唯一id"),
            ("item_group", "int", "物品组数"),
        ],
    },
    "guild_warehouse_sell_reply": {
         
        "desc": "部族仓库存物品返回",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
        ],
    },

    "guild_warehouse_buy_request": {
         
        "desc": "部族仓库兑换物品",
        "reply": "guild_warehouse_buy_reply",
        "payload": [
            ("type", "int", "兑换类型 1成员共享 2活动奖励"),
            ("id", "int", "道具id、异兽id或唯一id"),
            ("item_group", "int", "兑换组数"),
        ],
    },
    "guild_warehouse_buy_reply": {
         
        "desc": "部族仓库兑换物品返回",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
        ],
    },

    "guild_warehouse_update_notify":{
         
        "desc": "部族仓库更新通知 玩家存取道具 活动奖励发放时广播",
        "payload": [
        ],
    },

    "guild_warehouse_clear_request": {
         
        "desc": "部族仓库清理物品",
        "reply": "guild_warehouse_clear_reply",
        "payload": [
            ("item_id", "int", "道具id"),
            ("item_group", "int", "清理组数"),
        ],
    },
    "guild_warehouse_clear_reply": {
         
        "desc": "部族仓库兑换物品返回",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
        ],
    },


    #部族狩猎
    "guild_hunting_info_request": {
         
        "desc": "请求部族狩猎的信息",
        "reply": "guild_hunting_info_reply",
        "payload": [
        ],
    },
    "guild_hunting_info_reply": {
         
        "desc": "返回部族狩猎的信息",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
            ("info", "guild_hunting_info_p", "狩猎信息"),
            ('cross_type', 'int', '本活动的跨服类型 0：本服活动 1：小跨服活动 2：大跨服活动'),
        ],
    },

    "guild_hunting_inspire_request": {
         
        "desc": "请求部族狩猎鼓舞",
        "reply": "guild_hunting_inspire_reply",
        "payload": [
        ],
    },
    "guild_hunting_inspire_reply": {
         
        "desc": "返回部族狩猎的鼓舞结果",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
            ("inspire_times", "int", "已鼓舞的次数"),
        ],
    },

    "guild_hunting_challenge_request": {
         
        "desc": "请求部族狩猎挑战",
        "reply": "guild_hunting_challenge_reply",
        "payload": [
            ("in_battle", "simple_list", "出战异兽"),
            ("formation", "int", "阵形"),
        ],
    },
    "guild_hunting_challenge_reply": {
         
        "desc": "返回部族狩猎的挑战结果",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
        ],
    },

    "guild_hunting_blocking_list_request": {
         
        "desc": "请求部族狩猎阻击列表",
        "reply": "guild_hunting_blocking_list_reply",
        "payload": [
        ],
    },
    "guild_hunting_blocking_list_reply": {
         
        "desc": "返回部族狩猎的阻击列表",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
            ("blocking_list", "array of guild_hunting_blocking_list_p", "阻击列表"),
        ],
    },

    "guild_hunting_blocking_request": {
         
        "desc": "请求部族狩猎阻击",
        "reply": "guild_hunting_blocking_reply",
        "payload": [
            ("to_player_id", "int", "阻击对象的id"),
            ("in_battle", "simple_list", "出战异兽"),
            ("formation", "int", "阵形"),
        ],
    },
    "guild_hunting_blocking_reply": {
         
        "desc": "返回部族狩猎的阻击结果",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
        ],
    },

    "guild_hunting_challenge_reward_reply": {
         
        "desc": "领取部族狩猎挑战奖励返回",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
            ("dungeon", "int", "副本类型"),
            ("reward", "simple_list", "挑战奖励"),
            ("hurt_val", "int", "造成的伤害值"),
            ("get_integral", "int", "获得的积分"),
            ("new_rank_idx", "int", "新的名次"),
            ("up_rank_idx", "int", "上升名次"),
        ],
    },

    "guild_hunting_blocking_reward_reply": {
         
        "desc": "领取部族狩猎阻击奖励返回",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
            ("dungeon", "int", "副本类型"),
            ("result", "int", "1成功，0失败"),
            ("player_head", "player_head_p", "玩家头像"),
            ("to_player_head", "player_head_p", "被阻击的玩家头像"),
            ("old_integral", "int", "玩家原本积分"),
            ("to_old_integral", "int", "被阻击的玩家原本积分"),
            ("get_integral", "int", "获得的积分"),
            ("new_rank_idx", "int", "新的名次"),
            ("up_rank_idx", "int", "上升名次"),
        ],
    },

    "guild_hunting_blocking_rec_request": {
         
        "desc": "请求部族狩猎阻击记录",
        "reply": "guild_hunting_blocking_rec_reply",
        "payload": [
        ],
    },
    "guild_hunting_blocking_rec_reply": {
         
        "desc": "返回部族狩猎阻击记录",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
            ("rec", "array of guild_hunting_blocking_rec_p", "阻击记录"),
        ],
    },

    "guild_hunting_blocking_lineup_request": {
         
        "desc": "请求部族狩猎阻击阵容",
        "reply": "guild_hunting_blocking_lineup_reply",
        "payload": [
            ("to_player_id", "int", "阻击对象的id"),
        ],
    },
    "guild_hunting_blocking_lineup_reply": {
         
        "desc": "返回部族狩猎阻击阵容",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
            ("to_player_id", "int", "阻击对象的id"),
            ("to_lineup", "other_lineup_p", "阻击对象的阵容"),
        ],
    },

    "guild_hunting_log_request": {
         
        "desc": "请求部族狩猎日志",
        "reply": "guild_hunting_log_reply",
        "payload": [
        ],
    },
    "guild_hunting_log_reply": {
         
        "desc": "返回部族狩猎日志",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
            ("log", "array of guild_hunting_log_p", "战况广播"),
        ],
    },

    "guild_hunting_be_blocking_notify":{
         
        "desc": "部族狩猎 被阻击的玩家的通知",
        "payload": [
        ],
    },

    "guild_hunting_rank_inside_request": {
         
        "desc": "请求部族狩猎族内排行信息",
        "reply": "guild_hunting_rank_inside_reply",
        "payload": [
        ],
    },
    "guild_hunting_rank_inside_reply": {
         
        "desc": "返回部族狩猎族内排行信息",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
            ("rank_list", "array of guild_hunting_rank_p", "排行信息"),
            ("my_idx", "int", "玩家的名次"),
        ],
    },

    "guild_hunting_receive_request": {
         
        "desc": "部族狩猎领取奖励",
        "reply": "guild_hunting_receive_reply",
        "payload": [
        ],
    },
    "guild_hunting_receive_reply": {
         
        "desc": "返回领取结果",
        "payload": [
            ("code", "int", "0 表示成功， 其他表示错误码"),
            ("reward", "array of simple_list", "奖励列表"),
        ],
    },
    
}