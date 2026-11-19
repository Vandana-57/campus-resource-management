
import {
  createContext,
  useContext,
  useEffect,
  useState,
} from 'react';

import api from '../services/api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Restore the logged-in session when the application opens.
  useEffect(() => {
    const restoreSession = async () => {
      const token = localStorage.getItem('campus_access_token');

      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const response = await api.get('/auth/profile');
        setUser(response.data);
      } catch (error) {
        localStorage.removeItem('campus_access_token');
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    restoreSession();
  }, []);

  // Login using the Flask authentication API.
  const login = async (email, password) => {
    const response = await api.post('/auth/login', {
      email,
      password,
    });

    localStorage.setItem(
      'campus_access_token',
      response.data.access_token
    );

    setUser(response.data.user);

    return response.data;
  };

  // Register a student or faculty account.
  const register = async (name, email, password, role) => {
    const response = await api.post('/auth/register', {
      name,
      email,
      password,
      role,
    });

    return response.data;
  };

  // Logout the current user.
  const logout = () => {
    localStorage.removeItem('campus_access_token');
    setUser(null);
  };

  const value = {
    user,
    loading,
    isAuthenticated: Boolean(user),
    isAdmin: user?.role === 'admin',
    login,
    register,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error(
      'useAuth must be used inside an AuthProvider'
    );
  }

  return context;
}
