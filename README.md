# MODA_company_OCR

![GitHub release (latest by date)](https://img.shields.io/github/v/release/JunTingLin/MODA_company_OCR)


[![Quality gate](https://sonarcloud.io/api/project_badges/quality_gate?project=JunTingLin_MODA_company_OCR)](https://sonarcloud.io/summary/new_code?id=JunTingLin_MODA_company_OCR)

# 目錄
+ [專案簡易說明](#專案簡易說明)
+ [GUI/CMD](#guicmd-說明)
+ [使用範例Demo](https://www.youtube.com/watch?v=_2ykBWYJUKA&ab_channel=%E6%9E%97%E4%BF%8A%E9%9C%86)
+ [Google key file 申請與配置](./doc/Cloud%20Vision%20API.md)
+ [程式碼品質檢測SonarQube](./doc/SonarQube.md)

# 專案簡易說明

本程式旨在處理和分析包含「公司基本資料表」、「營業人銷售額與稅額申報書清單(401表)」、「營業人銷售額與稅額申報書(403表)」、「數位發展部數位產業署投標廠商聲明書」、「支票」、「ISO/IEC 27001證書」以及「投標報價單」多種格式的 PDF 文件和圖像檔案。

主要功能包括：
1.	OCR辨識與關鍵字提取：對文件進行光學字符識別（OCR）處理，依據不同檔案類型從中提取關鍵資訊。
2. 資料整理: 如有需要會依據ocr辨識的結果，進一部查表填充，使資料完整。
3. 資料自動歸檔：支援同一家公司資料和不同家公司資料批次匯入系統，按照ocr辨識的統一編號(ocr_id)或是使用者鍵入的統一編號(cid)來歸檔。
4. 檔名自動命名:  檔名自動按照文件類別重命名。
5. 數據核對：與商業司線上API進行資料核對，檢查本地提取的數據與官方資料庫中的記錄是否一致。

# GUI/CMD 說明

## GUI 截圖


## 命令行參數

以下是本程式支援的命令行參數列表：

| 參數       | 描述                                                         |
|------------|--------------------------------------------------------------|
| `-o`       | 指定輸出資料夾的路徑，所有處理後的文件將保存在此路徑。      |
| `-c`       | 統一編號，將這個統一編號加入到輸出的 JSON 文件中。          |
| `-a`       | 啟用自動分類功能，按照統一編號或文件類型對文件進行分類。      |
| `-api`     | 啟用與商業司API的連接，用於核對和驗證抽取的數據。            |
| `-f`       | 根據規則重新命名文件，以便於檔案管理和檢索。                  |
| `-s`       | 產生統計摘要文件，JSON格式，匯總處理結果的概要信息。    |
| `-e`       | 提供公司的英文名稱，並在27001證書處理過程中比對        |

### 使用範例

```bash
main 001.jpg 002.jpg -api -f -s -o ./path/12345678 -c 12345678 -e "Taiwan Technology Inc."
```

# 各文件辨識資料




