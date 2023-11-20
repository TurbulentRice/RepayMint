export default function Input({ label, name, isRequired, type="text" }) {
  return (
    <div class="col m-2">
      <label for={name} className="form-label"> {label}
        <input id={name} name={name} type={type} className="form-control" required={isRequired} />
      </label>
    </div>
  );
}
