import { useState, useEffect } from 'preact/hooks'
import LoanView from './Loan/LoanView';
import LoanIndex from './Loan/LoanIndex';
import LoanForm from './Loan/LoanForm';
import { addUserLoan, getUserLoans } from '../ajax';

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

  // Get loans from session
  useEffect(async () => {
    const fetchedLoans = await getUserLoans();
    setLoans(fetchedLoans);
  }, []);
  
  console.log('LOANS IN STATE:', loans);
  return (
    <div class="row">
      <div class="col-4">
        <LoanForm submit={submit} setValue={setValue} />
        <LoanIndex loans={loans} selectedLoanIndex={selectedLoanIndex} selectLoan={selectLoan} removeLoan={removeLoan}/>
      </div>
      <div class="col text-center">
        <LoanView loan={loans[selectedLoanIndex]} />
      </div>
    </div>
  );
}