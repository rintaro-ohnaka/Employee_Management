-- 社員管理ツールに使用するテーブルを記述している

-- 社員情報テーブル

CREATE TABLE employee_table(
    employee_id INT AUTO_INCREMENT,
    employee_name VARCHAR(255),
    employee_age INT,
    employee_gender VARCHAR(255),
    employee_image_id INT,
    employee_address VARCHAR(255),
    employee_department_id INT,
    PRIMARY KEY (employee_id)
)

--　証明写真テーブル

CREATE TABLE employee_image_table(
    employee_image_id INT AUTO_INCREMENT,
    employee_image VARCHAR(255),
    PRIMARY KEY (employee_image_id)
)

-- 部署テーブル

CREATE TABLE employee_department_table(
    employee_department_id INT AUTO_INCREMENT,
    employee_department_name VARCHAR(255),
    PRIMARY KEY (employee_department_id)
)