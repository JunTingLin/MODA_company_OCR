import json


def save_to_json(data, file_name):
    """將提取的信息以 JSON 格式保存"""
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)