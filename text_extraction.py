import re

def extract_info(text,filename):
    """從文字中提取關鍵信"""
    info = {}
    unified_number_pattern = r"\b\d{8}\b"  # 8個連續數字
    company_name_pattern = r"[^\n]+公司\b"  # 以「公司」结尾的字符串
    business_data_pattern = r"\b[A-Za-z][0-9]{6}\b"  # 以英文字母開頭，後面接6個數字

    unified_number = re.search(unified_number_pattern, text)
    company_name_match = re.search(company_name_pattern, text)
    business_data = re.findall(business_data_pattern, text)

    info['檔名'] = filename  # 添加文件名到信息中
    if "基本資料" in text:
        info['表格類型'] = '基本資料表'
        info['統一編號'] = unified_number.group() if unified_number else 'Not match'
        info['公司名稱'] = company_name_match.group().strip() if company_name_match else 'Not match'
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
    elif "403" in text:
        info['表格類型'] = '403表'
        info['統一編號'] = unified_number.group() if unified_number else 'Not match'
        if company_name_match:
            company_name_segment = company_name_match.group()
            company_name = company_name_segment.split()[-1]
            info['營業人名稱'] = company_name
        else:
            info['營業人名稱'] = 'Not match'

    return info

def extract_unified_number(text):
    """提取統一編"""
    unified_number_pattern = r"\b\d{8}\b"
    match = re.search(unified_number_pattern, text)
    return match.group() if match else None
