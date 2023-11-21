# RepayMint

Do you have multiple loans and want to know the fastest way to pay them off, while also paying the least interest possible?

RepayMint is a lightweight web application for modelling loan repayment timelines and comparing repayment strategies. It is based on Python data structures I wrote while paying off my student loans, to help visualize the many "What if's?":

- What if I increase/decrease my monthly payment?
- What if I target payments to a single loan at a time?
- What if I allocate payments to loans based on their relative contributions to a key factor, like interest rate or minimum payment?

This helped dispell some of the mystery behind the many loan repayment strategies, but it was not enough. To be useful to consumers, these tools also had to answer the big questions:

- What is the fastest way to pay off all my outstanding loans?
- What is the cheapest way (least interest paid)?

## Requirements
- Pyton 3.9+
- [Node Version Manager](https://github.com/nvm-sh/nvm)

## Stack
- [Flask](https://flask.palletsprojects.com/en/3.0.x/)
- [Vite](https://vitejs.dev/)
- [Preact](https://preactjs.com/)

## Getting Started

First, set up the back-end:
```sh
# Make sure the local Python executable is v3.9+
python -V
# Create virtual environment at project root
python -m venv
# Activate venv
source venv/bin/activate
# Install dependencies
pip install -r requirements.txt
# Run the Flask server in debug mode
flask --app router run --debug
```

Next, set up the front-end:
```sh
cd client/
# Install the Node version from .nvmrc if missing
nvm install
# Or, if correct Node version is already installed
nvm use
# Install dependencies
npm install
# Build the static Preact HTML/JS/CSS files in dist/
npm run build
# Run the dev server (proxies API requests to Flask server)
npm run dev
```

## Testing

Using unittest standard library.

```py
python -m unittest discover tests
```

# Loan Repayment Algorithms Overview

## Ordered Algorithms
Ordered algorithms are focused on targeting a single loan each pay cycle, paying only minimums on all except the target loan, paying one off at a time.

### Avalanche
Orders loans by interest rate and balance. Payments target the loan with the highest interest rate and balance until all loans are paid off.

This algorithm consistently results in the lowest interest paid
over the course of large loans.

### Blizzard
Orders loans by monthly interest cost. Payments target the loan with the largest monthly interest cost until all loans are paid off.

This algorithm is imilar to Avalanche, providing some benefits for small loans and/or large budgets.

### Snowball
Orders loans by balance. Payments target the loan with the lowest starting balance until all loans are paid off.

This algorithm is largely motivaitonal, quickly reducing the number of outstanding loans, but is not necessarily cost-effective.

## Unordered Algorithms
Unordered algorithms focus on targetting payments strategically. These methods can reduce short-terms monthly costs of loans.

### Cascade
Distributes a percentage of a monthly budget to each loan each pay cycle, proportional to the loan's percentage contribution to the total (sum) interest rate of all loans.

### Ice Slide
Distributes a percentage of a monthly budget to each loan each pay cycle, proportional to the loan's percentage contribution to the total (sum) monthly cost (minimum payments) of all loans.
