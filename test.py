# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
# from io import StringIO

# app = Flask(__name__)
# # DB_URL = <DBのURI>
# DB_URL = "mysql://root:wako19980207@loxalhonst/my_database"
# app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# class User(db.Model):
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.Integer)
#     gender = db.Column(db.Integer)
#     age = db.Column(db.Integer)
#     created_at = db.Column(db.DateTime)

#     def __init__(self, username, gender, age):
#         self.user_name = username
#         self.gender = gender
#         self.age = age
#         now = datetime.now()
#         self.created_at = now

#     def __repr__(self):
#         return '<User %r>' % self.username



# # csvファイルダウンロード
# @app.route("/download_csv")
# def download():
# # def download(obj):

#     f = StringIO()
#     # 引数のところがcsvfileって感じ？
#     writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_ALL, lineterminator="\n")

#     obj = 'employees'

#     # if obj == 'users':
#     if "output_csv" in request.form.keys():
#         writer.writerow(['id', 'username', 'gender', 'age', 'created_at'])
#         for u in User.query.all():
#             writer.writerow([u.id, u.username, u.gender, u.age, u.created_at])

#     res = make_response()
#     res.data = f.getvalue()
#     res.headers['Content-Type'] = 'text/csv'
#     res.headers['Content-Disposition'] = 'attachment; filename=' + obj + '.csv'
#     return res



# # 意味はわかるけど、細かいロジックの組み合わせの理解が追いついてないので、とりあえず実装してみる

# # ここでdbエンジンを作る
# from sqlalchemy import create_engine
# engine=create_engine("mysql://root:wako19980207@localhost/my_database")

# # モデルクラスを作る（テーブル定義を書く）
# # まずはモデルベースクラスを作る
# from sqlalchemy.ext.declarative import declarative_base
# Base=declarative_base()

# from sqlalchemy.schema import Column
# from sqlalchemy.types import Integer, String
# class User(Base):
#     __tablename__="user" #テーブル名を指定
#     user_id=Column(Integer, primary_key=True)
#     first_name=Column(String(255))
#     last_name=Column(String(255))
#     age=Column(Integer)
#     def full_name(self):#フルネームを返すメソッド
#         return "{self.first_name} {self.last_name}"

# # これでエンジンにUserクラスのテーブルが作成される？
# Base.metadata.create_all(engine)


# # セッションを作成する
# from sqlalchemy.orm import sessionmaker
# SessionClass=sessionmaker(engine) #セッションを作るクラスを作成
# session=SessionClass()

# # SELECT テーブルからデータを取り出すにはqueryを使う
# users=session.query(User).all() #userテーブルの全レコードをクラスが入った配列で返す
# user=session.query(User).first() #userテーブルの最初のレコードをクラスで返す

# # テーブル名が、、、というテーブルが存在してたとすれば、こう書く
# Base=declarative_base(bind=engine)
# class Exisiting_user(Base): #クラス名は何でもok
#     __tablename__="exisiting_user" 
#     __table_args__={"autoload": True}

# # 上記のコードを参考に自分のデータベースを反映してみる
# Base=declarative_base(bind=engine)
# class employee_table(Base): #クラス名は何でもok
#     __tablename__="employee_table" 
#     __table_args__={"autoload": True}