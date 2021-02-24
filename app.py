from flask import Flask
#following code creates a new Flask instance call app
app = Flask(__name__)
#First, we need to define the starting point, also known as the root. To do this, we'll use the function @app.route('/'). Add this to your code now.
@app.route('/')
def hello_world():
    return 'Hello world'
def surfs_up():
    return "Surf's up"
