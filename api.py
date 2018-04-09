 # -*- coding: utf-8 -*-  
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash,jsonify,Response
from flaskext.mysql import MySQL
from flask_apscheduler import APScheduler
import json
import cgi
import datetime
import time
import sys
import logging
from flask_cors import *

reload(sys)
sys.setdefaultencoding('utf8')

mysql = MySQL()
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = '123456'  
app.config['MYSQL_DATABASE_USER'] = 'uysk'
app.config['MYSQL_DATABASE_PASSWORD'] = 'pswd'
app.config['MYSQL_DATABASE_DB'] = 'library'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_CHARSET']= 'utf8'
mysql.init_app(app)

"""@app.route('/api/search', methods=['GET','POST'])
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
        #isbn
        cur5 = mysql.get_db().cursor()
        sql="SELECT * FROM bibliography WHERE ISBN LIKE \'%%%s%%\'  " % (searchText)
        cur5.execute(sql)
        #title
        cur6 = mysql.get_db().cursor()
        sql="SELECT * FROM bibliography WHERE title LIKE \'%%%s%%\' " % (searchText)
        cur6.execute(sql)
        #origin_title
        cur7 = mysql.get_db().cursor()
        sql="SELECT * FROM bibliography WHERE origin_title LIKE \'%%%s%%\' " % (searchText)
        cur7.execute(sql)
        #summary
        cur8 = mysql.get_db().cursor()
        sql="SELECT * FROM bibliography WHERE summary LIKE \'%%%s%%\' " % (searchText)
        cur8.execute(sql)
        #author
        cur9 = mysql.get_db().cursor()
        sql="SELECT * FROM bibliography WHERE author LIKE \'%%%s%%\' " % (searchText)
        cur9.execute(sql)
        #tags
        cur0 = mysql.get_db().cursor()
        sql="SELECT * FROM bibliography WHERE tags LIKE \'%%%s%%\' " % (searchText)
        cur0.execute(sql)

        data1 = cur5.fetchall()
        data2 = cur6.fetchall()
        data3 = cur7.fetchall()
        data4 = cur8.fetchall()
        data5 = cur9.fetchall()
        data6 = cur0.fetchall()

        data = data1 + data2 + data3 + data4 + data5 + data6 

        fields = cur6.description
        column_list=[]
        for i in fields:
            column_list.append(i[0])

        #entries = [dict(title=row[0], text=row[1]) for row in data]
        list_data=list(data)
        
        new_data = []
        for row in list_data:
            if row not in new_data:
                new_data.append(row)
        
        start_item=(searchPage-1)*item_number
        end_item=start_item+item_number
        if start_item>len(new_data)-1:
            return jsonify({'result':''}),201
        elif end_item>len(new_data)-1: 
            end_item=len(new_data)-1
        last_data=[]
        print start_item,end_item
        for i in range(start_item,end_item+1):
            print i
            last_data.append(new_data[i]) 
        result=[]
        for row in last_data:
            jsondata={}
            for i in range(len(column_list)):
                jsondata[column_list[i]] = row[i]
            result.append(jsondata)
        return jsonify({'result': result,'total':len(last_data), 'page':searchPage}), 201
    return jsonify({'result':'error'}),201"""
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
            sql="SELECT * FROM bibliography WHERE origin_title LIKE \'%%%s%%\' " % (searchText)
            cur8.execute(sql)
            sql="SELECT * FROM bibliography WHERE summary LIKE \'%%%s%%\' " % (searchText)
            cur9.execute(sql)
            sql="SELECT * FROM bibliography WHERE tags LIKE \'%%%s%%\' " % (searchText)
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
        print start_item,end_item
        for i in range(start_item,end_item+1):
            print i
            last_data.append(new_data[i]) 
        result=[]
        for row in last_data:
            jsondata={}
            for i in range(len(column_list)):
                jsondata[column_list[i]] = row[i]
            result.append(jsondata)
        return jsonify({'result': result,'total':len(new_data), 'page':searchPage}), 201
    return jsonify({'result':'error'}),201


#登陆
@app.route('/api/login', methods=['GET', 'POST'])
def api_login():
    error = None
    if request.method == 'POST':
        us=request.form['username']
        pw=request.form['password']
        cur3 = mysql.get_db().cursor()
        sql = "SELECT * from user where userID=\'%s\'" % (us)
        cur3.execute(sql)
        data = cur3.fetchone()
        if data is None:
            result='no'
            reason = 'Invalid username'
            portrait = None
            return jsonify({'result': result,'portrait':portrait,'reason': reason}), 201
        sql = "SELECT * from user where userID=\'%s\' and password=\'%s\'" % (us,pw)
        cur3.execute(sql)
        data = cur3.fetchone()
        
        admin = 'no'
        if data is None:
            result='no'
            portrait = None
            reason = 'Invalid password'
        else:
            list_data = list(data)
            print list_data[4]
            
            if (list_data[4] == 1):
                admin = 'yes'
               
                
            reason='successfully logged in!'
            portrait= 'http://ww1.sinaimg.cn/large/8a3aacd4ly1fkyd4ty3dyj208c07fwef.jpg'
            result='yes'
        return jsonify({'result': result, 'portrait': portrait,'reason': reason, 'admin' : admin}), 201
    return error,201

#注册
@app.route('/api/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        sus=request.form['username']
        spw=request.form['password']
        db_name=request.form['name']
        email=request.form['email']
        cur = mysql.get_db().cursor()

        sql="SELECT * from user where userID=\'%s\'" % (sus)
        cur.execute(sql)
        data = cur.fetchone()
        if data is not None:
            reason = 'username already used'
            result = 'no'
       
        else:
            #默认注册为用户和读者
            sql1 = "insert into user(userID, name, password, email, portrait) values (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')" % (sus,db_name, spw, email, '/image/minguo.jpg')
            cur.execute(sql1)

            sql2 = "insert into reader(readerID) values (\'%s\')" % (sus)
            cur.execute(sql2)
            mysql.get_db().commit()
            reason='Successfully signed up!'
            result='yes'
            return jsonify({'result': result,'reason': reason}), 201
    return jsonify({'result': result,'reason': reason}), 201

# 个人信息：显示个人信息
@app.route('/api/user_info',methods=['GET','POST'])
def get_lib_info():
    error = None
    if request.method == 'GET':
        user_id = request.args.get('user_id')
        cur = mysql.get_db().cursor()
        sql = "SELECT * FROM user WHERE userID= \'%s\'" %(user_id)
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

#@app.route('/lib_info/<user_id>',method=['GET','POST'])
#def change_jmp(user_id):
#    error = None
#    if request.method == 'GET'
#        return render_template('change_user_info.html',  user_id = user_id)
#    return "error"
#修改信息
@app.route('/api/change_info',methods=['GET','POST'])
def change_info():
    error = None
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        
        cur = mysql.get_db().cursor()
        sql = "update user set password = \'%s\', name= \'%s\',email= \'%s\'  where userID = \'%s\'" % (password,name,email,user_id)
        cur.execute(sql)
        mysql.get_db().commit()
        result = 'yes'
        reason = 'you have changed your information'
        
        return jsonify({'result': result,'reason': reason}), 201
    return jsonify({'result':'error'}),201

'''
#展示reader信息
@app.route('/api/reader_info/<user_id>',methods=['GET','POST'])
def get_reader_info(user_id):
    error = None
    if request.method == 'GET':
        #user_id = request.args.get('user_id')
        cur = mysql.get_db().cursor()
        sql = "SELECT * FROM user,reader WHERE userID=readerID and userID= \'%s\'" %(user_id)
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
        return jsonify({'result': result,'total':len(new_data)), 201
    return jsonify({'result':'error'}),201
'''



#借书、续借、还书：三个接口分别对应一个操作界面，操作界面上是通过输入book_id与reader_id进行借书操作，操作成功返回一个借阅成功的弹窗。

@app.route('/api/reserve',methods=['GET','POST'])
def reserve():
    error = None
    if request.method == 'POST':
        ISBN = request.form['ISBN']
        readerID = request.form['user_id']

        testExistance = mysql.get_db().cursor()
        sql_test = "SELECT * from bookInfo where bookInfo.ISBN=\'%s\'" % (ISBN)
        testExistance.execute(sql_test)
        data = testExistance.fetchall()
        if len(data) == 0:
            result = 'no'
            reason = 'the book does not exist.'
            return jsonify({'result': result,'reason': reason}), 201

        submit=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #时间处理
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=3)
        n_day = now + delta
        Invalid = n_day.strftime('%Y-%m-%d')
        cur = mysql.get_db().cursor()
        sql = "insert into ReserveRecord(readerID,ISBN,submit,Invalid) values(\'%s\',\'%s\',\'%s\',\'%s\')" % (readerID,ISBN,submit,Invalid)
        cur.execute(sql)
        #check if reader availableQuantity =reservedQuantity+inBorrowQuantity
        cur5 = mysql.get_db().cursor()
        sql5 = "SELECT availableQuantity,reservedQuantity,inBorrowQuantity from reader where readerID=\'%s\'" % (readerID)
        cur5.execute(sql5)
        data2 = cur5.fetchall()
        list_data2 = list(data2)
        if list_data2[0][0]<=(list_data2[0][1]+list_data2[0][2]):
            result = 'no'
            reason = 'you have run out of your availableQuantity'
            return jsonify({'result': result,'reason': reason}), 201
        #reader
        cur2 = mysql.get_db().cursor()
        sql2 = "update reader set reservedQuantity = reservedQuantity+1 where readerID = \'%s\'"%(readerID)
        cur2.execute(sql2)
        #check if  book ISBN 是否全部被预约和借光
        cur4 = mysql.get_db().cursor()
        sql4 = "SELECT quantity,borrowedQuantity,reservedQuantity from bookInfo where ISBN=\'%s\'" % (ISBN)
        cur4.execute(sql4)
        data = cur4.fetchall()
        list_data = list(data)
        if list_data[0][0]==(list_data[0][1]+list_data[0][2]):
            result = 'no'
            reason = 'this book has all been reserved or borrowed.'
            return jsonify({'result': result,'reason': reason}), 201
        #bookInfo
        cur3 = mysql.get_db().cursor()
        sql3 = "update bookInfo set reservedQuantity=reservedQuantity+1 where ISBN=\'%s\'" % (ISBN)
        cur3.execute(sql3)

        mysql.get_db().commit()
        
        result = 'yes'
        reason = 'you have reserved the book. Please fend the book before \'%s\'' %(Invalid)
        #返回一个Invalid
        return jsonify({'result': result,'reason': reason}), 201
    return jsonify({'result':'error'}),201
#续借
@app.route('/api/renew',methods=['GET','POST'])
def renew():
    error = None
    if request.method =='POST':
        bookID = request.form['bookID']
        readerID = request.form['user_id']
        startTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        now = datetime.datetime.now()
        bookID=int(bookID)

        testExistance = mysql.get_db().cursor()
        sql_test = "SELECT state from book where book.bookID=%d" % (bookID)
        testExistance.execute(sql_test)
        data = testExistance.fetchall()
        if len(data) == 0:
            result = 'no'
            reason = 'the book does not exist.'
            return jsonify({'result': result,'reason': reason}), 201

        #不确定下一行的声明
        delta = datetime.timedelta(days=0)
        result = 'yes'
        reason = 'no problem'
        #判断该reader是否已经借了该图书且未该已经逾期
        cur = mysql.get_db().cursor()
        sql = "select renewed,startTime from LendRecord where readerID = \'%s\' and bookID=%d and state <> '已还' and state<>'未还'" % (readerID,bookID)
        cur.execute(sql)
        data = cur.fetchall()
        list_data = list(data)
        list_len = len(list_data)
        lend_time= None
        if list_len==0:
            result = 'no'
            reason = 'you have not borrowed the book or returned the book'
            return jsonify({'result': result,'reason': reason}), 201
        elif list_data[0][0]==0:
            delta = datetime.timedelta(days=45)
            lend_time='续借一次'
        elif list_data[0][0]==1:
            delta = datetime.timedelta(days=60)
            lend_time='续借两次'
        else:#借了2次
            delta = datetime.timedelta(days=60)
            result = 'no'
            reason = 'you have renewed the book for two times'
            return jsonify({'result': result,'reason': reason}), 201
        
        n_day = list_data[0][1] + delta
        endTime = n_day.strftime('%Y-%m-%d')
        #修改LendRecord
        cur = mysql.get_db().cursor()
        sql = "update LendRecord set endTime=\'%s\',renewed=renewed+1,state=\'%s\' where readerID = \'%s\' and bookID=%d and state <> '已还' and state<>'未还' " % (endTime,lend_time,readerID,bookID)
        cur.execute(sql)
        mysql.get_db().commit()
        reason = 'you have renewed endTime to \'%s\'' %(endTime)
        return jsonify({'result': result,'reason': reason}), 201
    return jsonify({'result':'error'}),201

@app.route('/api/borrow',methods=['GET','POST'])
def borrow():
    error = None
    if request.method =='POST':
        bookID = request.form['bookID']
        bookID = int(bookID)
        readerID = request.form['user_id']
        startTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        now = datetime.datetime.now()

        testExistance = mysql.get_db().cursor()
        sql_test = "SELECT state from book where book.bookID=%d" % (bookID)
        testExistance.execute(sql_test)
        data = testExistance.fetchall()
        if len(data) == 0:
            result = 'no'
            reason = 'the book does not exist.'
            return jsonify({'result': result,'reason': reason}), 201
        
        result = 'yes'
        reason = 'no problem'
        #检测这本书是否被借
        cur8 = mysql.get_db().cursor()
        sql8 = "SELECT state from book where book.bookID=%d" % (bookID)
        cur8.execute(sql8)
        data = cur8.fetchall()
        if data[0][0]==1:
            result = 'no'
            reason = 'The book you want has been  borrowed.'
            return jsonify({'result': result,'reason': reason}), 201

        #check if book ISBN 是否全部被预约和借光
        cur4 = mysql.get_db().cursor()
        sql4 = "SELECT quantity,borrowedQuantity,reservedQuantity from bookInfo,book where bookInfo.ISBN=book.ISBN and book.bookID=%d" % (bookID)
        cur4.execute(sql4)
        data = cur4.fetchall()
        list_data = list(data)
        
        if list_data[0][0]==(list_data[0][1]+list_data[0][2]):
            result = 'no'
            reason = 'The book you want has all been reserved or borrowed.'
            return jsonify({'result': result,'reason': reason}), 201
        
        #check if reader availableQuantity =reservedQuantity+inBorrowQuantity
        cur5 = mysql.get_db().cursor()
        sql5 = "SELECT availableQuantity,reservedQuantity,inBorrowQuantity from reader where readerID=\'%s\'" % (readerID)
        cur5.execute(sql5)
        data2 = cur5.fetchall()
        list_data2 = list(data2)
        print list_data2
        
        if len(list_data2) == 0:
            result = 'no'
            reason = 'this userID is invalid'
            return jsonify({'result': result,'reason': reason}), 201
        elif list_data2[0][0]<=(list_data2[0][1]+list_data2[0][2]):
            result = 'no'
            reason = 'you have run out of your availableQuantity'
            return jsonify({'result': result,'reason': reason}), 201
        
        
        delta = datetime.timedelta(days=30)
        n_day = now + delta
        endTime = n_day.strftime('%Y-%m-%d')
        startTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #LendRecord
        cur = mysql.get_db().cursor()
        sql = "insert into LendRecord(readerID,bookID,startTime,endTime,renewed,state) values(\'%s\',%d,\'%s\',\'%s\',0,'在借')" % (readerID,bookID,startTime,endTime)
        cur.execute(sql)
        #reader
        cur2 = mysql.get_db().cursor()
        sql2 = "update reader set borrowQuantity=borrowQuantity+1,inBorrowQuantity=inBorrowQuantity+1 where readerID = \'%s\'"%(readerID)
        cur2.execute(sql2)
        #bookInfo
        cur3 = mysql.get_db().cursor()
        #嵌套了一层select
        sql3 = "update bookInfo set borrowedQuantity=borrowedQuantity+1 where bookInfo.ISBN = (select book.ISBN from book where book.bookID=%d)" %(bookID)
        cur3.execute(sql3)
        
        #book
        cur7 = mysql.get_db().cursor()
        sql7 = "update book set state=1 where bookID=%d" %(bookID)
        cur7.execute(sql7)

        mysql.get_db().commit()

        reason = 'you have borrowed the book'
        
        return jsonify({'result': result,'reason': reason}), 201
    return jsonify({'result':'error'}),201

#还书
@app.route('/api/rebook',methods=['GET','POST'])
def rebook():
    error = None
    if request.method =='POST':
        bookID = request.form['bookID']
        bookID = int(bookID)
        userID = request.form['user_id']
        
        result = 'yes'
        reason = 'no problem'
        
        #判断是否输入有误
        cur5 = mysql.get_db().cursor()
        sql5 = "SELECT state from LendRecord where bookID= %d and readerID = \'%s\' and state <> '未借' and state <> '已还' " % (bookID,userID)
        cur5.execute(sql5)
        data = cur5.fetchall()

        if len(data)==0:
            reason = 'The record does not exist.'
            result = 'no'
            return jsonify({'result': result,'reason': reason}), 201
        returnTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #record
        cur = mysql.get_db().cursor()
        sql = "update LendRecord set returnTime=\'%s\',state='已还' where readerID=\'%s\' and bookID= %d  " % (returnTime,userID,bookID)
        cur.execute(sql)
        #reader
        cur2 = mysql.get_db().cursor()
        sql2 = "update reader set returnQuantity=returnQuantity+1,inBorrowQuantity=inBorrowQuantity-1 where readerID = \'%s\'"%(userID)
        cur2.execute(sql2)
        #bookInfo
        cur3 = mysql.get_db().cursor()
        sql3 = "update bookInfo set borrowedQuantity=borrowedQuantity-1 where ISBN = (select ISBN from book where bookID=%d)" %(bookID)
        cur3.execute(sql3)
        
        #book
        cur4 = mysql.get_db().cursor()
        sql4 = "update book set state=0 where bookID=%d" %(bookID)
        cur4.execute(sql4)

        mysql.get_db().commit()

        reason = 'you have returned the book'
        
        return jsonify({'result': result,'reason': reason}), 201
    return jsonify({'result':'error'}),201

"""
#添加bibliography中有， bookInfo不一定有的书，只能一本本添加，最原始的版本
@app.route('/api/add_book233',methods=['GET','POST'])
def add_book233():
    error = None
    if request.method =='POST':
        ISBN = request.form['ISBN']
        title = request.form['title']
        subtitle = request.form['subtitle']
        origin_title = request.form['origin_title']
        author = request.form['author']
        translator = request.form['translator']
        publisher =request.form['publisher']
        pubdate = request.form['pubdate']
        binding = request.form['binding']
        tags = request.form['tags']
        catalog = request.form['catalog']
        location = request.form['location']
        price = request.form['price']
        quantity = request.form['quantity']
        
        #如果bookInfo已有，则加一份copy
        cur = mysql.get_db().cursor()
        sql = "select * from bookInfo where ISBN=\'%s\'" % (ISBN)
        cur.execute(sql)
        data = cur.fetchall()
        list_data = list(data)
        list_len = len(list_data)
        if list_len!=0:#相当于add_copy的过程
            
            cur0 = mysql.get_db().cursor()
            sql0 = "update bookInfo set quantity=quantity+\'%d\' where ISBN=\'%s\'"%(quantity,ISBN)
            cur0.execute(sql0)
            
            for i in range(quantity):
                cur00 = mysql.get_db().cursor()
                sql00 = "insert into book(ISBN) values(\'%s\')"%(ISBN)
                cur00.execute(sql00)
                mysql.get_db().commit()
            result = 'yes'
            reason = 'you have added \'%d\' more copies of the book'%(quantity)
            return jsonify({'result': result,'reason': reason}), 201
        
        #相当于添加新书
        cur = mysql.get_db().cursor()
        sql = "insert into bookInfo(ISBN,location,quantity) values(\'%s\',\'%s\',\'%d\')" % (ISBN,location,quantity)
        cur.execute(sql)
        
        for i in range(quantity):
            cur2 = mysql.get_db().cursor()
            sql2 = "insert into book(ISBN) values(\'%s\')" % (ISBN)
            cur2.execute(sql2)
            mysql.get_db().commit()
        
        result = 'yes'
        reason = 'you have added \'%d\' new books'%(quantity)
        return jsonify({'result': result,'reason': reason}), 201
    return jsonify({'result':'error'}),201
"""
#加copy，已知该ISBN已经在静态图书中有信息了
@app.route('/api/add_book',methods=['GET','POST'])
def add_book():
    error = None
    if request.method =='POST':
        ISBN = request.form['ISBN']
        quantity = request.form['quantity']
        quantity = int(quantity)
        #update bookInfo
        cur0 = mysql.get_db().cursor()
        sql0 = "update bookInfo set quantity=quantity+%d where ISBN=\'%s\'"%(quantity,ISBN)
        cur0.execute(sql0)
        #insert book
        for i in range(quantity):
            cur00 = mysql.get_db().cursor()
            sql00 = "insert into book(ISBN) values(\'%s\')"%(ISBN)
            cur00.execute(sql00)
        mysql.get_db().commit()
        result = 'yes'
        reason = 'you have added %d more copies of the book'%(quantity)
        return jsonify({'result': result,'reason': reason}), 201
    return jsonify({'result':'error'}),201

# add_first_book，已知静态中亦未有记录，
@app.route('/api/add_first_book',methods=['GET','POST'])
def add_first_book():
    print '?'    
    error = None
    if request.method =='POST':
        
        ISBN = request.form['ISBN']
        title = request.form['title']
        subtitle = request.form['subtitle']
        origin_title = request.form['origin_title']
        author = request.form['author']
        translator = request.form['translator']
        publisher =request.form['publisher']
        pubdate = request.form['pubdate']
        binding = request.form['binding']
        tags = request.form['tags']
        catalog = request.form['catalog']
        location = request.form['location']
        price = request.form['price']
        quantity = request.form['quantity']
        quantity = int(quantity)
        cur0 = mysql.get_db().cursor()
        sql0 = "insert into bibliography(ISBN,title,subtitle,origin_title,author,translator,publisher,pubdate,binding,tags,catalog,price) values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')" % (ISBN,title,subtitle,origin_title,author,translator,publisher,pubdate,binding,tags,catalog,price)
        cur0.execute(sql0)
        
        cur = mysql.get_db().cursor()
        sql = "insert into bookInfo(ISBN,location,quantity) values(\'%s\',\'%s\',%d)" % (ISBN,location,quantity)
        cur.execute(sql)
        mysql.get_db().commit()
        
        for i in range(quantity):
            cur2 = mysql.get_db().cursor()
            sql2 = "insert into book(ISBN) values(\'%s\')" % (ISBN)
            cur2.execute(sql2)
            mysql.get_db().commit()
        
        result = 'yes'
        reason = 'you have added \'%d\' new books'%(quantity)
        return jsonify({'result': result,'reason': reason}), 201
    return jsonify({'result':'error'}),401

#删除操作book 特定某一本删除
@app.route('/api/delete_book',methods=['GET','POST'])
def delete_book():
    error = None
    if request.method =='POST':
        bookID = request.form['bookID']
        bookID = int(bookID)
        # 如果book 被借
        cur0 = mysql.get_db().cursor()
        sql0 = "select state from book where bookID = %d" % (bookID)
        cur0.execute(sql0)
        data0 = cur0.fetchall()
        list_data0 = list(data0)
        if len(list_data0) == 0:
            result = 'no'
            reason = 'the book does not exist.'
            return jsonify({'result': result,'reason': reason}), 201
        if list_data0[0][0]==1:
            result = 'no'
            reason = 'the book has been borrowed'
            return jsonify({'result': result,'reason': reason}), 201
        #如果book被 预约
        #检查是否该 book ISBN 是否全部被预约和借光
        cur4 = mysql.get_db().cursor()
        sql4 = "SELECT quantity,borrowedQuantity,reservedQuantity from bookInfo,book where bookInfo.ISBN=book.ISBN and book.bookID=%d" % (bookID)
        cur4.execute(sql4)
        data = cur4.fetchall()
        list_data = list(data)
        if list_data[0][0]==(list_data[0][1]+list_data[0][2]):
            result = 'no'
            reason = 'this book has been reserved or borrowed'
            return jsonify({'result': result,'reason': reason}), 201
        #bookInfo quantity-1
        cur2 = mysql.get_db().cursor()
        sql2 = "update bookInfo set quantity = quantity-1 where ISBN = (select ISBN from book where bookID =%d)" % (bookID)
        cur2.execute(sql2)

        cur = mysql.get_db().cursor()
        sql = "delete from book where bookID = %d" % (bookID)
        cur.execute(sql)

        mysql.get_db().commit()

        result = 'yes'
        reason = 'book\'%d\' has been deleted' %(bookID)
        return jsonify({'result': result,'reason': reason}), 201
    return jsonify({'result':'error'}),201

#根据ISBN查看 search_each_book_by_ISBN
@app.route('/api/search_each_book_by_ISBN',methods=['GET','POST'])
def search_each_book_by_ISBN():
    error = None
    if request.method =='GET':
        ISBN = request.args.get('ISBN')
        cur = mysql.get_db().cursor()
        sql = "select book.bookID,bookInfo.location,book.state from book,bookInfo where book.ISBN=bookInfo.ISBN and book.ISBN=\'%s\'" %(ISBN)
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

#配合search_each_book_by_ISBN 的 search_readerID_by_bookID
@app.route('/api/search_readerID_by_bookID',methods=['GET','POST'])
def search_readerID_by_bookID():
    error = None
    if request.method =='GET':
        bookID = request.args.get('bookID')
        bookID = int(bookID)
        cur2 = mysql.get_db().cursor()
        sql2 = "select readerID from LendRecord where bookID=%d" %(bookID)
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

#get_dynamicInfo_and_staticInfo
@app.route('/api/get_dynamicInfo_and_staticInfo',methods=['GET','POST'])
def get_dynamicInfo_and_staticInfo():
    error = None
    if request.method =='GET':
        ISBN = request.args.get('ISBN')
        cur = mysql.get_db().cursor()
        sql = "select * from bibliography,bookInfo where bibliography.ISBN=bookInfo.ISBN and bookInfo.ISBN=\'%s\'" %(ISBN)
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

#search_staticInfo
@app.route('/api/search_staticInfo',methods=['GET','POST'])
def search_staticInfo():
    error = None
    if request.method =='GET':
        ISBN = request.args.get('ISBN')
        cur = mysql.get_db.cursor()
        sql = "select * from bibliography where ISBN=\'%s\'" %(ISBN)
        cur.execute(sql)
        data = cur.fetchall()
        
        fields = cur.description
        column_list=[]
        for i in fields:
            column_list.append(i[0])
        
        list_data=list(data)
        bookID_and_location=[]
        for row in list_data:
            jsondata={}
            for i in range(len(column_list)):
                jsondata[column_list[i]] = row[i]
            result.append(jsondata)
                
        return jsonify({'result': result,'total':len(list_data)}), 201
    return jsonify({'result':'error'}),201

#search_dynamicInfo
@app.route('/api/search_dynamicInfo',methods = ['GET','POST'])
def search_dynamicInfo():
    error = None
    if request.method =='GET':
        
        ISBN = request.args.get('ISBN')
        
        cur = mysql.get_db().cursor()
        sql = "select * from bookInfo where ISBN=\'%s\'" %(ISBN)
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


#修改图书信息
@app.route('/api/edit_book',methods=['GET','POST'])
def edit_book():
    error = None
    if request.method =='POST':
        ISBN = request.form['ISBN']
        title = request.form['title']
        subtitle = request.form['subtitle']
        origin_title = request.form['origin_title']
        author = request.form['author']
        translator = request.form['translator']
        publisher =request.form['publisher']
        pubdate = request.form['pubdate']
        binding = request.form['binding']
        tags = request.form['tags']
        catalog = request.form['catalog']
        location = request.form['location']
        price = request.form['price']
        
        cur = mysql.get_db().cursor()
        sql = "update bibliography set title=\'%s\',subtitle=\'%s\',origin_title=\'%s\',author=\'%s\',translator=\'%s\',publisher=\'%s\',pubdate=\'%s\',binding=\'%s\',tags=\'%s\',catalog=\'%s\',price=\'%s\' where ISBN = \'%s\'" % (title,subtitle,origin_title,author,translator,publisher,pubdate,binding,tags,catalog,price,ISBN)
        cur.execute(sql)
        
        cur2 = mysql.get_db().cursor()
        sql2 = "update bookInfo set location=\'%s\' where ISBN = \'%s\'" % (location,ISBN)
        cur2.execute(sql2)
        
        mysql.get_db().commit()

        result = 'yes'
        reason = 'no problem'
        return jsonify({'result': result,'reason': reason}), 201
    return jsonify({'result':'error'}),201

#提醒列表预定图书名单、逾期还书名单、读者黑名单

#预定名单
@app.route('/api/get_reserve_list',methods = ['GET','POST'])
def get_reserve_list():
    error = None
    if request.method == 'GET':
        Time = datetime.datetime.now()
        curDay = datetime.date(Time.year,Time.month,Time.day)
        
        cur = mysql.get_db().cursor()
        sql = "select user.name,user.userID,bibliography.ISBN,bibliography.title,ReserveRecord.Invalid from ReserveRecord,bibliography,user where ReserveRecord.readerID = user.userID and ReserveRecord.ISBN = bibliography.ISBN"
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
        delta='delta_date'
        for row in new_data:
            jsondata={}
            for i in range (len(column_list)-1):
                jsondata[column_list[i]] = row[i]
            jsondata[delta] = (curDay-row[4]).days
            result.append(jsondata)
        return jsonify({'result': result,'total':len(new_data)}), 201
    return jsonify({'result':'error'}),201
#逾期名单
#逾期名单
@app.route('/api/get_outofdate_list',methods = ['GET','POST'])
def get_outofdate_list():
    error = None
    if request.method == 'GET':
        Time = datetime.datetime.now()
        curDay = datetime.date(Time.year,Time.month,Time.day)
        cur = mysql.get_db().cursor()
        sql = "select user.name,user.userID,bibliography.title,LendRecord.bookID,LendRecord.endTime from LendRecord,book,bibliography,user where bibliography.ISBN = book.ISBN and book.bookID = LendRecord.bookID and LendRecord.readerID = user.userID and LendRecord.state<>'已还'"
        cur.execute(sql)
        data = cur.fetchall()
        fields = cur.description
        column_list=[]
        for i in fields:
            column_list.append(i[0])
        list_data=list(data)
        result=[]
        count=0
        for row in list_data:
            endTime = row[4]
            if endTime < curDay:
                jsondata={}
                jsondata['endTime'] = (curDay-endTime).days
                count=count+1
                for i in range(len(column_list)-1):
                    jsondata[column_list[i]] = row[i]
                result.append(jsondata)
        return jsonify({'result': result,'total':count}), 201
    return jsonify({'result':'error'}),201


#获得黑名单
@app.route('/api/get_black_list',methods = ['GET','POST'])
def get_black_list():
    error = None
    if request.method == 'GET':
        cur = mysql.get_db().cursor()
        sql = "select user.name,user.userID from Blacklist,user where user.userID=Blacklist.readerID"
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
        
        
        cur_date = datetime.datetime.now()
        curDate = datetime.date(cur_date.year,cur_date.month,cur_date.day)
        
        for row in new_data:
            jsondata={}
            for i in range (len(column_list)):
                jsondata[column_list[i]] = row[i]
            cur_userID = row[1]
            cur0 = mysql.get_db().cursor()
            sql0 = "select bibliography.title,LendRecord.endTime from LendRecord,book,bibliography where LendRecord.bookID=book.bookID and LendRecord.readerID=\'%s\' and LendRecord.state='未还' and book.ISBN = bibliography.ISBN" %(cur_userID)
            cur0.execute(sql0)
            data0 = cur0.fetchall()
            list_data0=list(data0)
            fields0  = cur0.description
            column_list0 = []
            for j in fields0:
                column_list0.append(j[0])
            
            book=[]
            for row0 in data0:
                book.append(row0[0])
            #将book也放入字典形jsondata中
            jsondata['book'] = book
            #以上代码得到book{}字典类型的包含了cur_readerID所有的book_title
            days = []
            for row0 in data0:
                endTime = row0[1]
                days.append((curDate - endTime).days)
            #将days也放入jsondata中
            jsondata['days'] = days
            #将汇总后的jsondata放入result中
            result.append(jsondata)
        return jsonify({'result': result,'total':len(new_data)}), 201
    return jsonify({'result':'error'}),201


#删除黑名单的方法是： 修改reader.availableQuantity
@app.route('/api/remove_from_blacklist',methods=['GET','POST'])
def remove_from_blacklist():
    error = None
    if request.method == 'POST':
        readerID = request.form['readerID']
        
        cur = mysql.get_db().cursor()
        sql = "update reader set availableQuantity=5 where readerID = \'%s\'" % (readerID)
        cur.execute(sql)
        #不仅重新激活availableQuantity，同时修改returnQuantity和inBorrowQuantity
        cur2 = mysql.get_db().cursor()
        sql2 = "update reader set inBorrowQuantity=0,returnQuantity=returnQuantity+5 where readerID = \'%s\'" % (readerID)
        cur2.execute(sql2)
        
        #删除该项的黑名单
        cur0 = mysql.get_db().cursor()
        sql0 = "delete from Blacklist where readerID=\'%s\'" % (readerID)
        cur0.execute(sql0)
        
        #修改bookInfo,book
        cur4 = mysql.get_db().cursor()
        sql4= "select bookID from LendRecord where readerID=\'%s\' and state='未还'" %(readerID)
        cur4.execute(sql4)
        data = cur4.fetchall()
        list_data = list(data)
        for row in list_data:
            bookID=row[0]
            sql4 = "update bookInfo set borrowedQuantity=borrowedQuantity-1  where ISBN=(select ISBN from book where bookID= %d)" % (bookID)
            cur4.execute(sql4)
            sql4 = 'update book set state=0 where bookID=%d' % (bookID)
            cur4.execute(sql4)

        #修改LendRecord
        Time = datetime.datetime.now().strftime("%Y-%m-%d")
        cur3 = mysql.get_db().cursor()
        sql3 = "update LendRecord set returnTime=\'%s\' , state = '已还' where readerID = \'%s\' and state='未还'" % (Time,readerID)
        cur3.execute(sql3)

        

        mysql.get_db().commit()
        result = 'yes'
        reason = 'you have remove user\'%s\' from blacklist'%(readerID)
        return jsonify({'result': result,'reason': reason}), 201
    return jsonify({'result':'error'}),201


#reader预定
@app.route('/api/reader_reserve_list',methods = ['GET','POST'])
def reader_reserve_list():
    error = None
    if request.method == 'GET':
        
        userID = request.args.get('user_id')
        curTime = datetime.datetime.now()
        Time = datetime.date(curTime.year,curTime.month,curTime.day)
        
        cur = mysql.get_db().cursor()
        sql = "select ISBN,Invalid,submit from ReserveRecord where readerID=\'%s\' order by Invalid desc"%(userID)
        cur.execute(sql)
        data = cur.fetchall()
        list_data = list(data)

        result = []
        cout = 0
        for row in list_data:
            jsondata={}
            Invalid = row[1]
            ISBN = row[0]
            submit = row[2]
            if Invalid>Time:
                cout= cout+1
                jsondata['Invalid']=Invalid
                jsondata['ISBN'] = ISBN
                jsondata['submit']=submit
                cur2 = mysql.get_db().cursor()
                sql2 = "select image,location,title from bibliography,bookInfo where bibliography.ISBN=bookInfo.ISBN and bookInfo.ISBN=\'%s\'"%(ISBN)
                cur2.execute(sql2)
                data2 = cur2.fetchall()
                list_data2 = list(data2)
                
                jsondata['image']=list_data2[0][0]
                jsondata['location'] = list_data2[0][1]
                jsondata['title']=list_data2[0][2]
                result.append(jsondata)
        return jsonify({'result': result,'total':cout}), 201
    return jsonify({'result':'error'}),201

#展示历史预约
@app.route('/api/reader_reserve_history',methods = ['GET','POST'])
def reader_reserve_history():
    error = None
    if request.method == 'GET':
        
        userID = request.args.get('user_id')
        
        cur = mysql.get_db().cursor()
        sql = "select A.ISBN,A.location,ReserveRecord.Invalid,image,title,submit from bibliography,ReserveRecord,reader,bookInfo A where A.ISBN=bibliography.ISBN and A.ISBN=ReserveRecord.ISBN and ReserveRecord.readerID=reader.readerID and reader.readerID=\'%s\' order by Invalid desc" % (userID)
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

#展示已借图书列表
@app.route('/api/reader_lend_list',methods = ['GET','POST'])
def reader_lend_list():
    error = None
    if request.method == 'GET':
        
        userID = request.args.get('user_id')
        
        cur = mysql.get_db().cursor()
        sql = "select bibliography.title,a.bookID,a.startTime,a.endTime,a.returnTime,a.state,image,book.ISBN from LendRecord a,reader,book,bibliography where a.readerID=reader.readerID and reader.readerID=\'%s\' and book.bookID=a.bookID and book.ISBN=bibliography.ISBN and a.state<>'已还' order by a.startTime desc" % (userID)
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

#展示历史已借表
@app.route('/api/reader_lend_history',methods = ['GET','POST'])
def reader_lend_history():
    error = None
    if request.method == 'GET':
        
        userID = request.args.get('user_id')
        
        cur = mysql.get_db().cursor()
        sql = "select bibliography.title,a.bookID,a.startTime,a.endTime,a.returnTime,a.state,image,book.ISBN from LendRecord a,reader,book,bibliography where a.readerID=reader.readerID and reader.readerID=\'%s\' and book.bookID=a.bookID and book.ISBN=bibliography.ISBN order by a.startTime desc" % (userID)
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

#每日更新内容
"""def daily_update():
    error = None
    
    curTime = datetime.datetime.now()
    Time = datetime.date(curTime.year,curTime.month,curTime.day)
    
    #拿出既非已还，又非未还的历史 进行endTime判断
    cur = mysql.get_db().cursor()
    sql = "select endTime,readerID,bookID from LendRecord where state<>'未还' and state<>'已还'"
    cur.execute(sql)
    data = cur.fetchall()
    list_data = list(data)
    
    result = []
    
    for row in list_data:
        #如果endTime逾期了，就进行修改
        if row[0]<Time:
            cur_readerID = row[1]
            cur_bookID = row[2]
            cur_bookID = int(cur_bookID)
            sql = "update reader set  availableQuantity=availableQuantity-1   where reader.readerID=\'%s\'"%(cur_readerID)
            cur.execute(sql)
            sql = "update LendRecord set state='未还' where readerID=\'%s\' and bookID=%d"(cur_readerID,cur_bookID)
            cur.execute(sql)
            sql = "select availableQuantity,readerID from reader where readerID = \'%s\'"(cur_readerID)
            cur.execute(sql)
            data0 = cur.fetchall()
            list_data0 = list(data0)
            #available = 0 拉进黑名单
            if list_data0[0]==0:
                regenateTime=datetime.datetime.now().strftime("%Y-%m-%d")
                black_reader = list_data0[1]
                sql = "insert into Blacklist(readerID,regenateTime) values(\'%s\',\'%s\')" % (black_reader,regenateTime)
                cur.execute(sql)
    mysql.get_db().submit()
    result ='yes'
    reason = 'no problem'
    return jsonify({'result': result,'reason':reason})"""

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
        
        print searchText, searchType, searchPage
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

