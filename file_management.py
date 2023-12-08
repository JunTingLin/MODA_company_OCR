import os
import shutil # 用於刪除資料夾
import json
import re
from ocr import detect_text_from_picture
from text_extraction import extract_info, extract_unified_number

def clear_directory(directory_path):
    """清空指定資料夾中的所有文件"""
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
    os.makedirs(directory_path)

def copy_files_to_output_folder(file_paths, output_folder):
    """將文件從集合中複製到輸出資料夾"""
    for file_path in file_paths:
        if os.path.isfile(file_path):
            shutil.copy(file_path, output_folder)

def remove_pdf_files_from_folder(folder_path):
    """從資料夾中刪除所有 PDF 文件"""
    for file in os.listdir(folder_path):
        if file.lower().endswith('.pdf'):
            os.remove(os.path.join(folder_path, file))

def organize_images_by_unified_number(json_file, source_folder):
    """根據統一編號組織圖片"""
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for entry in data:
        unified_number = entry.get("統一編號")
        if not unified_number or unified_number == "Not match":
            continue
        filenames = entry.get("檔名", "")
        if not filenames:
            continue
        filenames = filenames.split(",")

        target_folder = os.path.join(source_folder, unified_number)
        os.makedirs(target_folder, exist_ok=True)

        for filename in filenames:
            source_path = os.path.join(source_folder, filename)
            target_path = os.path.join(target_folder, filename)
            if os.path.exists(source_path):  # 確保文件存在
                shutil.move(source_path, target_path)

def numerical_sort(filename):
    """提取檔案名稱中的數字用於排序"""
    numbers = re.findall(r'\d+', filename)
    return int(numbers[0]) if numbers else 0


def process_directory(directory_path, update_progress=None, update_status=None):
    """處理指定文件夾內的所有圖片"""
    last_unified_number = None
    combined_text = ""
    combined_filenames = ""
    files = sorted(os.listdir(directory_path), key=numerical_sort) # 使用自定義排序函數對文件進行排序

    data = []  # 用於收集所有數據的列表

    for index, filename in enumerate(files):
        print(f'辨識和擷取 {filename}...')
        if update_progress and update_status: # 如果傳入了進度更新和狀態更新的信號
            current_progress = (index + 1) * 100 // len(files)
            update_progress.emit(current_progress)  # 發射進度更新信號
            update_status.emit(f'辨識和擷取 {filename}...')  # 發射狀態更新信號

        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(directory_path, filename)
            text_detected = detect_text_from_picture(file_path)

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
                    data.append(extracted_info)  # 添加到数据列表中
                combined_text = text_detected + '\n'
                combined_filenames = filename + ","

            last_unified_number = current_unified_number or last_unified_number

    # 處理最後一組文本
    if combined_text:
        extracted_info = extract_info(combined_text, combined_filenames.rstrip(','))
        data.append(extracted_info)  # 添加到数据列表中

    return data