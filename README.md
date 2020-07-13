# Employee_Management
従業員を管理するツール

## 21章課題：社員情報管理ツール
21章の課題：社員情報管理ツールについて説明します。  
社員情報では社員の情報を管理することができます。  
社員を新規登録、編集、削除、検索、社員のリストをCSV出力することも可能です。    

### 社員一覧ページでできること  
以下のページにアクセスすることができます。  

①社員編集ページ  
②社員削除  
③新規社員追加ページ  
④社員検索ページ  
⑤部署一覧ページ  
⑥CSVファイル出力 

### 社員編集ページでできること  
主に以下の機能があります。  

①社員情報を編集すること  

### 新規社員追加ページでできること  
主に以下の機能があります。  

①社員情報を追加すること  

### 社員検索ページでできること  
主に以下の機能があります。  

①社員情報を検索すること  

### 部署一覧ページでできること  
主に以下の機能があります。  

①部署情報を編集すること  
②部署情報を削除すること  

## 社員情報管理ツールの基本的な処理はapp.pyに保存してあります。  
### app.py

### model/database.py

### model/item.py  
### model/const.py  

## 社員情報管理ツールのHTMLは8つ存在します。  
### １、templates/employee_list.html  
  社員情報一覧ページのHTMLです。  
### ２、templates/employee_add.html  
  社員情報追加編集ページのHTMLです。  
### ３、templates/department_list.html  
  部署一覧ページのHTMLです。  
### 4、templates/department_add.html  
  部署情報追加編集ページのHTMLです。  
### 5、templates/employee_search.html  
  社員情報検索ページのHTMLです。  
### 6、templates/search_result.html  
  社員検索結果ページのHTMLです。  
### 7、templates/add_result.html  
  追加結果ページのHTMLです。  
  
## テーブル作成に使用するSQLファイルは以下の通りです。  
### employees.sql   

## 外部ライブラリを管理するファイルは以下の通りです。
### requirements.txt