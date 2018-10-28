from flask import Flask, session, redirect, url_for, escape, request, render_template
from hashlib import md5
import MySQLdb

app = Flask(__name__)

db = MySQLdb.connect(host="localhost", user=user, passwd=password, db=dbname)
cur = db.cursor()

@app.route('/')
def index():
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('index.html', session_user_name=username_session)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if 'username' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username_form  = request.form['username']
        password_form  = request.form['password']
        cur.execute("SELECT COUNT(1) FROM employee WHERE name = %s;", [username_form]) # CHECKS IF USERNAME EXSIST
        if cur.fetchone()[0]:
            cur.execute("SELECT ssn FROM employee WHERE name = %s;", [username_form]) # FETCH THE HASHED PASSWORD
            for row in cur.fetchall():
                if password_form == row[0]:
                    session['username'] = request.form['username']
                    return redirect(url_for('index'))
                else:
                    error = "Invalid Credential"
        else:
            error = "Invalid Credential"
    return render_template('login.html', error=error)
@app.route('/residents', methods=['GET', 'POST'])
def residents():
    query="SELECT Door_No,Block_No,R_Name,Phone,Email FROM RESIDENT"
    cur.execute(query)
    items = cur.fetchall()
    return render_template('display.html',items=items)

@app.route('/services')
def services():
    query="SELECT * from services"
    cur.execute(query)
    items = cur.fetchall()
    return render_template('services.html',items=items)
    
@app.route('/calendar')
def calendar():
    query="SELECT * from calendar"
    cur.execute(query)
    items = cur.fetchall()
    return render_template('calendar.html',items=items)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run(debug=True)
