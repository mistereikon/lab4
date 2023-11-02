from flask import Flask, url_for

app = Flask(__name__)
app.secret_key = b'secret'
app.static_url_path = '/static'

from app import views
