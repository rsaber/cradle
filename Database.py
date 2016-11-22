from Course import Course, Navbar
import sqlite3, os
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.sqlite")
gen = sqlite3.connect(db_path)
gen.execute('''
	CREATE TABLE COURSES(
		NAME STRING PRIMARY KEY NOT NULL,
		OBJECT BLOB
	)
''')
gen.execute('''
	CREATE TABLE USERS(
		NAME STRING PRIMARY KEY NOT NULL,
		PASSWORD STRING
	)
''')
#testing data
navArray = ["Homepage", "Course Outline", "Timetable", "Labs", "Assignments", "Tutors"]
docArray = {
    "Homepage" : "Homepage.md",
    "Course Outline" : "CourseOutline.md",
    "Timetable" : "Timetable.md",
    "Labs" : "Labs.md",
    "Assignments" : "Assignments.md",
    "Tutors" : "Tutors.md"
}
nav = Navbar(navArray)
COMP1234 = Course(nav, "COMP1234", "Homepage", docArray)

gen.execute("INSERT INTO COURSES (NAME, OBJECT) VALUES (?,?)", ("COMP1234", pickle.dumps(COMP1234)))
gen.execute("INSERT INTO USERS (NAME, PASSWORD) VALUES (?,?)", ("Zain", "1234"))
gen.commit()