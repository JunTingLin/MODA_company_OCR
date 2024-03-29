import re
from data_processing import load_unique_names

def extract_info(text,filenames):
    """從文字中提取關鍵信"""
    info = {}

    if "基本資料" in text and "商工登記公示資料查詢服務" in text:
        info['code'] = '01'
        info['filename'] = filenames
        info['ocr_data'] = text
        info['table'] = '基本資料表'
        info['ocr_cid'] = extract_unified_number(text)
        info['company_name'] = extract_company_name(text)
        info['boss_name'] = extract_representative_person_name(text)
        info['business_code'] = extract_business_data(text)
    elif "401" in text and ("營業人銷售額與稅額申報書清單" in text or "營業人銷售額與稅額申報書" in text):
        info['code'] = '02'
        info['filename'] = filenames
        info['ocr_data'] = text
        info['table'] = '納稅證明'
        info['ocr_cid'] = extract_unified_number(text)
        info['company_name'] = extract_company_name(text)
        info['boss_name'] = extract_responsible_person_name(text)
        info['date'] = extract_401_403_year_month(text)
        info['stamp'] = 'true' if "營業稅網路申報收件章" in text else 'false'
    elif "403" and "營業人銷售額與稅額申報書" in text:
        info['code'] = '02'
        info['filename'] = filenames
        info['ocr_data'] = text
        info['table'] = '納稅證明'
        info['ocr_cid'] = extract_unified_number(text)
        info['company_name'] = extract_company_name(text)
        info['boss_name'] = extract_responsible_person_name(text)
        info['date'] = extract_401_403_year_month(text)
        info['stamp'] = 'true' if "營業稅網路申報收件章" in text else 'false'
    elif "數位發展部數位產業署投標廠商聲明書" in text:
        info['code'] = '03'
        info['filename'] = filenames
        info['ocr_data'] = text
        info['table'] = '投標廠商聲明書'
        info['ocr_cid'] = extract_unified_number(text)
    elif ("bank" in text.lower() and "銀行" in text) or ("郵政匯票" in text):
        info['code'] = '04'
        info['filename'] = filenames
        info['ocr_data'] = text
        info['table'] = '支票'
        info['name'] = extract_payee_name(text)
        info['bank1'] = extract_bank_name(text)
        info['bank2'] = extract_branch_name(text)
        info['money'] = extract_amount(text)
        info['date'] = extract_check_date(text)
        info['serial'] = extract_serial(text)
    else:
        info['code'] = '00'
        info['filename'] = filenames
        info['ocr_data'] = text
        info['table'] = 'undefined'

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


def extract_401_403_year_month(text):
    """
    從文本中提取“年份月份”並轉換為公元格式

    :param text: 包含年月份的文本
    :return: 提取到的西元年月份
    """
    year_month_pattern = r"所屬年月份:\s*(\d{3})\s*年\s*(\d{2})"
    match = re.search(year_month_pattern, text)
    if match:
        year, month = match.groups()
        year = int(year) + 1911  # 將民國年轉換為西元年
        return f"{year}/{month}/01"
    else:
        return 'Not match'
    

def extract_bank_name(text):
    bank_names = load_unique_names('金融機構名稱')
    bank_names = clean_and_expand_bank_names(bank_names)
    for bank_name in bank_names:
        if bank_name in text:
            return bank_name
    return 'Not match'

def extract_branch_name(text):
    branch_names = load_unique_names('分支機構名稱')
    for branch_name in branch_names:
        if branch_name in text:
            return branch_name
    return 'Not match'

def clean_and_expand_bank_names(bank_names):
    cleaned_names = set()
    for name in bank_names:
        # 移除全形括號及其中的內容
        name = re.sub(r'（.*?）', '', name)
        # 只保留以「銀行」結尾的名稱
        if name.endswith('銀行'):
            cleaned_names.add(name)
            # 如果名称中包含「商業」，添加去除「商業」的版本
            if '商業' in name:
                cleaned_name = name.replace('商業', '')
                cleaned_names.add(cleaned_name)
    # 添加「郵政匯票」
    cleaned_names.add('郵政匯票')

    return cleaned_names

def extract_payee_name(text):
    if '數位發展部數位產業署' in text:
        return '數位發展部數位產業署'

    # 確保只匹配「憑票支付」之後直到第一個換行符之前的內容
    payee_pattern = r"憑票支付[^\S\n]*([^\n]+)"
    payee_match = re.search(payee_pattern, text)
    
    return payee_match.group(1) if payee_match else 'Not match'

def extract_amount(text):
    # 使用正規表示式來匹配至少包含一個逗號的金額格式
    amount_pattern = r"\d{1,3},\d{3}(,\d{3})*"
    amount_match = re.search(amount_pattern, text)
    
    return amount_match.group() if amount_match else 'Not match'

def extract_check_date(text):
    date_pattern = r"(\d{2,3}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)"
    date_match = re.search(date_pattern, text)
    
    if date_match:
        check_date = date_match.group(0)  # 獲取匹配的完整民國日期
        # 標準化日期，移除不必要的空格
        normalized_date = re.sub(r"\s+", "", check_date)
        return normalized_date
    return 'Not match'

def extract_serial(text):
    # 匹配英文字母開頭，數字結尾的序列，直到遇到換行符為止
    pattern_alpha_numeric = r'[A-Za-z]{1,3}\s*\d{4,}'
    match_alpha_numeric = re.search(pattern_alpha_numeric, text)
    
    if match_alpha_numeric:
        return match_alpha_numeric.group(0).replace(" ", "")  # 移除匹配結果中的空格
    
    # 如果上面的模式沒有匹配到，嘗試匹配一串連續數字，直到遇到\n為止
    pattern_numeric = r'\d{9,}(?=[^\n])'
    match_numeric = re.search(pattern_numeric, text)
    
    if match_numeric:
        return match_numeric.group(0)
    
    return 'Not match'


if __name__ == "__main__":
    result =extract_bank_name('')

