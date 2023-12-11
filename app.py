import os
from flask import Flask, send_from_directory, session, redirect, g
from dotenv import load_dotenv
from routes.api import api

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('APP_KEY')

app.register_blueprint(api, url_prefix='/api')

def client():
  return send_from_directory('./client/dist/', 'index.html')

@app.before_request
def check_user():
  g.user = session.get('user', None)

@app.route("/")
def main():
  if not g.user:
    return redirect("/login")
  return client()

@app.route("/assets/<filename>")
def assets(filename):
  return send_from_directory('./client/dist/assets/', filename)

@app.route("/logout")
def logout():
  session.pop('user', None)
  return redirect("/login")

@app.route("/login")
def login():
  return client()

@app.errorhandler(404)
def page_not_found():
  return redirect("/login")
