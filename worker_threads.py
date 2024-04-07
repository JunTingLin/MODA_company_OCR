from PySide2.QtCore import QThread, Signal
from pdf_processing import process_pdf_folder
from file_management import clear_directory, copy_files_to_output_folder, remove_pdf_files_from_folder,organize_images_by_unified_number, remove_or_replace_chinese_characters, pure_ocr_to_json, process_data_from_json, extract_filenames
from data_processing import load_business_code_mapping, add_business_description_to_data, save_to_json, add_checkbox_status_to_data, add_qr_codes_links_to_data
from data_processing import generate_match_data, check_api_data
import os
from image_processing import auto_rotate_images_in_folder




class WorkerThread(QThread):
    finished_processing = Signal()
    error_occurred = Signal(str)

    def __init__(self, file_paths, output_folder_path, updater, unified_number=None, archive=False, call_api=False, rename_files=False, summary=False, company_name_en=None):
        super(WorkerThread, self).__init__()
        self.output_folder_path = output_folder_path
        self.file_paths = file_paths
        self.output_json_path = os.path.join(self.output_folder_path, 'output.json')
        self.api_data_output_json_path = os.path.join(self.output_folder_path, 'api_data.json')
        self.output_pure_json_path = "pure_ocr_output.json"
        self.business_code_mapping_file = '公司行號營業項目代碼表.csv'
        self.updater = updater


    def run(self):
        try:
            # 清空輸出資料夾
            self.updater.update_status("正在清空輸出資料夾...")
            clear_directory(self.output_folder_path)
            # 複製文件到輸出資料夾
            self.updater.update_status("正在複製文件到輸出資料夾...")
            copy_files_to_output_folder(self.file_paths, self.output_folder_path)

            # 刪除或替換檔案名稱中的中文字符
            filenames = extract_filenames(self.file_paths)
            self.updater.update_status("正在刪除或替換檔案名稱中的中文字符...")
            updated_filenames =remove_or_replace_chinese_characters(self.output_folder_path, filenames)

            # 處理資料夾中的所有 PDF 並轉成圖片
            self.updater.update_status("正在處理資料夾中的所有 PDF 並轉成圖片...")
            updated_filenames = process_pdf_folder(self.output_folder_path, updated_filenames)
            # 刪除 PDF 文件
            self.updater.update_status("正在刪除 PDF 文件...")
            remove_pdf_files_from_folder(self.output_folder_path)
            # 自動旋轉圖片
            self.updater.update_status("正在自動旋轉圖片...")
            auto_rotate_images_in_folder(self.output_folder_path, updated_filenames, self.updater)
            # 處理圖片文件
            self.updater.update_status("正在辨識圖片...")
            pure_ocr_to_json(self.output_folder_path, updated_filenames, self.output_pure_json_path, self.updater)
            self.updater.update_status("正在擷取圖片...")
            processed_data = process_data_from_json(self.output_pure_json_path, self.updater)


            # 其他處理步驟
            self.updater.update_status("正在查表...")
            business_code_mapping = load_business_code_mapping(self.business_code_mapping_file)
            processed_data_with_desc = add_business_description_to_data(processed_data, business_code_mapping)
            processed_data_with_checkbox = add_checkbox_status_to_data(processed_data_with_desc, self.output_folder_path)
            processed_data_with_qr_codes = add_qr_codes_links_to_data(processed_data_with_checkbox, self.output_folder_path)
            # 儲存數據
            save_to_json(processed_data_with_qr_codes, self.output_json_path)
            # 歸檔
            self.updater.update_status("正在歸檔...")
            organize_images_by_unified_number(self.output_json_path, self.output_folder_path)


            self.updater.update_status("正在生成匹配狀況(api_data)...")
            match_data = generate_match_data(self.output_json_path)

            # 呼叫 check_api_data 並傳遞更新進度和狀態的方法
            api_data = check_api_data(match_data, self.updater)

            self.updater.update_status("正在儲存匹配狀況(api_data)...")
            save_to_json(api_data, self.api_data_output_json_path)

            # 發射處理完畢
            self.finished_processing.emit()

        except Exception as e:
            self.error_occurred.emit(str(e))  # 發射錯誤信息
            print(str(e))
            # 在這裡可以發射一個新的信號來處理這個特定的錯誤情況

        
    
        

