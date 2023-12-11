import Router from 'preact-router';
import Login from './components/Login';
import ProtectedRoute from './components/ProtectedRoute';

// Lazy loading for code splitting
const Dashboard = () => import('./components/Dashboard');

export function App() {
  return (
    <Router>
      <ProtectedRoute path="/" lazy={true} component={Dashboard} />
      <Login path="/login" />
    </Router>
  );
}
