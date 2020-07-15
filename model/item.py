class Employee(object):
    def __init__(self, id="", employee_id="", employee_name="", employee_age="", employee_gender="", employee_image_id="", employee_postal_code="", employee_prefecture="", employee_address="", department_id="", employee_start_date="", employee_leave_date="", employee_update_date="", employee_image=""):
        self.id = id
        self.employee_id = employee_id
        self.employee_name = employee_name
        self.employee_age = employee_age
        self.employee_gender = employee_gender
        self.employee_image_id = employee_image_id
        self.employee_postal_code = employee_postal_code
        self.employee_prefecture = employee_prefecture
        self.employee_address = employee_address
        self.department_id = department_id
        self.employee_start_date = employee_start_date
        self.employee_leave_date = employee_leave_date
        self.employee_update_date = employee_update_date
        self.employee_image = employee_image


class Department(object):
    def __init__(self, department_id="", department_name=""):
        self.department_id = department_id
        self.department_name = department_name

# class Department(object):
#     def __init__(self, department_id="", department_name=""):
#         self.department_id = department_id
#         self.department_name = department_name

class Image(object):
    def __init__(self, employee_image_id="", employee_image=""):
        self.employee_image_id = employee_image_id
        self.employee_image = employee_image

# 多重継承というのをやってみる
class EmpDept(Employee, Department):
    pass

# 画像も混ぜたクラスを作ってみる
class EmpDeptImg(EmpDept, Image):
    pass

# 全てを混ぜた最強クラス
class EmpDeptImgAll():
    def __init__(self, id="", employee_id="", employee_name="", department_name="", employee_age="", employee_gender="", employee_image_id="", employee_postal_code="", employee_prefecture="", employee_address="", department_id="", employee_start_date="", employee_leave_date="", employee_update_date="", employee_image=""):
        self.id = id
        self.employee_id = employee_id
        self.employee_name = employee_name
        self.department_name = department_name
        self.employee_age = employee_age
        self.employee_gender = employee_gender
        self.employee_image_id = employee_image_id
        self.employee_postal_code = employee_postal_code
        self.employee_prefecture = employee_prefecture
        self.employee_address = employee_address
        self.department_id = department_id
        self.employee_start_date = employee_start_date
        self.employee_leave_date = employee_leave_date
        self.employee_update_date = employee_update_date
        self.employee_image = employee_image
        # self.department_name = department_name