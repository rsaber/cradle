import os
from markdown2 import markdown_path
# Classes

# Navbar object has
#   a array of navbar elements
#      Sub elements are put into a array (max 1 level deep)
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
            if type(name) is str:
                if name == self.active:
                    toSend.append('<button type="submit" name="navbar" value="'+name+'" class="list-group-item list-group-item-action active ">'+name+'</button>')
                else:
                    toSend.append('<button type="submit" name="navbar" value="'+name+'" class="list-group-item list-group-item-action">'+name+'</button>')
            elif type(name) is list:
                if name == self.active:
                    #expand
                    toSend.append('<button type="submit" name="navbar" value="' + name + '" class="list-group-item list-group-item-action">' + name + '</button>')

                else:
                    toSend.append('<button type="submit" name="navbar" value="' + name + '" class="list-group-item list-group-item-action">' + name + '</button>')
        return toSend

# Course object has
#   a Navbar object
#   a name
#   the current state
#   a documents dict of holding the name of the relevent markdown document for a given state
#   a get content wrapper function

class Course:
    def __init__(self, nav, name, defaultState, documents):
        self.navbar = nav
        self.navbar.updateActive(defaultState)
        self.name = name
        self.state = defaultState
        self.documents = documents
    def getNavbar(self):
        return self.navbar.getButtons()
    def getContent(self):
        path = "courses/"+self.name+"/"+self.documents[self.state]
        markdown = '<div class="markdown-generated-output">\n'
        markdown = markdown + markdown_path(path, extras=["tables"])
        markdown = markdown + "</div>"
        return markdown
    def updateState(self, newState):
        self.state = newState
        self.navbar.updateActive(newState)