import { useState } from 'preact/hooks'
import Input from './Components/Input';
import axios from 'axios';

export function App() {
  const [values, setValues] = useState({});
  const setValue = (e) => {
    const key = e.target.name || e.target.id;
    const value = e.target.value;
    setValues({...values, [key]: value});
  };

  const submit = async (e) => {
    e.preventDefault();
    const res = await axios.post('/api/loan', values);
    console.log(res);
  };

  return (
    <form method="POST" onSubmit={submit}>
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

      <button class="form-control">Submit</button>
    </form>
  );
}
