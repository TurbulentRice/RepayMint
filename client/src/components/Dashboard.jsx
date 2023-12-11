import { useState, useEffect } from 'preact/hooks'
import LoanView from './Loan/LoanView';
import LoanIndex from './Loan/LoanIndex';
import LoanForm from './Loan/LoanForm';
import { addUserLoan, getUserLoans } from '../ajax';
import { clearToken } from '../util/token';
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
  
  const setValue = (e) => {
    const key = e.target.name || e.target.id;
    const value = e.target.value;
    setValues({...values, [key]: value});
  };

  const addLoan = async (e) => {
    e.preventDefault();
    updateError('form', false);
    try {
      const updatedLoans = await addUserLoan(values);
      setLoanData(updatedLoans);
      setValues({});
    } catch(e) {
      updateError('form', e.message);
    }
  };
  const removeLoan = (loanIndex) => {
    // Decrement selectedLoanIndex if that's the one being removed
    if (selectedLoanIndex && (loanIndex <= selectedLoanIndex)) {
      setSelectedLoanIndex(selectedLoanIndex - 1);
    }
    setLoanData({
      loans: loans.filter((loan, index) => index !== loanIndex),
      analysis
    });
  };

  const logout = () => {
    clearToken();
    window.location.href = "/logout";
  }

  useEffect(() => {
    (async () => {
      try {
        const fetchedLoans = await getUserLoans();
        setLoanData(fetchedLoans);
      } catch(e) {
        updateError('loanIndex', e.message);
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

          {/* Add loan */}
          <LoanForm submit={addLoan} values={values} setValue={setValue} />

          {/* Form error */}
          {errors.form && <div class="alert alert-danger mt-2">{errors.form}</div>}
        </div>
      </div>
      <div class="row">
        <div class="col-md-3 col-sm">

          {/* Loan list */}
          <LoanIndex loans={loans} selectedLoanIndex={selectedLoanIndex} selectLoan={setSelectedLoanIndex} removeLoan={removeLoan}/>

          {/* Loan list error */}
          {errors.loanIndex && <div class="alert alert-warning mt-4" role="alert">{errors.loanIndex}</div>}

          {/* Logout */}
          <button class="btn btn-link mt-4" onClick={logout}>Logout</button>
        </div>
        <div class="col">

          {/* Loan view */}
          <LoanView loans={loans} selectedLoanIndex={selectedLoanIndex} analysis={analysis} />
          
        </div>
      </div>
    </>
  );
}
