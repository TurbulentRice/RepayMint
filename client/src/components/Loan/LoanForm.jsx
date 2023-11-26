export default function LoanForm({ submit, setValue }) {
  // Probably don't even have to set these in state, since we can extract values from form submit
  return (
    <form method="POST" onSubmit={submit} class="mb-2">
      <div class="form-row align-items-center">
        {/* Title */}
        <div class="col-md-2">
          <Input
            label="Title"
            name="title"
            isRequired={true}
            onChange={setValue} />
        </div>
        {/* Start balance */}
        <div class="col-md-2">
          <Input
            label="Start balance"
            name="startBalance"
            isRequired={true}
            onChange={setValue}
            type="number"
            inputMode="decimal" />
        </div>
        {/* Interest rate */}
        <div class="col-md-2">
          <Input
            label="Interest rate"
            name="interestRate"
            isRequired={true}
            onChange={setValue}
            type="number"
            inputMode="decimal" />
        </div>
        {/* Monthly payment */}
        <div class="col-md-2">
          <Input
            label="Payment"
            name="paymentAmt"
            isRequired={true}
            onChange={setValue}
            type="number"
            inputMode="decimal" />
        </div>
        {/* Term */}
        <div class="col-md-2">
          <Input
            label="Term (mo)"
            name="term"
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
    <div class="form-group">
      <label for={name} className="col-form-label-sm">{label}</label>
      <input
        id={name}
        name={name}
        // type={type}
        inputMode={inputMode}
        className="form-control form-control-sm"
        required={isRequired}
        onChange={onChange} />
    </div>
  );
}
