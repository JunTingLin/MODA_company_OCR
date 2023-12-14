import re

def numerical_sort(filename):
    """提取檔案名稱中的數字用於排序"""
    numbers = re.findall(r'\d+', filename)
    return int(numbers[0]) if numbers else 0
