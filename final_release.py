 # -*- coding: utf-8 -*-  
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash,jsonify,Response
from flaskext.mysql import MySQL
import json
import cgi
import datetime
import time
import sys
import logging
import MySQLdb
from flask_cors import *
import requests
import calendar
import re
reload(sys)
sys.setdefaultencoding('utf8')

mysql = MySQL()
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = '123456'  
app.config['MYSQL_DATABASE_USER'] = 'uysk'
app.config['MYSQL_DATABASE_PASSWORD'] = 'pswd'
app.config['MYSQL_DATABASE_DB'] = 'spm'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_CHARSET']= 'utf8'
mysql.init_app(app)
#图书馆静态信息
class library_config():
    conn= MySQLdb.connect(
        host='localhost',
        port = 80,
        user='uysk',
        passwd='pswd',
        db ='spm',
        charset='utf8'
        )
    cur = conn.cursor()
    sql = "select *from Configuration"
    cur.execute(sql)
    config=cur.fetchall()

    library=config[0][0]
    lendDuration=config[0][1]
    renewDuration=config[0][2]
    renewable=config[0][3]
    InBorrow=config[0][4]
    
    cur.close()
    conn.close()

    def get_library(self):
        return self.library
    def get_lendDuration(self):
        return self.lendDuration
    def get_renewDuration(self):
        return self.renewDuration
    def get_renewable(self):
        return self.renewable
    def get_InBorrow(self):
        return self.InBorrow

library = library_config()

#图书馆动态信息
def getDueFine():
    conn= MySQLdb.connect(
        host='localhost',
        port = 80,
        user='uysk',
        passwd='pswd',
        db ='spm',
        charset='utf8'
        )
    cur = conn.cursor()
    sql = "select dueFine from Configuration"
    cur.execute(sql)
    data=cur.fetchall()
    dueFine=data[0][0]
    cur.close()
    conn.close()
    return dueFine

def getDamageFine():
    conn= MySQLdb.connect(
        host='localhost',
        port = 80,
        user='uysk',
        passwd='pswd',
        db ='spm',
        charset='utf8'
        )
    cur = conn.cursor()
    sql = "select DamageFine from Configuration"
    cur.execute(sql)
    data=cur.fetchall()
    DamageFine=data[0][0]
    cur.close()
    conn.close()
    return DamageFine

def getLostFine():
    conn= MySQLdb.connect(
        host='localhost',
        port = 80,
        user='uysk',
        passwd='pswd',
        db ='spm',
        charset='utf8'
        )
    cur = conn.cursor()
    sql = "select LostFine from Configuration"
    cur.execute(sql)
    data=cur.fetchall()
    LostFine=data[0][0]
    print LostFine
    cur.close()
    conn.close()
    return LostFine

def getDeposit():
    conn= MySQLdb.connect(
        host='localhost',
        port = 80,
        user='uysk',
        passwd='pswd',
        db ='spm',
        charset='utf8'
        )
    cur = conn.cursor()
    sql = "select deposit from Configuration"
    cur.execute(sql)
    data=cur.fetchall()
    deposit=data[0][0]
    cur.close()
    conn.close()
    return deposit

#根据name 获取 certificateNo
@app.route('/api/get_name_by_certificateNo',methods=['GET','POST'])
def get_name_by_certificateNo():
    error = None
    if request.method == 'GET':
        certificateNo = request.args.get('certificateNo')
        cur = mysql.get_db().cursor()
        sql = "select name,deposit from reader where certificateNo=\'%s\'" % (certificateNo)
        cur.execute(sql)
        data = cur.fetchall()
        if len(data)==0:
            name = ''
            deposit = ''
            return jsonify({'name':name,'deposit':deposit}),201
        data = list(data)
        name = data[0][0]
        deposit = data[0][1]
        return jsonify({'name':name,'deposit':deposit}),201
    return jsonify({'result':'error'}),401

#一个学生毕业之后，会清除这个学生的记录，同时还要在incomeRecord中增加一条记录，这个记录会在cuz_we_love_money 中的折线图中打印出来
@app.route('/api/return_deposit',methods=['GET','POST'])
def return_deposit():
    error = None
    if request.method == 'POST':
        certificateNo = request.form['certificateNo']
        cur = mysql.get_db().cursor()
        sql = "select * from reader where certificateNo=\'%s\'" % (certificateNo)
        
        cur.execute(sql)
        data = cur.fetchall()
        if len(data) == 0:
            result = 'no'
            reason = 'please input valid certificateNo'
            return jsonify({'result':result,'reason':reason}),201
        #首先需要判断该学生是否还有没有还的书，if True,不能执行删除该学生，退款押金的操作，退押金的操作设置type=4
        sql = "select *from lendRecord where readerID=\'%s\' and returnTime is NULL" % (certificateNo)
        cur.execute(sql)
        data = cur.fetchall()
        if len(data) != 0:
            result = 'no'
            reason = 'the student has book(s) not returned.'
            return jsonify({'result':result,'reason':reason}),201
        
        #如果学生合法且欠费都换成，则ok,删除并增加一条记录
        now = datetime.datetime.now()
        returnTime = now.strftime("%Y-%m-%d")
        #获取deposit
        sql = "select deposit from reader where certificateNo = \'%s\'" % (certificateNo)
        cur.execute(sql)
        data = cur.fetchall()
        deposit = data[0][0]
        print deposit
        sql = "insert into incomeRecord(recordTime,type,value) values(\'%s\',4,%d)" % (returnTime,deposit)
        cur.execute(sql)
        
        #删除该用户
        sql = "delete from reader where certificateNo=\'%s\'" % (certificateNo)
        cur.execute(sql)
        
        mysql.get_db().commit()
        result = 'yes'
        reason = 'the student has been deleted'
        
        return jsonify({'result':result,'reason':reason}),201
    return jsonify({'result':'error'}),401


#前台提供时间type=0,1,2分别代表年月日，如果0表示年，1表示月，两张图
#1. type-monthly/daily-income(total-account) 2. four-parts(total-indivially)
@app.route('/api/cuz_we_love_money',methods=['GET','POST'])
def cuz_we_love_money():
    error = None
    if request.method == 'GET':
        date_type = request.args.get('date_type')
        date_type = int(date_type)
        dateInfo = request.args.get('dateInfo')
        
        start_date = datetime.datetime.strptime(dateInfo,'%Y-%m-%d')
        startDate = datetime.date(start_date.year,start_date.month,start_date.day)
        endDate = startDate
        if date_type == 0:
            endDate = startDate + datetime.timedelta(days=365)
        if date_type == 1:
            cur_month = start_date.month
            next_month = cur_month%12 +1 
            cur_year =start_date.year
            cur_day = start_date.day
            endDate = datetime.date(cur_year,next_month,cur_day)
        if date_type == 2:
            endDate = startDate + datetime.timedelta(days=1)
        
        cur = mysql.get_db().cursor()
        sql = "select recordTime,type,value from incomeRecord"
        cur.execute(sql)
        data = cur.fetchall()
        list_data = list(data)
        
        dic_sum={}
        
        dic_type0={}
        dic_type1={}
        dic_type2={}
        dic_type3={}
        dic_type4={}
        dic_sum0 = []
        dic_sum0.append(dic_type0)
        dic_sum0.append(dic_type1)
        dic_sum0.append(dic_type2)
        dic_sum0.append(dic_type3)
        dic_sum0.append(dic_type4)
        
        for i in range(31):
            dic_sum[i+1]=0.0
        
        for i in range(5):
            for j in range(31):
                dic_sum0[i][j+1]= 0.0
        #初始化饼图三个数据
        dic_sum2=[]
        for i in range(5):
            dic_sum2.append(0.0)
        
        
        #将符合日期要求的更新字典
        for row in list_data:
            res_date = row[0]
            if res_date >= startDate and res_date<endDate:
                #根据时间更新折线图数据字典
                column_name=''
                if date_type == 0:
                    column_name = int(res_date.month)
                elif date_type == 1:
                    column_name = int(res_date.day)
                else:
                    column_name = 1
                dic_sum[column_name] += row[2]

                dic_sum0[row[1]][column_name] += row[2]
                #饼图信息提供
                dic_sum2[row[1]]+=row[2]
                
        return jsonify({'dic_sum':dic_sum,'dic_sum2':dic_sum2,'dic_sum0':dic_sum0}),201
    return jsonify({'result':'error'}),401

#获得特定ISBN当前在图书馆的图书位置以及按位置分类的quantity
@app.route('/api/book_location',methods=['GET','POST'])
def book_location():
    error = None
    if request.method =='GET':
        ISBN = request.args.get('ISBN')
        cur = mysql.get_db().cursor()
        sql = "select location from book where ISBN = \'%s\' and state=1 " % (ISBN)
        cur.execute(sql)
        data = cur.fetchall()
        data =list(data)
        if len(data)==0:
            result = 'no'
            reason = 'no book of this ISBN is in library now'
            return jsonify({'result':result,'reason':reason}),201
        location=[]
        for row in data:
            if row[0] not in location:
                location.append(row[0])
        result ={}
        for i in location:
            result[i]=0
        for row in data:
            for i in location:
                if row[0]==i:
                    result[i]=result[i]+1
        return jsonify({'result':result,'len':len(result)}), 201
    return jsonify({'result':'error'}),201

@app.route('/api/get_ReadingRoom',methods=['GET','POST'])
def get_ReadingRoom():
    error = None
    if request.method =='GET':
        cur = mysql.get_db().cursor()
        sql = "select library,name from ReadingRoom"
        cur.execute(sql)
        data = cur.fetchall()
        list_data = list(data)
        result=[]
        for row in list_data:
            jsondata = {}
            jsondata['library']=row[0]
            jsondata['name']=row[1]
            result.append(jsondata)
        return jsonify({'result':result,'len':len(result)}), 201
    return jsonify({'result':'error'}),201

@app.route('/api/get_BookShelf',methods=['GET','POST'])
def get_BookShelf():
    error = None
    if request.method =='GET':
        room = request.args.get('room')
        cur = mysql.get_db().cursor()
        sql = "select room,name from BookShelf where room = \'%s\'" %(room)
        cur.execute(sql)
        data = cur.fetchall()
        list_data = list(data)
        result=[]
        for row in list_data:
            if row[0] != room:
                continue
            jsondata = {}
            jsondata['name']=row[1]
            result.append(jsondata)
        return jsonify({'result':result,'len':len(result)}), 201
    return jsonify({'result':'error'}),201


#搜索
@app.route('/api/search', methods=['GET','POST'])
def search():
    error = None
    if request.method == 'GET':
        item_number = 15
        searchText=request.args.get('search')
        searchType=request.args.get('type')
        searchPage=request.args.get('page')
        if searchPage is None:
            searchPage=1
        else:
            searchPage=int(searchPage)
        
        cur5= mysql.get_db().cursor()
        cur6= mysql.get_db().cursor()
        cur7= mysql.get_db().cursor()
        cur8= mysql.get_db().cursor()
        cur9= mysql.get_db().cursor()
        cur0= mysql.get_db().cursor()
        
        #获取fields
        sql="SELECT * FROM bibliography WHERE ISBN LIKE \'%%%s%%\'  " % (searchText)
        cur5.execute(sql)
        data = cur5.fetchall()
        list_data = list(data)
        fields = cur5.description
        column_list=[]
        for i in fields:
            column_list.append(i[0])

        if searchType == '0':
            sql="SELECT * FROM bibliography WHERE ISBN LIKE \'%%%s%%\'  " % (searchText)
            cur5.execute(sql)
            sql="SELECT * FROM bibliography WHERE title LIKE \'%%%s%%\'  " % (searchText)
            cur6.execute(sql)
            sql="SELECT * FROM bibliography WHERE author LIKE \'%%%s%%\'  " % (searchText)
            cur7.execute(sql)
            sql="SELECT * FROM bibliography WHERE origintitle LIKE \'%%%s%%\' " % (searchText)
            cur8.execute(sql)
            sql="SELECT * FROM bibliography WHERE summary LIKE \'%%%s%%\' " % (searchText)
            cur9.execute(sql)
            sql="SELECT * FROM bibliography WHERE tag LIKE \'%%%s%%\' " % (searchText)
            cur0.execute(sql)
            
            data1 = cur5.fetchall()
            data2 = cur6.fetchall()
            data3 = cur7.fetchall()
            data4 = cur8.fetchall()
            data5 = cur9.fetchall()
            data6 = cur0.fetchall()
            
            data = data1 + data2  +  data3 + data4 + data5  +  data6
            list_data = list(data)
            
        elif searchType == '1':
            sql="SELECT * FROM bibliography WHERE title LIKE \'%%%s%%\' " % (searchText)
            cur5.execute(sql)
            data = cur5.fetchall()
            list_data = list(data)
            
        elif searchType == '2':
            sql="SELECT * FROM bibliography WHERE author LIKE \'%%%s%%\' " % (searchText)
            cur5.execute(sql)
            data = cur5.fetchall()
            list_data = list(data)
            
        elif searchType == '3':
            sql="SELECT * FROM bibliography WHERE ISBN LIKE \'%%%s%%\'  " % (searchText)
            cur5.execute(sql)
            data = cur5.fetchall()
            list_data = list(data)
            
        

        #entries = [dict(title=row[0], text=row[1]) for row in data
        new_data = []
        for row in list_data:
            if row not in new_data:
                new_data.append(row)
        
        start_item=(searchPage-1)*item_number
        end_item=start_item+item_number-1
        if start_item>len(new_data)-1:
            return jsonify({'result':'', 'total':len(new_data), 'page':searchPage}),201
        elif end_item>len(new_data)-1: 
            end_item=len(new_data)-1
        last_data=[]
        for i in range(start_item,end_item+1):
            last_data.append(new_data[i]) 
        result=[]
        for row in last_data:
            jsondata={}
            for i in range(len(column_list)):
                jsondata[column_list[i]] = row[i]
            result.append(jsondata)
        return jsonify({'result': result,'total':len(new_data), 'page':searchPage}), 201
    return jsonify({'result':'error'}),201

#注册/fr
@app.route('/api/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        certificateNo=request.form['certificateNo']
        password=request.form['password']
        name=request.form['name']

        date = datetime.datetime.now().strftime("%Y-%m-%d")
        cur = mysql.get_db().cursor()

        sql="SELECT * from reader where certificateNo=\'%s\'" % (certificateNo)
        cur.execute(sql)
        data = cur.fetchone()
        if data is not None:
            reason = 'certificateNo already used'
            result = 'no'
            return jsonify({'result': result,'reason': reason}), 201
        else:
            sql1 = "insert into reader(certificateNo, name, password, registerTime, deposit) values (\'%s\',\'%s\',\'%s\',\'%s\',%d)" % (certificateNo, name, password, date,getDeposit())
            cur.execute(sql1)
            #type 3：定金
            cur_date = datetime.datetime.now()
            curDate = datetime.date(cur_date.year,cur_date.month,cur_date.day)
            sql_deposit = "insert into incomeRecord(recordTime,type,value) values (\'%s\',3,%d)"%(curDate,getDeposit())
            cur.execute(sql_deposit)

            mysql.get_db().commit()
            reason='Successfully signed up!'
            result='yes'
            return jsonify({'result': result,'reason': reason}), 201
    return jsonify({'result': result,'reason': reason}), 201

#读者登陆/fr
@app.route('/api/reader_login', methods=['GET', 'POST'])
def api_reader_login():
    error = None
    if request.method == 'POST':
        certificateNo=request.form['certificateNo']
        password=request.form['password']

        cur = mysql.get_db().cursor()
        sql = "SELECT * from reader where certificateNo=\'%s\'" % (certificateNo)
        cur.execute(sql)
        data = cur.fetchone()
        if data is None:
            result='no'
            reason = 'Invalid certificateNo or password'
            return jsonify({'result': result,'reason': reason}), 201
        sql = "SELECT * from reader where certificateNo=\'%s\' and password=\'%s\'" % (certificateNo,password)
        cur.execute(sql)
        data = cur.fetchone()
        
        if data is None:
            result='no'
            reason = 'Invalid certificateNo or password'
        else:
            result='yes'
            reason='successfully logged in!'
        return jsonify({'result': result, 'reason': reason}), 201
    return error,201

#管理员登陆/fr
@app.route('/api/admin_login', methods=['GET', 'POST'])
def api_admin_login():
    error = None
    if request.method == 'POST':
        ID=request.form['ID']
        password=request.form['password']

        cur = mysql.get_db().cursor()
        sql = "SELECT * from librarian where ID=\'%s\'" % (ID)
        cur.execute(sql)
        data = cur.fetchone()
        if data is None:
            result='no'
            reason = 'Invalid ID or password'
            return jsonify({'result': result,'reason': reason}), 201
        sql = "SELECT * from librarian where ID=\'%s\' and password=\'%s\'" % (ID,password)
        cur.execute(sql)
        data = cur.fetchone()
        
        if data is None:
            result='no'
            reason = 'Invalid ID or password'
        else:
            result='yes'
            reason='successfully logged in!'
        return jsonify({'result': result, 'reason': reason}), 201
    return error,201

# 个人信息：显示个人信息/fr
@app.route('/api/user_info',methods=['GET','POST'])
def get_lib_info():
    error = None
    if request.method == 'GET':
        certificateNo = request.args.get('certificateNo')
        cur = mysql.get_db().cursor()
        sql = "SELECT * FROM reader WHERE certificateNo= \'%s\'" %(certificateNo)
        cur.execute(sql)
        data = cur.fetchall()

        fields = cur.description
        column_list=[]
        for i in fields:
            column_list.append(i[0])

        result=[]
        for row in data:
            jsondata={}
            for i in range (len(column_list)):
                jsondata[column_list[i]] = row[i]
            result.append(jsondata)
        return jsonify({'result': result,'total':len(data)}), 201
    return jsonify({'result':'error'}),201


#修改信息（只能修改密码）/fr
@app.route('/api/change_info',methods=['GET','POST'])
def change_info():
    error = None
    if request.method == 'POST':
        certificateNo = request.form['certificateNo']
        password = request.form['password']
        
        cur = mysql.get_db().cursor()
        sql = "update reader set password = \'%s\' where certificateNo = \'%s\'" % (password,certificateNo)
        cur.execute(sql)
        mysql.get_db().commit()
        result = 'yes'
        reason = 'the password has been changed.'
        
        return jsonify({'result': result,'reason': reason}), 201
    return jsonify({'result':'error'}),201


# add_book/fr
@app.route('/api/add_book',methods=['GET','POST'])
def add_book():
    error = None
    if request.method =='POST':
        ISBN = request.form['ISBN']
        location = request.form['location']
        quantity = request.form['quantity']
        quantity = int(quantity)

        getBookID = mysql.get_db().cursor()
        sql = "select bookID from book order by bookID desc limit 1" 
        getBookID.execute(sql)
        data=getBookID.fetchall()
        bookID_start = data[0][0]

        cur = mysql.get_db().cursor()
        sql = "select *from bibliography where ISBN=\'%s\'" %(ISBN)
        cur.execute(sql)
        data=cur.fetchall()
        data=list(data)
        #无该ISBN对应图书
        if len(data)==0:
            url = "https://api.douban.com/v2/book/isbn/%s" % (ISBN)
            response = requests.request("GET", url)
            res_json=response.json()
            if res_json.has_key('code'):
                result='no'
                reason='we cannot find the book you want through douban api.'
                return jsonify({'result': result,'reason': reason}), 201
            title = res_json['title']
            cover = res_json['image']
            if res_json['author']:
                author = res_json['author'][0]
            else:
                author = '佚名'
            press = res_json['publisher']

            pubdate = res_json['pubdate']
            price = res_json['price']
            catalog = res_json['catalog']
            authorinfo = res_json['author_intro']
            summary = res_json['summary']

            title=title.replace("'","\\\'")
            title=title.replace('"','\\\"')
            cover=cover.replace("'","\\\'")
            cover=cover.replace('"','\\\"')
            author=author.replace("'","\\\'")
            author=author.replace('"','\\\"')
            press=press.replace("'","\\\'")
            press=press.replace('"','\\\"')
            pubdate=pubdate.replace("'","\\\'")
            pubdate=pubdate.replace('"','\\\"')
            price=price.replace("'","\\\'")
            price=price.replace('"','\\\"')
            catalog=catalog.replace("'","\\\'")
            catalog=catalog.replace('"','\\\"')
            authorinfo=authorinfo.replace("'","\\\'")
            authorinfo=authorinfo.replace('"','\\\"')
            summary=summary.replace("'","\\\'")
            summary=summary.replace('"','\\\"')
            if price=='':
                price = 50.0
            cur0 = mysql.get_db().cursor()
            sql0 = "insert into bibliography(ISBN,title,cover,author,press,pubdate,price,catalog,authorinfo,summary) values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')" % (ISBN,title,cover,author,press,pubdate,price,catalog,authorinfo,summary)

            cur0.execute(sql0)
            
        for i in range(quantity):
            cur2 = mysql.get_db().cursor()
            sql2 = "insert into book(ISBN,location) values(\'%s\',\'%s\')" % (ISBN,location)
            cur2.execute(sql2)
    
        mysql.get_db().commit()
        result = 'yes'
        reason = 'you have added %d new books'%(quantity)
        bookID=[]
        for i in range(quantity): 
            bookID.append(i+bookID_start+1) 
        return jsonify({'result': result,'reason': reason,'bookID_range':bookID}), 201
    return jsonify({'result':'error'}),401



#借书、续借、还书：三个接口分别对应一个操作界面，操作界面上是通过输入book_id与reader_id进行借书操作，操作成功返回一个借阅成功的弹窗。


#借书 /fr
@app.route('/api/borrow',methods=['GET','POST'])
def borrow():
    error = None
    if request.method =='POST':
        certificateNo = request.form['certificateNo']
        bookID = request.form['bookID']
        bookID = int(bookID)
        #检查用户已借图书是否达到上限
        testLimit = mysql.get_db().cursor()
        sql="select borrowedNumber from reader where certificateNo = \'%s\'" % (certificateNo)
        testLimit.execute(sql)
        data = testLimit.fetchall()
        data = list(data)
        if len(data) == 0 :
            result = 'no'
            reason = 'reader does not exist.'
            return jsonify({'result': result,'reason': reason}), 201
        borrowedBook = data[0][0]
        #已达上限，提醒用户，借书失败
        if borrowedBook==library.get_InBorrow():
            result = 'no'
            reason = 'you have run out of your availableQuantity.'
            return jsonify({'result': result,'reason': reason}), 201
        #判断该书是否被借，是否存在
        testExistance = mysql.get_db().cursor()
        sql="select state,ISBN from book where bookID = %d" % (bookID)
        testExistance.execute(sql)
        data = testExistance.fetchall()
        data=list(data)
        if len(data)!=0:
            state=data[0][0]
            if state==0:
                result = 'no'
                reason = 'the book has been borrowed'
                return jsonify({'result': result,'reason': reason}), 201
        elif len(data)==0:
            result = 'no'
            reason = 'the book does not exist.'
            return jsonify({'result': result,'reason': reason}), 201
        #获得ISBN
        ISBN=data[0][1]
        #判断该用户是否借过此书且未还
        if borrowedBook>0:
            testISBN = mysql.get_db().cursor()
            sql="select ISBN from book,lendRecord where readerID = \'%s\' and returnTime is null and book.bookID=lendRecord.bookID" % (certificateNo)
            testISBN.execute(sql)
            data = testISBN.fetchall()
            for row in data:
                if row[0]==ISBN:
                    result = 'no'
                    reason = 'you have borrowed 1 copy of this book and not returned yet.'
                    return jsonify({'result': result,'reason': reason}), 201
        #未达上限，修改lendRecord添加借书记录,修改reader增加borrowedNumber,修改book表的location

        #LendRecord
        now = datetime.datetime.now()
        end = now + datetime.timedelta(days=library.get_lendDuration())
        startTime = now.strftime("%Y-%m-%d")
        endTime = end.strftime("%Y-%m-%d")
        cur = mysql.get_db().cursor()
        sql = "insert into lendRecord(readerID,bookID,borrowTime,dueTime) values(\'%s\',%d,\'%s\',\'%s\')" % (certificateNo,bookID,startTime,endTime)
        cur.execute(sql)
        #reader
        cur2 = mysql.get_db().cursor()
        sql2 = "update reader set borrowedNumber=borrowedNumber+1 where certificateNo = \'%s\'"%(certificateNo)
        cur2.execute(sql2)
        #book
        cur3 = mysql.get_db().cursor()
        sql3 = "update book set location=\'%s\',state=0 where bookID= %d " %(certificateNo,bookID)
        cur3.execute(sql3)
        mysql.get_db().commit()
        result = 'yes'
        reason = 'you have borrowed the book'
        return jsonify({'result': result,'reason': reason}), 201
    
    return jsonify({'result':'error'}),201

#续借/fr
@app.route('/api/renew',methods=['GET','POST'])
def renew():
    error = None
    if request.method =='POST':
        bookID = request.form['bookID']
        bookID=int(bookID)

        #检测bookID是否合法
        testExistance = mysql.get_db().cursor()
        sql_test = "select * from lendRecord where bookID = %d and returnTime is null" % (bookID)
        testExistance.execute(sql_test)
        data = testExistance.fetchall()
        if len(data)==0:
            result = 'no'
            reason = 'the record does not exist.'
            return jsonify({'result': result,'reason': reason}), 201
        #检测是否已经超过预期还书时间
        testDate = mysql.get_db().cursor()
        sql_test = "select dueTime from lendRecord where bookID = %d and returnTime is null" % (bookID)
        testDate.execute(sql_test)
        data = testDate.fetchall()
        dueDate = data[0][0]
        cur_date = datetime.datetime.now()
        curDate = datetime.date(cur_date.year,cur_date.month,cur_date.day)
        if (curDate-dueDate).days>0:
            result = 'no'
            reason = 'The book is overdue so it cannot be renewed. Please return it first.'
            return jsonify({'result': result,'reason': reason}), 201

        #检测是否已经该书达到最大续借次数
        testLimit = mysql.get_db().cursor()
        sql_test = "select renewed,borrowTime from lendRecord where bookID = %d and returnTime is null " % (bookID)
        testLimit.execute(sql_test)
        data = testLimit.fetchall()

        renewed_time=data[0][0]
        #已达最大次数
        if renewed_time==library.get_renewable():
            result = 'no'
            reason = 'the book has been renewed twice.'
            return jsonify({'result': result,'reason': reason}), 201
        #未达最大次数，为读者续借，修改lendRecord
        else:
            dueTime = data[0][1] + datetime.timedelta(days=library.get_lendDuration()+(renewed_time+1)*library.get_renewDuration())
            cur = mysql.get_db().cursor()
            sql = "update lendRecord set dueTime=\'%s\',renewed=renewed+1 where bookID=%d and returnTime is null " % (dueTime,bookID)
            cur.execute(sql)
            mysql.get_db().commit()
            reason = 'you have renewed dueTime to \'%s\'' %(dueTime)
            result = 'yes'
            return jsonify({'result': result,'reason': reason}), 201
    return jsonify({'result':'error'}),201

#还书/fr
@app.route('/api/rebook',methods=['GET','POST'])
def rebook():
    error = None
    if request.method =='POST':
        bookID = request.form['bookID']
        #condition 0：正常 1：损坏 2：丢失
        #type 0:超时 1：损坏 2：丢失
        bookCondition = request.form['bookCondition']
        
        bookID = int(bookID)
        bookCondition = int(bookCondition)
        
        #获取读者信息
        cur = mysql.get_db().cursor()
        sql = "SELECT readerID,dueTime from lendRecord where bookID= %d and returnTime is null " % (bookID)
        cur.execute(sql)
        data = cur.fetchall()
        readerID = data[0][0]
        dueDate = data[0][1]
        #获取当日日期
        cur_date = datetime.datetime.now()
        curDate = datetime.date(cur_date.year,cur_date.month,cur_date.day)
        #获取图书价格
        cur = mysql.get_db().cursor()
        sql = "SELECT price from bibliography,book where bookID= %d and bibliography.ISBN=book.ISBN " % (bookID)
        cur.execute(sql)
        data = cur.fetchall()
        price = data[0][0]
        list_price = []
        for i in price:
            if i in "0123456789.":
                list_price.append(i)
        price = ''.join(list_price)
        price =float(price)
        
        #lendRecord
        date = datetime.datetime.now()
        cur = mysql.get_db().cursor()
        sql = "update lendRecord set returnTime=\'%s\' where readerID=\'%s\' and bookID= %d " % (date,readerID,bookID)
        cur.execute(sql)
        #reader
        cur2 = mysql.get_db().cursor()
        sql2 = "update reader set borrowedNumber=borrowedNumber-1 where certificateNo = \'%s\'"%(readerID)
        cur2.execute(sql2)
        #book
        cur3 = mysql.get_db().cursor()
        sql3 = "update book set location = 'A101-24', state = 1, bookCondition = %d where bookID = %d " %(bookCondition,bookID)
        cur3.execute(sql3)
        #罚金判决
        #判断是否超时
        fine = 0
        if (curDate-dueDate).days>0:
            fine = (curDate-dueDate).days*getDueFine()
            cur_fine = mysql.get_db().cursor()
            sql_fine = "insert into incomeRecord(recordTime,type,value) values (\'%s\',0,%f)"%(curDate,fine)
            cur_fine.execute(sql_fine)

        #判断图书状态
        if bookCondition == 0:
            mysql.get_db().commit()
            reason = 'the book has been returned. And the overdue fine is %f yuan.'%(fine)
            result = 'yes'
            return jsonify({'result': result,'reason': reason,'overdue_fine':fine}), 201
        #图书损坏
        elif bookCondition == 1:
            fine_damage = getDamageFine()+price
            cur_fine = mysql.get_db().cursor()
            sql_fine = "insert into incomeRecord(recordTime,type,value) values (\'%s\',1,%f)"%(curDate,fine_damage)
            cur_fine.execute(sql_fine)
            mysql.get_db().commit()
            totalFine=fine+fine_damage
            reason = 'the book has been returned. And the total fine is %f yuan.'%(totalFine)
            result = 'yes'
            return jsonify({'result': result,'reason': reason,'overdue_fine':fine,'damage_fine':fine_damage}), 201
        else:
            fine_lost = getLostFine()+price
            cur_fine = mysql.get_db().cursor()
            sql_fine = "insert into incomeRecord(recordTime,type,value) values (\'%s\',2,%f)"%(curDate,fine_lost)
            cur_fine.execute(sql_fine)
            mysql.get_db().commit()
            totalFine=fine+fine_lost
            reason = 'the book has been returned. And the total fine is %f yuan.'%(totalFine)
            result = 'yes'
            return jsonify({'result': result,'reason': reason,'overdue_fine':fine,'lost_fine':fine_lost}), 201
    return jsonify({'result':'error'}),201

#还书时 根据bookID判断罚金数目/fr
@app.route('/api/get_fine_by_bookID',methods=['GET','POST'])
def get_fine_by_bookID():
    error = None
    if request.method =='GET':
        bookID = request.args.get('bookID')
        bookCondition = request.args.get('bookCondition')
        bookID=int(bookID)
        bookCondition=int(bookCondition)

        #获取读者信息
        cur = mysql.get_db().cursor()
        sql = "SELECT readerID,dueTime from lendRecord where bookID= %d and returnTime is null " % (bookID)
        cur.execute(sql)
        data = cur.fetchall()
        readerID = data[0][0]
        dueDate = data[0][1]
        #获取当日日期
        cur_date = datetime.datetime.now()
        curDate = datetime.date(cur_date.year,cur_date.month,cur_date.day)
        #获取图书价格
        cur = mysql.get_db().cursor()
        sql = "SELECT price from bibliography,book where bookID= %d and bibliography.ISBN=book.ISBN " % (bookID)
        cur.execute(sql)
        data = cur.fetchall()
        price = data[0][0]
        list_price = []
        for i in price:
            if i in "0123456789.":
                list_price.append(i)
        price = ''.join(list_price)
        price =float(price)
        #判断是否超时
        fine_overdue = 0
        fine_damage = 0
        fine_lost =0
        if (curDate-dueDate).days>0:
            fine_overdue = (curDate-dueDate).days*getDueFine()

        #判断图书状态
        #图书损坏
        if bookCondition == 1:
            fine_damage = getDamageFine()+price
            
        elif bookCondition==2:
            fine_lost = getLostFine()+price

        return jsonify({'overdue_fine':fine_overdue,'damage_fine':fine_damage,'lost_fine':fine_lost}), 201
    return jsonify({'result':'error'}),201

#删除操作book 特定某一本删除 /fr
@app.route('/api/delete_book',methods=['GET','POST'])
def delete_book():
    error = None
    if request.method =='POST':
        bookID = request.form['bookID']
        bookID = int(bookID)
        cur = mysql.get_db().cursor()
        sql = "select state from book where bookID = %d" % (bookID)
        cur.execute(sql)
        data = cur.fetchall()
        # 判断bookID是否存在
        if len(data)==0:
            result = 'no'
            reason = 'the book does not exist.'
            return jsonify({'result': result,'reason': reason}), 201
        # 书在图书馆，可以直接删除
        elif data[0][0]==1:
            result = 'yes'
            reason = 'the book has been deleted'
            cur = mysql.get_db().cursor()
            sql = "delete from book where bookID = %d" % (bookID)
            cur.execute(sql)
            
            #删除该书的借阅记录
            cur = mysql.get_db().cursor()
            sql = "delete from lendRecord where bookID = %d" % (bookID)
            cur.execute(sql)

            mysql.get_db().commit()
            return jsonify({'result': result,'reason': reason}), 201
        #书不在图书馆，要求持有该书的学生先进行还书操作
        else:
            result = 'no'
            reason = 'The book has been borrowed. It need to be returned befored get deleted(even lost,the step is needed in our procedure).'
            return jsonify({'result': result,'reason': reason}), 201
    return jsonify({'result':'error'}),201

#根据ISBN查看 search_each_book_by_ISBN /fr
@app.route('/api/search_each_book_by_ISBN',methods=['GET','POST'])
def search_each_book_by_ISBN():
    error = None
    if request.method =='GET':
        ISBN = request.args.get('ISBN')
        cur = mysql.get_db().cursor()
        sql = "select bookID,location,state from book where ISBN=\'%s\'" %(ISBN)
        cur.execute(sql)
        data = cur.fetchall()
        
        fields = cur.description
        column_list=[]
        for i in fields:
            column_list.append(i[0])
        
        list_data=list(data)
        bookID_location_state=[]
        for row in list_data:
            jsondata={}
            for i in range(len(column_list)):
                jsondata[column_list[i]] = row[i]
            bookID_location_state.append(jsondata)
        
        return jsonify({'bookID_location_state': bookID_location_state,'total':len(list_data)}), 201
    return jsonify({'result':'error'}),201

#配合search_each_book_by_ISBN 的 search_readerID_by_bookID /fr
@app.route('/api/search_readerID_by_bookID',methods=['GET','POST'])
def search_readerID_by_bookID():
    error = None
    if request.method =='GET':
        bookID = request.args.get('bookID')
        bookID = int(bookID)
        cur2 = mysql.get_db().cursor()
        sql2 = "select readerID from lendRecord where bookID= %d " %(bookID)
        cur2.execute(sql2)
        data2 = cur2.fetchall()
        
        fields2 = cur2.description
        column_list2=[]
        for i in fields2:
            column_list2.append(i[0])
        
        list_data2 = list(data2)
        reader_who_borrow =[]
        for row in list_data2:
            jsondata2={}
            for i in range(len(column_list2)):
                jsondata2[column_list2[i]] = row[i]
            reader_who_borrow.append(jsondata2)
        
        return jsonify({'reader_who_borrow':reader_who_borrow}), 201
    return jsonify({'result':'error'}),201

#get_dynamicInfo_and_staticInfo by isbn /fr
@app.route('/api/get_dynamicInfo_and_staticInfo',methods=['GET','POST'])
def get_dynamicInfo_and_staticInfo():
    error = None
    if request.method =='GET':
        ISBN = request.args.get('ISBN')
        cur = mysql.get_db().cursor()
        sql = "select * from bibliography,book where bibliography.ISBN=book.ISBN and book.ISBN=\'%s\'" %(ISBN)
        cur.execute(sql)
        data = cur.fetchall()
        
        fields = cur.description
        column_list=[]
        for i in fields:
            column_list.append(i[0])
        
        list_data=list(data)
        bookID_and_location=[]
        
        result=[]
        for row in list_data:
            jsondata={}
            for i in range(len(column_list)):
                jsondata[column_list[i]] = row[i]
            result.append(jsondata)
        
        return jsonify({'result': result,'total':len(list_data)}), 201
    return jsonify({'result':'error'}),201

#search_staticInfo /fr
@app.route('/api/search_staticInfo',methods=['GET','POST'])
def search_staticInfo():
    error = None
    if request.method =='GET':
        ISBN = request.args.get('ISBN')
        cur = mysql.get_db().cursor()
        sql = "select * from bibliography where ISBN=\'%s\'" %(ISBN)
        cur.execute(sql)
        data = cur.fetchall()
        
        fields = cur.description
        column_list=[]
        for i in fields:
            column_list.append(i[0])
        result=[]
        list_data=list(data)
        bookID_and_location=[]
        for row in list_data:
            jsondata={}
            for i in range(len(column_list)):
                jsondata[column_list[i]] = row[i]
            result.append(jsondata)
                
        return jsonify({'result': result,'total':len(list_data)}), 201
    return jsonify({'result':'error'}),201

#search_dynamicInfo /fr
@app.route('/api/search_dynamicInfo',methods = ['GET','POST'])
def search_dynamicInfo():
    error = None
    if request.method =='GET':
        
        ISBN = request.args.get('ISBN')
        
        cur = mysql.get_db().cursor()
        sql = "select * from book where ISBN=\'%s\'" %(ISBN)
        cur.execute(sql)
        
        data = cur.fetchall()
        
        fields = cur.description
        column_list=[]
        for i in fields:
            column_list.append(i[0])
        list_data=list(data)
        
        new_data = []
        for row in list_data:
            if row not in new_data:
                new_data.append(row)
        result=[]
        for row in new_data:
            jsondata={}
            for i in range (len(column_list)):
                jsondata[column_list[i]] = row[i]
            result.append(jsondata)
        return jsonify({'result': result,'total':len(new_data)}), 201
    return jsonify({'result':'error'}),201


#修改图书信息 只可以修改location /fr
@app.route('/api/edit_book',methods=['GET','POST'])
def edit_book():
    error = None
    if request.method =='POST':
        bookID = request.form['bookID']
        bookID = int(bookID)
        location = request.form['location']
        #检查该书是否在图书馆
        testExistance = mysql.get_db().cursor()
        sql_test = "select state from book where bookID = %d" % (bookID)
        testExistance.execute(sql_test)
        data=testExistance.fetchall()
        if len(data)==0:
            result = 'no'
            reason = 'the book does not exist.'
            return jsonify({'result': result,'reason': reason}), 201
        elif data[0][0] == 0:
            result = 'no'
            reason = 'the book has been borrowed.'
            return jsonify({'result': result,'reason': reason}), 201
        
        cur = mysql.get_db().cursor()
        sql = "update book set location=\'%s\' where bookID = %d" % (location,bookID)
        cur.execute(sql)
        
        mysql.get_db().commit()
        result = 'yes'
        reason = 'you have changed the location of book %d' % (bookID)
        return jsonify({'result': result,'reason': reason}), 201
    return jsonify({'result':'error'}),201

#提醒列表、逾期还书名单、读者黑名单




#展示已借图书列表/fr
@app.route('/api/reader_lend_list',methods = ['GET','POST'])
def reader_lend_list():
    error = None
    if request.method == 'GET':
        certificateNo = request.args.get('certificateNo')
        
        cur = mysql.get_db().cursor()
        sql = "select bibliography.title,a.bookID,a.borrowTime,a.dueTime,a.returnTime,cover,book.ISBN from lendRecord a,book,bibliography where  a.readerID=\'%s\' and book.bookID=a.bookID and book.ISBN=bibliography.ISBN and returnTime is null order by a.borrowTime desc" % (certificateNo)
        cur.execute(sql)
        data = cur.fetchall()
        

        fields = cur.description
        column_list=[]
        for i in fields:
            column_list.append(i[0])
        
        result=[]
        for row in data:
            jsondata={}
            for i in range (len(column_list)):
                jsondata[column_list[i]] = row[i]
            result.append(jsondata)
        return jsonify({'result': result,'total':len(data)}), 201
    return jsonify({'result':'error'}),201

#展示历史已借表/fr
@app.route('/api/reader_lend_history',methods = ['GET','POST'])
def reader_lend_history():
    error = None
    if request.method == 'GET':
        
        certificateNo = request.args.get('certificateNo')
        
        cur = mysql.get_db().cursor()
        sql = "select bibliography.title,lendRecord.bookID,lendRecord.borrowTime,lendRecord.dueTime,lendRecord.returnTime,cover,book.ISBN from lendRecord,book,bibliography where lendRecord.readerID=\'%s\' and book.bookID=lendRecord.bookID and book.ISBN=bibliography.ISBN and returnTime is not null order by lendRecord.borrowTime desc" % (certificateNo)
        cur.execute(sql)
        data = cur.fetchall()
        
        fields = cur.description
        column_list=[]
        for i in fields:
            column_list.append(i[0])
        list_data=list(data)
        
        new_data = []
        for row in list_data:
            if row not in new_data:
                new_data.append(row)
        result=[]
        for row in new_data:
            jsondata={}
            for i in range (len(column_list)):
                jsondata[column_list[i]] = row[i]
            result.append(jsondata)
        return jsonify({'result': result,'total':len(new_data)}), 201
    return jsonify({'result':'error'}),201

#展示罚金配置信息/ fr
@app.route('/api/fine_configuration',methods = ['GET','POST'])
def fine_configuration():
    error = None
    if request.method == 'GET':
        result = {}
        result['DueFine'] = getDueFine()
        result['DamageFine'] = getDamageFine()
        result['LostFine'] = getLostFine()
        result['deposit'] = getDeposit()
        return jsonify(result), 201
    return jsonify({'result':'error'}),201

#修改罚金配置信息 /fr
@app.route('/api/edit_configuration',methods = ['GET','POST'])
def edit_configuration():
    error = None
    if request.method == 'POST':
        DueFine = request.form['DueFine']
        DamageFine = request.form['DamageFine']
        LostFine = request.form['LostFine']
        deposit = request.form['deposit']
        DueFine=float(DueFine)
        DamageFine=float(DamageFine)
        LostFine=float(LostFine)
        deposit=int(deposit)
        cur = mysql.get_db().cursor()
        sql = "update Configuration set DueFine=%f, DamageFine=%f, LostFine=%f, deposit=%d " % (DueFine,DamageFine,LostFine,deposit)
        cur.execute(sql)
        mysql.get_db().commit()
        result = 'yes'
        reason = 'you have changed the fine configuration.'
        print getDueFine()

        return jsonify({'result': result,'reason': reason}), 201
    return jsonify({'result':'error'}),201

#front
@app.route('/',methods=['GET','POST'])
def index():
    error = None
    if request.method == 'GET':
        return render_template('index.html')
    else: 
        return "error"

@app.route('/sss',methods=['GET','POST'])
def sss():
    error = None
    if request.method == 'GET':
        searchText=request.args.get('search')
        searchType=request.args.get('type')
        searchPage=request.args.get('page')
        if searchPage is None:
            searchPage = 1
        return render_template('searchResult.html',searchText=searchText, searchType=searchType, searchPage=searchPage)
    return "error"
	
@app.route('/log',methods=['GET','POST'])
def log():
    error = None
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        return render_template('login.html',username=username,password=password)
    return "error"

@app.route('/register',methods=['GET','POST'])
def register():
    error = None
    if request.method == 'GET':
        # username=request.form['username']
        # password=request.form['password']
        # name=request.form['name']
        # tel=request.form['tel']
        return render_template('signup.html')
    return "error"

@app.route('/bookinfo',methods=['GET','POST'])
def bookinfo():
    error = None
    if request.method == 'GET':
        ISBN = request.args.get('search')
        return render_template('book_info_2.html',  searchText= ISBN)
    else: 
        return "error"
        
@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'GET':
        return render_template('login.html')
    
    else: 
        return "error"

@app.route('/loginAdmin',methods=['GET','POST'])
def loginAdmin():
    error = None
    if request.method == 'GET':
        return render_template('loginAdmin.html')
    
    else: 
        return "error"

@app.route('/chart',methods=['GET','POST'])
def chart():
    error = None
    if request.method == 'GET':
        return render_template('chart.html')
    else: 
        return "error"


@app.route('/userinfo',methods=['GET','POST'])
def userinfo():
    error = None
    if request.method == 'GET':
        return render_template('userinfo.html')
    
    else: 
        return "error"
     
@app.route('/alteruser',methods=['GET','POST'])
def alteruser():
    error = None
    if request.method == 'GET':
        return render_template('alteruser.html')
    else: 
        return "error"


@app.route('/userIndex',methods=['GET','POST'])
def userIndex():
    error = None
    if request.method == 'GET':
        return render_template('UserIndex.html')
    else: 
        return "error"        

@app.route('/admin',methods=['GET','POST'])
def admin():
    error = None
    if request.method == 'GET':
        return render_template('AdminIndex.html')
    else: 
        return "error"

@app.route('/alterInfo',methods=['GET','POST'])
def alterInfo():
    error = None
    if request.method == 'GET':
        return render_template('alterInfo.html')
    else: 
        return "error"        
        
@app.route('/userInfo',methods=['GET','POST'])
def userInfo():
    error = None
    if request.method == 'GET':
        return render_template('userInfo.html')
    else: 
        return "error"   
        
      
@app.route("/test/<imageid>")
def test(imageid):
    return render_template("{}.html".format(imageid))
    
@app.route("/favicon.ico")
def fav():
    image = file("/root/favicon.ico")
    resp = Response(image, mimetype="image/jpeg")
    return resp
    
@app.route("/image/<imageid>")
def image(imageid):
    image = file("/root/images/{}".format(imageid))
    resp = Response(image, mimetype="image/jpeg")
    return resp


if __name__ == "__main__":

    """app.config.from_object(Config())
    scheduler = APScheduler()
    # it is also possible to enable the API directly
    # scheduler.api_enabled = True
    scheduler.init_app(app)
    scheduler.start()"""
    app.debug = True
    app.run(host='0.0.0.0',port=80,threaded=True)
