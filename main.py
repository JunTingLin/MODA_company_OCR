import os
import re
from ocr import detect_text_from_picture
from text_extraction import extract_info, extract_unified_number
from pdf_processing import convert_pdf_to_images
from file_management import clear_directory, organize_images_by_unified_number
from data_processing import save_to_json
from data_processing import load_business_code_mapping, add_business_description_to_data


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
    open('output.json', 'w').close()  # 清空先前的 output.json 文件
    pdf_path = 'scan_test.pdf'  # 替換為您的 PDF 文件路徑
    directory_path = 'data'  # 輸出圖片的資料夾路徑

    clear_directory(directory_path)  # 清空 data 資料夾
    convert_pdf_to_images(pdf_path, directory_path, dpi=300)  # 指定 DPI
    business_code_mapping = load_business_code_mapping('公司行號營業項目代碼表.csv')
    processed_data = process_directory(directory_path)
    processed_data_with_desc = add_business_description_to_data(processed_data, business_code_mapping)
    save_to_json(processed_data_with_desc, 'output.json')
    organize_images_by_unified_number('output.json', directory_path)

if __name__ == "__main__":
    main()
