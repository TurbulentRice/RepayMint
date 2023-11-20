import os
from flask import Flask, send_from_directory, request, session, redirect, render_template
from dotenv import load_dotenv
from loan import *

load_dotenv()  # take environment variables from .env.

app = Flask(__name__)
app.secret_key = os.environ.get('APP_KEY')

cached_loan = None

@app.route("/")
def main():
  if 'username' in session:
    return send_from_directory('./dist/', 'index.html')
  else:
    return redirect('/login')

@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "GET":
    return send_from_directory('./dist/', 'index.html')
  elif request.method == "POST":
    username = request.args.get("username")
    session['username'] = request.form['username']
    # password = request.args.get("password")
    # session['password'] = request.form['password']
    return redirect('/')


@app.route("/assets/<filename>")
def assets(filename):
  return send_from_directory('./dist/assets/', filename)

# @app.route("/lib/<filename>")
# def lib(filename):
#   print('FILENAME: ' + filename)
#   return send_from_directory('./node_modules/', filename)

@app.route("/api/loan", methods=["GET", "POST"])
def api():
  if request.method == "POST":
    data = request.json
    start_balance = float(data['startBalance'])
    interest_rate = float(data['interestRate'])
    payment_amt = float(data['paymentAmt'])
    title = data['title']
    loan = StandardLoan(start_balance, interest_rate, payment_amt, title)
  return loan.Payment_History