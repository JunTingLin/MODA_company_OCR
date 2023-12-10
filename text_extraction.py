import re

def extract_info(text,filename):
    """從文字中提取關鍵信"""
    info = {}
    unified_number_pattern = r"\b\d{8}\b"  # 8個連續數字
    company_name_pattern = r"[^\n]+公司\b"  # 以「公司」结尾的字符串
    representative_pattern = r"\d+\n(.+?)\n(?:新北|臺北|桃園|臺中|臺南|高雄|基隆|新竹|嘉義|苗栗|彰化|南投|雲林|屏東|宜蘭|花蓮|臺東|澎湖|金門|連江)" # 以縣市名稱結尾的字符串
    business_data_pattern = r"\b[A-Za-z][0-9]{6}\b"  # 以英文字母開頭，後面接6個數字

    unified_number = re.search(unified_number_pattern, text)
    company_name_match = re.search(company_name_pattern, text)
    representative_match = re.search(representative_pattern, text)
    business_data = re.findall(business_data_pattern, text)

    info['檔名'] = filename  # 加檔名到資訊中

    if "投標廠商聲明書" in text:
        info['表格類型'] = '投標廠商聲明書'
        info['統一編號'] = unified_number.group() if unified_number else 'Not match'
    elif "基本資料" in text:
        info['表格類型'] = '基本資料表'
        info['統一編號'] = unified_number.group() if unified_number else 'Not match'
        info['公司名稱'] = company_name_match.group().strip() if company_name_match else 'Not match'
        info['代表人姓名'] = representative_match.group(1).strip() if representative_match else 'Not match'
        info['所營事業資料'] = ','.join(business_data) if business_data else 'Not match'
    elif "401" in text:
        info['表格類型'] = '401表'
        info['統一編號'] = unified_number.group() if unified_number else 'Not match'
        # 僅對401表，提取公司名稱的特殊邏輯
        if company_name_match:
            company_name_segment = company_name_match.group()
            company_name = company_name_segment.split()[-1]
            info['營業人名稱'] = company_name
        else:
            info['營業人名稱'] = 'Not match'
        # 使用 extract_responsible_person_name 函數提取負責人姓名
        info['負責人姓名'] = extract_responsible_person_name(text)
    elif "403" in text:
        info['表格類型'] = '403表'
        info['統一編號'] = unified_number.group() if unified_number else 'Not match'
        if company_name_match:
            company_name_segment = company_name_match.group()
            company_name = company_name_segment.split()[-1]
            info['營業人名稱'] = company_name
        else:
            info['營業人名稱'] = 'Not match'
        # 使用 extract_responsible_person_name 函數提取負責人姓名
        info['負責人姓名'] = extract_responsible_person_name(text)

    return info

def extract_responsible_person_name(text):
    # 第一種正則表達式
    responsible_person_pattern_1 = r"負責人姓?\s*名?\s+(.+)\n" 
    # 第二種正則表達式
    responsible_person_pattern_2 = r"\b\d{9}\b\n(.+)"
    
    # 嘗試使用第一種正則表達式
    responsible_person_match = re.search(responsible_person_pattern_1, text)
    if responsible_person_match and is_valid_name(responsible_person_match.group(1).strip()):
        return responsible_person_match.group(1).strip()
    
    # 如果第一種正則表達式無效，嘗試第二種
    responsible_person_match = re.search(responsible_person_pattern_2, text)
    if responsible_person_match and is_valid_name(responsible_person_match.group(1).strip()):
        return responsible_person_match.group(1).strip()
    
    return 'Not match'

def is_valid_name(name):
    # 檢查是否為中文姓名
    if all(u'\u4e00' <= c <= u'\u9fff' for c in name):
        return len(name) >= 2 and len(name) <= 3
    
    # 檢查是否為英文姓名
    # 假設英文姓名由字母、空格和可能的分隔符組成
    elif re.match(r"^[A-Za-z\s,.'-]+$", name):
        # 可以在這裡添加更多關於英文姓名的檢查條件
        return True

    return False

def extract_unified_number(text):
    """提取統一編"""
    unified_number_pattern = r"\b\d{8}\b"
    match = re.search(unified_number_pattern, text)
    return match.group() if match else None
