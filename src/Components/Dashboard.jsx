import { useState, useEffect } from 'preact/hooks'
import axios from 'axios';
import Input from './Input';
import LoanView from './LoanView';
import LoanIndex from './LoanIndex';

export default function Dashboard() {
  const [loans, setLoans] = useState([]);
  const [selectedLoan, setSelectedLoan] = useState(0);
  const [values, setValues] = useState({});

  const findLoanIndex = (loan) => loans.findIndex(loan);
  
  const addLoan = (newLoan) => setLoans([...loans, newLoan]);
  const removeLoan = (oldLoanIndex) => setLoans(loans.filter((loan, index) => index !== oldLoanIndex));

  const selectLoan = (loanToSelect) => setSelectedLoan(loans.findIndex((loan) => loan === loanToSelect));

  const setValue = (e) => {
    const key = e.target.name || e.target.id;
    const value = e.target.value;
    setValues({...values, [key]: value});
  };
  
  const submit = async (e) => {
    e.preventDefault();
    const { data } = await axios.post('/api/loan/new', values);
    addLoan(data);
  };

  // Get loans from session
  useEffect(async () => {
    const { data } = await axios.get('/api/loans');
    setLoans([...data])
  }, []);
  
  console.log('LOANS IN STATE:', loans);
  return (
    <div class="row">
      <div class="col-4">
        <form method="POST" onSubmit={submit} class="mb-2">
          <Input
            label="Title"
            name="title"
            isRequired={true}
            onChange={setValue} />
          <Input
            label="Starting Balance"
            name="startBalance"
            isRequired={true}
            onChange={setValue}
            type="number"
            inputMode="decimal" />
          <Input
            label="Interest Rate"
            name="interestRate"
            isRequired={true}
            onChange={setValue}
            type="number"
            inputMode="decimal" />
          <Input
            label="Payment Amount"
            name="paymentAmt"
            isRequired={true}
            onChange={setValue}
            type="number"
            inputMode="decimal" />

          <button class="form-control btn btn-primary">Submit</button>
        </form>
        <LoanIndex loans={loans} selectLoan={selectLoan} removeLoan={removeLoan}/>
      </div>
      <div class="col text-center">
        <LoanView loan={loans[selectedLoan] ?? null} />
      </div>
    </div>
  );
}