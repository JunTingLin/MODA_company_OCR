import os
from ocr import detect_text_from_picture
from text_extraction import extract_info

def save_to_file(info, file_name):
    """將提取的信息追加到文件"""
    with open(file_name, 'a', encoding='utf-8') as file:  # 使用 'a' 模式來追加數據
        for key, value in info.items():
            file.write(f'{key},{value}\n')
        file.write('\n')  # 在每個條目之間添加一個空行

def process_directory(directory_path):
    """處理指定資料夾內的所有圖片"""
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # 檢查是否是圖片文件
            file_path = os.path.join(directory_path, filename)
            text_detected = detect_text_from_picture(file_path)
            extracted_info = extract_info(text_detected)
            save_to_file(extracted_info, 'output.txt')

def main():
    directory_path = 'data'  # 替換為您的資料夾路徑
    open('output.txt', 'w').close()  # 清空先前的 output.txt 文件
    process_directory(directory_path)

if __name__ == "__main__":
    main()
