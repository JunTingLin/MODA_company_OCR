import re

def numerical_sort(filename):
    """提取文件名中的數字用於排序，先根據文件名前半部分，然後是頁碼"""
    name_part, page_number = re.match(r'(.*_page_)(\d+)', filename).groups()
    return (name_part, int(page_number))
