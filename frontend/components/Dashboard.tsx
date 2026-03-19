import React, { useState, useEffect } from 'react';
import { User } from '../types';
import { apiService } from '../services/api';
import { 
  CreditCard, 
  Sparkles, 
  History, 
  ArrowRight, 
  Zap, 
  TrendingUp,
  Activity
} from 'lucide-react';

interface DashboardProps {
  user: User;
  onNavigate: (route: string) => void;
}

interface DashboardStats {
  total_banners: number;
  total_spent: number;
}

const Dashboard: React.FC<DashboardProps> = ({ user, onNavigate }) => {
  const [stats, setStats] = useState<DashboardStats>({ total_banners: 0, total_spent: 0 });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await apiService.getDashboardStats();
        setStats(data);
      } catch (e) {
        console.error(e);
      }
    };
    fetchStats();
  }, []);

  return (
    <div className="max-w-6xl mx-auto space-y-8 animate-in float-up duration-500">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-3xl p-8 text-white shadow-lg shadow-indigo-200">
        <div className="flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="space-y-2">
            <h2 className="text-3xl font-bold">Chào mừng trở lại, {user.full_name}! 👋</h2>
            <p className="text-indigo-100">Hôm nay bạn muốn thiết kế gì?</p>
          </div>
          <button 
            onClick={() => onNavigate(__APP_ROUTES__.GENERATE)}
            className="flex items-center gap-2 bg-white text-indigo-600 px-6 py-3 rounded-xl font-bold hover:shadow-lg transition-all transform hover:scale-105"
          >
            <Sparkles className="h-5 w-5" />
            Tạo Banner Mới
          </button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex items-center gap-4">
          <div className="p-4 bg-blue-50 text-blue-600 rounded-xl">
            <Zap className="h-8 w-8" />
          </div>
          <div>
            <p className="text-sm text-slate-500 font-medium">Số dư hiện tại</p>
            <h3 className="text-2xl font-bold text-slate-800">{user.tokens} Tokens</h3>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex items-center gap-4">
          <div className="p-4 bg-purple-50 text-purple-600 rounded-xl">
            <TrendingUp className="h-8 w-8" />
          </div>
          <div>
            <p className="text-sm text-slate-500 font-medium">Banner đã tạo</p>
            <h3 className="text-2xl font-bold text-slate-800">{stats.total_banners}</h3>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex items-center gap-4">
          <div className="p-4 bg-green-50 text-green-600 rounded-xl">
            <Activity className="h-8 w-8" />
          </div>
          <div>
            <p className="text-sm text-slate-500 font-medium">Tổng chi tiêu</p>
            <h3 className="text-2xl font-bold text-slate-800">{stats.total_spent} Tokens</h3>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div>
        <h3 className="text-xl font-bold text-slate-800 mb-4">Thao tác nhanh</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <button 
            onClick={() => onNavigate(__APP_ROUTES__.BILLING)}
            className="group bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-all text-left"
          >
            <div className="mb-4 bg-indigo-50 w-12 h-12 rounded-xl flex items-center justify-center text-indigo-600 group-hover:scale-110 transition-transform">
              <CreditCard className="h-6 w-6" />
            </div>
            <h4 className="font-bold text-slate-800 mb-1">Mua Token</h4>
            <div className="flex items-center text-sm text-indigo-600 font-medium">
              Nạp thêm vào tài khoản <ArrowRight className="h-4 w-4 ml-1" />
            </div>
          </button>

          <button 
            onClick={() => onNavigate(__APP_ROUTES__.HISTORY)}
            className="group bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-all text-left"
          >
            <div className="mb-4 bg-orange-50 w-12 h-12 rounded-xl flex items-center justify-center text-orange-600 group-hover:scale-110 transition-transform">
              <History className="h-6 w-6" />
            </div>
            <h4 className="font-bold text-slate-800 mb-1">Xem Lịch Sử</h4>
            <div className="flex items-center text-sm text-orange-600 font-medium">
              Xem lại các banner đã tạo <ArrowRight className="h-4 w-4 ml-1" />
            </div>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
