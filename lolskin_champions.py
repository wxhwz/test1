import requests
import json

from sqlalchemy import false


def mapping_path(old_path:str):
    return old_path.replace("/lol-game-data/assets","https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default",1).lower()

def download_and_parse_json(url):
    try:
        # 发送GET请求
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功

        # 解析JSON数据
        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return None

hero_nicknames = {
    "黑暗之女": "火女",
    "狂战士": None,
    "正义巨像": None,
    "卡牌大师": "卡牌",
    "德邦总管": "赵信",
    "无畏战车": "螃蟹",
    "诡术妖姬": "妖姬",
    "猩红收割者": "吸血鬼",
    "远古恐惧": "稻草人",
    "正义天使": "天使",
    "无极剑圣": "剑圣",
    "牛头酋长": "牛头",
    "符文法师": "瑞兹",
    "亡灵战神": "老司机",
    "战争女神": "轮子妈",
    "众星之子": "奶妈",
    "迅捷斥候": "提莫",
    "麦林炮手": "小炮",
    "祖安怒兽": "狼人",
    "雪原双子": "雪人",
    "赏金猎人": "女枪",
    "寒冰射手": "寒冰",
    "蛮族之王": "蛮王",
    "武器大师": "武器",
    "堕落天使": None,
    "时光守护者": "基兰",
    "炼金术士": "炼金",
    "痛苦之拥": "寡妇",
    "瘟疫之源": "老鼠",
    "死亡颂唱者": "死歌",
    "虚空恐惧": "大虫子",
    "殇之木乃伊": "木乃伊",
    "披甲龙龟": "龙龟",
    "冰晶凤凰": "冰鸟",
    "恶魔小丑": "小丑",
    "祖安狂人": "蒙多",
    "琴瑟仙女": "琴女",
    "虚空行者": None,
    "刀锋舞者": "刀妹",
    "风暴之怒": "风女",
    "海洋之灾": "船长",
    "英勇投弹手": "飞机",
    "天启者": None,
    "瓦洛兰之盾": "宝石",
    "邪恶小法师": "小法",
    "巨魔之王": "巨魔",
    "诺克萨斯统领": "乌鸦",
    "皮城女警": "女警",
    "蒸汽机器人": "机器人",
    "熔岩巨兽": "石头人",
    "不祥之刃": "卡特",
    "永恒梦魇": "梦魇",
    "扭曲树精": "大树",
    "荒漠屠夫": "鳄鱼",
    "德玛西亚皇子": "皇子",
    "蜘蛛女皇": "蜘蛛",
    "发条魔灵": "发条",
    "齐天大圣": "猴子",
    "复仇焰魂": "火男",
    "盲僧": "瞎子",
    "暗夜猎手": "vn",
    "机械公敌": None,
    "魔蛇之拥": "蛇女",
    "上古领主": "蝎子",
    "大发明家": "大头",
    "沙漠死神": "狗头",
    "狂野女猎手": "豹女",
    "兽灵行者": None,
    "圣锤之毅": None,
    "酒桶": None,
    "不屈之枪": "潘森",
    "探险家": "ez",
    "铁铠冥魂": "铁男",
    "牧魂人": "掘墓",
    "离群之刺": None,
    "狂暴之心": None,
    "德玛西亚之力": None,
    "曙光女神": "日女",
    "虚空先知": "蚂蚱",
    "刀锋之影": "男刀",
    "放逐之刃": "瑞文",
    "深渊巨口": "大嘴",
    "暮光之眼": "慎",
    "光辉女郎": "拉克丝",
    "远古巫灵": "泽拉斯",
    "龙血武姬": "龙女",
    "九尾妖狐": "狐狸",
    "法外狂徒": "男枪",
    "潮汐海灵": "小鱼人",
    "不灭狂雷": "狗熊",
    "傲之追猎者": "狮子狗",
    "惩戒之箭": "韦鲁斯",
    "深海泰坦": "泰坦",
    "奥术先驱": "维克托",
    "北地之怒": "猪妹",
    "无双剑姬": "剑姬",
    "爆破鬼才": "炸弹人",
    "仙灵女巫": "璐璐",
    "荣耀行刑官": "德莱文",
    "战争之影": "人马",
    "虚空掠夺者": "螳螂",
    "诺克萨斯之手": "诺手",
    "未来守护者": "杰斯",
    "冰霜女巫": "冰女",
    "皎月女神": "皎月",
    "德玛西亚之翼": "鸟人",
    "暗黑元首": "辛德拉",
    "铸星龙王": "龙王",
    "影流之镰": "凯隐",
    "暮光星灵": "佐伊",
    "荆棘之兴": "婕拉",
    "虚空之女": "卡莎",
    "星籁歌姬": "酸辣粉",
    "迷失之牙": "纳尔",
    "生化魔人": "扎克",
    "疾风剑豪": "风男",
    "虚空之眼": "大眼",
    "岩雀": "岩雀",
    "青钢影": "青钢影",
    "影哨": "阿克尚",
    "虚空女皇": "卑尔维斯",
    "弗雷尔卓德之心": "布隆",
    "戏命师": "烬",
    "永猎双子": "千珏",
    "祖安花火": "泽丽",
    "暴走萝莉": "金克丝",
    "河流之王": "塔姆",
    "狂厄蔷薇": "贝蕾亚",
    "破败之王": "佛耶戈",
    "涤魂圣枪": "赛娜",
    "圣枪游侠": "奥巴马",
    "影流之主": "劫",
    "暴怒骑士": "克烈",
    "时间刺客": "艾克",
    "元素女皇": "琪亚娜",
    "皮城执法官": "蔚",
    "暗裔剑魔": "剑魔",
    "唤潮鲛姬": "娜美",
    "沙漠皇帝": "沙皇",
    "魔法猫咪": "猫咪",
    "沙漠玫瑰": "莎弥拉",
    "魂锁典狱长": "锤石",
    "海兽祭司": "触手妈",
    "虚空遁地兽": "挖掘机",
    "翠神": "艾翁",
    "复仇之矛": "滑板鞋",
    "星界游神": "巴德",
    "幻翎": "洛",
    "逆羽": "霞",
    "山隐之焰": "奥恩",
    "解脱者": "塞拉斯",
    "万花通灵": "妮蔻",
    "残月之肃": "月男",
    "镕铁少女": "芮尔",
    "血港鬼影": "水鬼",
    "愁云使者": "薇古丝",
    "封魔剑魂": "永恩",
    "铁血狼母": "狼母",  # 新英雄，暂无广泛认可的代称
    "流光镜影": None,  # 新英雄，暂无广泛认可的代称
    "不破之誓": None,  # 新英雄，暂无广泛认可的代称
    "腕豪": "瑟提",
    "含羞蓓蕾": "莉莉娅",
    "灵罗娃娃": "格温",
    "炼金男爵": "烈娜塔",
    "双界灵兔": None,  # 新英雄，暂无广泛认可的代称
    "不羁之悦": "尼菈",
    "纳祖芒荣耀": "奎桑提",
    "炽炎雏龙": "斯莫德",
    "明烛": "米利欧",
    "异画师": "慧",
    "百裂冥犬": "狼狗"
}



# 使用示例
url = "https://raw.communitydragon.org/pbe/plugins/rcp-be-lol-game-data/global/zh_cn/v1/champion-summary.json"
json_data = download_and_parse_json(url)


if json_data:
    print("JSON数据解析成功:")
    # filter_data = [
    #     champion for champion in json_data if champion['id'] < 30000]

    filter_data = [
            {key:mapping_path(value) if key in ['squarePortraitPath'] else value
             for key,value in champion.items()
             if key in ['id','name','description','alias','squarePortraitPath']}
            for champion in json_data if champion['id'] < 30000 and champion['id'] != -1
        ]

    for champion in filter_data:
        if hero_nicknames[champion['name']]:
            champion['alias_cn'] = hero_nicknames[champion['name']]
        else:
            champion['alias_cn'] = None

    # print(json.dumps(filter_data, indent=2, ensure_ascii=False))

    with open('./lol_champions.json','w',encoding='utf-8')as f:
        json.dump(filter_data,f,ensure_ascii=False,indent=4)
