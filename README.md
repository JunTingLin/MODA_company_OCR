# MODA_company_OCR

![GitHub release (latest by date)](https://img.shields.io/github/v/release/JunTingLin/MODA_company_OCR)


[![Quality gate](https://sonarcloud.io/api/project_badges/quality_gate?project=JunTingLin_MODA_company_OCR)](https://sonarcloud.io/summary/new_code?id=JunTingLin_MODA_company_OCR)



# 專案簡易說明

本程式旨在處理和分析包含「公司基本資料表」、「營業人銷售額與稅額申報書清單(401表)」、「營業人銷售額與稅額申報書(403表)」以及「數位發展部數位產業署投標廠商聲明書」等多種格式的 PDF 文件和圖像檔案。主要功能包括：
1.	OCR辨識與關鍵字提取：對文件進行光學字符識別（OCR）處理，從中提取關鍵資訊，如統一編號、公司名稱等。
2.	資料歸檔與整理：將同一家公司的不同類型表格整理歸檔到統一編號資料夾中，便於管理與查找。
3.	數據核對：與商業司線上API進行資料核對，檢查本地提取的數據與官方資料庫中的記錄是否一致，確保資料的準確性。

# 操作說明

## 配置Google key file

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/400c2575-6c56-4742-81f6-ac40459da63f)

先到GCP選取專案新增專案

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/c44d7014-b2b9-4bfd-86e4-7f0e6b063ce5)

隨便取個專案名稱建立

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/1955099f-6151-4862-ab02-9a6a9afd80d3)

左上角確認是剛剛建立的專案名稱API和服務憑證

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/a0e768dd-345e-4b54-b4a9-b01cc0913e93)

點選 管理服務帳戶

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/df33d089-5eff-492c-acba-9fe142821461)

點選 建立服務帳戶

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/dc8e962c-f65a-4c5f-ab8f-a0d71569a881)

隨便取個服務帳戶名稱直接按完成

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/65e4cdbc-768c-4999-8794-1d18e53938a1)

即可看到一筆服務帳戶已被建立

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/fca479c3-7216-4d86-9536-21d908c81039)

點選三個點點管理金鑰

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/28e82aa6-5c9a-4cff-a954-4d6daa4bbf79)

進入金鑰頁籤後選擇 新增金鑰 金鑰類型請選擇JSON格式 並按下建立

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/9f5a003a-13ec-42c8-9205-f4265b870522)

JSON key file會自動下載到電腦內，一般window都是放在「下載」內


## 啟用Cloud Vision API服務

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/9ac52b80-6b57-456d-8983-565a6587fd31)

上面搜索框幫我選Cloud Vision API

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/84b717fb-0dff-41f0-876f-0dbae9479f95)

進入後點選 啟用

## 將此專案綁定帳單帳戶

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/498d29dd-bde3-461b-96cf-f5ca9ee9b602)

側邊攔點選 帳單

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/ee375bbc-794e-4508-bf7a-e8371c62fea1)

這邊將我們的專案綁定到帳單帳戶設定帳戶

綁定後 需稍等5~10分鐘再開始使用程式

## 使用程式-UI版本

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/e34edd0e-32ac-4f33-b27d-bf057a3df992)

將打包的資料夾解壓縮 看到的應該會長這樣，點選app.exe來啟動程式

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/3c090ca7-9ffc-477a-82af-d5b411911bbd)

啟動後請先點選 選擇金鑰檔案 幫我選擇剛剛在GCP下載下來的JSON。

追加: 下此再次啟動程式，會加載上一次的key file 位置

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/a3ee7992-c594-480e-88cc-d4744021ad96)

選擇要辨識的多張圖檔或pdf 檔案，這邊示範選擇一個pdf檔。

追加: 將檔案filter設定*.png *.jpg *.pdf一起，不用分開了

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/c815b6bc-88af-4d09-a51c-edc4405463d4)

假如放錯檔案，也可點選它在按下移除

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/cbb97cc7-d645-43b6-b72e-58cb837df41b)

選擇輸出位置，預設是您使用者桌面下的ocr_result資料夾，會自動幫你建立

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/8a00f0a7-f39f-4efc-b982-490ecc74e2b1)

點選step1按鈕即可使執行辨識和歸檔作業

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/521daa12-6bf1-4bc8-a552-7f4e30d8fbc5)

Step1處理完成 彈出對話框

點選 開啟輸出資料夾按鈕 查看

可以發現各種表格已正確轉向根據統編自動歸檔，並產生output.json

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/a462c789-dc73-4db2-a8c7-69216c94f4af)

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/4b458a99-a469-471d-803e-d6ac013b6e45)

Output.json如上，紀錄每一張(頁)圖檔的擷取結果，多張跨頁也有正常處理。

追加: OCR擷取文字也放入output.json

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/3e82f04d-fb5b-42e1-b3f1-5454a90d64de)

接下來點選step2按鈕

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/2214211c-ed81-4c46-a1d0-557d9990fb14)

跑完之後一樣會出現完成的對話框

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/aea4ffe1-c81b-4643-a4df-9ce123fd76b2)

再次開啟輸出資料夾，可以發現多了一個api_data.json

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/fa6fc62c-0e71-4451-8dbe-56405b5cf007)

api_data.json的格式如上，以公司為單位自成一區塊，並且判斷該公司的所有表個和遠端商業司API資料「公司名稱」和「負責人姓名」是否allMatch，假如並非allMatch呈現的內容以遠端API抓到的資料為主。


追加: 商業司api回傳也放入api_data.json

## 使用程式-CMD版本

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/0d6c5b2f-fccb-4d41-855d-a4a634e30287)

將打包資料解壓縮，此時您需要將從GCP下載下來的key手動改名成service-account-file.json，並且放置在跟main.exe同一層目錄底下

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/b3808b6c-2ab8-4d58-9546-63fd5a90bcfb)

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/3489803f-c1a1-45c0-9617-1a0e7f804ad7)

在上面的路徑列直接改成cmd並且敲Enter鍵，即會以此路徑開一個新的cmd彈窗，當然您想直接透過cd 指定切換到程式根目錄底下也是可以。

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/f4965bec-ee5d-47ad-ad49-d36f1c950dfe)

確認cmd彈窗是程式目錄底下後，敲擊main，可以發現出現usage使用說明，另外也告知您error，因為使用方式不對

`usage: main [-h] files output_folder`

使用main -h ，可以看到相關help說明告知您如何操作

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/7e2b9c7e-f482-45dd-8bd1-caceeda26487)

main 後面第一個參數接檔案路徑(當有多個檔案需要進行OCR，請使用逗號隔開) 第二個參數接輸出資料夾目錄

`main C:\Users\junting\Desktop\MODA_company_OCR\temp\test1\scan_test.pdf,C:\Users\junting\Desktop\MODA_company_OCR\temp\test1\基本資料_16590299_頁面_1.jpg,C:\Users\junting\Desktop\MODA_company_OCR\temp\test1\基本資料_16590299_頁面_2.jpg C:\Users\junting\Desktop\MODA_company_OCR\data`
(使用絕對路徑或相對路經均可以被接受)

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/819a0c09-a8c5-4ab7-b9cc-12b89ce2c611)

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/40069587-1452-45d4-89de-1f24e1a88f4c)

按下Enter即開始執行，Cmd上面也會條列出現在的進度狀況



# 開發小筆記

## 程式碼品質檢測

### 使用本地部屬SonarQube 

SonarQube Server:

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/a02feee9-a6f7-4737-a6a7-8db8e0eb355c)


docker hub Supported tags: https://hub.docker.com/_/sonarqube

`docker run -d --name sonarqube -p 9000:9000 sonarqube:9-community`

此時最新版是sonarqube10，但後續要裝的報表pdf插件不支援

SonarQube Scanner:

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/97cc18a8-c2a7-48b8-84bf-551494a323b5)


`docker run --rm -e SONAR_HOST_URL="http://host.docker.internal:9000" -e SONAR_LOGIN="sqp_d4d1b9c7210b0c1c393dfd989b453dd39d2d3323" -v "C:\Users\junting\Desktop\MODA_company_OCR:/usr/src" sonarsource/sonar-scanner-cli -D"sonar.projectKey=MODA_company_OCR" -D"sonar.sources=."`

SONAR_LOGIN裡面貼的是http://localhost:9000/  新專案產生的金鑰

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/9606e10f-c423-4fbc-b965-a6277ab2142d)


掃完後即可以在網頁Server上查看結果


#### 安裝pdf報表插件

jar檔下載地址: https://gitee.com/zzulj/sonar-pdf-plugin/releases

`docker cp C:\Users\junting\Desktop\sonar-pdfreport-plugin-4.0.1.jar 540a02ed9326:/opt/sonarqube/extensions/plugins/`

將jar檔複製到容器指定的位置

`docker ps`

`540a02ed9326`

`docker restart 540a02ed9326`

重新啟動容器

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/2178c0ef-0ea0-4d32-8a57-46e4b2fd42fe)

這邊記得將SonarQube 的username 和 password 填進來

`docker exec -u root -it 540a02ed9326 /bin/bash`

使用root的身分進入容器互動介面

root@540a02ed9326:/opt/sonarqube# chmod 777 /opt/sonarqube/

這裡踩過坑，記得要開放權限，免得pdf檔案寫不進去

![image](https://github.com/JunTingLin/MODA_company_OCR/assets/92431095/44266c96-15ff-41b0-8b64-cec726224d0d)

此時這裡就可以下載pdf報表了

### 使用本地部屬SonarCloud 

超簡單，僅需去SonarCloud 註冊帳號，選擇github公開repo，私人repo才要收費

有新的commit產生才會重新analysis






