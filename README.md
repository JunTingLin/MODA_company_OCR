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






