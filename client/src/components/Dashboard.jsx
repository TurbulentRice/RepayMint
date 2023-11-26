import { useState, useEffect } from 'preact/hooks'
import LoanView from './Loan/LoanView';
import LoanIndex from './Loan/LoanIndex';
import LoanForm from './Loan/LoanForm';
import { addUserLoan, getUserLoans } from '../ajax';
import logo from '../img/repaymint-logo-400.png'

export default function Dashboard() {
  const [loans, setLoans] = useState([]);
  const [selectedLoanIndex, setSelectedLoanIndex] = useState(0);
  const [values, setValues] = useState({});
  
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
    const newLoan = await addUserLoan(values);
    addLoan(newLoan);
  };

  useEffect(() => {
    (async () => {
      const fetchedLoans = await getUserLoans();
      setLoans(fetchedLoans);
    })()
  }, []);

  return (
    <>
      <div class="row">
        <div class="col-3 text-center">
          <div class="d-flex">
            <img src={logo} width={124} alt="RepayMint Logo" class="mx-auto"/>
          </div>
          <a href="/logout" class="mb-0">Logout</a>
        </div>
        <div class="col">
          <LoanForm submit={submit} setValue={setValue} />
        </div>
      </div>
      <div class="row">
        <div class="col">
          <LoanIndex loans={loans} selectedLoanIndex={selectedLoanIndex} selectLoan={selectLoan} removeLoan={removeLoan}/>
        </div>
        <div class="col">
          <LoanView loans={loans} />
        </div>
      </div>
    </>
  );
}
