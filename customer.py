from flask import Flask, Response, request,flash, render_template, make_response, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from datetime import datetime


app=Flask(__name__)
CORS(app)

app.config['SECRET_KEY']='zy112612' # 密码
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://admin:zy112612@e6156-1.cudpmdtzmg9e.us-east-1.rds.amazonaws.com:3306/customer'
    # 协议：mysql+pymysql
    # 用户名：root
    # 密码：2333
    # IP地址：localhost
    # 端口：3306
    # 数据库名：runoob #这里的数据库需要提前建好
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
db=SQLAlchemy(app)

#测试连上
with app.app_context():
    sql = 'select * from Customers'
    result = db.session.execute(sql)
    print(result.fetchall())


@app.route('/', methods=['GET'])
def home():
    return 'Hello World!'

#{"username":"ywang", "password":"0002", "email": "wg@gmail.com", "address": "400w"}
@app.route('/customer/register', methods=['GET', 'POST'])
def register():
    response = ""
    if request.method == 'POST':
        data = json.loads(request.get_data())

        username = data['username']
        password = data['password']
        email = data['email']
        address = data['address']
        print(email)
        try:
            sql = "SELECT COUNT('{}') FROM Customers where email = '{}' ".format(email, email)
            result = db.session.execute(sql).fetchall()[0][0]
        except Exception as err:
            return {"message": "error! input error"}
        
        print(result)
        if result > 0:
            response = {"message": "error! email is used"}
        else:
            try:
                sql= "INSERT INTO Customers VALUES ('{}', '{}', '{}', '{}');".format(email,username, password, address)
                db.session.execute(sql)
            except Exception as err:
                return {"message": "error! input error"}
            sql = 'select * from Customers'
            result = db.session.execute(sql)
            print(result.fetchall())
            
            response = {"message": "register successfully"}
       
    return response

def sreach(data):
    
    password = data['password']
    email = data['email']
    try:
        sql = "SELECT * FROM Customers where email = '{}' ".format(email)
        result = db.session.execute(sql).fetchone()
    except Exception as err:
        return {"message": "error! input error"}
    
    if result :
        stored_password= result[2]
        print(stored_password)
        if stored_password == password:
            print("successfully")
            response ={"message":"login successfully"}
        else:
            print("unmatch")
            response = {"message":"password unmatch"}
    else:
        print("please register")
        response= {"message": "you need to register firstly"}
    
    return response


@app.route('/customer/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        data = json.loads(request.get_data())
        password = data['password']
        email = data['email']
        
        try:
            sql = "SELECT * FROM Customers where email = '{}' ".format(email)
            result = db.session.execute(sql).fetchone()
        except Exception as err:
            return {"message": "error! input error"}
        
        if result :
            stored_password= result[2]
            print(stored_password)
            if stored_password == password:
                print("successfully")
                return {"message":"login successfully"}
            else:
                print("unmatch")
                return {"message":"password unmatch"}
        else:
            print("please register")
            return {"message": "you need to register firstly"}
        
    return msg
        

        
    

    
@app.route("/people/<email>", methods=["GET"])
def get_customer_by_email(email):
    
    sql = "select * from Customers where email = '" + email + "'"
    result = db.session.execute(sql).fetchone()

    if result:
        data_email=result[0]
        name=result[1]
        password= result[2]
        address= result[3]
        list=[data_email, name, password, address]
        
        rsp = Response(json.dumps(list), status=200, content_type="application/json")
        
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp
    

if __name__=='__main__':
    # db.create_all() # 创建这两个表
    sreach({"password":"0002", "email": "da@gmail.com"})
    app.run(host='0.0.0.0', port=8080, debug=True)