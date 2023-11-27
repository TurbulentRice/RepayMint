import { useState, useEffect } from 'preact/hooks'
import LoanView from './Loan/LoanView';
import LoanIndex from './Loan/LoanIndex';
import LoanForm from './Loan/LoanForm';
import { addUserLoan, getUserLoans } from '../ajax';
import logo from '../img/repaymint-logo-400.png'

export default function Dashboard() {
  const [loanData, setLoanData] = useState({
    loans: [],
    analysis: {}
  });
  const { loans, analysis } = loanData;
  const [selectedLoanIndex, setSelectedLoanIndex] = useState(0);
  const [values, setValues] = useState({});
  const [errors, setErrors] = useState({});
  const updateError = (errorName, errorMessage) => setErrors((currentErrors) => ({...currentErrors, [errorName]: errorMessage}));
  
  const addLoan = (newLoan) => setLoans([...loans, newLoan]);
  const removeLoan = (loanIndex) => {
    // Decrement selectedLoanIndex if that's the one being removed
    if (selectedLoanIndex && (loanIndex <= selectedLoanIndex)) {
      setSelectedLoanIndex(selectedLoanIndex - 1);
    }
    setLoans(loans.filter((loan, index) => index !== loanIndex));
  };
  const selectLoan = (loanIndex) => setSelectedLoanIndex(loanIndex);

  const setValue = (e) => {
    const key = e.target.name || e.target.id;
    const value = e.target.value;
    setValues({...values, [key]: value});
  };
  
  const submit = async (e) => {
    e.preventDefault();
    updateError('form', false);
    try {
      const newLoan = await addUserLoan(values);
      addLoan(newLoan);
    } catch(e) {
      console.error(e);
      updateError('form', 'Payment amount must be enough to cover monthly interest.');
    }
  };

  useEffect(() => {
    (async () => {
      try {
        const fetchedLoans = await getUserLoans();
        setLoanData(fetchedLoans);
      } catch(e) {
        console.error(e);
        updateError('loanIndex', 'Could not retreive user loans.');
      }
    })()
  }, []);

  return (
    <>
      <div class="row">
        <div class="col col-3 text-center mb-2">
          <img src={logo} width={100} alt="RepayMint Logo"/>
        </div>
        <div class="col border border-top-0 rounded text-center">
          <LoanForm submit={submit} setValue={setValue} />
          {errors.form && <div class="alert alert-danger mt-2">{errors.form}</div>}
        </div>
      </div>
      <div class="row">
        <div class="col-md-3 col-sm">
          <LoanIndex loans={loans} selectedLoanIndex={selectedLoanIndex} selectLoan={selectLoan} removeLoan={removeLoan}/>
          <a href="/logout" class="mt-4">Logout</a>
        </div>
        <div class="col">
          <LoanView loans={loans} analysis={analysis} />
        </div>
      </div>
    </>
  );
}
