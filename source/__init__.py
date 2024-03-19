# Import the Flask class from the flask module
from flask import Flask

# Create an instance of the Flask class
# __name__ is a special Python variable that represents the name of the current module
app = Flask(__name__)

# Import the routes module from the source package
# This is where you define the URL routes and corresponding view functions
from source import routes