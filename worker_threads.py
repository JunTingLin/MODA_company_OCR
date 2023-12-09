from PySide2.QtCore import QThread, Signal
from pdf_processing import process_pdf_folder
from file_management import clear_directory, copy_files_to_output_folder, process_directory, remove_pdf_files_from_folder, process_directory,organize_images_by_unified_number
from data_processing import load_business_code_mapping, add_business_description_to_data, save_to_json
from data_processing import generate_summary, check_api_data
import os




class WorkerThread(QThread):
    update_progress = Signal(int)
    update_status = Signal(str)
    finished_processing = Signal(list)  # 新增：處理完畢信號，返回數據列表

    def __init__(self, output_folder_path, file_paths):
        super(WorkerThread, self).__init__()
        self.output_folder_path = output_folder_path
        self.file_paths = file_paths

    def run(self):
        # 清空輸出資料夾
        self.update_status.emit("正在清空輸出資料夾...")
        clear_directory(self.output_folder_path)

        # 複製文件到輸出資料夾
        self.update_status.emit("正在複製文件到輸出資料夾...")
        copy_files_to_output_folder(self.file_paths, self.output_folder_path)

        # 處理資料夾中的所有 PDF 並轉成圖片
        self.update_status.emit("正在處理資料夾中的所有 PDF 並轉成圖片...")
        process_pdf_folder(self.output_folder_path)

        # 刪除 PDF 文件
        self.update_status.emit("正在刪除 PDF 文件...")
        remove_pdf_files_from_folder(self.output_folder_path)

        # 處理圖片文件
        self.update_status.emit("正在處理圖片文件...")
        self.update_progress.emit(90)
        processed_data = process_directory(self.output_folder_path, self.update_progress, self.update_status)


        # 其他處理步驟
        self.update_status.emit("正在查表...")
        self.update_progress.emit(95)
        business_code_mapping_file = '公司行號營業項目代碼表.csv'
        business_code_mapping = load_business_code_mapping(business_code_mapping_file)
        processed_data_with_desc = add_business_description_to_data(processed_data, business_code_mapping)
        
        # 儲存數據
        output_json_path = os.path.join(self.output_folder_path, 'output.json')
        save_to_json(processed_data_with_desc, output_json_path)
        # 歸檔
        self.update_status.emit("正在歸檔...")
        self.update_progress.emit(97)
        organize_images_by_unified_number(output_json_path, self.output_folder_path)

        # 發射處理完畢的數據
        self.finished_processing.emit(processed_data)
    
    def run_step2(self, output_json_path, summary_output_json_path):
        self.update_status.emit("正在生成摘要...")
        summary_data = generate_summary(output_json_path)

        # 呼叫 check_api_data 並傳遞更新進度和狀態的方法
        summary_data = check_api_data(summary_data, self.update_progress, self.update_status)

        self.update_status.emit("正在儲存摘要...")
        save_to_json(summary_data, summary_output_json_path)
        self.update_progress.emit(100)
        self.finished_processing.emit(summary_data)
