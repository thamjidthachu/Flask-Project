import sqlite3
from flask import *

app = Flask(__name__)
app.secret_key="abcbc"

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('student_create.html')

@app.route('/savedata',methods=['POST'])
def savestudent():
    if request.method == 'POST':
        na = request.form['sname']
        ag = request.form['sage']
        em = request.form['semail']
        pl = request.form['splace']
        un = request.form['uname']
        pw = request.form['spass']
        con = sqlite3.connect('studentData.db')
        cursr = con.cursor()
        cursr.execute('insert into student(name,age,email,place,username,password) values(?,?,?,?,?,?)',(na,ag,em,pl,un,pw))
        con.commit()
        return redirect(url_for('studview'))


@app.route('/view')
def studview():
    con = sqlite3.connect('studentData.db')
    con.row_factory = sqlite3.Row
    cursr = con.cursor()
    cursr.execute('select * from student')
    r = cursr.fetchall()
    return render_template('student_view.html',view=r)




@app.route('/studdel/<id>')
def studentdelete(id):
    con = sqlite3.connect('studentData.db')
    cursr = con.cursor()
    cursr.execute('delete from student where studid=?',(id))
    con.commit()
    return redirect(url_for('studview'))

@app.route('/studedit/<id>',methods=['POST','GET'])
def studentedited(id):
    if request.method == 'POST':
        na = request.form['sname']
        ag = request.form['sage']
        em = request.form['semail']
        pl = request.form['splace']
        con = sqlite3.connect('studentData.db')
        cursr = con.cursor()
        cursr.execute('update student set name=?, age=?, email=?, place=? where studid=?',(na,ag,em,pl,id))
        con.commit()
        return redirect(url_for('home'))
    else :
        con = sqlite3.connect('studentData.db')
        con.row_factory = sqlite3.Row
        cursr = con.cursor()
        cursr.execute('select * from student where studid=?',(id))
        r = cursr.fetchall()
        return render_template('student_view.html',edit=r)



@app.route('/studentedit/<id>')
def studentedits(id):
    con = sqlite3.connect('studentData.db')
    con.row_factory = sqlite3.Row
    cursr = con.cursor()
    cursr.execute('select * from student where studid=?',(id))
    r = cursr.fetchall()
    return render_template('student_update.html',edit=r)
 

@app.route('/authenticate',methods=['GET','POST'])
def autheticate():
    if request.method == 'POST':
        un = request.form['username']
        pw = request.form['password']
        con = sqlite3.connect('studentData.db')
        con.row_factory = sqlite3.Row
        cursr = con.cursor()
        cursr.execute('select * from student where username=? and password=?',(un,pw))
        r = cursr.fetchone()

        if r[9] == "Yes":
            cursr.execute('select * from student where admin!=? and teacher!=?',('Yes','Yes'))
            data = cursr.fetchall()
            return render_template('teacher_view.html',view=data)
        elif r[8] == "Yes":
            cursr.execute('select * from student')
            data = cursr.fetchall()
            return render_template('student_view.html',view=data)
        elif (r[7] == "Yes"):
            cursr.execute('select * from student where admin!=? and teacher=?',('Yes','Yes'))
            data = cursr.fetchall()
            return render_template('individual_view.html',view=r,staff=data)
        else:
            return "Unauthorised Credentials"


@app.route('/approve/<id>')
def approve(id):
    con = sqlite3.connect('studentData.db')
    con.row_factory = sqlite3.Row
    cursr = con.cursor()
    cursr.execute('update student set status=? where studid=?',('Yes',id))
    con.commit()
    return redirect(url_for('studview'))


@app.route('/makestaff/<id>')
def makestaff(id):
    con = sqlite3.connect('studentData.db')
    con.row_factory = sqlite3.Row
    cursr = con.cursor()
    cursr.execute('update student set teacher=? where studid=?',('Yes',id))
    con.commit()
    return redirect(url_for('studview'))

@app.route('/makeadmin/<id>')
def makeadmin(id):
    con = sqlite3.connect('studentData.db')
    con.row_factory = sqlite3.Row
    cursr = con.cursor()
    cursr.execute('update student set admin=? where studid=?',('Yes',id))
    con.commit()
    return redirect(url_for('studview'))




    



if __name__ == "__main__" :
    app.run(debug=True)