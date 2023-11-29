import os
import re
import fitz  # PyMuPDF
import shutil # 用於刪除資料夾
import json
from ocr import detect_text_from_picture
from text_extraction import extract_info, extract_unified_number

def save_to_json(data, file_name):
    """將提取的信息以 JSON 格式保存"""
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def numerical_sort(filename):
    """提取檔案名稱中的數字用於排序"""
    numbers = re.findall(r'\d+', filename)
    return int(numbers[0]) if numbers else 0

def clear_directory(directory_path):
    """清空指定資料夾中的所有文件"""
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
    os.makedirs(directory_path)

def process_directory(directory_path):
    """處理指定文件夾內的所有圖片"""
    last_unified_number = None
    combined_text = ""
    combined_filenames = ""
    files = sorted(os.listdir(directory_path), key=numerical_sort) # 使用自定義排序函數對文件進行排序

    data = []  # 用于收集所有数据的列表

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
                    data.append(extracted_info)  # 添加到数据列表中
                combined_text = text_detected + '\n'
                combined_filenames = filename + ","

            last_unified_number = current_unified_number or last_unified_number

    # 處理最後一組文本
    if combined_text:
        extracted_info = extract_info(combined_text, combined_filenames.rstrip(','))
        data.append(extracted_info)  # 添加到数据列表中

    return data

def convert_pdf_to_images(pdf_path, output_folder, dpi=300):
    """將 PDF 文件中的每頁轉換為圖片並儲存"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with fitz.open(pdf_path) as doc:
        zoom = dpi / 72  # 将 DPI 转换为 fitz 的缩放因子
        mat = fitz.Matrix(zoom, zoom)

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)  # 加載頁面
            pix = page.get_pixmap(matrix=mat)  # 獲取頁面的像素映射，应用缩放因子
            output_file = f'{output_folder}/page_{page_num + 1}.png'
            pix.save(output_file)

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

def main():
    open('output.json', 'w').close()  # 清空先前的 output.json 文件
    pdf_path = 'scan_test.pdf'  # 替換為您的 PDF 文件路徑
    directory_path = 'data'  # 輸出圖片的資料夾路徑

    clear_directory(directory_path)  # 清空 data 資料夾
    convert_pdf_to_images(pdf_path, directory_path, dpi=300)  # 指定 DPI
    processed_data = process_directory(directory_path)
    save_to_json(processed_data, 'output.json')
    organize_images_by_unified_number('output.json', directory_path)

if __name__ == "__main__":
    main()
