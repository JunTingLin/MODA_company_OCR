import sys
import os
import subprocess
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile

# 匯入其他模組的函數
from data_processing import load_business_code_mapping, add_business_description_to_data, save_to_json
from file_management import clear_directory, copy_files_to_output_folder, remove_pdf_files_from_folder, organize_images_by_unified_number, process_directory
from pdf_processing import process_pdf_folder

class AppWindow(QMainWindow):
    def __init__(self):
        super(AppWindow, self).__init__()

        # 加載 UI 文件
        ui_file = QFile("ui/main.ui")  
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        # 初始化設置
        self.initialize_ui()

        # 設置按鈕的功能
        self.window.button_choose_file.clicked.connect(self.choose_file)
        self.window.button_remove_file.clicked.connect(self.remove_file)
        self.window.button_choose_output_folder.clicked.connect(self.choose_output_folder)
        self.window.button_open_output_folder.clicked.connect(self.open_output_folder)
        self.window.button_step1.clicked.connect(self.execute_step1)

        self.window.show()

    def initialize_ui(self):
        # 初始化進度條和清空列表
        self.window.progressBar.setValue(0)
        self.window.listWidget.clear()
        self.window.label_status.setText("")

        # 初始化輸出資料夾路徑
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        self.output_folder_path = os.path.join(desktop_path, "ocr_result")
        self.window.lineEdit.setText(self.output_folder_path)

    def choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "選擇文件", "", "圖片檔案 (*.png *.jpg *.jpeg);;PDF 檔案 (*.pdf)")
        if file_path:
            self.window.listWidget.addItem(file_path)

    def remove_file(self):
        selected_item = self.window.listWidget.currentItem()
        if selected_item:
            self.window.listWidget.takeItem(self.window.listWidget.row(selected_item))

    def choose_output_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "選擇輸出資料夾")
        if folder_path:
            self.window.lineEdit.setText(folder_path)
            self.output_folder_path = folder_path

    def open_output_folder(self):
        if os.path.exists(self.output_folder_path):
            if sys.platform == 'win32':
                os.startfile(self.output_folder_path)
            elif sys.platform == 'darwin':  # macOS
                subprocess.Popen(['open', self.output_folder_path])
            else:  # Linux and other OS
                subprocess.Popen(['xdg-open', self.output_folder_path])
        else:
            QMessageBox.warning(self, "警告", "資料夾不存在或無法打開")

    def execute_step1(self):
        # 獲取檔案路徑和輸出資料夾
        file_paths = [self.window.listWidget.item(i).text() for i in range(self.window.listWidget.count())]
        output_folder_path = self.window.lineEdit.text()

        # 清空輸出資料夾並更新進度條
        clear_directory(output_folder_path)
        self.window.progressBar.setValue(10)

        # 複製文件到輸出資料夾並更新進度條
        copy_files_to_output_folder(file_paths, output_folder_path)
        self.window.progressBar.setValue(20)

        # 處理資料夾中的所有 PDF 和圖片文件並更新進度條
        process_pdf_folder(output_folder_path)
        self.window.progressBar.setValue(50)

        # 轉換完畢後刪除 PDF 文件並更新進度條
        remove_pdf_files_from_folder(output_folder_path)
        self.window.progressBar.setValue(60)

        # 其他處理步驟並更新進度條
        business_code_mapping_file = '公司行號營業項目代碼表.csv'
        business_code_mapping = load_business_code_mapping(business_code_mapping_file)
        processed_data = process_directory(output_folder_path)
        self.window.progressBar.setValue(80)

        processed_data_with_desc = add_business_description_to_data(processed_data, business_code_mapping)
        save_to_json(processed_data_with_desc, 'output.json')
        organize_images_by_unified_number('output.json', output_folder_path)
        self.window.progressBar.setValue(90)

        # 完成處理並將進度條設置為滿
        self.window.progressBar.setValue(100)

        # 顯示完成提示
        QMessageBox.information(self, "完成", "處理完成！")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = AppWindow()
    sys.exit(app.exec_())
