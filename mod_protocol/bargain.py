

header = []


error_msg = [
]

record_define = [
    ## 礼包数据
    ('bargain_gift_p', [
        ('id', 'int', "礼包id"),
        ('help_list', 'simple_list', "已砍价玩家, [[玩家id, 砍价金额]]"),
        ('buy_count', 'int', "已购买次数"),
    ], True),
]

protocol_define = {
    "bargain_gift_notify": {
        "desc": "礼包变化推送",
        "payload": [
            ("code", "int"),
            ("gift", "bargain_gift_p", "礼包信息"),
        ],
    },

    "bargain_info_request": {
        "desc": "请求砍价礼包信息",
        "payload": [
        ],
    },

    "bargain_info_reply": {
        "desc": "砍价礼包信息返回",
        "payload": [
            ("code", "int"),
            ("help_conut", "int", "已帮助砍价次数"),
            ('help_list', 'simple_list', "已帮助好友 [[玩家id, 礼包id]]"),
            ("gift_list", "array of bargain_gift_p", "礼包列表"),
        ],
    },

    "bargain_help_request": {
        "desc": "请求帮助砍价",
        "payload": [
            ("friend_id", "int", "好友id"),
            ("gift_id", "int", "礼包id"),
        ],
    },

    "bargain_help_reply": {
        "desc": "帮助砍价返回",
        "payload": [
            ("code", "int"),
            ("help_conut", "int", "已帮助砍价次数"),
            ('help_list', 'simple_list', "已帮助好友 [[玩家id, 礼包id]]"),
        ],
    },
    
    "bargain_help_a_request": {
        "desc": "请求帮助砍价",
        "payload": [
            ("friend_id", "int", "好友id"),
            ("gift_id", "int", "礼包id"),
        ],
    },

    "bargain_help_a_reply": {
        "desc": "帮助砍价返回",
        "payload": [
            ("code", "int"),
            ("help_conut", "int", "已帮助砍价次数"),
            ('help_list', 'simple_list', "已帮助好友 [[玩家id, 礼包id]]"),
        ],
    },
    
    "bargain_help_b_request": {
        "desc": "请求帮助砍价",
        "payload": [
            ("friend_id", "int", "好友id"),
            ("gift_id", "int", "礼包id"),
        ],
    },

    "bargain_help_b_reply": {
        "desc": "帮助砍价返回",
        "payload": [
            ("code", "int"),
            ("help_conut", "int", "已帮助砍价次数"),
            ('help_list', 'simple_list', "已帮助好友 [[玩家id, 礼包id]]"),
        ],
    },
}
