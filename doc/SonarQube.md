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