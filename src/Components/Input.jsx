export default function Input({ label, name, isRequired, onChange, type="text", inputMode=false }) {
  return (
    <label for={name} className="form-label"> {label}
      <input
        id={name}
        name={name}
        // type={type}
        inputMode={inputMode}
        className="form-control"
        required={isRequired}
        onChange={onChange} />
    </label>
  );
}
