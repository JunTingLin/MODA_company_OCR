import os
import re
from collections import defaultdict
from ocr import detect_text_from_picture
from text_extraction import extract_info

def save_to_file(info, file_name):
    """將提取的信息追加到文件"""
    with open(file_name, 'a', encoding='utf-8') as file:
        for key, value in info.items():
            file.write(f'{key},{value}\n')
        file.write('\n')

def process_grouped_files(files, output_file):
    """處理分組的文件並提取信息"""
    combined_text = ''
    for file_path in files:
        print(f'Processing {file_path}...')
        combined_text += detect_text_from_picture(file_path) + '\n'
    extracted_info = extract_info(combined_text)
    save_to_file(extracted_info, output_file)

def main():
    directory_path = 'data'  # 替換為您的資料夾路徑
    file_groups = defaultdict(list)

    # 根據文件名分組文件
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            group_id = re.match(r'(基本資料_\d+)', filename)
            if group_id:
                file_groups[group_id.group()].append(os.path.join(directory_path, filename))

    open('output.txt', 'w').close()  # 清空先前的 output.txt 文件

    # 處理每一組文件
    for group_files in file_groups.values():
        process_grouped_files(group_files, 'output.txt')

if __name__ == "__main__":
    main()
