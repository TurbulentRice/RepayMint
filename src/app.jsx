import Router from 'preact-router';
import Dashboard from './Components/Dashboard';
import Login from './Components/Login';

export function App() {
  return (
    <Router>
      <Dashboard path="/" />
      <Login path="/login" />
    </Router>
  );
}
