import Dashboard from './Components/Dashboard';
import Router from 'preact-router';
import Login from './Components/Login';

export function App() {
  return (
    <Router>
      <Dashboard path="/" />
      <Login path="/login" />
    </Router>
  );
}
