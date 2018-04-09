
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash,jsonify
from flaskext.mysql import MySQL
import json

mysql = MySQL()
app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'  
app.config['MYSQL_DATABASE_USER'] = 'uysk'
app.config['MYSQL_DATABASE_PASSWORD'] = 'pswd'
app.config['MYSQL_DATABASE_DB'] = 'library'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


class A(object):
    count = 2
    def __init__(self):
        A.count += 1
        self.order = A.count

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
        
        print searchText
        return render_template('searchResult.html',searchText=searchText)
    """cur1 = mysql.get_db().cursor()
    cur1.execute('select title,author from bibliography where ISBN = "9787010002095"')
    entries = [dict(title=row[0], text=row[1]) for row in cur1.fetchall()]
    return render_template('show_entries.html', entries=entries)"""

    return "error"
	

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0',port=80)

