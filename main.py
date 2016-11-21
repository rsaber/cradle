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
@app.route('/course/<code>', methods=['GET', 'POST'])
def main(code):
    db = get_db()
    cursor = db.execute("SELECT OBJECT FROM COURSES WHERE NAME=?", (code,)).fetchall()
    course = pickle.loads(cursor[0][0])
    if request.method == "POST" and request.form['navbar']:
        course.updateState(request.form['navbar']) #update state
    return render_template('layout.html', course=course.name, navbar=course.getNavbar(), content=course.getContent())


if __name__ == '__main__':
    app.run()