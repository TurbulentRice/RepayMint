import os
from flask import Flask, send_from_directory, request
from dotenv import load_dotenv
from loan import *

load_dotenv()  # take environment variables from .env.

app = Flask(__name__)

cached_loan = None

@app.route("/")
def main():
  return send_from_directory('./dist/', 'index.html')

@app.route("/assets/<filename>")
def assets(filename):
  return send_from_directory('./dist/assets/', filename)

@app.route("/api/loan", methods={"GET", "POST"})
def api():
  if request.method == "POST":
    data = request.json
    start_balance = float(data['startBalance'])
    interest_rate = float(data['interestRate'])
    payment_amt = float(data['paymentAmt'])
    title = data['title']
    loan = StandardLoan(start_balance, interest_rate, payment_amt, title)
  return loan.Payment_History