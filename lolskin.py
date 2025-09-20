import requests
import json
import os

skin_json_dir = './lolskin_json_dir'
champions_json_path= './lol_champions.json'

def mapping_path(old_path:str):
    if old_path is None:
        return None
    else:
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


def parse_skin_json(id:int):
    json_data_zh = download_and_parse_json(f'https://raw.communitydragon.org/pbe/plugins/rcp-be-lol-game-data/global/zh_cn/v1/champions/{id}.json')
    if json_data_zh:
        filter_data_zh = {
            "id": json_data_zh['id'],
            "name" : json_data_zh['name'],
            "skins":[
                {key:mapping_path(value) if key in ['uncenteredSplashPath', 'loadScreenPath','rarityGemPath'] else value
                 for key,value in skin.items()
                 if key in ['name','uncenteredSplashPath','loadScreenPath','rarity','regionRarityId','rarityGemPath']}
                for skin in json_data_zh['skins'] if skin['isBase'] == False
            ]
        }
    json_data_en = download_and_parse_json(
        f'https://raw.communitydragon.org/pbe/plugins/rcp-be-lol-game-data/global/default/v1/champions/{id}.json')
    if json_data_en:
        filter_data_en = {
            "id": json_data_en['id'],
            "name": json_data_en['name'],
            "skins": [
                {key: mapping_path(value) if key in ['uncenteredSplashPath', 'loadScreenPath','rarityGemPath'] else value
                 for key, value in skin.items()
                 if key in ['name', 'uncenteredSplashPath', 'loadScreenPath', 'rarity', 'regionRarityId','rarityGemPath']}
                for skin in json_data_en['skins'] if skin['isBase'] == False
            ]
        }
    if filter_data_en and filter_data_zh:
        # 创建合并后的 JSON 对象
        merged_json = {
            "id": filter_data_en["id"],
            "name": filter_data_zh["name"],  # 使用中文名称
            "name_en": filter_data_en["name"],
            "skins": []
        }

        # 合并皮肤，通过 uncenteredSplashPath 匹配
        for skin2 in filter_data_zh["skins"]:
            # 查找 json1 中对应的皮肤
            skin1 = next((s for s in filter_data_en["skins"] if s["uncenteredSplashPath"] == skin2["uncenteredSplashPath"]),
                         None)
            if skin1:
                # 复制中文皮肤数据并添加英文名称
                merged_skin = skin2.copy()
                merged_skin["name_en"] = skin1["name"]  # 添加英文名称
                merged_json["skins"].append(merged_skin)

        #print(json.dumps(merged_json, indent=2, ensure_ascii=False))

        with open(f'{skin_json_dir}/{id}.json', 'w', encoding='utf-8') as f:
            json.dump(merged_json, f, ensure_ascii=False, indent=4)



if not os.path.exists(skin_json_dir):
    os.makedirs(skin_json_dir)

with open(champions_json_path,'r',encoding='utf-8') as f:
    champions_data = json.load(f)
    for champion_data in champions_data:
        parse_skin_json(champion_data['id'])
        print(f'{champion_data['name']}：数据处理完毕')
