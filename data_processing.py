import json
import csv


def save_to_json(data, file_name):
    """將提取的信息以 JSON 格式保存"""
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def load_business_code_mapping(csv_file):
    """從 CSV 檔案載入營業項目代碼和中文名稱的映射"""
    mapping = {}
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # 跳過標題行
        for row in reader:
            code, description = row
            mapping[code.strip()] = description.strip()
    return mapping

def add_business_description_to_data(json_data, mapping):
    """向 JSON 数据添加營業項目的中文描述"""
    for entry in json_data:
        if entry.get("表格類型") == "基本資料表":
            codes = entry.get("所營事業資料", "").split(',')
            descriptions = [mapping.get(code, "Not found") for code in codes]
            entry["營業項目"] = ','.join(descriptions)
    return json_data

