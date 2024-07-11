# main.py
# This file initializes the Flask application and sets up the main configurations.

from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
    from address_routes import *
    app.run(debug=True)
