import os
import shutil # 用於刪除資料夾
import json
import random
import string
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
        unified_number = entry.get("ocr_cid")
        if not unified_number or unified_number == "Not match":
            continue
        filenames = entry.get("filename", [])
        if not filenames:
            continue

        target_folder = os.path.join(source_folder, unified_number)
        os.makedirs(target_folder, exist_ok=True)

        for filename in filenames:
            source_path = os.path.join(source_folder, filename)
            target_path = os.path.join(target_folder, filename)
            if os.path.exists(source_path):  # 確保文件存在
                shutil.move(source_path, target_path)

def remove_or_replace_chinese_characters(directory_path, filenames):
    updated_filenames = []
    for filename in filenames:
        new_filename = filename
        if '頁面' in new_filename:
            new_filename = new_filename.replace('頁面', 'page')

        # 刪除其他中文字符，但保留「頁面」已經被替換成「page」的部分
        new_filename = re.sub(r'[^\x00-\x7F]+', '', new_filename)

        # 如果檔名變成空的或只有檔案擴展名，則替換為隨機亂碼
        if new_filename == '' or new_filename.startswith('.'):
            new_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=6)) + os.path.splitext(filename)[1]

        # 構建完整的舊檔案和新檔案路徑
        old_file_path = os.path.join(directory_path, filename)
        new_file_path = os.path.join(directory_path, new_filename)

        # 重新命名檔案
        os.rename(old_file_path, new_file_path)

        updated_filenames.append(new_filename)

    return updated_filenames


def pure_ocr_to_json(directory_path, filenames, output_json_path, update_progress=None, update_status=None):
    """將純文字的OCR結果儲存到JSON檔案"""

    data = []
    for index, filename in enumerate(filenames):
        print(f"正在辨識 {filename}...")

        if update_progress and update_status:
            current_progress = (index + 1) * 100 // len(filenames)
            update_progress.emit(current_progress)
            update_status.emit(f'正在辨識 {filename}...')


        file_path = os.path.join(directory_path, filename)
        text_detected = detect_text_from_picture(file_path)
        info = {}
        info['filename'] = filename
        info['ocr_data'] = text_detected
        data.append(info)

    with open(output_json_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def process_data_from_json(ocr_json, update_progress=None, update_status=None):
    with open(ocr_json, 'r', encoding='utf-8') as file:
        data = json.load(file)

    combined_text = ""
    filenames = []
    processed_data = []
    skip_next = False

    for index,entry in enumerate(data):
        print(f"正在擷取 {entry['filename']}...")

        if update_progress and update_status:
            current_progress = (index + 1) * 100 // len(entry['filename'])
            update_progress.emit(current_progress)
            update_status.emit(f"正在擷取 {entry['filename']}...")
        
        if skip_next:
            skip_next = False
            continue

        if "公司基本資料" in entry["ocr_data"] and "商工登記公示資料查詢服務" in entry["ocr_data"]:
            current_unified_number = extract_unified_number(entry["ocr_data"])
            combined_text += entry["ocr_data"] + '\n'
            filenames.append(entry["filename"])
            if index + 1 < len(data):
                next_entry = data[index + 1]
                next_unified_number = extract_unified_number(next_entry["ocr_data"])
            if index + 1 < len(data) and (current_unified_number == next_unified_number or next_unified_number=='Not match') and "數位發展部數位產業署投標廠商聲明書" not in next_entry["ocr_data"] and "營業人銷售額與稅額申報書清單" not in next_entry["ocr_data"] and "營業人銷售額與稅額申報書" not in next_entry["ocr_data"]:
                # 合併下一頁
                combined_text += next_entry["ocr_data"] + '\n'
                filenames.append(next_entry["filename"])
                skip_next = True
                extracted_info = extract_info(combined_text, filenames)
                processed_data.append(extracted_info)
                combined_text = ""
                filenames = []
            else:
                extracted_info = extract_info(combined_text, filenames)
                processed_data.append(extracted_info)
                combined_text = ""
                filenames = []

        elif "數位發展部數位產業署投標廠商聲明書" in entry["ocr_data"]:
            # 投標廠商聲明書處理邏輯
            combined_text += entry["ocr_data"] + '\n'
            filenames.append(entry["filename"])
            if index + 1 < len(data):
                next_entry = data[index + 1]
                combined_text += next_entry["ocr_data"] + '\n'
                filenames.append(next_entry["filename"])
                skip_next = True
                extracted_info = extract_info(combined_text, filenames)
                processed_data.append(extracted_info)
                combined_text = ""
                filenames = []

        else:
            # 其他表單
            filenames.append(entry["filename"])
            extracted_info = extract_info(entry["ocr_data"], filenames)
            processed_data.append(extracted_info)
            filenames = []

    # 處理最後一組合併的文本
    if combined_text:
        extracted_info = extract_info(combined_text, filenames)
        processed_data.append(extracted_info)

    return processed_data
    
def extract_filenames(file_paths):
    """從檔案路徑清單中提取檔案名"""
    filenames = [os.path.basename(path) for path in file_paths]
    return filenames



if __name__ == "__main__":
    updated_filenames = remove_or_replace_chinese_characters(r'C:\Users\junting\Desktop\ocr_result',["scan_test_all_頁面_01.jpg"])
    print(updated_filenames)