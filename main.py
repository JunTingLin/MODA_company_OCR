import os
import re
from ocr import detect_text_from_picture
from text_extraction import extract_info, extract_unified_number
from pdf_processing import process_pdf_folder
from file_management import clear_directory, organize_images_by_unified_number, copy_files_to_output_folder, remove_pdf_files_from_folder
from data_processing import save_to_json
from data_processing import load_business_code_mapping, add_business_description_to_data
from data_processing import generate_summary, check_api_data


def numerical_sort(filename):
    """提取檔案名稱中的數字用於排序"""
    numbers = re.findall(r'\d+', filename)
    return int(numbers[0]) if numbers else 0


def process_directory(directory_path):
    """處理指定文件夾內的所有圖片"""
    last_unified_number = None
    combined_text = ""
    combined_filenames = ""
    files = sorted(os.listdir(directory_path), key=numerical_sort) # 使用自定義排序函數對文件進行排序

    data = []  # 用於收集所有數據的列表

    for filename in files:
        print(f'辨識和擷取 {filename}...')
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




def main():
    output_folder_path = 'data'  # 替換為您的資料夾路徑
    file_paths = [
        'C:\\Users\\junting\\Desktop\\MODA_company_OCR\\temp\\test1\\scan_test.pdf',
        'C:\\Users\\junting\\Desktop\\MODA_company_OCR\\temp\\test1\\基本資料_16590299_頁面_1.jpg',
        'C:\\Users\\junting\\Desktop\\MODA_company_OCR\\temp\\test1\\基本資料_16590299_頁面_2.jpg'
    ]
    output_json_path = 'output.json'
    summary_output_json_path = 'summary_output.json'
    business_code_mapping_file = '公司行號營業項目代碼表.csv'

    # 先清空輸出資料夾，然後複製文件到輸出資料夾
    clear_directory(output_folder_path)
    copy_files_to_output_folder(file_paths, output_folder_path)
    
    # 處理資料夾中的所有 PDF 和圖片文件
    process_pdf_folder(output_folder_path)
    remove_pdf_files_from_folder(output_folder_path)  # 轉換完畢後刪除 PDF 文件

    business_code_mapping = load_business_code_mapping(business_code_mapping_file)
    processed_data = process_directory(output_folder_path)
    processed_data_with_desc = add_business_description_to_data(processed_data, business_code_mapping)
    save_to_json(processed_data_with_desc, output_json_path)
    organize_images_by_unified_number(output_json_path, output_folder_path)

    summary_data = generate_summary(output_json_path)
    summary_data = check_api_data(summary_data)
    save_to_json(summary_data, summary_output_json_path)


if __name__ == "__main__":
    main()
