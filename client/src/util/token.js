const getToken = () => localStorage.getItem('token');
const clearToken = () => localStorage.removeItem('token');
const isTokenValid = () => {
    const token = getToken();
    if (token) {
      try {
        // Decode the token to check its expiration
        const decodedToken = JSON.parse(atob(token.split('.')[1]));
        const expirationTime = decodedToken.exp * 1000; // Convert seconds to milliseconds

        // Check if the token has expired
        return expirationTime > Date.now();
      } catch (error) {
        console.error('Error decoding token:', error);
        return false;
      }
    }
    return false;
};

export { getToken, clearToken, isTokenValid };
