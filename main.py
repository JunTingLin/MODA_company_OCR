import os
import re
import fitz  # PyMuPDF
import shutil # 用於刪除資料夾
from ocr import detect_text_from_picture
from text_extraction import extract_info, extract_unified_number

def save_to_file(info, file_name):
    """將提取的信息追加到文件"""
    with open(file_name, 'a', encoding='utf-8') as file:  # 使用 'a' 模式來追加數據
        for key, value in info.items():
            file.write(f'{key},{value}\n')
        file.write('\n')  # 在每個條目之間添加一個空行

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

def convert_pdf_to_images(pdf_path, output_folder):
    """將 PDF 文件中的每頁轉換為圖片並儲存"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with fitz.open(pdf_path) as doc:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)  # 加載頁面
            pix = page.get_pixmap()  # 獲取頁面的像素映射
            output_file = f'{output_folder}/page_{page_num + 1}.png'
            pix.save(output_file)

def organize_images_by_unified_number(output_file, source_folder):
    """根據統一編號組織圖"""
    with open(output_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    unified_number_to_files = {}
    current_unified_number = None
    current_filenames = []

    for line in lines:
        if line.strip() == '':
            # 遇到空行，處理目前資料塊
            if current_unified_number and current_filenames:
                if current_unified_number not in unified_number_to_files:
                    unified_number_to_files[current_unified_number] = []
                unified_number_to_files[current_unified_number].extend(current_filenames)
            current_unified_number = None
            current_filenames = []
        elif line.startswith('檔名'):
            current_filenames = line.split(',')[1:]
            current_filenames = [filename.strip() for filename in current_filenames if filename.strip()]
        elif line.startswith('統一編號'):
            current_unified_number = line.split(',')[1].strip()

    # 處理最後一個資料區塊
    if current_unified_number and current_filenames:
        if current_unified_number not in unified_number_to_files:
            unified_number_to_files[current_unified_number] = []
        unified_number_to_files[current_unified_number].extend(current_filenames)

    # 建立資料夾並移動文件
    for unified_number, filenames in unified_number_to_files.items():
        target_folder = os.path.join(source_folder, unified_number)
        os.makedirs(target_folder, exist_ok=True)
        for filename in filenames:
            source_path = os.path.join(source_folder, filename)
            target_path = os.path.join(target_folder, filename)
            if os.path.exists(source_path):  # 確保文件存在
                shutil.move(source_path, target_path)

def main():
    open('output.txt', 'w').close()  # 清空先前的 output.txt 文件
    pdf_path = 'scan_test.pdf'  # 替換為您的 PDF 文件路徑
    directory_path = 'data'  # 輸出圖片的資料夾路徑

    clear_directory(directory_path)  # 清空 data 資料夾
    convert_pdf_to_images(pdf_path, directory_path)
    process_directory(directory_path)
    organize_images_by_unified_number('output.txt', directory_path)

if __name__ == "__main__":
    main()
