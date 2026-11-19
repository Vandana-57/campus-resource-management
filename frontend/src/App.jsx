
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

import { AuthProvider, useAuth } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';

import './App.css';

function HomeRedirect() {
  const { user, loading } = useAuth();

  if (loading) {
    return <div className="loading-screen">Loading application...</div>;
  }

  return <Navigate to={user ? '/dashboard' : '/login'} replace />;
}

// Temporary pages. We will implement these in the next stages.
function Login() {
  return (
    <main className="app-page">
      <h1>Campus Resource Management</h1>
      <p>Login page will be implemented next.</p>
    </main>
  );
}

function Register() {
  return (
    <main className="app-page">
      <h1>Create Account</h1>
      <p>Registration page will be implemented next.</p>
    </main>
  );
}

function Dashboard() {
  const { user, logout } = useAuth();

  return (
    <main className="app-page">
      <h1>Welcome, {user?.name}</h1>
      <p>Role: {user?.role}</p>
      <p>Dashboard will be implemented next.</p>
      <button onClick={logout}>Logout</button>
    </main>
  );
}

function Resources() {
  return <main className="app-page"><h1>Campus Resources</h1></main>;
}

function BookingHistory() {
  return <main className="app-page"><h1>My Bookings</h1></main>;
}

function AdminDashboard() {
  return <main className="app-page"><h1>Admin Dashboard</h1></main>;
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<HomeRedirect />} />

      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      <Route element={<ProtectedRoute />}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/resources" element={<Resources />} />
        <Route path="/bookings" element={<BookingHistory />} />
      </Route>

      <Route element={<ProtectedRoute adminOnly />}>
        <Route path="/admin" element={<AdminDashboard />} />
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
