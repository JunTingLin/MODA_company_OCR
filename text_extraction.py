import re

def extract_info(text):
    """從文字中提取關鍵信息"""
    info = {}
    unified_number_pattern = r"\b\d{8}\b"  # 8個連續數字
    company_name_pattern = r"[^\n]+公司\n"  # 以「公司」結尾的字串
    business_data_pattern = r"\b[A-Za-z][0-9]{6}\b"  # 以英文字母開頭，後面接6個數字
    
    unified_number = re.search(unified_number_pattern, text)
    company_name = re.search(company_name_pattern, text)
    business_data = re.findall(business_data_pattern, text)

    info['統一編號'] = unified_number.group() if unified_number else 'Not match'
    info['公司名稱'] = company_name.group().strip() if company_name else 'Not match'
    info['所營事業資料'] = ','.join(business_data) if business_data else 'Not match'

    return info
