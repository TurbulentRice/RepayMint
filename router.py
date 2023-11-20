import os
from flask import Flask, send_from_directory, request
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

app = Flask(__name__)

@app.route("/")
def main():
  return send_from_directory('./dist/', 'index.html')

@app.route("/assets/<filename>")
def assets(filename):
  return send_from_directory('./dist/assets/', filename)

@app.route("/api/")
def api():
  if request.method == "POST":
    request.args.get()
  return "butt"