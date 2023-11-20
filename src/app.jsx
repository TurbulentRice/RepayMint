import { useState } from 'preact/hooks'
import Input from './Components/Input';

export function App() {
  const [values, setValues] = useState({});
  const setValue = (e) => {
    const key = e.target.name || e.target.id;
    const value = e.target.value;
    setValues({...values, [key]: value});
  };

  return (
    <form method="POST" action="/api/">
      <div class="row">
        <Input label="Title" name="title" />
        <Input label="Starting Balance" name="startBalance" />
      </div>
      <button class="form-control">Submit</button>
    </form>
  );
}
