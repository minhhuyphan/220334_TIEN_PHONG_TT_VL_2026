import React from 'react';
import {
  LayoutDashboard,
  Palette,
  CreditCard,
  History as HistoryIcon,
  LogOut,
  Sparkles,
  Shield,
  X,
  Home
} from 'lucide-react';
import { User } from '../types';

interface SidebarProps {
  currentRoute: string;
  onNavigate: (route: string) => void;
  onLogout: () => void;
  user: User;
  isOpen: boolean;
  onClose: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ currentRoute, onNavigate, onLogout, user, isOpen, onClose }) => {
  const navItems = [
    { id: '/', label: 'Trang Chủ', icon: Home },
    { id: __APP_ROUTES__.DASHBOARD, label: 'Tổng Quan', icon: LayoutDashboard },
    { id: __APP_ROUTES__.GENERATE, label: 'Tạo Banner AI', icon: Palette },
    { id: __APP_ROUTES__.BILLING, label: 'Gói Cước', icon: CreditCard },
    { id: __APP_ROUTES__.HISTORY, label: 'Lịch Sử', icon: HistoryIcon },
  ];

  // Add Admin menu only for admin users
  if (user.is_admin) {
    navItems.push({ id: __APP_ROUTES__.ADMIN, label: 'Quản Trị', icon: Shield });
  }

  return (
    <>
      {/* Mobile Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-40 md:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar Content */}
      <aside className={`fixed md:static inset-y-0 left-0 w-64 bg-white border-r border-slate-200 z-50 transform transition-transform duration-300 ease-in-out md:translate-x-0 flex flex-col ${isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}>
        <div className="p-6 flex items-center justify-between gap-3">
          <div
            className="flex items-center gap-3 cursor-pointer hover:opacity-80 transition-opacity"
            onClick={() => onNavigate('/')}
          >
            <img src="/logo.png" alt="Logo" className="h-10 w-10 object-contain" />
            <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600">
              Zephyr
            </h1>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-slate-400 hover:text-slate-600 md:hidden"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <nav className="flex-1 px-4 py-4 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentRoute === item.id;
            const isAdmin = item.id === __APP_ROUTES__.ADMIN;
            return (
              <button
                key={item.id}
                onClick={() => onNavigate(item.id)}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${isActive
                  ? isAdmin
                    ? 'bg-purple-50 text-purple-700 font-semibold'
                    : 'bg-indigo-50 text-indigo-700 font-semibold'
                  : 'text-slate-600 hover:bg-slate-50'
                  }`}
              >
                <Icon className={`h-5 w-5 ${isActive
                  ? isAdmin
                    ? 'text-purple-600'
                    : 'text-indigo-600'
                  : 'text-slate-400'
                  }`} />
                {item.label}
              </button>
            );
          })}
        </nav>

        <div className="p-4 border-t border-slate-100">
          <button
            onClick={onLogout}
            className="w-full flex items-center gap-3 px-4 py-3 text-red-500 hover:bg-red-50 rounded-xl transition-colors"
          >
            <LogOut className="h-5 w-5" />
            Đăng Xuất
          </button>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
