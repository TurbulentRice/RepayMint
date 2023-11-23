import os
from flask import Flask, send_from_directory, request, session, redirect, render_template
from dotenv import load_dotenv
from app.loan import StandardLoan
from app.priority_queue import PriorityQueue

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('APP_KEY')

# From README example
example_queue = PriorityQueue([
  StandardLoan(16228.66, 3.52, title="Loan 1"),
  StandardLoan(14346.09, 1.77, title="Loan 2"),
  StandardLoan(9336.35, 2.4, title="Loan 3"),
  StandardLoan(5117.88, 1.22, title="Loan 4"),
], 1713.39, 'Test Queue')
# example_method_compare = example_queue.finish()

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
    loan = StandardLoan(start_balance, interest_rate, payment_amt, title)
    loan.payoff()
    loanJson = loan.to_json()
    # TODO replace with DB
    if 'loans' not in session:
      session['loans'] = []
    session['loans'].append(loanJson)
    return loanJson

@app.route("/api/loan/payoff", methods=["GET", "POST"])
def payoff_loan():
  if request.method == "POST":
    data = request.json
    # title = data['title']
    # loan = next((loan for loan in session['loans'] if loan['title'] == data['title']), None)
    start_balance = float(data['startBalance'])
    interest_rate = float(data['interestRate'])
    payment_amt = float(data['paymentAmt'])
    title = data['title']
    loan = StandardLoan(start_balance, interest_rate, payment_amt, title)
    loan.payoff()
    return loan.to_json()
  
@app.route("/api/loans/payoff", methods=["GET", "POST"])
def payoff_loans():
  if request.method == "POST":
    data = request.json
    return

@app.route("/api/loans")
def get_user_loans():
  # if 'loans' not in session:
  #   session['loans'] = []
  # Get user loans from database, solve them all
  return example_queue.avalanche().to_json()

@app.route("/api/queues")
def get_user_queues():
  # if 'loans' not in session:
  #   session['loans'] = []
  # Get user loans from database, solve them all
  return {
    "avalanche": example_queue.avalanche().to_json(),
    "blizzard": example_queue.blizzard().to_json(),
    "cascade": example_queue.cascade().to_json(),
    "iceSlide": example_queue.ice_slide().to_json(),
    "snowball": example_queue.snowball().to_json()
  }
