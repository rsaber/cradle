from flask import Flask, render_template, request

app = Flask(__name__)

# Classes

# Navbar object has
#   a array of navbar elements
#   the current active element
class Navbar:
    def __init__(self, elements):
        self.elements = elements
        self.active = ""
    def updateActive(self, state):
        self.active = state
    def getButtons(self):
        toSend = []
        for name in self.elements:
            if name == self.active:
                toSend.append('<button type="submit" name="navbar" value="'+name+'" class="list-group-item list-group-item-action active ">'+name+'</button>')
            else:
                toSend.append('<button type="submit" name="navbar" value="'+name+'" class="list-group-item list-group-item-action">'+name+'</button>')
        return toSend
# Course object has
#   a Navbar object
#   a name
#   the current state
#   a get content state function which takes in current state
#   a get content wrapper function

class Course:
    def __init__(self, nav, name, defaultState, getStateContent):
        self.navbar = nav
        self.navbar.updateActive(defaultState)
        self.name = name
        self.state = defaultState
        self.getStateContent = getStateContent
    def getNavbar(self):
        return self.navbar.getButtons()
    def getContent(self):
        return self.getStateContent(self.state)
    def updateState(self, newState):
        self.state = newState
        self.navbar.updateActive(newState)
#testing data
def COMP1234CONTENT(state):
    if state == "Homepage":
        return ''''
        <h2>Welcome to COMP1234!</h2>
        <h4>This text will be written in Markdown and published using cradle</h4>
        <p>Hi everyone, welcome to this course. I hope you learn everything you need to</p>
        '''
    elif state == "Course Outline":
        return ''''
        <h2>COMP1234 Pass Requirments</h2>
        <p>how about you don't be stupid</p>
        '''
    elif state == "Timetable":
        return ''''
        <h2>COMP1234 Only Class</h2>
        <p>it's at fuck off o'clock</p>
        '''
navArray = ["Homepage", "Course Outline", "Timetable", "Labs", "Assignments", "Tutors"]
nav = Navbar(navArray)
COMP1234 = Course(nav, "COMP1234", "Homepage", COMP1234CONTENT)


# Routing code

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == "POST":
        #update navbar
        if request.form['navbar']:
            COMP1234.updateState(request.form['navbar'])
    return render_template('layout.html', navbar = COMP1234.getNavbar(), course=COMP1234.name, content=COMP1234.getContent())


if __name__ == '__main__':
    app.run()