export default function LoanForm({ submit, values, setValue }) {
  return (
    <form method="POST" onSubmit={submit} class="mb-2">
      <div class="form-row align-items-center">
        {/* Title */}
        <div class="col-md-2">
          <Input
            label="Title"
            name="title"
            value={values.title}
            isRequired={true}
            onInput={setValue} />
        </div>
        {/* Start balance */}
        <div class="col-md-2">
          <Input
            label="Start balance"
            name="startBalance"
            value={values.startBalance}
            isRequired={true}
            onInput={setValue}
            type="number"
            inputMode="decimal"
            step=".01" />
        </div>
        {/* Interest rate */}
        <div class="col-md-2">
          <Input
            label="Interest rate"
            name="interestRate"
            value={values.interestRate}
            isRequired={true}
            onInput={setValue}
            type="number"
            inputMode="decimal"
            step=".01" />
        </div>
        {/* Monthly payment */}
        <div class="col-md-2">
          <Input
            label="Payment"
            name="paymentAmt"
            value={values.paymentAmt}
            isRequired={true}
            onInput={setValue}
            type="number"
            inputMode="decimal"
            step=".01" />
        </div>
        {/* Term */}
        <div class="col-md-2">
          <Input
            label="Term (mo)"
            name="term"
            value={values.term}
            isRequired={true}
            onInput={setValue}
            type="number"
            inputMode="numeric" />
        </div>

        <div class="col-md-10">
          <button class="form-control btn btn-primary mt-2">+ Add loan</button>
        </div>
        
      </div>

    </form>
  );
}

function Input({ label, name, value, isRequired, onInput, type, inputMode, step }) {
  return (
    <div class="form-group">
      <label for={name} className="col-form-label-sm">{label}</label>
      <input
        id={name}
        name={name}
        value={value || ''}
        type={type || 'text'}
        step={step}
        inputMode={inputMode || false}
        className="form-control form-control-sm"
        required={isRequired}
        onInput={onInput} />
    </div>
  );
}
