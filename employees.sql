-- 社員管理ツールに使用するテーブルを記述している

-- 社員情報テーブル

CREATE TABLE employee_table(
    employee_id INT AUTO_INCREMENT,
    employee_name VARCHAR(255),
    employee_age INT,
    employee_gender VARCHAR(255),
    employee_image_id INT,
    employee_postal_code INT,
    employee_prefecture VARCHAR(255),
    employee_address VARCHAR(255),
    department_id INT,
    employee_start_date VARCHAR(255),
    employee_leave_date VARCHAR(255),
    employee_update_date VARCHAR(255),
    PRIMARY KEY (employee_id)
)

--　証明写真テーブル

CREATE TABLE employee_image_table(
    employee_image_id INT AUTO_INCREMENT,
    employee_image VARCHAR(255),
    employee_image_update_date VARCHAR(255),
    PRIMARY KEY (employee_image_id)
)

-- 部署テーブル

CREATE TABLE department_table(
    department_id INT AUTO_INCREMENT,
    department_name VARCHAR(255),
    department_create_date VARCHAR(255),
    department_update_date VARCHAR(255),
    PRIMARY KEY (department_id)
)