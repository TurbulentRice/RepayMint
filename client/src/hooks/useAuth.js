import { useEffect, useState } from 'preact/hooks';
import { isTokenValid, clearToken, getToken } from '../util/token';

export default function useAuth() {
  const [isAuthenticated, setIsAuthenticated] = useState(getToken());

  useEffect(() => {
    if (!isTokenValid()) {
      clearToken();
      setIsAuthenticated(false);
    } else {
      setIsAuthenticated(true);
    }
  }, [getToken()]);

  return { isAuthenticated }
};
