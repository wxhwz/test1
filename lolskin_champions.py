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

    # print(json.dumps(filter_data, indent=2, ensure_ascii=False))

    with open('./lol_champions.json','w',encoding='utf-8')as f:
        json.dump(filter_data,f,ensure_ascii=False,indent=4)
