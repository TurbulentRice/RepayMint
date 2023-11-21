export default function Login() {
  return (
    <form method="POST">
      <p><input type="text" name="username" class="form-control" /></p>
      <p><input type="submit" value="login" class="form-control" /></p>
    </form>
  );
}
