import os
import shutil # 用於刪除資料夾
import json

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