/**
 * Interface Loan
 * @param {Object} loanData JSON representing Loan object
 * @returns {Object}
 */
const unpackLoanData = (loanData) => ({
  interestRate: loanData.int_rate,
  paymentAmount: loanData.payment_amt,
  paymentHistory: loanData.payment_history,
  startBalance: loanData.start_balance,
  term: loanData.term,
  title: loanData.title
});

export async function addUserLoan(body) {
  const res = await fetch('/api/loan/new', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(body)
  });
  const data = await res.json();
  return unpackLoanData(data);
}

export async function getUserLoans() {
  const res = await fetch('/api/loans');
  const data = await res.json();
  return data.map((loanData) => unpackLoanData(loanData));
}
