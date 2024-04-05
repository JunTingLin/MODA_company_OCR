from PySide2.QtCore import QThread, Signal
from pdf_processing import process_pdf_folder
from file_management import clear_directory, copy_files_to_output_folder, remove_pdf_files_from_folder,organize_images_by_unified_number, remove_or_replace_chinese_characters, pure_ocr_to_json, process_data_from_json, extract_filenames
from data_processing import load_business_code_mapping, add_business_description_to_data, save_to_json, add_checkbox_status_to_data, add_qr_codes_links_to_data
from data_processing import generate_summary, check_api_data
import os
from image_processing import auto_rotate_images_in_folder




class WorkerThread(QThread):
    update_progress = Signal(int)
    update_status = Signal(str)
    finished_processing = Signal(list)  # 新增：處理完畢信號，返回數據列表
    error_occurred = Signal(str)  # 新增錯誤發生信號

    def __init__(self, output_folder_path, file_paths):
        super(WorkerThread, self).__init__()
        self.output_folder_path = output_folder_path
        self.file_paths = file_paths
        self.output_pure_json_path = "pure_ocr_output.json"

    def run(self):
        try:
            # 清空輸出資料夾
            self.update_status.emit("正在清空輸出資料夾...")
            print("正在清空輸出資料夾...")
            clear_directory(self.output_folder_path)
            # 複製文件到輸出資料夾
            self.update_status.emit("正在複製文件到輸出資料夾...")
            print("正在複製文件到輸出資料夾...")
            copy_files_to_output_folder(self.file_paths, self.output_folder_path)

            # 刪除或替換檔案名稱中的中文字符
            filenames = extract_filenames(self.file_paths)
            self.update_status.emit("正在刪除或替換檔案名稱中的中文字符...")
            print("正在刪除或替換檔案名稱中的中文字符...")
            updated_filenames =remove_or_replace_chinese_characters(self.output_folder_path, filenames)

            # 處理資料夾中的所有 PDF 並轉成圖片
            self.update_status.emit("正在處理資料夾中的所有 PDF 並轉成圖片...")
            print("正在處理資料夾中的所有 PDF 並轉成圖片...")
            updated_filenames = process_pdf_folder(self.output_folder_path, updated_filenames)
            # 刪除 PDF 文件
            self.update_status.emit("正在刪除 PDF 文件...")
            print("正在刪除 PDF 文件...")
            remove_pdf_files_from_folder(self.output_folder_path)
            # 自動旋轉圖片
            self.update_status.emit("正在自動旋轉圖片...")
            print("正在自動旋轉圖片...")
            auto_rotate_images_in_folder(self.output_folder_path, updated_filenames, self.update_progress, self.update_status)
            # 處理圖片文件
            self.update_status.emit("正在處理圖片文件...")
            print("正在處理圖片文件...")
            self.update_progress.emit(90)
            print("正在辨識圖片...")
            pure_ocr_to_json(self.output_folder_path, updated_filenames, self.output_pure_json_path, self.update_progress, self.update_status)
            print("正在擷取圖片...")
            processed_data = process_data_from_json(self.output_pure_json_path, self.update_progress, self.update_status)


            # 其他處理步驟
            self.update_status.emit("正在查表...")
            print("正在查表...")
            self.update_progress.emit(95)
            business_code_mapping_file = '公司行號營業項目代碼表.csv'
            business_code_mapping = load_business_code_mapping(business_code_mapping_file)
            processed_data_with_desc = add_business_description_to_data(processed_data, business_code_mapping)
            processed_data_with_checkbox = add_checkbox_status_to_data(processed_data_with_desc, self.output_folder_path)
            processed_data_with_qr_codes = add_qr_codes_links_to_data(processed_data_with_checkbox, self.output_folder_path)
            # 儲存數據
            output_json_path = os.path.join(self.output_folder_path, 'output.json')
            save_to_json(processed_data_with_qr_codes, output_json_path)
            # 歸檔
            self.update_status.emit("正在歸檔...")
            print("正在歸檔...")
            self.update_progress.emit(97)
            organize_images_by_unified_number(output_json_path, self.output_folder_path)

            # 發射處理完畢的數據
            self.finished_processing.emit(processed_data)

        except Exception as e:
            self.error_occurred.emit(str(e))  # 發射錯誤信息
            print(str(e))
            # 在這裡可以發射一個新的信號來處理這個特定的錯誤情況
    
    def run_step2(self, output_json_path, summary_output_json_path):
        self.update_status.emit("正在生成摘要...")
        print("正在生成摘要...")
        summary_data = generate_summary(output_json_path)

        # 呼叫 check_api_data 並傳遞更新進度和狀態的方法
        summary_data = check_api_data(summary_data, self.update_progress, self.update_status)

        self.update_status.emit("正在儲存摘要...")
        print("正在儲存摘要...")
        save_to_json(summary_data, summary_output_json_path)
        self.update_progress.emit(100)
        self.finished_processing.emit(summary_data)
