# 代码生成器

## 运行代码 
修改get_erl.py
    import mod_protocol.协议文件名 as mod
    mod_name = "协议文件名"
运行get_erl.py 生成代码文件

## 配置文件说明
同目录下cfg.py
author_name： 作者名
out_path：lib和rpc输出目录， 会先创建一个名字为模块名的文件夹
out_hrl_path：hrl文件输出目录
### 非必要函数配置开关
need_event_fun: 是否需要非必要事件函数

## 使用前提说明
协议文件名需要与功能模块名一致
1. 确保协议文件存在
2. 协议文件的协议名要求
    模块名_函数名_request 
        如：ancient_test_info_request
            ancient_test 是模块名 输出目录下，创建ancient_test文件夹，ancient_test_lib.erl, ancient_test_lib.rpc
            info 是函数名  会生成对应的
                lib入口函数： info()    函数名()
                检查函数: check_info()  check_函数名()
                执行函数：do_info()     do_函数名()
    模块名_函数名_reply
        对应上面的结构
3. record_define 模块返回给客户端的结构体
    会自动生成转换函数
    结构体名_p
    to_ancient_test_info_p(A)               转换单个
    to_ancient_test_info_p([A|B], List)     转换列表
    同时也会在 模块名.hrl 生成对应的record文件
4. 模块名_info_request 比较特殊
    会根据协议内容在 模块名.hrl 生成对应名为：player_模块名 的record文件
5. look()和save_info()
    默认操作对应的结构是 player_模块名

## 
    
