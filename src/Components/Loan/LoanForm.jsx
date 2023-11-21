export default function LoanForm({ submit, setValue }) {
  // Probably don't even have to set these in state, since we can extract values from form submit
  return (
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

      <button class="form-control btn btn-primary mt-2">Submit</button>
    </form>
  );
}

function Input({ label, name, isRequired, onChange, type="text", inputMode=false }) {
  return (
    <>
      <label for={name} className="form-label">{label}</label>
      <input
        id={name}
        name={name}
        // type={type}
        inputMode={inputMode}
        className="form-control"
        required={isRequired}
        onChange={onChange} />
    </>
  );
}
