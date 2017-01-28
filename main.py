from flask import Flask, render_template, request, g, session, redirect
import pickle
from Course import Navbar, Course
import sqlite3, os
app = Flask(__name__)
app.secret_key = 'FUCK YOU SHOULD NOT BE SEEING THIS'


#setting up the databse code was greatly influenced by:
# http://stackoverflow.com/questions/28126140/python-sqlite3-operationalerror-no-such-table
# http://flask.pocoo.org/docs/0.11/patterns/sqlite3/
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "database.sqlite")
        db = g._database = sqlite3.connect(db_path)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Routing code
@app.route('/', methods=['GET', 'POST'])
def main():
    db = get_db()
    if request.method == "POST":
        if request.form['email'] and request.form['password']:
            usr = request.form['email']
            passw = request.form['password']
            c = db.execute("SELECT PASSWORD FROM USERS WHERE EMAIL=?", (usr,)).fetchall()
            if not 0 in c:
                return render_template('landing.html', fail=1)
            if passw == c[0][0]:
                return render_template('dashboard.html')
            else:
                return render_template('landing.html', fail=1)
        else:
            return render_template('landing.html', fail=1)
    return render_template('landing.html', fail=0)

@app.route('/register', methods=['GET', 'POST'])
def getRegister():
    db = get_db()
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        pass1 = request.form['password1']
        pass2 = request.form['password2']
        PCF=0
        PF=0
        EF=0
        if len(pass1) < 6:
            PCF = 1
        if pass1 != pass2:
            PF = 1
        c = db.execute("SELECT EMAIL FROM USERS WHERE EMAIL=?", (email,)).fetchall()
        try:
            c[0][0]
        except IndexError:
            EF=0
        else:
            EF = 1
        if EF or PCF or PF:
            return render_template('register.html', emailFail=EF, passwordFail=PF, passwordCharFail=PCF, name=name, email=email)
        else:
            db.execute("INSERT INTO USERS (EMAIL, NAME, PASSWORD) VALUES (?,?,?)", (email, name, pass1))
            db.commit()
            return  render_template('dashboard.html')
    return render_template('register.html', emailFail=0, passwordFail=0, passwordCharFail=0)

@app.route('/course/<code>', methods=['GET', 'POST'])
def getCourse(code):
    db = get_db()
    cursor = db.execute("SELECT OBJECT FROM COURSES WHERE NAME=?", (code,)).fetchall()
    course = pickle.loads(cursor[0][0])
    if request.method == "POST" and request.form['navbar']:
        course.updateState(request.form['navbar']) #update state
    return render_template('coursePage.html', course=course.name, navbar=course.getNavbar(), content=course.getContent())


if __name__ == '__main__':
    app.run()