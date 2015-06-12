from flask import Flask
from flask_sslify import SSLify

app = Flask(__name__)
app.config.from_object('config')
sslify = SSLify(app)

from jawfish import views
