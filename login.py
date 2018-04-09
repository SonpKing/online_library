
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash,jsonify
from flaskext.mysql import MySQL
import json
import cgi

mysql = MySQL()
app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'  
app.config['MYSQL_DATABASE_USER'] = 'uysk'
app.config['MYSQL_DATABASE_PASSWORD'] = 'pswd'
app.config['MYSQL_DATABASE_DB'] = 'library'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/',methods=['GET','POST'])
def index():
    error = None
    if request.method == 'POST':
        #form = cgi.FieldStorage()
        #searchText = form['search']
        searchText=request.args.get('search')
        #searchType=request.args.get('type')
        #searchText=str(searchText)
        print searchText
        return render_template('searchResult.html',searchText=searchText)
    """cur1 = mysql.get_db().cursor()
    cur1.execute('select title,author from bibliography where ISBN = "9787010002095"')
    entries = [dict(title=row[0], text=row[1]) for row in cur1.fetchall()]
    return render_template('show_entries.html', entries=entries)"""

    return render_template('index.html')


@app.route('/sss',methods=['GET','POST'])
def sss():
    error = None
    if request.method == 'POST':
        #form = cgi.FieldStorage()
        #searchText = form['search']
        searchText=request.form.get('search')
        #searchType=request.args.get('type')
        #searchText=str(searchText)
        print searchText
        return render_template('searchResult.html',searchText=searchText)
    """cur1 = mysql.get_db().cursor()
    cur1.execute('select title,author from bibliography where ISBN = "9787010002095"')
    entries = [dict(title=row[0], text=row[1]) for row in cur1.fetchall()]
    return render_template('show_entries.html', entries=entries)"""

    return render_template('index.html')
	
	
@app.route('/add', methods=['POST'])
def add_entry():
    a = A()
    if not session.get('logged_in'):
        abort(401) 
    cur2 = mysql.get_db().cursor()
    sql = "insert into Book(bookName,description) values (\'%s\',\'%s\')" % (request.form['title'],request.form['text'])
    cur2.execute(sql)
    mysql.get_db().commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        us=request.form['username']
        pw=request.form['password']
        cur3 = mysql.get_db().cursor()
        sql = "SELECT * from user where id=\'%s\'" % (us)
        cur3.execute(sql)
        data = cur3.fetchone()
        if data is None:
            error = 'Invalid username'
            flash('Invalid username')
            return render_template('login.html', error=error)
        sql = "SELECT * from user where id=\'%s\' and password=\'%s\'" % (us,pw)
        cur3.execute(sql)
        data = cur3.fetchone()
        if data is None:
            error = 'Invalid password'
            flash('Invalid password')
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        sus=request.form['username']
        spw=request.form['password']
        cpw=request.form['conpswd']
        cur4 = mysql.get_db().cursor()
        sql="SELECT * from user where id=\'%s\'" % (sus)
        cur4.execute(sql)
        data = cur4.fetchone()
        if data is not None:
            error = 'username already used'
            flash('username already used')
        elif spw!=cpw:
            error = 'confirm password is not same'
            flash('confirm password is not same')
        else:
            sql = "insert into user(id,passWord) values (\'%s\',\'%s\')" % (sus,spw)
            cur4.execute(sql)
            mysql.get_db().commit()
            flash('You have signed up!')
            return render_template('login.html', error=error)
    return render_template('signup.html', error=error)

@app.route('/search', methods=['GET','POST'])
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
        for i in range(start_item,end_item):
                last_data.append(new_data[i]) 
        result=[]
        for row in last_data:
            jsondata={}
            for i in range(len(column_list)):
                jsondata[column_list[i]] = row[i]
            result.append(jsondata)
        return jsonify({'result': result}), 201
    return jsonify({'result':'error'}),400
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0',port=80)

