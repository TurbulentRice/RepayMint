import { formatDecimal } from "./util/number";
import { getToken } from "./util/token";

export async function login(formData) {
  const res = await fetch('/api/login', {
      method: 'POST',
      body: formData,
  });
  if (res.ok) {
    const data = await res.json();
    localStorage.setItem('token', data.token);
  } else {
    throw new Error('Login failed!');
  }
};

export async function signup(formData) {
  const res = await fetch('/api/signup', {
    method: 'POST',
    body: formData,
  });
  if (res.ok) {
    const data = await res.json();
    localStorage.setItem('token', data.token);
  } else {
    throw new Error('Signup failed!');
  }
}

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
  title: loanData.title,
  analysis: unpackLoanAnalysis(loanData.analysis)
});

export async function addUserLoan(body) {
  const token = getToken();
  const res = await fetch('/api/loan/new', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(body)
  });
  if (!res.ok) {
    throw new Error('Something went wrong! ' + res.statusText)
  }
  const data = await res.json();
  return {
    loans: data.loans.map((loanData) => unpackLoanData(loanData)),
    analysis: unpackLoanAnalysis(data.analysis)
  }
}

export async function getUserLoans() {
  const token = getToken();
  const res = await fetch('/api/loans', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  if (!res.ok) {
    throw new Error('Something went wrong! ' + res.statusText)
  }
  const data = await res.json();
  return {
    loans: data.loans.map((loanData) => unpackLoanData(loanData)),
    analysis: unpackLoanAnalysis(data.analysis)
  }
}

export async function getUserQueues() {
  const token = getToken();
  const res = await fetch('/api/queues', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  const data = await res.json();
  for (const queue in data) {
    data[queue].loans = data[queue].loans.map((loanData) => unpackLoanData(loanData));
    data[queue].analysis = unpackLoanAnalysis(data[queue].analysis);
  }
  return data;
}
