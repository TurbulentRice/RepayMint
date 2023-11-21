import axios from "axios";

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
  const { data } = await axios.post('/api/loan/new', body);
  return unpackLoanData(data);
}

export async function getUserLoans() {
  const { data } = await axios.get('/api/loans');
  return data.map((loanData) => unpackLoanData(loanData));
}
