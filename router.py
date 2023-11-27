import os
from flask import Flask, send_from_directory, request, session, redirect, render_template
from dotenv import load_dotenv
from app.loan import StandardLoan
from app.priority_queue import PriorityQueue

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('APP_KEY')

# TODO Replace with actual db lol
db = {
  'userLoans': [
    [6228.66, 3.52, 745.10, "Loan 1", 240],
    [5117.88, 1.22, 301.24, "Loan 2", 120],
    [4346.09, 1.77, 145.67, "Loan 3", 120],
    [1336.35, 2.4, 99.99, "Loan 4", 120]
  ]
}

# TODO Lookup loans and return completed queue object
def get_user_queue_from_db():
  user_loans = [StandardLoan(loan[0], loan[1], pa=loan[2], title=loan[3], term=loan[4]) for loan in db['userLoans']]
  user_queue = PriorityQueue(user_loans, 1292.00, 'User Queue')
  # user_queue.payoff()
  return user_queue

# This is just to store Loans in session until we connect db
# @app.before_request
# def make_session_permanent():
#   session.permanent = True

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
    term = int(data['term'])
    title = data['title']
    loan = StandardLoan(start_balance, interest_rate, pa=payment_amt, title=title, term=term)
    isValid = loan.payoff()
    if isValid:
      # TODO Add loan to db
      db['userLoans'].append([loan.start_balance, loan.int_rate, loan.payment_amt, loan.title, loan.term])
      loanJson = loan.to_json()
      return loanJson
    else:
      return 'Payments cannot cover interest.', 400

# @app.route("/api/loan/payoff", methods=["GET", "POST"])
# def payoff_loan():
#   if request.method == "POST":
#     data = request.json
#     # title = data['title']
#     # loan = next((loan for loan in session['loans'] if loan['title'] == data['title']), None)
#     start_balance = float(data['startBalance'])
#     interest_rate = float(data['interestRate'])
#     payment_amt = float(data['paymentAmt'])
#     title = data['title']
#     loan = StandardLoan(start_balance, interest_rate, payment_amt, title)
#     # loan.payoff()
#     return loan.to_json()
  
# @app.route("/api/loans/payoff", methods=["GET", "POST"])
# def payoff_loans():
#   if request.method == "POST":
#     # data = request.json
#     return

@app.route("/api/loans")
def get_user_loans():
  # TODO Get user loans from database, solve them all
  user_queue = get_user_queue_from_db()
  user_queue.payoff()
  return {
    "loans": user_queue.to_json(),
    "analysis": user_queue.get_analysis()
  }

@app.route("/api/queues")
def get_user_queues():
  # if 'loans' not in session:
  #   session['loans'] = []
  # Get user loans from database, solve them all
  user_queue = get_user_queue_from_db()
  avalanche = user_queue.avalanche()
  blizzard = user_queue.blizzard()
  cascade = user_queue.cascade()
  iceSlide = user_queue.ice_slide()
  snowball = user_queue.snowball()
  return {
    "avalanche": {
      "loans": avalanche.to_json(),
      "analysis": avalanche.get_analysis()
    },
    "blizzard": {
      "loans": blizzard.to_json(),
      "analysis": blizzard.get_analysis()
    },
    "cascade": {
      "loans": cascade.to_json(),
      "analysis": cascade.get_analysis()
    },
    "iceSlide": {
      "loans": iceSlide.to_json(),
      "analysis": iceSlide.get_analysis()
    },
    "snowball": {
      "loans": snowball.to_json(),
      "analysis": snowball.get_analysis()
    }
  }
