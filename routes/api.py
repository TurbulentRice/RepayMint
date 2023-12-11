import os
import datetime
from flask import Blueprint, current_app, jsonify, request, session, g
from financetools import Loan, LoanQueue
import jwt
from models.user_model import UserModel
from models.loan_model import LoanModel

api = Blueprint('api', __name__)

db_host = os.environ.get("DB_HOST")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
dn_name = os.environ.get("DB_NAME")

user_model = UserModel(db_host, db_user, db_password, dn_name)
loan_model = LoanModel(db_host, db_user, db_password, dn_name)

def api_auth(request):
  if 'Authorization' in request.headers:
    token = request.headers['Authorization'].split('Bearer ')[1]
    try:
      # Verify and decode the JWT
      decoded_token = jwt.decode(token, current_app.secret_key, algorithms=['HS256'])
      g.user = decoded_token
      return True
    except jwt.ExpiredSignatureError:
      return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
      return jsonify({'error': 'Invalid token'}), 401

def get_user_queue_from_db(user_id):
  loans = loan_model.get_user_loans(user_id)

  if not loans:
    return None
  
  user_loans = [Loan(loan[0], loan[1], pa=loan[2], title=loan[3], term=loan[4]) for loan in loans]
  user_queue = LoanQueue(user_loans)
  return user_queue

@api.route("/signup", methods=["POST"])
def signup():
  username = request.form["username"]
  password = request.form["password"]

  if not username or not password:
    return jsonify({'error': 'Missing username or password'}), 401
  
  # Check if the username is already taken
  if user_model.get_user_by_username(username):
    return jsonify({'error': 'Username already exists'}), 401

  # Register new user
  user_model.register_user(username, password)

  # Log in the new user
  user_id, username, is_valid_login = user_model.verify_login(username, password)
  if is_valid_login:
    session['user'] = {'user_id': user_id, 'username': username}
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    token = jwt.encode({'user_id': user_id, 'username': username, 'exp': expiration_time}, current_app.secret_key, algorithm='HS256')
    return jsonify({'token': token})
  return jsonify({'error': 'Invalid login credentials'}), 401


@api.route("/login", methods=["GET", "POST"])
def login():
  username = request.form["username"]
  password = request.form["password"]

  user_id, username, is_valid_login = user_model.verify_login(username, password)

  if is_valid_login:
    session['user'] = {'user_id': user_id, 'username': username}
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    token = jwt.encode({'user_id': user_id, 'username': username, 'exp': expiration_time}, current_app.secret_key, algorithm='HS256')
    return jsonify({'token': token})
  return jsonify({'error': 'Invalid login credentials'}), 401

# TODO fix this
@api.route("/loan/new", methods=["POST"])
def new_loan():
  # API auth
  if not api_auth(request):
    return jsonify({'error': 'Could not authenticate request'}), 401
  
  user_id = g.user['user_id']
  data = request.json
  start_balance = float(data['startBalance'])
  interest_rate = float(data['interestRate'])
  payment_amt = float(data['paymentAmt'])
  term = int(data['term'])
  title = data['title']

  loan = Loan(start_balance, interest_rate, payment_amt, title, term)
  if not loan.can_payoff():
    return jsonify({'error': 'Payments cannot cover interest.'}), 400
  
  loan_model.create_loan(user_id, loan.start_balance, loan.int_rate, loan.payment_amt, loan.title, loan.term)

  user_queue = get_user_queue_from_db(user_id)

  if not user_queue:
    return jsonify({
      "loans": [],
      "analysis": {}
    })

  user_queue.payoff()

  return jsonify({
    "loans": user_queue.to_json(),
    "analysis": user_queue.get_analysis()
  })
      
@api.route("/loans")
def get_user_loans():
  if not api_auth(request):
    return jsonify({'error': 'Could not authenticate request'}), 401
  
  user_queue = get_user_queue_from_db(g.user['user_id'])

  if not user_queue:
    return jsonify({
      "loans": [],
      "analysis": {}
    })

  user_queue.payoff()

  return jsonify({
    "loans": user_queue.to_json(),
    "analysis": user_queue.get_analysis()
  })

@api.route("/queues")
def get_user_queues():
  if not api_auth(request):
    return jsonify({'error': 'Could not authenticate request'}), 401
  
  user_queue = get_user_queue_from_db(g.user['user_id'])

  if not user_queue:
    return jsonify({'error': 'No loans found'}), 400

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