from flask import Flask, session, redirect, url_for, escape, request, render_template,json
from hashlib import md5
import MySQLdb

app = Flask(__name__)

db = MySQLdb.connect(host="localhost", user="Michelle", passwd="pass", db="hodor")
cur = db.cursor()

@app.route('/', methods=['GET'])

def home():

    # Main page

    return render_template('home.html')

@app.route('/login')

def index():

    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('index.html', session_user_name=username_session)
    return redirect(url_for('logout'))


@app.route('/signIn', methods=['GET', 'POST'])
def signIn():
    error = None
    if 'username' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username_form  = request.form['username']
        password_form  = request.form['password']
        cur.execute("SELECT COUNT(1) FROM RESIDENT WHERE R_name = %s;", [username_form]) # CHECKS IF USERNAME EXSIST
        if cur.fetchone()[0]:
            cur.execute("SELECT Password FROM RESIDENT WHERE R_name = %s;", [username_form]) # FETCH THE HASHED PASSWORD
            for row in cur.fetchall():
                if password_form == row[0]:
                    session['username'] = request.form['username']
                    return redirect(url_for('index'))
                else:
                    error = "Invalid Credential"
        else:
            error = "Invalid Credential"
    return render_template('log.html', error=error)

@app.route('/signup',methods=['GET','POST'])
def signup():
  if request.method=='POST':
    Door_No=request.form['door']
    Block_No=request.form['block']
    R_Name=request.form['name']
    Phone=request.form['phone']
    Residency_Type=request.form['rtype']
    Email=request.form['email']
    Password=request.form['passw']
    query="INSERT INTO resident(Door_No,Block_No,R_Name,Phone,Residency_Type,Email,Password) VALUES(%s,%s,%s,%s,%s,%s,%s)"
    cur.execute(query,(Door_No,Block_No,R_Name,Phone,Residency_Type,Email,Password))
    db.commit()
  return render_template('signup.html')
    
    
@app.route('/residents', methods=['GET', 'POST'])
def residents():
    query="SELECT Door_No,Block_No,R_Name,Phone,Residency_Type,Email FROM RESIDENT"
    cur.execute(query)
    items = cur.fetchall()
    return render_template('residents.html',items=items)

@app.route('/services',methods=['GET','POST'])
def services():
    if request.method=='POST':
        intime = request.form['intime']
        outtime = request.form['outtime']
        service = request.form['service']
        query="select S_ID,S_Name ,Type_Of_Service from services s where not exists(select In_Time,Out_Time from avail_Service a where In_Time<= '"+intime+"' and Out_Time>= '"+outtime+"' and a.S_Id=s.S_ID) and s.Type_Of_Service='"+service+"' "
        cur.execute(query)
        items = cur.fetchall()
        db.commit()
        return render_template('services.html',items=items)
    else:
            error = "Invalid Credential"
    return render_template('services.html',error=error)

@app.route('/avail',methods=['GET','POST'])
def avail():
  if request.method=='POST':
    S_ID=request.form['sid']
    Door_No=request.form['door']
    In_Time = request.form['intime']
    Out_Time = request.form['outtime']
    query="INSERT INTO avail_service(S_ID,Door_No,In_Time,Out_Time) VALUES(%s,%s,%s,%s)"
    cur.execute(query,(S_ID,Door_No,In_Time,Out_Time))
    db.commit()
  return render_template('avail.html')

@app.route('/calendar')
def calendar():
    query="call delete_old()"
    cur.execute(query)
    items = cur.fetchall()
    db.commit()
    query="SELECT * from calendar order by DATE"
    cur.execute(query)
    items = cur.fetchall()
    return render_template('calendar.html',items=items)

@app.route('/oldevents')
def oldevents():
    query="SELECT * from OLD_CALENDAR  order by DATE"
    cur.execute(query)
    items = cur.fetchall()
    return render_template('past.html',items=items)

   
@app.route('/booking',methods=['GET','POST'])
def booking():
    error = None
    if request.method=='POST':
        E_ID=request.form['eid']
        Door_No=request.form['door']
        No_Of_People=request.form['people']
        query="INSERT INTO booking(E_ID,Door_No,No_Of_People) VALUES(%s,%s,%s)"
        cur.execute(query,(E_ID,Door_No,No_Of_People))
        db.commit()
    return render_template('booking.html',error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run(debug=True)
