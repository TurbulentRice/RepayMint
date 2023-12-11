import { useState } from "preact/hooks";
import useToggle from "../hooks/useToggle";
import { login, signup } from "../ajax";
import { route } from "preact-router";

export default function Login() {
  const { toggles, toggle } = useToggle({ isSignup: false });
  const [error, setError] = useState();
  const action = toggles.isSignup ? signup : login;
  const handleLogin = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    try {
      await action(formData);
      route("/");
    } catch (e) {
      setError(e.message);
    }
  }
  return (
    <div class="col-6 m-auto">
      <ul class="nav nav-tabs my-4">
        <li class="nav-item">
          <button class={`nav-link${!toggles.isSignup ? ' active' : ''}`} onClick={() => toggle('isSignup')}>Login</button>
        </li>
        <li class="nav-item">
          <button class={`nav-link${toggles.isSignup ? ' active' : ''}`} onClick={() => toggle('isSignup')}>Sign up</button>
        </li>
      </ul>
      <form method="POST" onSubmit={handleLogin}>
        <div class="form-group">
          <label for="username">Username: </label>
          <input type="text" name="username" class="form-control" required />
        </div>
        <div class="form-group">
          <label for="password">Password: </label>
          <input type="text" name="password" class="form-control" required />
        </div>
        <p><button class="btn btn-primary form-control" type="submit">{toggles.isSignup ? "Sign up" : "Login"}</button></p>
      </form>
      {/* Error */}
      {error && <div class="alert alert-danger" role="alert">{error}</div>}
    </div>
  );
}
