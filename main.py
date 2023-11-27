from ocr import detect_text
from text_extraction import extract_info

def save_to_file(info, file_name):
    """將提取的信息保存到文件"""
    with open(file_name, 'w', encoding='utf-8') as file:
        for key, value in info.items():
            file.write(f'{key},{value}\n')

def read_from_file(file_name):
    """從文件中讀取内容並返回字符串"""
    with open(file_name, 'r', encoding='utf-8') as file:
        return file.read()

def main():
    # 主程序邏輯
    # text_detected = detect_text('data\基本資料_16325089.jpg')
    text_detected = read_from_file('old.txt')
    extracted_info = extract_info(text_detected)
    save_to_file(extracted_info, 'output.txt')

if __name__ == "__main__":
    main()
