from PySide2.QtCore import QThread, Signal
from pdf_processing import process_pdf_folder
from image_processing import auto_rotate_images_in_folder

from file_management import (
    clear_directory, copy_files_to_folder, remove_pdf_files_from_folder,
    organize_images_by_unified_number, remove_or_replace_chinese_characters,
    pure_ocr_to_json, process_data_from_json, extract_filenames,
    rename_file_by_code, move_json_files_to_subfolder, copy_and_replace
)
from data_processing import (
    load_business_code_mapping, add_business_description_to_data,
    save_to_json, add_checkbox_status_to_data, add_qr_codes_links_to_data,
    generate_match_data, check_api_data, add_company_compare_result_to_data,
    add_cid_to_data, group_by_cid
)

import os




class WorkerThread(QThread):
    finished_processing = Signal()
    error_occurred = Signal(str)

    def __init__(self, file_paths, output_folder_path, updater, unified_number=None, archive=False, call_api=False, rename_files=False, summary=False, company_name_en=None):
        super(WorkerThread, self).__init__()
        self.file_paths = file_paths
        self.output_folder_path = output_folder_path
        self.updater = updater

        self.unified_number = unified_number
        self.archive = archive
        self.call_api = call_api
        self.rename_files = rename_files
        self.summary = summary
        self.company_name_en = company_name_en

        self.working_directory = "working"
        self.output_json_path = os.path.join(self.working_directory, 'output.json')
        self.api_data_output_json_path = os.path.join(self.working_directory, 'api_data.json')
        self.summary_data_output_json_path = os.path.join(self.working_directory, 'summary.json')
        self.output_pure_json_path = "pure_ocr_output.json"
        self.business_code_mapping_file = '公司行號營業項目代碼表.csv'


    def run(self):
        try:
            self.updater.update_status("正在創建和清空工作資料夾...")
            clear_directory(self.working_directory)

            self.updater.update_status("正在複製文件到工作資料夾...")
            copy_files_to_folder(self.file_paths, self.working_directory)

            filenames = extract_filenames(self.file_paths)
            self.updater.update_status("正在刪除或替換檔案名稱中的中文字符...")
            updated_filenames =remove_or_replace_chinese_characters(self.working_directory, filenames)

            self.updater.update_status("正在處理資料夾中的所有 PDF 並轉成圖片...")
            updated_filenames = process_pdf_folder(self.working_directory, updated_filenames, self.updater)

            self.updater.update_status("正在刪除 PDF 文件...")
            remove_pdf_files_from_folder(self.working_directory)

            self.updater.update_status("正在自動旋轉圖片...")
            auto_rotate_images_in_folder(self.working_directory, updated_filenames, self.updater)

            self.updater.update_status("正在辨識圖片...")
            pure_ocr_to_json(self.working_directory, updated_filenames, self.output_pure_json_path, self.updater)

            self.updater.update_status("正在擷取圖片...")
            processed_data = process_data_from_json(self.output_pure_json_path, self.updater)

            self.updater.update_status("正在查表business_name...")
            business_code_mapping = load_business_code_mapping(self.business_code_mapping_file)

            self.updater.update_status("正在添加business_name...")
            processed_data = add_business_description_to_data(processed_data, business_code_mapping)

            self.updater.update_status("正在添加checkbox_status...")
            processed_data = add_checkbox_status_to_data(processed_data, self.working_directory)

            self.updater.update_status("正在添加qr_codes_links...")
            processed_data = add_qr_codes_links_to_data(processed_data, self.working_directory)

            if self.company_name_en:
                self.updater.update_status("正在添加company_compare_result...")
                processed_data = add_company_compare_result_to_data(processed_data, self.company_name_en)

            if self.unified_number:
                self.updater.update_status("正在添加cid...")
                processed_data = add_cid_to_data(processed_data, self.unified_number)

            self.updater.update_status("正在儲存辨識擷取資料(output.json)...")
            save_to_json(processed_data, self.output_json_path)

            if self.rename_files:
                self.updater.update_status("正在修改檔名...")
                rename_file_by_code(self.output_json_path, self.working_directory)

            if self.archive:
                self.updater.update_status("正在歸檔...")
                organize_images_by_unified_number(self.output_json_path, self.working_directory)

            if self.call_api:
                self.updater.update_status("正在生成匹配狀況...")
                match_data = generate_match_data(self.output_json_path)
                self.updater.update_status("正在檢查 API 回傳的資料...")
                api_data = check_api_data(match_data, self.updater)
                self.updater.update_status("正在儲存匹配狀況(api_data.json)...")
                save_to_json(api_data, self.api_data_output_json_path)
            
            if self.summary:
                self.updater.update_status("正在儲存摘要資料...")
                summary_data = group_by_cid(self.output_json_path)
                save_to_json(summary_data, self.summary_data_output_json_path)

            self.updater.update_status("正在檢查是否需要將 JSON 檔案移動到子資料夾...")
            move_json_files_to_subfolder(self.working_directory, [self.output_json_path, self.api_data_output_json_path, self.summary_data_output_json_path])

            self.updater.update_status("正在複製和取代工作資料夾到輸出資料夾...")
            copy_and_replace(self.working_directory, self.output_folder_path)

            # 發射處理完畢
            self.finished_processing.emit()
            self.updater.update_status("處理完成！")

        except Exception as e:
            self.error_occurred.emit(str(e))  # 發射錯誤信息
            print(str(e))
            # 在這裡可以發射一個新的信號來處理這個特定的錯誤情況

        
    
        

