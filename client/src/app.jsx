import Router from 'preact-router';
import Dashboard from './components/Dashboard';
import Login from './components/Login';

export function App() {
  return (
    <Router>
      <Dashboard path="/" />
      <Login path="/login" />
    </Router>
  );
}
