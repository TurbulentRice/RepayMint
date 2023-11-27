import { formatDecimal } from "./util";

/**
 * Interface Loan Data
 * @param {Object} loanData JSON representing Loan object
 * @returns {Object}
 */
const unpackLoanData = (loanData) => ({
  interestRate: loanData.int_rate,
  paymentAmt: loanData.payment_amt,
  paymentHistory: loanData.payment_history,
  startBalance: formatDecimal(loanData.start_balance),
  term: loanData.term,
  title: loanData.title
});

/**
 * Interface Loan Analysis
 * @param {Object} loanAnalysis JSON representing Loan analytics
 * @returns {Object} 
 */
const unpackLoanAnalysis = (loanAnalysis) => ({
  duration: loanAnalysis.duration,
  numPayments: loanAnalysis.num_payments,
  principalPaid: formatDecimal(loanAnalysis.principal_paid),
  interestPaid: formatDecimal(loanAnalysis.interest_paid),
  totalPaid: formatDecimal(loanAnalysis.total_paid),
  avgPI: loanAnalysis.avg_pi,
  percentPrincipal: loanAnalysis.percent_principal
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
  return {
    loans: data.loans.map((loanData) => unpackLoanData(loanData)),
    analysis: unpackLoanAnalysis(data.analysis)
  }
}

export async function getUserQueues() {
  const res = await fetch('/api/queues');
  const data = await res.json();
  for (const queue in data) {
    data[queue].loans = data[queue].loans.map((loanData) => unpackLoanData(loanData));
    data[queue].analysis = unpackLoanAnalysis(data[queue].analysis);
  }
  return data;
}
