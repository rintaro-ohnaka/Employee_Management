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


-- 社員情報データを入れてみる
INSERT INTO employee_table(
    employee_name,
    employee_age,
    employee_gender,
    employee_postal_code,
    employee_prefecture,
    employee_address,
    employee_start_date,
    employee_leave_date
) VALUES (
    '{employee_name}',
    '{employee_age}',
    '{employee_gender}',
    '{employee_postal_code}',
    '{employee_prefecture}',
    '{employee_address}',
    '{employee_start_date}',
    '{employee_leave_date}'
)

-- 写真データを入れてみる
INSERT INTO employee_image_table(
    employee_image,
    employee_image_update_date
) VALUES (
    '{employee_image}',
    'LOCALTIME()'
)

-- 部署データを入れてみる
INSERT INTO department_table(
    department_name,
    department_create_date,
    department_update_date
) VALUES (
    '{department_name}',
    'LOCALTIME()',
    'LOCALTIME()'
)