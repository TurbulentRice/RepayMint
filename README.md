# RepayMint

RepayMint is a lightweight web application for comparing loan repayment strategies. It is based around a Python package, [financetools](https://github.com/TurbulentRice/financetools), that I started writing while paying off my student loans, to help conceptualize the many "What if's" that arose:

- What if I increase/decrease my monthly payment?
- What if I target payments to a single loan at a time?
- What if I allocate payments to loans based on certain factors, like their interest rate or minimum payment?

This helped dispell some of the mystery, but to be useful, these tools also had to answer big questions, like:

- What is the fastest way to pay off all my outstanding loans?
- What is the cheapest way (least interest paid)?

You can install [financetools](https://github.com/TurbulentRice/financetools) via `pip install git+https://github.com/TurbulentRice/financetools.git`

![RepayMint App](./examples/default.png)

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
flask --app app run --debug
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
