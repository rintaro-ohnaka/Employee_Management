# coding:utf-8

from flask import Flask, flash, request, redirect, url_for, session, Response, make_response
app = Flask(__name__)
app.config['SECRET_KEY'] = 'employee_management'
from flask import render_template
import mysql.connector
from mysql.connector import errorcode
import os
import random, string
from werkzeug.utils import secure_filename
import model.database as db

UPLOAD_FOLDER = './static/'
ALLOWED_EXTENSIONS = {'png', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# host = 'localhost' # データベースのホスト名又はIPアドレス
# username = 'root'  # MySQLのユーザ名
# passwd   = 'wako19980207'    # MySQLのパスワード
# dbname   = 'my_database'    # データベース名

# これは移す
# DB接続
# def get_connection():
#     cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
#     cursor = cnx.cursor()
#     return cursor, cnx

# 移動
# 従業員データを取得し、配列に代入する
# def retrieve_employees(cursor):
#     employees = []
#     for (id, employee_id, employee_name, employee_age, employee_gender, employee_image_id, employee_postal_code, employee_prefecture, employee_address, department_id, employee_start_date, employee_leave_date, employee_update_date) in cursor:
#         item = { "id":id, "employee_id":employee_id, "employee_name":employee_name, "employee_age":employee_age, "employee_gender":employee_gender, "employee_image_id":employee_image_id, "employee_postal_code":employee_postal_code, "employee_prefecture":employee_prefecture, "employee_address":employee_address, "department_id":department_id, "employee_start_date":employee_start_date, "employee_leave_date":employee_leave_date, "employee_update_date":employee_update_date}
#         employees.append(item)
#     return employees

# 移動
# 社員情報をSQLで取得
# def get_employee_query():
#     cursor, cnx = db.get_connection()
#     employee_list = "SELECT * FROM employee_table"
    
#     cursor.execute(employee_list)
#     employees = retrieve_employees(cursor)
#     return employees

# ここに社員一覧の情報を表示するロジックを書く
@app.route("/", methods=['GET', 'POST'])
def employee_list():
    employees = db.get_employee_query()
    
    params = {
    "employees" : employees,
    }
    return render_template("employee_list.html", **params)


# ランダムな文字列を生成する
# import random, string
# def randomname(n):
#    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
#    return ''.join(randlst)

def create_employee_image_id():
    employee_image_id = [random.choice(string.ascii_letters + string.digits) for i in range(10)]
    return ''.join(employee_image_id)

def create_department_id():
    department_id = [random.choice(string.ascii_letters + string.digits) for i in range(10)]
    return ''.join(department_id)




# 新規追加の画面を表示する関数
@app.route("/show_add_page", methods=["GET", "POST"])
def show_add_page():
    flash("ようこそ、社員情報追加のページへ", "")
    # ここで部署のリストを渡している
    department = db.get_department_query()
    params = {
    "department" : department
    }
    return render_template("employee_add.html", **params)

# ここでまとめて社員情報を追加する関数を定義しておく
@app.route("/add_employee", methods=["GET", "POST"])
def add_employee():
    employee_id, employee_name, employee_age, employee_gender, employee_image, employee_postal_code, employee_prefecture, employee_address, department_name_id, employee_start_date, employee_leave_date, department_name, department_id = request_add_employee()
    check_add_employee(employee_id, employee_name, employee_age, employee_gender, employee_image, employee_postal_code, employee_prefecture, employee_address, department_id, employee_start_date, employee_leave_date, department_name)
    return render_template("result.html")


# 新規追加のリクエストを受ける関数
# @app.route("/request_add_employee", methods=["GET", "POST"])
def request_add_employee():
    employee_id = request.form.get("employee_id", "")
    employee_name = request.form.get("employee_name", "")
    employee_age = request.form.get("employee_age", "")
    employee_gender = request.form.get("employee_gender", "")
    employee_image = request.files.get("employee_image", "")
    employee_postal_code = request.form.get("employee_postal_code", "")
    employee_prefecture = request.form.get("employee_prefecture", "")
    employee_address = request.form.get("employee_address", "")
    department_name_id = request.form.get("department_name", "")
    employee_start_date = request.form.get("employee_start_date", "")
    employee_leave_date = request.form.get("employee_leave_date", "")
    department_name, department_id = check_department(department_name_id)
    # department_array = department_name_id.split("&")
    # department_name = department_array[0]
    # department_id = department_array[1]
    return employee_id, employee_name, employee_age, employee_gender, employee_image, employee_postal_code, employee_prefecture, employee_address, department_name_id, employee_start_date, employee_leave_date, department_name, department_id


# formの入力に不備がないかのチェック関数
def check_add_employee(employee_id, employee_name, employee_age, employee_gender, employee_image, employee_postal_code, employee_prefecture, employee_address, department_id, employee_start_date, employee_leave_date, department_name):
    # とりあえず、formで値が送られているかチャックするロジックを書いてみよう
    if employee_id == "" or employee_name == "" or employee_age == "" or employee_postal_code == "" or employee_address == "" or employee_start_date == "" or department_name == "":
    # if employee_id == "" or employee_name == "" or employee_age == "" or employee_gender == "" or employee_image == "" or employee_postal_code == "" or employee_prefecture == "" or employee_address == "" or employee_start_date == "" or department_name == "":
        flash("入力される情報に不備があったため、登録に失敗しました")
    elif not employee_age.isdecimal():
        flash("年齢は数字で入れてくれ", "")
    elif not employee_postal_code.isdecimal():
        flash("郵便番号は数字だけ入れてくれ", "")
    else:
        # execute_add_employee(employee_id, employee_name, employee_age, employee_gender, employee_image, employee_postal_code, employee_prefecture, employee_address, department_id, employee_start_date, employee_leave_date, department_name)
        employee_image_id = create_employee_image_id()
        filename = save_filename(employee_image)
        execute_add_employee(employee_id, employee_name, employee_age, employee_gender, employee_image_id, employee_postal_code, employee_prefecture, employee_address, department_id, employee_start_date, employee_leave_date, filename, department_name)
        flash("新規追加することに成功したよ！")



# 画像を保存する関数
def save_filename(employee_image):
    filename = secure_filename(employee_image.filename)
    employee_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return filename

# DBに保存を実行
def execute_add_employee(employee_id, employee_name, employee_age, employee_gender, employee_image_id, employee_postal_code, employee_prefecture, employee_address, department_id, employee_start_date, employee_leave_date, filename, department_name):
    cursor, cnx = db.get_connection()
    query_employee = db.add_query_employee_table(employee_id, employee_name, employee_age, employee_gender, employee_image_id, employee_postal_code, employee_prefecture, employee_address, department_id, employee_start_date, employee_leave_date)
    query_employee_image = db.add_query_employee_image_table(employee_image_id, filename)
    cursor.execute(query_employee)
    cursor.execute(query_employee_image)
    cnx.commit()
    # return redirect("/")

# 移動
# tableに値を保存
# def add_query_employee_table(employee_id, employee_name, employee_age, employee_gender, employee_image_id, employee_postal_code, employee_prefecture, employee_address, department_id, employee_start_date, employee_leave_date):
#     query_employee = f"INSERT INTO employee_table (\
#     employee_id,\
#     employee_name,\
#     employee_age,\
#     employee_gender,\
#     employee_image_id,\
#     employee_postal_code,\
#     employee_prefecture,\
#     employee_address,\
#     department_id,\
#     employee_start_date,\
#     employee_leave_date\
#     ) VALUES (\
#     '{employee_id}',\
#     '{employee_name}',\
#     '{employee_age}',\
#     '{employee_gender}',\
#     '{employee_image_id}',\
#     '{employee_postal_code}',\
#     '{employee_prefecture}',\
#     '{employee_address}',\
#     '{department_id}',\
#     '{employee_start_date}',\
#     '{employee_leave_date}'\
#     )"
#     return query_employee

# 移動
# def add_query_employee_image_table(employee_image_id, filename):
#     sql_img = "./static/" + filename
#     query_employee_image = f"INSERT INTO employee_image_table (employee_image_id, employee_image, employee_image_update_date) VALUES ('{employee_image_id}', '{sql_img}', LOCALTIME())"
#     return query_employee_image

# 移動
# def add_query_department_table(department_id, department_name):
#     query_department = f"INSERT INTO department_table (department_id, department_name, department_create_date, department_update_date) VALUES ('{department_id}', '{department_name}', LOCALTIME(), LOCALTIME())"
#     return query_department






# 社員情報の編集画面を表示
@app.route("/show_edit_employee", methods=["GET", "POST"])
def show_edit_employee():
    cursor, cnx = db.get_connection()
    # id = int(request.form.get("id", ""))

    id = request.form.get("id", "")
    # if id == str:
    #     id = int(id)

    # 部署一覧を取得している
    department = db.get_department_query()
    # 選択した社員の全てのステータスをここで取得
    get_query_employee_information = f"SELECT id, employee_id, employee_name, employee_age, employee_gender, employee_table.employee_image_id, employee_postal_code, employee_prefecture, employee_address, employee_table.department_id, employee_start_date, employee_leave_date, employee_update_date, employee_image, department_table.department_name FROM employee_table JOIN employee_image_table ON employee_table.employee_image_id = employee_image_table.employee_image_id JOIN department_table ON employee_table.department_id = department_table.department_id WHERE employee_table.id = {id} "
    # get_query_employee_information = f"SELECT id, employee_id, employee_name, employee_age, employee_gender, employee_table.employee_image_id, employee_postal_code, employee_prefecture, employee_address, department_id, employee_start_date, employee_leave_date, employee_update_date, employee_image FROM employee_table JOIN employee_image_table ON employee_table.employee_image_id = employee_image_table.employee_image_id WHERE employee_table.id = {id} "
    # get_query_employee_information = f"SELECT * FROM employee_table WHERE id = {id} "
    cursor.execute(get_query_employee_information)

    employees = db.retrieve_edit_employee(cursor)
    
    
    params = {
    "employees" : employees,
    "department" : department
    }

    return render_template("employee_add.html", **params)





# 社員情報を編集する機能をまとめて関数になる
@app.route("/edit_employee", methods=["GET", "POST"])
def edit_employee():
    id, employee_id, employee_name, employee_age, employee_gender, employee_image, employee_image_id, employee_postal_code, employee_prefecture, employee_address, employee_start_date, employee_leave_date, department_name, department_id = request_edit_employee()
    # employee_image_id = create_employee_image_id()
    # filename = save_filename(employee_image)
    check_edit_employee(id, employee_id, employee_name, employee_age, employee_gender, employee_image, employee_image_id, employee_postal_code, employee_prefecture, employee_address, department_id, employee_start_date, employee_leave_date, department_name)
    return render_template("result.html")

# 社員情報編集時のリクエストを受けとる関数
def request_edit_employee():
    id = int(request.form.get("id", ""))
    employee_id = request.form.get("employee_id", "")
    employee_name = request.form.get("employee_name", "")
    employee_age = request.form.get("employee_age", "")
    employee_gender = request.form.get("employee_gender", "")
    employee_image = request.files.get("employee_image", "")
    employee_image_id = request.form.get("employee_image_id", "")
    employee_postal_code = request.form.get("employee_postal_code", "")
    employee_prefecture = request.form.get("employee_prefecture", "")
    employee_address = request.form.get("employee_address", "")
    department_name_id = request.form.get("department_name", "")
    employee_start_date = request.form.get("employee_start_date", "")
    employee_leave_date = request.form.get("employee_leave_date", "")

    department_name, department_id = check_department(department_name_id)
    # if department_name_id == "":
    #     department_name = ""
    #     department_id = ""
    # else:
    #     department_array = department_name_id.split("&")
    #     department_name = department_array[0]
    #     department_id = department_array[1]
    return id, employee_id, employee_name, employee_age, employee_gender, employee_image, employee_image_id, employee_postal_code, employee_prefecture, employee_address, employee_start_date, employee_leave_date, department_name, department_id

# 部署が入力されているかのチェック関数
def check_department(department_name_id):
    if department_name_id == "":
        department_name = ""
        department_id = ""
    else:
        department_array = department_name_id.split("&")
        department_name = department_array[0]
        department_id = department_array[1]
    return department_name, department_id


# 実際に変更を実行している関数
# def execute_edit_employee(id, employee_id, employee_name, employee_age, employee_gender, employee_image, employee_postal_code, employee_prefecture, employee_address, employee_start_date, employee_leave_date, department_name, department_id):
#     cursor, cnx = db.get_connection()
#     employee_image_id = create_employee_image_id()
#     filename = save_filename(employee_image)

#     query_update_employee = db.get_query_update_employee(id, employee_id, employee_name, employee_age, employee_gender, employee_image_id, employee_postal_code, employee_prefecture, employee_address, employee_start_date, employee_leave_date, department_name, department_id)
#     cursor.execute(query_update_employee)
#     cnx.commit()
#     return

# こっちで新しいの作ってみる
def execute_edit_employee(id, employee_id, employee_name, employee_age, employee_gender, employee_image, employee_image_id, employee_postal_code, employee_prefecture, employee_address, employee_start_date, employee_leave_date, department_name, department_id):
    cursor, cnx = db.get_connection()
    # employee_image_id = create_employee_image_id()
    # query_update = db.create_query_update_employee(id, employee_id, employee_name, employee_age, employee_gender, employee_image, employee_postal_code, employee_prefecture, employee_address, employee_start_date, employee_leave_date, department_name, department_id)
    query_update = get_query_edit_employee(id, employee_id, employee_name, employee_age, employee_gender, employee_image, employee_image_id, employee_postal_code, employee_prefecture, employee_address, employee_start_date, employee_leave_date, department_name, department_id)
    if employee_image.filename != "":
        filename = save_filename(employee_image)
        query_update_image = db.create_query_update_image(filename, employee_image_id)
        cursor.execute(query_update_image)

    # query_update_department = db.create_query_update_department(department_name, department_id)
    cursor.execute(query_update)

    # cursor.execute(query_update_department)
    cnx.commit()
    return

def get_query_edit_employee(id, employee_id, employee_name, employee_age, employee_gender, employee_image, employee_image_id, employee_postal_code, employee_prefecture, employee_address, employee_start_date, employee_leave_date, department_name, department_id):
    query_update = db.create_query_update_employee(id, employee_id, employee_name, employee_age, employee_gender, employee_image, employee_image_id, employee_postal_code, employee_prefecture, employee_address, employee_start_date, employee_leave_date, department_name, department_id)
    # if employee_image.filename != "":
    #     employee_image_id = create_employee_image_id()
    #     query_update += f", employee_image_id = '{employee_image_id}'"
    #     filename = save_filename(employee_image)
    if employee_gender != "":
        query_update += f", employee_gender = '{employee_gender}'"
    if employee_prefecture != "":
        query_update += f", employee_prefecture = '{employee_prefecture}'"
    if department_id != "":
        query_update += f", department_id = '{department_id}' "

    query_update += f" WHERE id = {id}"
    return query_update

# 移動
# updateのクエリ取得
# def get_query_update_employee(id, employee_id, employee_name, employee_age, employee_gender, employee_image_id, employee_postal_code, employee_prefecture, employee_address, employee_start_date, employee_leave_date, department_name, department_id):
#     query_update_employee = f"UPDATE employee_table SET \
#     employee_id = '{employee_id}', \
#     employee_name = '{employee_name}', \
#     employee_age = '{employee_age}', \
#     employee_gender = '{employee_gender}', \
#     employee_image_id = '{employee_image_id}', \
#     employee_postal_code = '{employee_postal_code}', \
#     employee_prefecture = '{employee_prefecture}', \
#     employee_address = '{employee_address}', \
#     department_id = '{department_id}', \
#     employee_start_date = '{employee_start_date}', \
#     employee_leave_date = '{employee_leave_date}' \
#     WHERE id = {id} "
#     return query_update_employee

# 編集時のform入力に不備がないかのチェック関数
def check_edit_employee(id, employee_id, employee_name, employee_age, employee_gender, employee_image, employee_image_id, employee_postal_code, employee_prefecture, employee_address, department_id, employee_start_date, employee_leave_date, department_name):
    # とりあえず、formで値が送られているかチャックするロジックを書いてみよう
    if employee_id == "" or employee_name == "" or employee_age == "" or employee_postal_code == "" or employee_address == "" or employee_start_date == "" or department_name == "":
    # if employee_id == "" or employee_name == "" or employee_age == "" or employee_gender == "" or employee_image == "" or employee_postal_code == "" or employee_prefecture == "" or employee_address == "" or employee_start_date == "":
        flash("入力される情報に不備があったため、登録に失敗しました", "")
    elif not employee_age.isdecimal():
        flash("年齢は数字で入れてくれ", "")
    elif not employee_postal_code.isdecimal():
        flash("郵便番号は数字だけ入れてくれ", "")
    else:
        execute_edit_employee(id, employee_id, employee_name, employee_age, employee_gender, employee_image, employee_image_id, employee_postal_code, employee_prefecture, employee_address, employee_start_date, employee_leave_date, department_name, department_id)
        flash("編集することに成功したよ！", "")



# 社員情報を削除
@app.route("/delete_employee", methods=["GET", "POST"])
def delete_employee():
    cursor, cnx = db.get_connection()
    id = request.form.get("id", "")
    # employee_id = request.form.get("employee_id", "")

    get_query_delete_employee = f"DELETE FROM employee_table WHERE id = {id} "
    # get_query_delete_employee = f"DELETE FROM employee_table WHERE employee_id = '{employee_id}' "
    cursor.execute(get_query_delete_employee)
    cnx.commit()

    return redirect("/")




# 移動
# 部署を受け取る
# def retrieve_department(cursor):
#     department = []
#     for (department_id, department_name) in cursor:
#         item = {"department_id":department_id, "department_name":department_name}
#         department.append(item)
#     return department

# 移動
# SQL文を取得
# def get_department_query():
#     cursor, cnx = get_connection()
#     department_list = "SELECT department_id, department_name FROM department_table"
#     cursor.execute(department_list)
#     department = retrieve_department(cursor)
#     return department

# 部署の一覧を表示
@app.route("/department", methods=["GET", "POST"])
def department_list():
    department = db.get_department_query()
    params = {
    "department" : department
    }
    return render_template("department_list.html", **params)


# 部署の追加と編集どちらも一つの関数で表現してみる
@app.route("/add_edit_department", methods=["GET", "POST"])
def add_edit_department():
    change_department_name = request.form.get("change_department_name", "")
    department_name = request.form.get("department_name", "")
    if change_department_name != "" and department_name != "":
        db.change_department(change_department_name, department_name)
        flash("部署の編集に成功したよ")
    elif change_department_name == "":
        flash("部署名が入力されてないよ")
    else:
        create_department(change_department_name)
        flash("部署の新規追加に成功したよ")
    return render_template("result.html")

# 部署のリストから編集ボタンか新規追加を押した時、編集ページに飛ぶための関数
@app.route("/connect_add_edit_department", methods=["GET", "POST"])
def connect_add_edit_department():
    department_name = request.form.get("department_name", "")
    return render_template("department_add.html", department_name=department_name)


# 移動
# 部署名の編集
# def change_department(change_department_name, department_name):
#     cursor, cnx = get_connection()
#     # update文
#     get_query_update_department = f"UPDATE department_table SET department_name = '{change_department_name}' WHERE department_name = '{department_name}' "
#     cursor.execute(get_query_update_department)
#     cnx.commit()

# 移動
# 部署の新規作成
def create_department(change_department_name):
    cursor, cnx = db.get_connection()
    department_id = create_department_id()
    # insert文
    get_query_create_department = f"INSERT INTO department_table (department_id, department_name) VALUES ('{department_id}', '{change_department_name}') "
    cursor.execute(get_query_create_department)
    cnx.commit()

# 部署の削除
@app.route("/delete_department", methods=["GET", "POST"])
def delete_department():
    cursor, cnx = db.get_connection()
    department_name = request.form.get("department_name", "")
    get_query_delete_department = f"DELETE FROM department_table WHERE department_name = '{department_name}' "
    cursor.execute(get_query_delete_department)
    cnx.commit()
    return redirect("/department")



# 社員情報一覧から検索画面にページを遷移
@app.route("/search", methods=["GET", "POST"])
def link_search_employee():
    department = db.get_department_query()
    params = {
    "department" : department
    }
    return render_template("employee_search.html", **params)

# 移動
# 入力された値の情報を元に条件分岐
# def get_query_search_employee(get_query_search_employee_table, department_name, search_employee_id, search_employee_name):
#     if department_name != "":
#         get_query_search_employee_table += f" AND department_name = '{department_name}'"
#     if search_employee_id != "":
#         get_query_search_employee_table += f" AND employee_id = '{search_employee_id}'"
#     if search_employee_name != "":
#         get_query_search_employee_table += f" AND employee_name LIKE '%{search_employee_name}%'"
#     return get_query_search_employee_table

# 移動
# 検索した従業員データを取得し、配列に代入する
# def retrieve_serarch_employees(cursor):
#     search_employees = []
#     for (id, employee_id, employee_name, department_name) in cursor:
#         item = {"id":id, "employee_id":employee_id, "employee_name":employee_name, "department_name":department_name}
#         search_employees.append(item)
#     return search_employees


# 社員情報の入力を受け取る
def get_request_employee():
    department_name = request.form.get("department_name", "")
    search_employee_id = request.form.get("search_employee_id", "")
    search_employee_name = request.form.get("search_employee_name", "")
    return department_name, search_employee_id, search_employee_name

#社員情報検索
@app.route("/search_employee", methods=["GET", "POST"])
def employee_search():
    cursor, cnx = db.get_connection()
    department_name, search_employee_id, search_employee_name = get_request_employee()

    get_query_search_employee_table = "SELECT id, employee_id, employee_name, department_name FROM employee_table JOIN department_table ON employee_table.department_id = department_table.department_id WHERE employee_id IS NOT NULL"
    get_query_search_employee_table = db.get_query_search_employee(get_query_search_employee_table, department_name, search_employee_id, search_employee_name)

    cursor.execute(get_query_search_employee_table)
    search_employees = db.retrieve_serarch_employees(cursor)
    if len(search_employees) == 0:
        flash("登録されている社員がいません", "")
    else:
        flash("検索結果はこちらになります", "")
    return render_template("search_result.html", search_employees=search_employees)




# ここでとりあえず、csvとしてレスポンス（ブラウザでダウンロードする）ことはできた
# 全社員情報をcsv出力する
@app.route('/download', methods=["GET", "POST"])
def download():

    cursor, cnx = db.get_connection()
    csv_employees = db.get_csv_employee_query()
    csv = ""
    csv = csv_employees
    response = make_response(csv)
    response.headers["Content-Disposition"] = "attachment; filename=employees.csv"
    return response

# 移動
# ここに社員情報全部持ってくる、cursorのsqlを全てにする
# def csv_retrieve_employees(cursor):
#     csv_employees = "id, 社員ID, 氏名, 年齢, 性別, 画像ID, 郵便番号, 都道府県, 住所, 部署ID, 入社日, 退社日, 更新日, 部署名\n"
#     for (id, employee_id, employee_name, employee_age, employee_gender, employee_image_id, employee_postal_code, employee_prefecture, employee_address, department_id, employee_start_date, employee_leave_date, employee_update_date, department_name) in cursor:

#         csv_employees += f"{id}, {employee_id}, {employee_name}, {employee_age}, {employee_gender}, {employee_image_id}, {employee_postal_code}, {employee_prefecture}, {employee_address}, {department_id}, {employee_start_date}, {employee_leave_date}, {employee_update_date}, {department_name}\n"

#     return csv_employees

# 移動
# 全社員情報をSQLで取得
# def get_csv_employee_query():
#     cursor, cnx = get_connection()
#     employee_list = "SELECT id, employee_id, employee_name, employee_age, employee_gender, employee_image_id, employee_postal_code, employee_prefecture, employee_address, employee_table.department_id, employee_start_date, employee_leave_date, employee_update_date, department_name FROM employee_table JOIN department_table ON employee_table.department_id = department_table.department_id"

#     cursor.execute(employee_list)
#     csv_employees = db.csv_retrieve_employees(cursor)
#     return csv_employees

# ここに社員一覧の情報を表示するロジックを書く
# @app.route("/", methods=['GET', 'POST'])
# def employee_list():
#     employees = get_employee_query()
    
#     params = {
#     "employees" : employees,
#     }
#     return render_template("employee_list.html", **params)





# CSVファイルに出力
# @app.route("/csv", methods=["GET", "POST"])
# def output_csv():
#     cursor, cnx = get_connection()
#     output_csvfile = "SELECT * FROM employee_table INTO OUTFILE './static/employee.csv' "
#     # output_csvfile = "SELECT * FROM employee_table INTO OUTFILE './static/employee_table.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'"
#     cursor.execute(output_csvfile)
#     return redirect('/')


# 先に従業員追加の処理を実装して、そこでデータをinsertで入力する
# 従業員の新規追加ボタンの実装
# @app.route("/add", methods=["GET", "POST"])
# def employee_add():
#     # ここではformで送信された値を受け取っている
#     # 新規登録を実行したあとはこちらで受け取っている
#     if "employee_image" in request.files:
#         employee_id = request.form.get("employee_id", "")
#         employee_name = request.form.get("employee_name", "")
#         employee_age = request.form.get("employee_age", "")
#         employee_gender = request.form.get("employee_gender", "")
#         employee_image = request.files["employee_image"]
#         employee_postal_code = request.form.get("employee_postal_code", "")
#         employee_prefecture = request.form.get("employee_prefecture", "")
#         employee_address = request.form.get("employee_address", "")
#         department_name_id = request.form.get("department_name", "")
#         # department_name = request.form.get("department_name", "")
#         # department_id = request.form.get("department_id", "")
#         employee_start_date = request.form.get("employee_start_date", "")
#         employee_leave_date = request.form.get("employee_leave_date", "")

#         # とりあえず、formで値が送られているかチャックするロジックを書いてみよう
#         if employee_id == "" or employee_name == "" or employee_age == "" or employee_gender == "" or employee_image == "" or employee_postal_code == "" or employee_prefecture == "" or employee_address == "" or employee_start_date == "":
#             flash("入力される情報に不備があったため、登録に失敗しました")
#             return redirect("/")
#         else:
#             # department_nameとdepartment_idのvalueを分割してみる
#             department_array = department_name_id.split("&")
#             department_name = department_array[0]
#             department_id = department_array[1]

#             # このIDにはランダムな文字列を生成して代入する、生成ロジックは別関数で作成する
#             employee_image_id = create_employee_image_id()
#             # このdepartment_idは生成せずに選択された既存のidを使用する
#             # department_id = create_department_id()
#             filename = save_filename(employee_image)
#             add_employee(employee_id, employee_name, employee_age, employee_gender, employee_image_id, employee_postal_code, employee_prefecture, employee_address, department_id, employee_start_date, employee_leave_date, filename, department_name)
#             # params = {
#             # "employee_information" : employee_information
#             # }
#             flash("新規追加することに成功したよ！")
#             return redirect("/")
#     # else:
#     #     flash("ようこそ、社員情報追加のページへ", "")
#     #     # ここで部署のリストを渡している
#     #     department = get_department_query()
#     #     params = {
#     #     "department" : department
#     #     }
#     # # return render_template("employee_add.html", **params)
#     # return render_template("employee_add.html", **params)

#     # 新規追加はこっちでやる
#     flash("ようこそ、社員情報追加のページへ", "")
#     # ここで部署のリストを渡している
#     department = get_department_query()
#     # test = ""
#     params = {
#     "department" : department
#     # "test" : test
#     }
#     # return render_template("employee_add.html", **params)
#     return render_template("employee_add.html", **params)


# # 社員情報を編集するロジックを記述
# # @app.route("/edit_employee", methods=["GET", "POST"])
# def edit_employee_before():
#     cursor, cnx = get_connection()
#     if "employee_image" in request.files:
#         id = int(request.form.get("id", ""))
#         employee_id = request.form.get("employee_id", "")
#         employee_name = request.form.get("employee_name", "")
#         employee_age = request.form.get("employee_age", "")
#         employee_gender = request.form.get("employee_gender", "")
#         employee_image = request.files["employee_image"]
#         employee_postal_code = request.form.get("employee_postal_code", "")
#         employee_prefecture = request.form.get("employee_prefecture", "")
#         employee_address = request.form.get("employee_address", "")
#         department_name_id = request.form.get("department_name", "")
#         employee_start_date = request.form.get("employee_start_date", "")
#         employee_leave_date = request.form.get("employee_leave_date", "")

#         # department_nameとdepartment_idのvalueを分割してみる
#         department_array = department_name_id.split("&")
#         department_name = department_array[0]
#         department_id = department_array[1]

#         # このIDにはランダムな文字列を生成して代入する、生成ロジックは別関数で作成する
#         employee_image_id = create_employee_image_id()
#         filename = save_filename(employee_image)

#     get_query_update_employee = f"UPDATE employee_table SET \
#     employee_id = '{employee_id}', \
#     employee_name = '{employee_name}', \
#     employee_age = '{employee_age}', \
#     employee_gender = '{employee_gender}', \
#     employee_image_id = '{employee_image_id}', \
#     employee_postal_code = '{employee_postal_code}', \
#     employee_prefecture = '{employee_prefecture}', \
#     employee_address = '{employee_address}', \
#     department_id = '{department_id}', \
#     employee_start_date = '{employee_start_date}', \
#     employee_leave_date = '{employee_leave_date}' \
#     WHERE id = {id} "
    
#     cursor.execute(get_query_update_employee)
#     cnx.commit()

#     return redirect('/')

    # get_query_update_employee = f"UPDATE "
    # cursor.execute(get_query_update_employee)
    # cnx.commit()


# 社員情報の検索
# @app.route("/search_employee", methods=["GET", "POST"])
# def employee_search():
#     cursor, cnx = get_connection()
#     department_name = request.form.get("department_name", "")
#     search_employee_id = request.form.get("search_employee_id", "")
#     search_employee_name = request.form.get("search_employee_name", "")
#     sql_and, get_query_search_employee_table, query_department_name, query_employee_id, query_employee_name = get_query_variable(department_name, search_employee_id, search_employee_name)
#     get_query_search_employee = find_employee(sql_and, get_query_search_employee_table, query_department_name, query_employee_id, query_employee_name, department_name, search_employee_id, search_employee_name)
#     cursor.execute(get_query_search_employee)
#     search_employees = retrieve_serarch_employees(cursor)
#     return render_template("search_result.html", search_employees=search_employees)


# # 検索するSQLを受け取り
# def get_query_variable(department_name, search_employee_id, search_employee_name):
#     get_query_search_employee_table = "SELECT employee_id, employee_name, department_name FROM employee_table JOIN department_table ON employee_table.department_id = department_table.department_id WHERE "
#     query_department_name = f"department_name = '{department_name}'"
#     query_employee_id = f"employee_id = '{search_employee_id}'"
#     query_employee_name = f"employee_name LIKE '%{search_employee_name}%'"
#     # query_employee_name = f"employee_name = '{search_employee_name}'"
#     sql_and = " AND "
#     return sql_and, get_query_search_employee_table, query_department_name, query_employee_id, query_employee_name

# # 検索をする従業員を条件分岐で分ける
# def find_employee(sql_and, get_query_search_employee_table, query_department_name, query_employee_id, query_employee_name, department_name, search_employee_id, search_employee_name):
#     if department_name != "" and search_employee_id == "" and search_employee_name == "":
#         get_query_search_employee = get_query_search_employee_table + query_department_name
#     elif department_name == "" and search_employee_id != "" and search_employee_name == "":
#         get_query_search_employee = get_query_search_employee_table + query_employee_id
#     elif department_name == "" and search_employee_id != "" and search_employee_name == "":
#         get_query_search_employee = get_query_search_employee_table + query_employee_name
#     elif department_name != "" and search_employee_id != "" and search_employee_name == "":
#         get_query_search_employee = get_query_search_employee_table + query_department_name + sql_and + query_employee_id
#     elif department_name == "" and search_employee_id != "" and search_employee_name != "":
#         get_query_search_employee = get_query_search_employee_table + query_employee_id + sql_and + query_employee_name
#     elif department_name != "" and search_employee_id == "" and search_employee_name != "":
#         get_query_search_employee = get_query_search_employee_table + query_department_name + sql_and + query_employee_name
#     else:
#         get_query_search_employee = get_query_search_employee_table + query_department_name + sql_and + query_employee_id + sql_and + query_employee_name
    
#     return get_query_search_employee

# # 条件分岐をちょっと変えてみる
# def find_employee():
#     cursor, cnx = get_connection()
#     department_name = request.form.get("department_name", "")
#     search_employee_id = request.form.get("search_employee_id", "")
#     search_employee_name = request.form.get("search_employee_name", "")

#     get_query_search_employee_table = "SELECT employee_id, employee_name, department_name FROM employee_table JOIN department_table ON employee_table.department_id = department_table.department_id WHERE employee_id IS NOT NULL "
    
#     if department_name != "":
#         get_query_search_employee_table += f"AND department_name = '{department_name}'"
#     if search_employee_id != "":
#         get_query_search_employee_table += f"AND employee_id = '{search_employee_id}'"
#     if search_employee_name != "":
#         get_query_search_employee_table += f"AND employee_name LIKE '%{search_employee_name}%'"
#     return get_query_search_employee_table

#     cursor.execute(get_query_search_employee_table)





# 部署の追加、今は編集だけど
# @app.route("/edit_department", methods=["GET", "POST"])
# def edit_department():
#     change_department_name = request.form.get("change_department_name", "")
#     department_name = request.form.get("department_name", "")
#     change_department(change_department_name, department_name)
#     return render_template("department_add.html")

# # 部署のリストから編集ボタンを押した時、編集ページに飛ぶための関数
# @app.route("/edit_department_link", methods=["GET", "POST"])
# def connect_edit_department():
#     department_name = request.form.get("department_name", "")
#     return render_template("department_add.html", department_name=department_name)

# @app.route("/add_department", methods=["GET", "POST"])
# def add_department():
#     change_department_name = request.form.get("change_department_name", "")
#     # department_name = request.form.get("department_name", "")
#     create_department(change_department_name)
#     return render_template("department_add.html")

# @app.route("add_department_link", methods=["GET", "POST"])
# def connect_add_department():
#     return render_template("department_add.html")



