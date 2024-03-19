import re

def extract_info(text,filenames):
    """從文字中提取關鍵信"""
    info = {}
    info['檔名'] = filenames  # 加檔名到資訊中
    info['OCR文字'] = text  # 加入 OCR 辨識結果

    if "數位發展部數位產業署投標廠商聲明書" in text:
        info['表格類型'] = '投標廠商聲明書'
        info['統一編號'] = extract_unified_number(text)
    elif "基本資料" in text and "商工登記公示資料查詢服務" in text:
        info['表格類型'] = '基本資料表'
        info['統一編號'] = extract_unified_number(text)
        info['公司名稱'] = extract_company_name(text)
        info['代表人姓名'] = extract_representative_person_name(text)
        info['所營事業資料'] = extract_business_data(text)
    elif "401" in text and ("營業人銷售額與稅額申報書清單" in text or "營業人銷售額與稅額申報書" in text):
        info['表格類型'] = '401表'
        info['統一編號'] = extract_unified_number(text)
        info['營業人名稱'] = extract_company_name(text)
        info['負責人姓名'] = extract_responsible_person_name(text)
        info['營業稅網路申報收件章'] = '是' if "營業稅網路申報收件章" in text else '否'
        if info['營業稅網路申報收件章'] == '是':
            info['蓋章日期'] = extract_stamp_date(text)
    elif "403" and "營業人銷售額與稅額申報書" in text:
        info['表格類型'] = '403表'
        info['統一編號'] = extract_unified_number(text)
        info['營業人名稱'] = extract_company_name(text)
        info['負責人姓名'] = extract_responsible_person_name(text)
        info['營業稅網路申報收件章'] = '是' if "營業稅網路申報收件章" in text else '否'
        if info['營業稅網路申報收件章'] == '是':
            info['蓋章日期'] = extract_stamp_date(text)
    else:
        pass

    return info

def extract_unified_number(text):
    """提取統一編"""
    # 第一種正則表達式: (?<!\d) 表示「不在數字前」，確保匹配的8位數字前面不是其他數字
    unified_number_pattern_1 = r"(?<!\d)\d{8}(?=\n)"
    # 第二種正則表達式: (?!\d) 表示「不在數字後」，確保匹配的8位數字後面不是其他數字
    unified_number_pattern_2 = r"(?<=\n)\d{8}(?!\d)"
    
    # 嘗試使用第一種正則表達式
    unified_number_match = re.search(unified_number_pattern_1, text)
    if unified_number_match:
        return unified_number_match.group().strip()

    # 如果第一種正則表達式無效，嘗試第二種
    unified_number_match = re.search(unified_number_pattern_2, text)
    if unified_number_match:
        return unified_number_match.group().strip()

    return 'Not match'

def extract_company_name(text):
    company_name_pattern = r"[^\w]*(.*?公司)\b"  # 以「公司」结尾的字符串
    company_name_match = re.search(company_name_pattern, text)
    if company_name_match:
        company_name = company_name_match.group(1).strip()
        company_name = company_name.replace("營業名稱", "").replace("營業人名稱", "").strip()
        return company_name
    else:
        return 'Not match'

def extract_business_data(text):
    business_data_pattern = r"\b[A-Za-z][0-9]{6}\b"  # 以英文字母開頭，後面接6個數字
    business_data_match = re.findall(business_data_pattern, text)
    return ','.join(business_data_match) if business_data_match else 'Not match'

def extract_representative_person_name(text):
    # 第一種正則表達式: # 以縣市名稱結尾的字符串
    responsible_person_pattern_1 = r"\n(.+?)\n(?:新北|臺北|桃園|臺中|臺南|高雄|基隆|新竹|嘉義|苗栗|彰化|南投|雲林|屏東|宜蘭|花蓮|臺東|澎湖|金門|連江)" # 以縣市名稱結尾的字符串
    # 第二種正則表達式：匹配「代表人姓名\n」後的姓名
    responsible_person_pattern_2 = r"代表人姓名\n(.+?)\n"

    # 嘗試使用第一種正則表達式
    responsible_person_match = re.search(responsible_person_pattern_1, text)
    if responsible_person_match and is_valid_name(responsible_person_match.group(1).strip()):
        return responsible_person_match.group(1).strip()

    # 如果第一種正則表達式無效，嘗試第二種
    responsible_person_match = re.search(responsible_person_pattern_2, text)
    if responsible_person_match and is_valid_name(responsible_person_match.group(1).strip()):
        return responsible_person_match.group(1).strip()

    return 'Not match'



def extract_responsible_person_name(text):
    # 第一種正則表達式
    responsible_person_pattern_1 = r"負責人姓?\s*名?\s+(.+)\n" 
    # 第二種正則表達式
    responsible_person_pattern_2 = r"\b\d{9}\b\n(.+)"
    # 第三種正則表達式
    responsible_person_pattern_3 = r"負責人姓名([^\n]+)"
    
    # 嘗試使用第一種正則表達式
    responsible_person_match = re.search(responsible_person_pattern_1, text)
    if responsible_person_match and is_valid_name(responsible_person_match.group(1).strip()):
        return responsible_person_match.group(1).strip()
    
    # 如果第一種正則表達式無效，嘗試第二種
    responsible_person_match = re.search(responsible_person_pattern_2, text)
    if responsible_person_match and is_valid_name(responsible_person_match.group(1).strip()):
        return responsible_person_match.group(1).strip()
    
    responsible_person_match = re.search(responsible_person_pattern_3, text)
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


def extract_stamp_date(text):
    """
    從文本中提取「蓋章日期」。

    :param text: 包含日期的文本
    :return: 提取到的日期或者「日期未匹配」
    """
    # 修改後的日期正則表達式，考慮了日期元素之間可能存在的空格
    date_pattern = r"\d{3}\s*\.\s*\d{2}\s*\.\s*\d{2}"
    date_match = re.search(date_pattern, text)
    return date_match.group(0) if date_match else '日期未匹配'


if __name__ == "__main__":
    text = ""
    info = extract_info(text, 'filename')
    import data_processing
    data_processing.save_to_json(info, 'debug.json')
