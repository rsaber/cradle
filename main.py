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
        if request.form['username'] and request.form['password']:
            usr = request.form['username']
            passw = request.form['password']
            c = db.execute("SELECT PASSWORD FROM USERS WHERE NAME=?", (usr,)).fetchall()
            if not 0 in c:
                return render_template('landing.html', fail=1)
            if passw == c[0][0]:
                return render_template('dashboard.html')
            else:
                return render_template('landing.html', fail=1)
        else:
            return render_template('landing.html', fail=1)
    return render_template('landing.html', fail=0)

@app.route('/course/<code>', methods=['GET', 'POST'])
def getCourse(code):
    db = get_db()
    cursor = db.execute("SELECT OBJECT FROM COURSES WHERE NAME=?", (code,)).fetchall()
    course = pickle.loads(cursor[0][0])
    if request.method == "POST" and request.form['navbar']:
        course.updateState(request.form['navbar']) #update state
    return render_template('layout.html', course=course.name, navbar=course.getNavbar(), content=course.getContent())


if __name__ == '__main__':
    app.run()