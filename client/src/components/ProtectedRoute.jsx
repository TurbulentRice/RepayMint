import { useEffect } from "preact/hooks";
import { Route, route } from "preact-router";
import LazyRoute from "preact-lazy-route";
import useAuth from "../hooks/useAuth";

export default function ProtectedRoute({ path, lazy, component }) {
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    if (!isAuthenticated) route('/login', true);
  }, [isAuthenticated]);

  if (!isAuthenticated) return null;

  const RoutComponent = lazy ? LazyRoute : Route;

  return isAuthenticated ? <RoutComponent path={path} component={component} /> : null;
}
