import argparse
from progress_updater import CommandLineUpdater
from worker_threads import WorkerThread


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='OCR處理程序')
    parser.add_argument('files', nargs='+', help='檔案路徑，空格分隔')
    parser.add_argument('-o', '--output_folder', required=True, help='輸出資料夾路徑')
    parser.add_argument('-c', '--unified_number', help='統一編號')
    parser.add_argument('-a', '--archive', action='store_true', help='系統自動分類')
    parser.add_argument('-api', '--call_api', action='store_true', help='調用商業司API')
    parser.add_argument('-f', '--rename_files', action='store_true', help='檔名按照規則修改')
    parser.add_argument('-s', '--summary', action='store_true', help='產出summary.json')
    parser.add_argument('-e', '--company_name_en', help='公司英文名稱')

    args = parser.parse_args()

    updater = CommandLineUpdater()
    # 解析命令列參數...
    worker = WorkerThread(
        args.files, args.output_folder, updater,
        args.unified_number, args.archive, args.call_api,
        args.rename_files, args.summary, args.company_name_en
        )
    # 啟動 worker thread
    worker.start()
    # 等待 worker thread 完成
    worker.wait()