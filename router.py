import os
from flask import Flask, send_from_directory, request, session, redirect, render_template
from dotenv import load_dotenv
from app.loan import *

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('APP_KEY')

# This is just to store Loans in session until we connect db
@app.before_request
def make_session_permanent():
  session.permanent = True

@app.route("/")
def main():
  if 'username' not in session:
    return redirect("/login")
  return send_from_directory('./client/dist/', 'index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    username = request.args.get("username")
    session['username'] = request.form['username']
    return redirect("/")
  elif 'username' in session:
    return redirect("/")
  else:
    return send_from_directory('./client/dist/', 'index.html')

@app.route("/logout")
def logout():
  session.clear()
  return redirect("/login")

@app.route("/assets/<filename>")
def assets(filename):
  return send_from_directory('./client/dist/assets/', filename)

@app.route("/api/loan/new", methods=["GET", "POST"])
def new_loan():
  if request.method == "POST":
    data = request.json
    start_balance = float(data['startBalance'])
    interest_rate = float(data['interestRate'])
    payment_amt = float(data['paymentAmt'])
    title = data['title']
    loan = StandardLoan(start_balance, interest_rate, payment_amt, title).to_json()
    # TODO replace with DB
    if 'loans' not in session:
      session['loans'] = []
    session['loans'].append(loan)
    return loan

@app.route("/api/loan/payoff", methods=["GET", "POST"])
def payoff_loan():
  if request.method == "POST":
    data = request.json
    title = data['title']
    loan = next((loan for loan in session['loans'] if loan['title'] == data['title']), None)
    return loan.to_json()

@app.route("/api/loans")
def get_user_loans():
  if 'loans' not in session:
    session['loans'] = []
  return session['loans']