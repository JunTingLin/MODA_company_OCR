import json
import csv
import requests
from checkbox_detector import is_checked
import os
import pandas as pd


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

def load_unique_names(column_name, csv_file='R2_Location.csv'):
    """
    根據列名從 CSV 檔案中提取唯一的名稱集合。

    :param column_name: 需要提取的列名，例如 '金融機構名稱' 或 '分支機構名稱'
    :return: 一個包含唯一名稱的集合
    """
    df = pd.read_csv(csv_file)
    # 指定提取列的數據，並將其轉換為集合去重覆
    unique_names = set(df[column_name].dropna().unique())
    return unique_names

def add_business_description_to_data(json_data, mapping):
    """向 JSON 数据添加營業項目的中文描述"""
    for entry in json_data:
        if entry.get("table") == "基本資料表":
            codes = entry.get("business_code", "").split(',')
            descriptions = [mapping.get(code, "Not found") for code in codes]
            entry["business_name"] = ','.join(descriptions)
    return json_data

def add_checkbox_status_to_data(json_data, directory_path):
    """向 JSON 數據添加勾選狀況"""
    for entry in json_data:
        if entry.get("table") == "投標廠商聲明書":
            entry["check"] = is_checked(os.path.join(directory_path, entry["filename"][0])) # 僅第一頁
    return json_data


def generate_summary(input_json_path):
    with open(input_json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    company_summary = {}

    for entry in data:
        # 投標廠商聲明書不納入統計
        if entry.get("table") == "投標廠商聲明書":
            continue

        # 獲取每筆資料的統一編號
        unified_number = entry.get("ocr_cid")
        # 跳過統一編號為 None 或無效的記錄
        if (not unified_number) or  (unified_number == "Not match") or (len(unified_number) != 8):
            continue
        # 獲取每筆資料的公司名稱，如果都沒有找到則預設為 "Not match"
        company_name = entry.get("company_name").strip()
        # 獲取每筆資料的負責人姓名，如果沒有找到則預設為 "Not match"
        representative_name = entry.get("boss_name").strip()

        # 檢查統一編號是否已經存在於摘要字典中
        if unified_number not in company_summary:
            # 如果不存在，則新增一個新的摘要記錄
            company_summary[unified_number] = {
                "ocr_cid": unified_number,
                "company_name": company_name,
                "boss_name": representative_name,
                "allMatch": True  # 設定一個標誌，表示目前為止名稱與編號是匹配的
            }
        else:
            # 如果該統一編號已存在，檢查名稱是否與已儲存的名稱相符
            if company_summary[unified_number]["company_name"] != company_name or company_name == "Not match":
                # 如果不匹配，將 allMatch 標誌設為 False
                company_summary[unified_number]["allMatch"] = False
            # 檢查負責人姓名是否與已儲存的姓名相符
            if company_summary[unified_number]["boss_name"] != representative_name or representative_name == "Not match":
                # 如果不匹配，將 allMatch 標誌設為 False
                company_summary[unified_number]["allMatch"] = False
            

    # 將摘要字典轉換成列表並返回
    return list(company_summary.values())


def check_api_data(summary_data, update_progress=None, update_status=None):
    for i, item in enumerate(summary_data):
        unified_number = item['ocr_cid']

        # 如果統一編號為None，則跳過當前迭代
        if unified_number is None:
            continue

        print(f"正在比對 {unified_number} 公司的資料是否相符...")
        if update_progress and update_status:
            update_status.emit(f"正在比對 {unified_number} 公司的資料是否相符...")
            current_progress = (i + 1) * 100 // len(summary_data)
            update_progress.emit(current_progress)

        response = requests.get(f"https://data.gcis.nat.gov.tw/od/data/api/5F64D864-61CB-4D0D-8AD9-492047CC1EA6?$format=json&$filter=Business_Accounting_NO eq {unified_number}&$skip=0&$top=1")
        # 如果回傳狀態碼為200且回傳內容不為空
        if response.status_code == 200 and response.content.strip():
            try:
                api_data = response.json()
                item["api"] = api_data  # 將 API 回傳的 JSON 資料加入

                api_company_name = api_data[0]['Company_Name'] if api_data else 'Not match'
                api_responsible_name = api_data[0]['Responsible_Name'] if api_data else 'Not match'
                
                # 比對公司名稱
                if api_company_name == 'Not match' or item["company_name"] != api_company_name:
                    item["company_name"] = api_company_name
                    item["allMatch"] = False
        
                # 比對負責人姓名
                if api_responsible_name == 'Not match' or item["boss_name"] != api_responsible_name:
                    item["boss_name"] = api_responsible_name
                    item["allMatch"] = False
            except json.JSONDecodeError:
                item["api"] = "Error in API response"
                item["allMatch"] = False
        else:
            item["api"] = "No data available"
            item["allMatch"] = False

    return summary_data
