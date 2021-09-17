import xml.dom.minidom


# xml工具


# 模块协议
class ModPro():
    id = 0
    name = ""
    desc = ""
    protocol = {}

    def __init__(self, id, name, desc):
        self.id = id
        self.name = name
        self.desc = desc
        self.protocol = {}

# 协议
class Protocol():
    id = 0
    name = ""
    desc = ""
    c2s = None
    s2c = None

    def __init__(self, id, name, desc):
        self.id = id
        self.name = name
        self.desc = desc
        self.c2s = None
        self.s2c = None
        
# 结构体
class Record():
    name = ""
    desc = ""
    keys = {}

    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        self.keys = {}

# key对象
class Key():
    name = ""
    type = ""
    desc = ""
    is_array = False

    def __init__(self, name, type, desc):
        self.name = name
        self.type = type
        self.desc = desc

# 解析协议
def analysis_protocol(file_path):
    # 使用minidom解析器打开 XML 文档
    DOMTree = xml.dom.minidom.parse(file_path)
    collection = DOMTree.documentElement
    # 解析结构体
    records = {}
    types = collection.getElementsByTagName("type")
    for tmp_type in types:
        type_name,type_record = get_record_obj(tmp_type)
        records[type_name] = type_record


    # 解析模块协议
    protocols = {}
    sections = collection.getElementsByTagName("section")
    for tmp_section in sections:
        section_id = tmp_section.getAttribute("id")
        section_name = tmp_section.getAttribute("name")
        section_desc = tmp_section.getAttribute("desc")
        mod_pro = ModPro(section_id, section_name, section_desc)
        msgs = tmp_section.getElementsByTagName("msg")
        # 遍历每条协议
        for tmp_msg in msgs:
            msg_id = tmp_msg.getAttribute("id")
            msg_name = tmp_msg.getAttribute("name")
            msg_desc = tmp_msg.getAttribute("desc")
            protocol = Protocol(msg_id, msg_name, msg_desc)
            # c2s
            c2ss = tmp_msg.getElementsByTagName("c2s")
            for tmp_c2s in c2ss:
                _,c2s_record = get_record_obj(tmp_c2s)
                c2s_record.name = msg_name
                c2s_record.desc = msg_desc
                protocol.c2s = c2s_record
            # s2c
            s2cs = tmp_msg.getElementsByTagName("s2c")
            for tmp_s2c in s2cs:
                _,s2c_record = get_record_obj(tmp_s2c)
                s2c_record.name = msg_name
                s2c_record.desc = msg_desc
                protocol.s2c = s2c_record
            mod_pro.protocol[msg_name] = protocol
        protocols[section_name] = mod_pro
    return records,protocols


#获取record对象
def get_record_obj(record):
    record_name = record.getAttribute("name")
    record_desc = record.getAttribute("desc")
    record_obj = Record(record_name, record_desc)
    # 遍历字段
    fs = record.getElementsByTagName("f")
    fs_dict = fs_to_key_dict(fs)
    loops = record.getElementsByTagName("loop")
    loops_dict = fs_to_key_dict(loops)
    fs_dict.update(loops_dict)
    record_obj.keys = fs_dict
    return record_name,record_obj
#获取key对象
def get_key_obj(key):
    key_type = key.getAttribute("t")
    key_name = key.getAttribute("name")
    key_desc = key.getAttribute("desc")
    key_obj = Key(key_name, key_type, key_desc)
    return key_name,key_obj
# fs转key_dict
def fs_to_key_dict(fs):
    key_dict = {}
    for tmp_f in fs:
        f_name,f_key = get_key_obj(tmp_f)
        key_dict[f_name] = f_key
    return key_dict
# loops转key_dict
def loops_to_key_dict(loops):
    key_dict = {}
    for tmp_loop in loops:
        loop_name,loop_key = get_key_obj(tmp_loop)
        loop_key.is_array = True
        key_dict[loop_name] = loop_key
    return key_dict


