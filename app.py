import sys
import os
import subprocess
import json
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from worker_threads import WorkerThread




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

        # 加載先前保存的金鑰文件路徑
        self.load_key_file_path()

        # 設置按鈕的功能
        self.window.button_choose_file.clicked.connect(self.choose_file)
        self.window.button_remove_file.clicked.connect(self.remove_file)
        self.window.button_choose_output_folder.clicked.connect(self.choose_output_folder)
        self.window.button_open_output_folder.clicked.connect(self.open_output_folder)
        self.window.button_step1.clicked.connect(self.execute_step1)
        self.window.button_step2.clicked.connect(self.execute_step2)

        # 為選擇金鑰文件的按鈕設置點擊事件
        self.window.button_choose_key_file.clicked.connect(self.choose_key_file)

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
        file_path, _ = QFileDialog.getOpenFileName(self, "選擇文件", "", "所有支持的檔案 (*.png *.jpg *.jpeg *.pdf);;圖片檔案 (*.png *.jpg *.jpeg);;PDF 檔案 (*.pdf)")
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

        # 初始化並啟動 WorkerThread
        self.worker_thread = WorkerThread(output_folder_path, file_paths)
        self.worker_thread.error_occurred.connect(self.handle_error)
        self.worker_thread.finished_processing.connect(self.handle_processed_data) 
        self.worker_thread.update_progress.connect(self.window.progressBar.setValue)
        self.worker_thread.update_status.connect(lambda message: self.window.label_status.setText(message))
        self.worker_thread.start()

    def execute_step2(self):
        output_json_path = os.path.join(self.output_folder_path, 'output.json')
        summary_output_json_path = os.path.join(self.output_folder_path, 'summary_output.json')

        self.worker_thread = WorkerThread(self.output_folder_path, [])
        self.worker_thread.finished_processing.connect(self.handle_processed_data)
        self.worker_thread.update_progress.connect(self.window.progressBar.setValue)
        self.worker_thread.update_status.connect(lambda message: self.window.label_status.setText(message))
        self.worker_thread.run_step2(output_json_path, summary_output_json_path)

    def handle_processed_data(self):
        # 更新進度條到 100% 並顯示完成提示
        self.window.label_status.setText("處理完成！")
        self.window.progressBar.setValue(100)
        QMessageBox.information(self, "完成", "處理完成！")

    def choose_key_file(self):
        # 打開文件選擇對話框
        key_file_path, _ = QFileDialog.getOpenFileName(self, "選擇金鑰文件", "", "JSON 檔案 (*.json)")
        if key_file_path:
            # 將文件路徑設置到編輯框
            self.window.lineEdit_keyfile_path.setText(key_file_path)
            
            # 設置環境變數
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key_file_path
            print("金鑰文件已設置: " + key_file_path)

            # 保存金鑰文件路徑
            self.save_key_file_path(key_file_path)

    def handle_error(self, error_message):
        self.window.label_status.setText("發生錯誤！")
        self.window.progressBar.setValue(0)
        QMessageBox.critical(self, "錯誤", error_message)

    def load_key_file_path(self):
        try:
            with open('key_file_path.json', 'r') as file:
                data = json.load(file)
                key_file_path = data.get('key_file_path')
                if key_file_path:
                    self.window.lineEdit_keyfile_path.setText(key_file_path)
                    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key_file_path
                    print("金鑰文件已設置: " + key_file_path)
        except (FileNotFoundError, json.JSONDecodeError):
            print("未找到先前的金鑰文件路徑")

    def save_key_file_path(self, path):
        data = {'key_file_path': path}
        with open('key_file_path.json', 'w') as file:
            json.dump(data, file)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = AppWindow()
    sys.exit(app.exec_())
