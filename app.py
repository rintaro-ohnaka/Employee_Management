# coding:utf-8

from flask import Flask, flash, request, redirect, url_for, session
app = Flask(__name__)
app.config['SECRET_KEY'] = 'employee_management'
from flask import render_template
import mysql.connector
from mysql.connector import errorcode
import os
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = './static/'
ALLOWED_EXTENSIONS = {'png', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


host = 'localhost' # データベースのホスト名又はIPアドレス
username = 'root'  # MySQLのユーザ名
passwd   = 'wako19980207'    # MySQLのパスワード
dbname   = 'my_database'    # データベース名


# DB接続
def get_connection():
    cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
    cursor = cnx.cursor()
    return cursor, cnx

# 従業員データを取得し、配列に代入する
def retrieve_employees(cursor):
    employees = []
    for (employee_id, employee_name) in cursor:
        item = {"employee_id":employee_id, "employee_name":employee_name}
        employees.append(item)
    return employees

# 社員情報をSQLで取得
def get_employee_query():
    cursor, cnx = get_connection()
    employee_list = "SELECT employee_id, employee_name FROM employee_table"
    cursor.execute(employee_list)
    employees = retrieve_employees(cursor)
    return employees

# ここに社員一覧の情報を表示するロジックを書く
@app.route("/", methods=['GET', 'POST'])
def employee_list():
    employees = get_employee_query()
    params = {
    "employees" : employees
    }
    return render_template("employee_list.html", **params)


# ランダムな文字列を生成する
import random, string
def randomname(n):
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
   return ''.join(randlst)

def create_employee_image_id():
    employee_image_id = [random.choice(string.ascii_letters + string.digits) for i in range(10)]
    return ''.join(employee_image_id)

def create_department_id():
   department_id = [random.choice(string.ascii_letters + string.digits) for i in range(10)]
   return ''.join(department_id)


# 先に従業員追加の処理を実装して、そこでデータをinsertで入力する
# 従業員の新規追加ボタンの実装

@app.route("/add", methods=["GET", "POST"])
def employee_add():
    # ここではformで送信された値を受け取っている
    if "employee_image" in request.files:
        employee_id = request.form.get("employee_id", "")
        employee_name = request.form.get("employee_name", "")
        employee_age = request.form.get("employee_age", "")
        employee_gender = request.form.get("employee_gender", "")
        employee_image = request.files["employee_image"]
        employee_postal_code = request.form.get("employee_postal_code", "")
        employee_prefecture = request.form.get("employee_prefecture", "")
        employee_address = request.form.get("employee_address", "")
        department_name = request.form.get("department_name", "")
        employee_start_date = request.form.get("employee_start_date", "")
        employee_leave_date = request.form.get("employee_leave_date", "")
        # このIDにはランダムな文字列を生成して代入する、生成ロジックは別関数で作成する
        employee_image_id = create_employee_image_id()
        department_id = create_department_id()
        filename = save_filename(employee_image)
        add_employee(employee_id, employee_name, employee_age, employee_gender, employee_image_id, employee_postal_code, employee_prefecture, employee_address, department_id, employee_start_date, employee_leave_date, filename, department_name)
        # params = {
        # "employee_information" : employee_information
        # }
    else:
        flash("ようこそ、社員情報追加のページへ", "")
    # return render_template("employee_add.html", **params)
    return render_template("employee_add.html")

# 受け取った値、変数をまとめて配列にする
# def get_employee_information():
#     employee_information = []
#     return

# 画像を保存する関数
def save_filename(employee_image):
    filename = secure_filename(employee_image.filename)
    employee_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return filename

# DBに保存を実行
def add_employee(employee_id, employee_name, employee_age, employee_gender, employee_image_id, employee_postal_code, employee_prefecture, employee_address, department_id, employee_start_date, employee_leave_date, filename, department_name):
    cursor, cnx = get_connection()
    query_employee = add_query_employee_table(employee_id, employee_name, employee_age, employee_gender, employee_image_id, employee_postal_code, employee_prefecture, employee_address, department_id, employee_start_date, employee_leave_date)
    query_employee_image = add_query_employee_image_table(employee_image_id, filename)
    query_department = add_query_department_table(department_id, department_name)
    cursor.execute(query_employee)
    cursor.execute(query_employee_image)
    cursor.execute(query_department)
    cnx.commit()
    # return redirect("/")

# tableに値を保存
def add_query_employee_table(employee_id, employee_name, employee_age, employee_gender, employee_image_id, employee_postal_code, employee_prefecture, employee_address, department_id, employee_start_date, employee_leave_date):
    query_employee = f"INSERT INTO employee_table (\
    employee_id,\
    employee_name,\
    employee_age,\
    employee_gender,\
    employee_image_id,\
    employee_postal_code,\
    employee_prefecture,\
    employee_address,\
    department_id,\
    employee_start_date,\
    employee_leave_date\
    ) VALUES (\
    '{employee_id}',\
    '{employee_name}',\
    '{employee_age}',\
    '{employee_gender}',\
    '{employee_image_id}',\
    '{employee_postal_code}',\
    '{employee_prefecture}',\
    '{employee_address}',\
    '{department_id}',\
    '{employee_start_date}',\
    '{employee_leave_date}'\
    )"
    return query_employee

def add_query_employee_image_table(employee_image_id, filename):
    sql_img = "./static/" + filename
    query_employee_image = f"INSERT INTO employee_image_table (employee_image_id, employee_image, employee_image_update_date) VALUES ('{employee_image_id}', '{sql_img}', LOCALTIME())"
    return query_employee_image

def add_query_department_table(department_id, department_name):
    query_department = f"INSERT INTO department_table (department_id, department_name, department_create_date, department_update_date) VALUES ('{department_id}', '{department_name}', LOCALTIME(), LOCALTIME())"
    return query_department
