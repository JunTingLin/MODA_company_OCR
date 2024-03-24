from pdf_processing import process_pdf_folder
from file_management import clear_directory, organize_images_by_unified_number, copy_files_to_output_folder, remove_pdf_files_from_folder, remove_or_replace_chinese_characters, pure_ocr_to_json, process_data_from_json, extract_filenames
from data_processing import save_to_json
from data_processing import load_business_code_mapping, add_business_description_to_data, add_checkbox_status_to_data
from data_processing import generate_summary, check_api_data
from image_processing import auto_rotate_images_in_folder
import os
import argparse


def main(file_paths, output_folder_path):
    # 設置 Google 應用認證
    google_credentials_path = 'service-account-file.json'  # 如果需要，更改為您的文件路徑
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_credentials_path

    output_json_full_path = os.path.join(output_folder_path, 'output.json')
    summary_output_json_full_path = os.path.join(output_folder_path, 'summary_output.json')
    output_pure_json_path = os.path.join("pure_ocr_output.json")
    business_code_mapping_file = '公司行號營業項目代碼表.csv'

    # 先清空輸出資料夾，然後複製文件到輸出資料夾
    print("正在清空輸出資料夾...")
    clear_directory(output_folder_path)
    print("正在複製文件到輸出資料夾...")
    copy_files_to_output_folder(file_paths, output_folder_path)

    filenames = extract_filenames(file_paths)
    print("正在刪除或替換檔案名稱中的中文字符...")
    updated_filenames =remove_or_replace_chinese_characters(output_folder_path, filenames)

    # 處理資料夾中的所有 PDF 和圖片文件
    print("正在處理資料夾中的所有 PDF 並轉成圖片...")
    updated_filenames = process_pdf_folder(output_folder_path, updated_filenames)
    print("正在刪除 PDF 文件...")
    remove_pdf_files_from_folder(output_folder_path)  # 轉換完畢後刪除 PDF 文件
    print("正在自動旋轉圖片...")
    auto_rotate_images_in_folder(output_folder_path, updated_filenames)  # 自動旋轉圖片

    print("正在查表...")
    business_code_mapping = load_business_code_mapping(business_code_mapping_file)
    print("正在辨識圖片...")
    pure_ocr_to_json(output_folder_path, updated_filenames, output_pure_json_path)
    print("正在擷取圖片...")
    processed_data = process_data_from_json(output_pure_json_path)
    processed_data_with_desc = add_business_description_to_data(processed_data, business_code_mapping)
    processed_data_with_checkbox = add_checkbox_status_to_data(processed_data_with_desc, output_folder_path)
    save_to_json(processed_data_with_checkbox, output_json_full_path)
    print("正在歸檔...")
    organize_images_by_unified_number(output_json_full_path, output_folder_path)

    # 生成摘要並檢查 API 回傳的資料
    print("正在生成摘要...")
    summary_data = generate_summary(output_json_full_path)
    summary_data = check_api_data(summary_data)
    print("正在儲存摘要...")
    save_to_json(summary_data, summary_output_json_full_path)

    print("處理完成！")


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='OCR處理程序')
    # parser.add_argument('files', help='檔案路徑，用逗號分隔')
    # parser.add_argument('output_folder', help='輸出資料夾路徑')
    # args = parser.parse_args()

    # file_paths = args.files.split(',')  # 用逗號分隔檔案路徑
    # output_folder_path = args.output_folder
    # main(file_paths, output_folder_path)
    main([r"C:\Users\junting\Desktop\ocr_data\支票範例\check-TT0746839.png"],r'C:\Users\junting\Desktop\ocr_result')