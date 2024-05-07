import re
from data_processing import load_unique_names
from datetime import datetime

def extract_info(text,filenames):
    """從文字中提取關鍵信"""
    info = {}

    if "基本資料" in text and "登記公示資料查詢服務" in text:
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
    elif 'ISO' in text and '27001' in text:
        info['code'] = '05'
        info['filename'] = filenames
        info['ocr_data'] = text
        info['table'] = 'ISO27001'
        info['company_name'] = extract_english_company_name(text)
        # info['compare'] = ''
        info['expiry_date'] = extract_27001_valid_date(text)
    elif '電腦軟體投標廠商報價單' in text:
        info['code'] = '06'
        info['filename'] = filenames
        info['ocr_data'] = text
        info['table'] = '報價單'
        info['ocr_cid'] = extract_unified_number(text)
        info['company_name'] = extract_company_name(text)
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
        company_name = company_name\
            .replace("營業名稱", "")\
            .replace("營業人名稱", "")\
            .replace("營業人名 稱", "")\
            .replace("廠商名稱","")\
            .replace(":","")\
            .strip()
        return company_name
    else:
        return 'Not match'
    
import re

def extract_english_company_name(text):
    # 分別匹配 "Corporation"、"LLC"、"LTD"、"INC"
    company_types = ["Corporation", "LLC", "LTD", "INC"]
    for company_type in company_types:
        # \b 是單詞邊界，[^\n]*? 代表非貪婪匹配任意字符直到換行
        pattern = r"[^\n]*?\b" + company_type + r"\b[^\n]*"
        match = re.search(pattern, text, re.IGNORECASE)  # 不區分大小寫
        if match:
            # 去除結果中可能的多餘空格
            company_name = " ".join(match.group(0).strip().split())
            return company_name
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
    # 對分行名稱按長度進行降序排序
    sorted_branch_names = sorted(branch_names, key=len, reverse=True)
    for branch_name in sorted_branch_names:
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
    # 定義兩種金額的匹配模式
    patterns = [
        r"\d{1,3},\d{3}(,\d{3})*",  # 使用逗號分隔的金額格式
        r"\d{1,3}\.\d{3}(\.\d{3})*"  # 使用點分隔的金額格式
    ]

    for pattern in patterns:
        amount_match = re.search(pattern, text)
        if amount_match:
            # 移除匹配到的金額中的分隔符號，無論是逗號還是點
            return amount_match.group().replace(',', '').replace('.', '')

    # 如果兩種模式都沒有匹配成功，返回'Not match'
    return 'Not match'

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
    pattern_alpha_numeric = r'[A-Za-z]{1,3} *\d{4,}'
    match_alpha_numeric = re.search(pattern_alpha_numeric, text)
    
    if match_alpha_numeric:
        return match_alpha_numeric.group(0).replace(" ", "")  # 移除匹配結果中的空格
    
    # 如果上面的模式沒有匹配到，嘗試匹配一串連續數字，直到遇到\n為止
    pattern_numeric = r'\d{9,}(?=[^\n])'
    match_numeric = re.search(pattern_numeric, text)
    
    if match_numeric:
        return match_numeric.group(0)
    
    return 'Not match'

def extract_27001_valid_date(text):
    # BSI
    expiry_date_bsi = re.search(r"Expiry Date: (\d{4}-\d{2}-\d{2})", text)
    if expiry_date_bsi:
        return datetime.strptime(expiry_date_bsi.group(1), "%Y-%m-%d").strftime("%Y/%m/%d")

    # EY
    expiry_date_ey = re.search(r"Expiration date of certificate: (\w+ \d{1,2}, \d{4})", text)
    if expiry_date_ey:
        return datetime.strptime(expiry_date_ey.group(1), "%B %d, %Y").strftime("%Y/%m/%d")
    
    # Schellman
    expiry_date_schellman = re.search(r"Expiration Date\n(\w+ \d{1,2}, \d{4})", text)
    if expiry_date_schellman:
        return datetime.strptime(expiry_date_schellman.group(1), "%B %d, %Y").strftime("%Y/%m/%d")
    
    # AFNOR
    expiry_date_afnor = re.search(r"jusqu'au\n(\d{4}-\d{2}-\d{2})", text)
    if expiry_date_afnor:
        return datetime.strptime(expiry_date_afnor.group(1), "%Y-%m-%d").strftime("%Y/%m/%d")
    
    # TUV
    expiry_date_tuv = re.search(r"證書有效期至(\d{4}-\d{2}-\d{2})", text)
    if expiry_date_tuv:
        return datetime.strptime(expiry_date_tuv.group(1), "%Y-%m-%d").strftime("%Y/%m/%d")
    
    # SGS
    expiry_date_sgs = re.search(r"until (\d{1,2} \w+ \d{4})", text)
    if expiry_date_sgs:
        return datetime.strptime(expiry_date_sgs.group(1), "%d %B %Y").strftime("%Y/%m/%d")

    return 'Not match'
    


if __name__ == "__main__":
    result1 = extract_amount("Bar\nation\n本行支票\nal Ba\nerno\nshin 10\nak Tais\nal Bank\national\nntern\nshin\nak Tag\nal Bay\nationa\nntern\nshin I\nk Tais\nBanke\nona\nnational Bank Talshin International Bank\nInternational Bank Taishin International\naishin International Bank Taishin Interna\nank Taishin International Bank Taishin i\nPal Bank Taishin International Bank Talehi\n支\nnationa\nS\n示\nional Bank Taishin International Bank\nrnational Bank Talshin International\nnternational Bank Taishin Interna\nhin International Bank\nOk Tairin Internatio\nnal Bar Taish 票\n支付\nnation PAY TO THE ORDER OF.\nnterne\nshin Iternational\nTan Intern\n數位發展部數位產業署\n幣\nBa\nBNEW TAIWAN DOLLARS.\nation\nternational Bank\nhin\nhal Ban\nnation\nnterna\nNT$ 500,000\n伍拾萬元整\n台新國際商業銀行\nShunt Taighin International Bank BAR\nk -\nal Bank\national Ba\nDal Bank Tais\nVernational Bank Taishin International Bank Tals\nin International Bank Taishin International Bank\nnternationak Taishin International Bank Taishin Internation\nshin International Bank Taishin International Bank Taishin Inters\nk Taishin International Bank Taishin International Bank Taishin\nal Bank Taishin Internation\nishin International Bank\national Bank Taishin International Bank pohime\n帳號\nA/C NO\n支票號碼\nCHECK NO..\n期\nional Bank Taishin Intern\n230200100 tonal Bank ishin\nTT0746839\n年\n月\n日\n13 Day\nDATE 112 Year 03Month\ntional Bank Tall\national Bank Talshin\nthin\nBer\nnation\nnation\n驗 印\nin Intern\nTeishin\nnational Bank Tal\nInternational Bar\nsational Bank Taishin Intern\nnational Bank Talehin\nalshin International Bank Tal\nBank Tel\n經辦\nonal Ban\nernation\nBank Taishin Intern\nsational Bank Talshin\nIshin International Bank Tal\nTaishin International Ban\nBank Talehin Internation\nInternational nk Talehin Intern\ntional Bank Taishin Inter 覆核\nonal Bank\nTaishin\nBand Tal\nTaishin International Bar\nonal Bank Taishin Internation\nnational Bank Taishin Intern\nAUTHORIZED SIGNATURE Taishin International Bank Taishin\nTaishin International Bank Ta\n此致 To\n台照\n禁止背書轉讓\n台新國際商業銀行基隆路分行\n* fest\n⑈0746839⑈⑆018120735⑆04 ⑈230200100⑈")
    result2 = extract_amount("Bank\nRukong Bank Shih Kong Bank Shin Kong Bank Shin Kong Bank Shin Kong Bank Shin Kongank\n00277399999992\n帳\nKong Bank Shin Kong Bank Shin Kong Bank Shin 中華民國112年03月29日\n支票號碼 0498442\nn Ko\n08\n多市分\n驗印\nong Bank Shin Kong Bank Shin Kong Bank Shin Kong Bank Shin Kong Bank Shin Kong Bank\n憑票支付 數位發展部數位產業署\n行\nng Bank Shih Kong Bank\nKong Bank Shin Kong Bank Shin Kong Bank Shin Korzank\n光\n新台幣伍拾萬元整\nBank Shin\nNT$\nng Bank $500.000 Bank Shin Kong Bank Shin Kong Bank\nShin Konank\n會計\n此致\n新光金控\n|新光銀行 竹科分行 Kong Bank Shic\n臺灣新光商業銀行竹科分行\nMKng 付款行代號:08-103-0277\n科目:(借)本行支票\n付款地:新竹市光復路一段333號\nBank Shin Kong Bank S\n發理\n劉素萍\ntrong Bank\n主管\nnong Bank\n(貸)")
    result3 = extract_amount('發票日:中華民國113年4月 10日\n郵政匯票\n匯票號碼:1176000916-9\n憑票支付數位發展部數位產業署\n新臺幣伍萬元整\n11760009169\nNT$\n$50.000.00\n備註:\n禁止背書轉讓\n兌款局戳記\n印\n一、本匯票可於各地郵局兌領。\n二、本匯票務請用掛號向窗口交寄。\n三、請查對匯款金額及抬頭是否相符,並請詳閱背面\n注意事項。\n四、本郵政匯票可由全國票據交換所交換。\n證\n欄\n113. 4. 10\n發票員蓋章\n米米米米米\n主管員蓋章\n匯款局郵戳\n002127\n⑈6000916⑈⑆017010011⑆41 * 700000000\"\n主管:\n257')
    print(result2)

