from pdf_processing import process_pdf_folder
from file_management import clear_directory, organize_images_by_unified_number, copy_files_to_output_folder, remove_pdf_files_from_folder, process_directory
from data_processing import save_to_json
from data_processing import load_business_code_mapping, add_business_description_to_data
from data_processing import generate_summary, check_api_data
import os


def main():
    output_folder_path = 'data'  # 替換為您的資料夾路徑
    file_paths = [
        'C:\\Users\\junting\\Desktop\\MODA_company_OCR\\temp\\test1\\scan_test.pdf',
        'C:\\Users\\junting\\Desktop\\MODA_company_OCR\\temp\\test1\\基本資料_16590299_頁面_1.jpg',
        'C:\\Users\\junting\\Desktop\\MODA_company_OCR\\temp\\test1\\基本資料_16590299_頁面_2.jpg'
    ]
    output_json_full_path = os.path.join(output_folder_path, 'output.json')
    summary_output_json_full_path = os.path.join(output_folder_path, 'summary_output.json')
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
    save_to_json(processed_data_with_desc, output_json_full_path)
    organize_images_by_unified_number(output_json_full_path, output_folder_path)

    # 生成摘要並檢查 API 回傳的資料
    summary_data = generate_summary(output_json_full_path)
    summary_data = check_api_data(summary_data)
    save_to_json(summary_data, summary_output_json_full_path)


if __name__ == "__main__":
    main()
