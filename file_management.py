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

def rename_file_by_code(json_file, source_folder):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 初始化一個字典來維護每一組 cid-code 的計數器
    count_dict = {}

    for item in data:
        code = item['code']
        cid = item['cid']
        filenames = item['filename']

        # 根據 cid 和 code 建立一個唯一的鍵
        key = f"{cid}-{code}"
        if key not in count_dict:
            count_dict[key] = 0

        new_filenames = []

        for filename in filenames:
            # 更新計數器
            count_dict[key] += 1
            new_filename = f"{cid}-{code}-{count_dict[key]:03d}{os.path.splitext(filename)[-1]}"
            new_filenames.append(new_filename)

            old_filepath = os.path.join(source_folder, filename)
            new_filepath = os.path.join(source_folder, new_filename)

            # 重新命名檔案
            os.rename(old_filepath, new_filepath)

        item['filename'] = new_filenames

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)



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
    """將純文字的OCR結果儲存到JSON檔案，並對含有「證書」的文件進行特殊處理"""

    data = []
    new_block = False 
    has_touch_certificate = False

    for index, filename in enumerate(filenames):
        print(f"正在辨識 {filename}...")

        # 更新進度
        if update_progress and update_status:
            current_progress = (index + 1) * 100 // len(filenames)
            update_progress.emit(current_progress)
            update_status.emit(f'正在辨識 {filename}...')

        file_path = os.path.join(directory_path, filename)

        if "_page_" not in filename or "_page_1." in filename:
            new_block = True
            has_touch_certificate = False
        else:
            new_block = False

        # 檢查是否處於證書處理流程中
        if has_touch_certificate and not new_block:
            # 如果當前文件名符合連續頁面的條件，則僅添加文件名
            data[-1]['filename'].append(filename)
            continue

        # 進行OCR處理
        text_detected = detect_text_from_picture(file_path)
        if 'ISO' in text_detected and '27001' in text_detected:
            # 標記證書處理流程開始
            has_touch_certificate = True


        info = {'filename': [filename], 'ocr_data': text_detected}
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
            filenames.extend(entry["filename"])
            if index + 1 < len(data):
                next_entry = data[index + 1]
                next_unified_number = extract_unified_number(next_entry["ocr_data"])
            if index + 1 < len(data) and (current_unified_number == next_unified_number or next_unified_number=='Not match') and "數位發展部數位產業署投標廠商聲明書" not in next_entry["ocr_data"] and "營業人銷售額與稅額申報書清單" not in next_entry["ocr_data"] and "營業人銷售額與稅額申報書" not in next_entry["ocr_data"]:
                # 合併下一頁
                combined_text += next_entry["ocr_data"] + '\n'
                filenames.extend(next_entry["filename"])
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
            filenames.extend(entry["filename"])
            if index + 1 < len(data):
                next_entry = data[index + 1]
                combined_text += next_entry["ocr_data"] + '\n'
                filenames.extend(next_entry["filename"])
                skip_next = True
                extracted_info = extract_info(combined_text, filenames)
                processed_data.append(extracted_info)
                combined_text = ""
                filenames = []

        else:
            # 其他表單
            filenames.extend(entry["filename"])
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
    # pure_ocr_to_json(r"C:\Users\junting\Desktop\ocr_data\27001_sample\去重覆", ["1000-16300572-147-test_doc_27001_page_1.jpg","1000-16300572-147-test_doc_27001_page_2.jpg","1000-16300572-147-test_doc_27001_page_3.jpg","1000-16300572-147-test_doc_27001_page_4.jpg","1000-23737538-415-test_doc_27001_page_1.png"], "pure_ocr_output.json")

    # print(process_data_from_json("pure_ocr_output.json"))

    rename_file_by_code(r"C:\Users\junting\Desktop\ocr_result\output.json", r"C:\Users\junting\Desktop\ocr_result")