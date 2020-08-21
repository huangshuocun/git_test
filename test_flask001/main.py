from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

#定义flask对象app
app=Flask(__name__)
#定义app属性为连接mysql数据库做准备
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://rocky@115.159.52.81:3306/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
#定义SQL数据库对象，将flask对象app作为参数传递
db=SQLAlchemy(app)
#定义命令管理器对象，将flask对象app作为参数传递
manager=Manager(app)
#迁移工具初始化
#数据库迁移:所有对象都要关联flask对象app，数据库迁移涉及数据库对象db，所以要传
migrate=Migrate(app,db)
#数据库迁移要用到命令，所以要给命令管理器manager创建数据库迁移命令对象
manager.add_command('sql_update',MigrateCommand)

#定义student表结构-建表,将db对象传到类表当中。
class Student(db.Model):
    __tablename__='student'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),nullable=False,unique=True)
    gender=db.Column(db.Enum('男','女','保密'))
    city=db.Column(db.String(20))
    birthday=db.Column(db.Date)
    bio=db.Column(db.Text)
    money=db.Column(db.Float)

class Exam(db.Model):
    __tablename__='teacher'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    gender = db.Column(db.Enum('男', '女', '保密'))
    course = db.Column(db.String(20),nullable=False,unique=True)
    birthday = db.Column(db.Date)

#有迁移工具，该建表命令用不到了,python main.py db upgrade自动创建表加二狗
@manager.command
def add_table():
    '''创建新表'''
    db.create_all()
@manager.command
def insert_data():
    '''插入表数据'''
    u1 = Student(name='tom', gender='男', city='北京', birthday='1990-3-21', bio='哈哈', money=238)
    u2 = Student(name='lucy', gender='女', city='上海', birthday='1995-9-12', bio='版画', money=736)
    u3 = Student(name='jack', gender='男', city='武汉', birthday='1998-5-14', bio='班花', money=541)
    u4 = Student(name='bob', gender='男', city='苏州', birthday='1994-3-9', bio='拉拉', money=9004)
    u5 = Student(name='lily', gender='女', city='南京', birthday='1992-3-17', bio='啦啦', money=555)
    u6 = Student(name='eva', gender='女', city='芜湖', birthday='1974-2-5', bio='露露', money=8942)
    u7 = Student(name='alex', gender='男', city='成都', birthday='1999-5-26', bio='开开', money=244)
    u8 = Student(name='jam', gender='男', city='太原', birthday='1997-5-9', bio='笨笨', money=984)
    u9 = Student(name='rob', gender='男', city='青岛', birthday='1999-9-7', bio='奔奔', money=90)
    u10 = Student(name='ella', gender='女', city='大连', birthday='2000-10-1', bio='娇娇', money=459)
    db.session.add_all([u1,u2,u3,u4,u5,u6,u7,u8,u9,u10])
    db.session.commit()

#从mysql数据库中取数据然后显示到home页面
@app.route('/')
def home():
    stu=Student.query.all()
    top3=Student.query.order_by(Student.money.desc()).limit(3)
    return render_template('home.html',stu=stu,top3=top3)

if __name__=="__main__":
    manager.run()
