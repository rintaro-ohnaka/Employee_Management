# coding:utf-8

from flask import Flask
app = Flask(__name__)
from flask import render_template
from flask import request
import mysql.connector
from mysql.connector import errorcode


host = 'localhost' # データベースのホスト名又はIPアドレス
username = 'root'  # MySQLのユーザ名
passwd   = 'wako19980207'    # MySQLのパスワード
dbname   = 'my_database'    # データベース名


# DB接続
def get_connection():
    cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
    cursor = cnx.cursor()
    return cursor, cnx

def retrieve_employees(cursor):
    employees = []
    for (employee_id, employee_name) in cursor:
        item = {"employee_id":employee_id, "employee_name":employee_name}
        employees.append(item)
    return employees

# 社員情報をSQLで取得
def get_employee_query():
    cursor, cnx = get_connection()
    employee_list = ""
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