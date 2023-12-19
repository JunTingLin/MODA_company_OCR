import re

def numerical_sort(filename):
    """提取文件名中的數字用於排序。對於包含 '_page_' 的文件，先根據文件名前半部分，然後是頁碼排序；對於不包含 '_page_' 的文件，則根據原始檔名排序。"""
    if '_page_' in filename:
        name_part, page_number = re.match(r'(.*_page_)(\d+)', filename).groups()
        return (name_part, int(page_number))
    else:
        return (filename, 0)

