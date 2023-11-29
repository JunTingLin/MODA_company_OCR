import os
from ocr import detect_text_from_picture
from text_extraction import extract_info, extract_unified_number

def save_to_file(info, file_name):
    """將提取的信息追加到文件"""
    with open(file_name, 'a', encoding='utf-8') as file:  # 使用 'a' 模式來追加數據
        for key, value in info.items():
            file.write(f'{key},{value}\n')
        file.write('\n')  # 在每個條目之間添加一個空行

def process_directory(directory_path):
    """處理指定文件夾內的所有圖片"""
    last_unified_number = None
    combined_text = ""
    combined_filenames = ""
    files = sorted(os.listdir(directory_path))  # 對文件進行排序，確保順序

    for filename in files:
        print(f'Processing {filename}...')
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(directory_path, filename)
            text_detected = detect_text_from_picture(file_path)
            current_unified_number = extract_unified_number(text_detected)

            if current_unified_number == last_unified_number or not current_unified_number:
                combined_text += text_detected + '\n'
                combined_filenames += filename + ","
            else:
                if combined_text:
                    extracted_info = extract_info(combined_text, combined_filenames.rstrip(','))
                    save_to_file(extracted_info, 'output.txt')
                combined_text = text_detected + '\n'
                combined_filenames = filename + ","

            last_unified_number = current_unified_number or last_unified_number

    # 處理最後一組文本
    if combined_text:
        extracted_info = extract_info(combined_text, combined_filenames.rstrip(','))
        save_to_file(extracted_info, 'output.txt')


def main():
    directory_path = 'data'  # 替換為您的資料夾路徑
    open('output.txt', 'w').close()  # 清空先前的 output.txt 文件
    process_directory(directory_path)

if __name__ == "__main__":
    main()
