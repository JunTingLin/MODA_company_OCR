import os
import shutil # 用於刪除資料夾
import json
from ocr import detect_text_from_picture
from text_extraction import extract_info, extract_unified_number
from utils import numerical_sort

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


def process_directory(directory_path, update_progress=None, update_status=None):
    combined_text = ""
    combined_filenames = ""
    files = sorted(os.listdir(directory_path), key=numerical_sort)

    data = []
    skip_next = False

    for index, filename in enumerate(files):
        print(f"正在辨識和擷取 {filename}...")
        if skip_next:
            skip_next = False
            continue

        if update_progress and update_status:
            current_progress = (index + 1) * 90 // len(files)
            update_progress.emit(current_progress)
            update_status.emit(f'辨識和擷取 {filename}...')

        file_path = os.path.join(directory_path, filename)
        text_detected = detect_text_from_picture(file_path)

        if "公司基本資料" in text_detected:
            current_unified_number = extract_unified_number(text_detected)
            combined_text += text_detected + '\n'
            combined_filenames += filename + ","
            if index + 1 < len(files):
                next_file = files[index + 1]
                next_file_path = os.path.join(directory_path, next_file)
                next_text_detected = detect_text_from_picture(next_file_path)
                next_unified_number = extract_unified_number(next_text_detected)
            if index + 1 < len(files) and (current_unified_number == next_unified_number or not next_unified_number) and "數位發展部數位產業署投標廠商聲明書" not in next_text_detected and "營業人銷售額與稅額申報書清單" not in next_text_detected and "營業人銷售額與稅額申報書" not in next_text_detected:
                # 合併下一頁
                combined_text += next_text_detected + '\n'
                combined_filenames += next_file + ","
                skip_next = True
                extracted_info = extract_info(combined_text, combined_filenames.rstrip(','))
                data.append(extracted_info)
                combined_text = ""
                combined_filenames = ""
            else:
                extracted_info = extract_info(combined_text, combined_filenames.rstrip(','))
                data.append(extracted_info)
                combined_text = ""
                combined_filenames = ""

        elif "數位發展部數位產業署投標廠商聲明書" in text_detected:
            # 投標廠商聲明書處理邏輯
            combined_text += text_detected + '\n'
            combined_filenames += filename + ","
            if index + 1 < len(files):
                next_file = files[index + 1]
                next_file_path = os.path.join(directory_path, next_file)
                next_text_detected = detect_text_from_picture(next_file_path)
                combined_text += next_text_detected + '\n'
                combined_filenames += next_file + ","
                skip_next = True
                
                extracted_info = extract_info(combined_text, combined_filenames.rstrip(','))
                data.append(extracted_info)
                combined_text = ""
                combined_filenames = ""

        elif "401" in text_detected and ("營業人銷售額與稅額申報書清單" in text_detected or "營業人銷售額與稅額申報書" in text_detected):
            # 401表僅單頁處理
            extracted_info = extract_info(text_detected, filename)
            data.append(extracted_info)

        elif "403" in text_detected and "營業人銷售額與稅額申報書" in text_detected :
            # 403表僅單頁處理
            extracted_info = extract_info(text_detected, filename)
            data.append(extracted_info)

        else:
            # 其他圖片單頁處理(輸出圖片上的文字)
            extracted_info = extract_info(text_detected, filename)
            data.append(extracted_info)
            

        # last_unified_number = current_unified_number

    # 處理最後一組合併的文本
    if combined_text:
        extracted_info = extract_info(combined_text, combined_filenames.rstrip(','))
        data.append(extracted_info)

    return data
