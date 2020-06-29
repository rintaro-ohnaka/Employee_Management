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

@app.route("/", methods=['GET', 'POST'])
def employee_list():

    try:
        cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
        cursor = cnx.cursor()

        # SQL文を書いてデータを引っ張ってくる
        employee_list = ""
        # cursorの中にSQL文で取ってきたデータを入れるイメージ
        cursor.execute(employee_list)

        employees = []
        for (employee_id, employee_name) in cursor:
            item = {"employee_id":employee_id, "employee_name":employee_name}
            employees.append(item)

        params = {
        "employees" : employees
        }

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("ユーザ名かパスワードに問題があります。")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("データベースが存在しません。")
        else:
            print(err)
    else:
        cnx.close()

    return render_template("employee_list.html", **params)