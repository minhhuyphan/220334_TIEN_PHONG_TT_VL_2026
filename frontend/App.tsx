import React, { useState, useEffect, useCallback } from 'react';
import { BrowserRouter, Routes, Route, Navigate, useNavigate, useLocation, Outlet } from 'react-router-dom';
import { User } from './types';
import { apiService } from './services/api';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import Dashboard from './components/Dashboard';
import BannerGenerator from './components/BannerGenerator';
import Billing from './components/Billing';
import History from './components/History';
import Login from './components/Login';
import AdminPanel from './components/AdminPanel';
import HomePage from './components/HomePage';
import { Toaster, toast } from 'react-hot-toast';

// Wrapper for components needing onNavigate
const ComponentWrapper: React.FC<{ 
  component: React.ComponentType<any>, 
  user: User, 
  [key: string]: any 
}> = ({ component: Component, user, ...rest }) => {
  const navigate = useNavigate();
  const handleNavigate = (route: string) => {
    navigate(route);
  };

  return <Component user={user} currentUser={user} onNavigate={handleNavigate} {...rest} />;
};

const MainLayout: React.FC<{ user: User, onLogout: () => void }> = ({ user, onLogout }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  
  const handleNavigate = (route: string) => {
    navigate(route);
    setIsSidebarOpen(false); // Close sidebar after navigation on mobile
  };

  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden">
      <Sidebar 
        currentRoute={location.pathname} 
        onNavigate={handleNavigate} 
        onLogout={onLogout} 
        user={user}
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
      />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header user={user} onMenuClick={() => setIsSidebarOpen(true)} />
        <main className="flex-1 overflow-y-auto p-4 md:p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

const AppContent: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [activeTaskId, setActiveTaskId] = useState<string | null>(localStorage.getItem('current_banner_task_id'));
  const navigate = useNavigate();
  const location = useLocation();

  const fetchUser = useCallback(async () => {
    try {
      const userData = await apiService.getMe();
      setUser(userData);
      // Determine if we need to redirect after login (e.g. from / -> /dashboard)
      if (location.pathname === '/') {
        navigate(__APP_ROUTES__.DASHBOARD);
      }
    } catch (error) {
      console.error("Auth session expired", error);
      localStorage.removeItem(__TOKEN_KEY__);
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  }, [navigate, location.pathname]);

  useEffect(() => {
    const token = localStorage.getItem(__TOKEN_KEY__);
    if (token) {
      fetchUser();
    } else {
      setIsLoading(false);
    }
  }, []);

  // Global Task Polling
  useEffect(() => {
    let intervalId: any;
    
    // Listen for storage changes in other tabs
    const handleStorageChange = () => {
      const storedId = localStorage.getItem('current_banner_task_id');
      if (storedId !== activeTaskId) {
        setActiveTaskId(storedId);
      }
    };
    window.addEventListener('storage', handleStorageChange);

    if (activeTaskId) {
      intervalId = setInterval(async () => {
        try {
          const task = await apiService.getTaskStatus(activeTaskId);
          
          if (task.status === 'completed') {
            localStorage.removeItem('current_banner_task_id');
            setActiveTaskId(null);
            toast.success("Tạo banner thành công! Kiểm tra trong lịch sử.", { duration: 5000 });
            fetchUser(); // Refresh tokens
          } else if (task.status === 'failed') {
            localStorage.removeItem('current_banner_task_id');
            setActiveTaskId(null);
            toast.error(task.error || "Tạo banner thất bại");
          }
        } catch (err) {
          console.error("Global polling error", err);
        }
      }, 3000);
    }

    return () => {
      if (intervalId) clearInterval(intervalId);
      window.removeEventListener('storage', handleStorageChange);
    };
  }, [activeTaskId, fetchUser]);

  const handleLogin = (userData: User, token: string) => {
    localStorage.setItem(__TOKEN_KEY__, token);
    setUser(userData);
    navigate(__APP_ROUTES__.DASHBOARD);
  };

  const handleLogout = () => {
    localStorage.removeItem(__TOKEN_KEY__);
    setUser(null);
    navigate('/');
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  // Khi chưa đăng nhập: hiển thị trang chủ public
  if (!user) {
    return (
      <Routes>
        <Route path="/" element={<HomePage onLoginSuccess={handleLogin} />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    );
  }

  return (
    <Routes>
      <Route element={<MainLayout user={user} onLogout={handleLogout} />}>
        <Route path={__APP_ROUTES__.DASHBOARD} element={<ComponentWrapper component={Dashboard} user={user} />} />
        <Route path={__APP_ROUTES__.GENERATE} element={<ComponentWrapper component={BannerGenerator} user={user} refreshUser={fetchUser} />} />
        <Route path={__APP_ROUTES__.BILLING} element={<ComponentWrapper component={Billing} user={user} refreshUser={fetchUser} />} />
        <Route path={__APP_ROUTES__.HISTORY} element={<ComponentWrapper component={History} user={user} />} />
        <Route path="/" element={<Navigate to={__APP_ROUTES__.DASHBOARD} replace />} />
      </Route>
      
      {/* Admin Route - Standalone Layout */}
      <Route 
        path={__APP_ROUTES__.ADMIN} 
        element={<ComponentWrapper component={AdminPanel} user={user} />} 
      />
    </Routes>
  );
};

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Toaster position="top-right" reverseOrder={false} />
      <AppContent />
    </BrowserRouter>
  );
};

export default App;
