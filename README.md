# RepayMint

RepayMint is a lightweight web application for modeling loan repayment timelines and comparing repayment strategies. It is based on Python data structures I wrote while figuring out the best way to repay my student loans, to help conceptualize the many "What if's" that arose:

- What if I increase/decrease my monthly payment?
- What if I target payments to a single loan at a time?
- What if I allocate payments to loans based on certain factors, like their interest rate or minimum payment?

This helped dispell some of the mystery, but to be useful, these tools also had to answer the big questions:

- What is the fastest way to pay off all my outstanding loans?
- What is the cheapest way (least interest paid)?

![RepayMint App](./examples/repaymint_ui.png)

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
python -m venv venv
# Activate venv
source venv/bin/activate
# Install dependencies
pip install -r requirements.txt
# Run the Flask server in debug mode
flask --app router run --debug
# OR
./run.sh
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

## Matplotlib / Tkinter GUI

[main.py](main.py) is leftover from before the move to Preact and everything was serverless.

```py
python main.py
```

# Loan Repayment Algorithms Overview

Given the following loans and monthly budget:

Budget:               $1,713.39/mo

Loan 1:
  - Start balance:    $16,228.66
  - Interest rate:    3.52%

Loan 2:
  - Start balance:    $14,346.09
  - Interest rate:    1.77%

Loan 3:
  - Start balance:    $9,336.35
  - Interest rate:    2.4%

Loan 4:
  - Start balance:    $5,117.88
  - Interest rate:    1.22%

## Ordered Algorithms
Ordered algorithms are focused on targeting a single loan each pay cycle, paying only minimums on all except the target loan, paying one off at a time.

### Avalanche
Orders loans by interest rate and balance. Payments target the loan with the highest interest rate and balance until all loans are paid off.

This algorithm consistently results in the lowest interest paid
over the course of large loans.

<img src="examples/avalanche/My_Loans(avalanche_branch)_1.png" width="450" alt="Avalanche Example 1">
<img src="examples/avalanche/My_Loans(avalanche_branch)_2.png" width="450" alt="Avalanche Example 2">
<img src="examples/avalanche/My_Loans(avalanche_branch)_3.png" width="450" alt="Avalanche Example 3">
<img src="examples/avalanche/My_Loans(avalanche_branch)_4.png" width="450" alt="Avalanche Example 4">

### Blizzard
Orders loans by monthly interest cost. Payments target the loan with the largest monthly interest cost until all loans are paid off. The targeted loan can change with every payment when multiple loans are equally "expensive." This accounts for the tooth-like pattern in loan payment histories.

This algorithm is similar to Avalanche, providing some benefits for small loans and/or large budgets.

<img src="examples/blizzard/My_Loans(blizzard_branch)_1.png" width="450" alt="Blizzard Example 1">
<img src="examples/blizzard/My_Loans(blizzard_branch)_2.png" width="450" alt="Blizzard Example 2">
<img src="examples/blizzard/My_Loans(blizzard_branch)_3.png" width="450" alt="Blizzard Example 3">
<img src="examples/blizzard/My_Loans(blizzard_branch)_4.png" width="450" alt="Blizzard Example 4">

### Snowball
Orders loans by balance. Payments target the loan with the lowest starting balance until all loans are paid off.

This algorithm is largely motivaitonal, quickly reducing the number of outstanding loans, but is not necessarily cost-effective.

<img src="examples/snowball/My_Loans(snowball_branch)_1.png" width="450" alt="Snowball Example 1">
<img src="examples/snowball/My_Loans(snowball_branch)_2.png" width="450" alt="Snowball Example 2">
<img src="examples/snowball/My_Loans(snowball_branch)_3.png" width="450" alt="Snowball Example 3">
<img src="examples/snowball/My_Loans(snowball_branch)_4.png" width="450" alt="Snowball Example 4">

## Unordered Algorithms
Unordered algorithms distribute payments strategically, according to need, and result in steady payment histories. These methods can reduce short-terms monthly costs of loans.

### Cascade
Distributes a percentage of a monthly budget to each loan each pay cycle, proportional to the loan's percentage contribution to the total (sum) interest rate of all loans.

<img src="examples/cascade/My_Loans(cascade_branch)_1.png" width="450" alt="Cascade Example 1">
<img src="examples/cascade/My_Loans(cascade_branch)_2.png" width="450" alt="Cascade Example 2">
<img src="examples/cascade/My_Loans(cascade_branch)_3.png" width="450" alt="Cascade Example 3">
<img src="examples/cascade/My_Loans(cascade_branch)_4.png" width="450" alt="Cascade Example 4">

### Ice Slide
Distributes a percentage of a monthly budget to each loan each pay cycle, proportional to the loan's percentage contribution to the total (sum) monthly cost (minimum payments) of all loans.

<img src="examples/ice_slide/My_Loans(ice_slide_branch)_1.png" width="450" alt="Ice Slide Example 1">
<img src="examples/ice_slide/My_Loans(ice_slide_branch)_2.png" width="450" alt="Ice Slide Example 2">
<img src="examples/ice_slide/My_Loans(ice_slide_branch)_3.png" width="450" alt="Ice Slide Example 3">
<img src="examples/ice_slide/My_Loans(ice_slide_branch)_4.png" width="450" alt="Ice Slide Example 4">
