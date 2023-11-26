export default function LoanForm({ submit, setValue }) {
  // Probably don't even have to set these in state, since we can extract values from form submit
  return (
    <form method="POST" onSubmit={submit} class="mb-2">
      <div class="row">
        {/* Title */}
        <div class="col">
          <Input
            label="Title"
            name="title"
            isRequired={true}
            onChange={setValue} />
        </div>
        {/* Start balance */}
        <div class="col">
          <Input
            label="Starting Balance"
            name="startBalance"
            isRequired={true}
            onChange={setValue}
            type="number"
            inputMode="decimal" />
        </div>
      </div>
      <div class="row">
        {/* Interest rate */}
        <div class="col">
          <Input
            label="Interest Rate"
            name="interestRate"
            isRequired={true}
            onChange={setValue}
            type="number"
            inputMode="decimal" />
        </div>
        {/* Monthly payment */}
        <div class="col">
          <Input
            label="Payment Amount"
            name="paymentAmt"
            isRequired={true}
            onChange={setValue}
            type="number"
            inputMode="decimal" />
        </div>
        {/* Term */}
        <div class="col">
          <Input
            label="Term (months)"
            name="terms"
            isRequired={true}
            onChange={setValue}
            type="number" />
        </div>
      </div>

      <button class="form-control btn btn-primary mt-2">+ Add loan</button>
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
