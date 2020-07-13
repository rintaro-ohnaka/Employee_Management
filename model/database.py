import mysql.connector
from model.const import DB

# DB接続
def get_connection():
    cnx = mysql.connector.connect(host=DB["DB_HOST"], user=DB["DB_USER_NAME"], password=DB["DB_PASSWORD"], database=DB["DB_NAME"])
    # cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
    cursor = cnx.cursor()
    return cursor, cnx

# 社員データを取得し、配列に代入する
def retrieve_employees(cursor):
    employees = []
    for (id, employee_id, employee_name, employee_age, employee_gender, employee_image_id, employee_postal_code, employee_prefecture, employee_address, department_id, employee_start_date, employee_leave_date, employee_update_date) in cursor:
        item = { "id":id, "employee_id":employee_id, "employee_name":employee_name, "employee_age":employee_age, "employee_gender":employee_gender, "employee_image_id":employee_image_id, "employee_postal_code":employee_postal_code, "employee_prefecture":employee_prefecture, "employee_address":employee_address, "department_id":department_id, "employee_start_date":employee_start_date, "employee_leave_date":employee_leave_date, "employee_update_date":employee_update_date}
        employees.append(item)
    return employees

# 社員情報をSQLで取得
def get_employee_query():
    cursor, cnx = get_connection()
    employee_list = "SELECT * FROM employee_table"
    # employee_list = "SELECT id, employee_id, employee_name FROM employee_table"
    cursor.execute(employee_list)
    employees = retrieve_employees(cursor)
    return employees

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

# updateのクエリ取得
def get_query_update_employee(id, employee_id, employee_name, employee_age, employee_gender, employee_image_id, employee_postal_code, employee_prefecture, employee_address, employee_start_date, employee_leave_date, department_name, department_id):
    query_update_employee = f"UPDATE employee_table SET \
    employee_id = '{employee_id}', \
    employee_name = '{employee_name}', \
    employee_age = '{employee_age}', \
    employee_gender = '{employee_gender}', \
    employee_image_id = '{employee_image_id}', \
    employee_postal_code = '{employee_postal_code}', \
    employee_prefecture = '{employee_prefecture}', \
    employee_address = '{employee_address}', \
    department_id = '{department_id}', \
    employee_start_date = '{employee_start_date}', \
    employee_leave_date = '{employee_leave_date}' \
    WHERE id = {id} "
    return query_update_employee

def retrieve_edit_employee(cursor):
    employees = []
    for (id, employee_id, employee_name, employee_age, employee_gender, employee_image_id, employee_postal_code, employee_prefecture, employee_address, department_id, employee_start_date, employee_leave_date, employee_update_date, employee_image) in cursor:
        item = { "id":id, "employee_id":employee_id, "employee_name":employee_name, "employee_age":employee_age, "employee_gender":employee_gender, "employee_image_id":employee_image_id, "employee_postal_code":employee_postal_code, "employee_prefecture":employee_prefecture, "employee_address":employee_address, "department_id":department_id, "employee_start_date":employee_start_date, "employee_leave_date":employee_leave_date, "employee_update_date":employee_update_date, "employee_image":employee_image}
        employees.append(item)
    return employees


# 部署を受け取る
def retrieve_department(cursor):
    department = []
    for (department_id, department_name) in cursor:
        item = {"department_id":department_id, "department_name":department_name}
        department.append(item)
    return department

# SQL文を取得
def get_department_query():
    cursor, cnx = get_connection()
    department_list = "SELECT department_id, department_name FROM department_table"
    cursor.execute(department_list)
    department = retrieve_department(cursor)
    return department

# 部署名の編集
def change_department(change_department_name, department_name):
    cursor, cnx = get_connection()
    # update文
    get_query_update_department = f"UPDATE department_table SET department_name = '{change_department_name}' WHERE department_name = '{department_name}' "
    cursor.execute(get_query_update_department)
    cnx.commit()

# 部署の新規作成
def create_department(change_department_name):
    cursor, cnx = get_connection()
    department_id = create_department_id()
    # insert文
    get_query_create_department = f"INSERT INTO department_table (department_id, department_name) VALUES ('{department_id}', '{change_department_name}') "
    cursor.execute(get_query_create_department)
    cnx.commit()

# 入力された値の情報を元に条件分岐
def get_query_search_employee(get_query_search_employee_table, department_name, search_employee_id, search_employee_name):
    if department_name != "":
        get_query_search_employee_table += f" AND department_name = '{department_name}'"
    if search_employee_id != "":
        get_query_search_employee_table += f" AND employee_id = '{search_employee_id}'"
    if search_employee_name != "":
        get_query_search_employee_table += f" AND employee_name LIKE '%{search_employee_name}%'"
    return get_query_search_employee_table

# 検索した従業員データを取得し、配列に代入する
def retrieve_serarch_employees(cursor):
    search_employees = []
    for (id, employee_id, employee_name, department_name) in cursor:
        item = {"id":id, "employee_id":employee_id, "employee_name":employee_name, "department_name":department_name}
        search_employees.append(item)
    return search_employees

# ここに社員情報全部持ってくる、cursorのsqlを全てにする
def csv_retrieve_employees(cursor):
    csv_employees = "id, 社員ID, 氏名, 年齢, 性別, 画像ID, 郵便番号, 都道府県, 住所, 部署ID, 入社日, 退社日, 更新日, 部署名\n"
    for (id, employee_id, employee_name, employee_age, employee_gender, employee_image_id, employee_postal_code, employee_prefecture, employee_address, department_id, employee_start_date, employee_leave_date, employee_update_date, department_name) in cursor:

        csv_employees += f"{id}, {employee_id}, {employee_name}, {employee_age}, {employee_gender}, {employee_image_id}, {employee_postal_code}, {employee_prefecture}, {employee_address}, {department_id}, {employee_start_date}, {employee_leave_date}, {employee_update_date}, {department_name}\n"

    return csv_employees

# 全社員情報をSQLで取得
def get_csv_employee_query():
    cursor, cnx = get_connection()
    employee_list = "SELECT id, employee_id, employee_name, employee_age, employee_gender, employee_image_id, employee_postal_code, employee_prefecture, employee_address, employee_table.department_id, employee_start_date, employee_leave_date, employee_update_date, department_name FROM employee_table JOIN department_table ON employee_table.department_id = department_table.department_id"
    cursor.execute(employee_list)
    csv_employees = csv_retrieve_employees(cursor)
    return csv_employees