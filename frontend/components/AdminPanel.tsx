import React, { useState, useEffect } from 'react';
import { 
  Users, 
  CreditCard, 
  Image, 
  Shield, 
  ShieldOff,
  Search,
  TrendingUp,
  DollarSign,
  Activity,
  Package,
  Plus,
  Edit,
  Trash2,
  ArrowLeft,
  Save,
  X,
  Settings,
  BarChart,
  History as HistoryIcon,
  Maximize2,
  Globe
} from 'lucide-react';
import { apiService } from '../services/api';
import { User } from '../types';
import toast from 'react-hot-toast';
import ConfirmModal from './ConfirmModal';
import AdminSeoSettings from './AdminSeoSettings';

interface AdminUser {
  id: number;
  email: string;
  full_name: string;
  tokens: number;
  is_admin: number;
  created_at: string;
  avatar_url?: string;
  google_id?: string;
}

interface AdminPayment {
  id: number;
  user_id: number;
  package_name: string;
  amount_vnd: number;
  tokens_received: number;
  status: string;
  created_at: string;
  completed_at: string | null;
  sepay_transaction_id?: string;
  payment_code?: string;
}

interface AdminBanner {
  id: number;
  user_id: number;
  request_description: string;
  aspect_ratio: string;
  resolution: string;
  image_url: string;
  token_cost: number;
  created_at: string;
  prompt_used?: string;
}

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, Legend } from 'recharts';

interface AdminStats {
  total_users: number;
  total_admins: number;
  total_revenue: number;
  total_banners: number;
  total_tokens_sold: number;
  api_cost_estimate?: number;
  chart_data?: any[];
  recent_payments?: any[];
  recent_banners?: any[];
}

interface Package {
  id: number;
  name: string;
  description: string;
  amount_vnd: number;
  tokens: number;
  is_active: number;
  created_at?: string;
}

interface AdminPanelProps {
  currentUser: User;
  onNavigate: (route: string) => void;
}

const AdminPanel: React.FC<AdminPanelProps> = ({ currentUser, onNavigate }) => {
  const [activeTab, setActiveTab] = useState<'users' | 'payments' | 'banners' | 'stats' | 'packages' | 'settings' | 'seo'>('stats');
  const [users, setUsers] = useState<AdminUser[]>([]);
  const [payments, setPayments] = useState<AdminPayment[]>([]);
  const [banners, setBanners] = useState<AdminBanner[]>([]);
  const [packages, setPackages] = useState<Package[]>([]);
  const [bannerCost, setBannerCost] = useState<number>(1);
  const [referenceImageCost, setReferenceImageCost] = useState<number>(0.5);
  const [aiModel, setAiModel] = useState<string>('gemini-2.5-flash');
  const [imageModel, setImageModel] = useState<string>('gemini-3.0-fast-image-preview');
  const [systemPrompt, setSystemPrompt] = useState<string>('');
  const [googleApiKey, setGoogleApiKey] = useState<string>('');
  const [geminiSafeMode, setGeminiSafeMode] = useState<string>('OFF');
  const [stats, setStats] = useState<AdminStats>({
    total_users: 0,
    total_admins: 0,
    total_revenue: 0,
    total_banners: 0,
    total_tokens_sold: 0
  });
  
  const [searchTerm, setSearchTerm] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Detail Modal States
  const [selectedUserDetail, setSelectedUserDetail] = useState<AdminUser | null>(null);
  const [selectedPaymentDetail, setSelectedPaymentDetail] = useState<AdminPayment | null>(null);
  const [selectedBannerDetail, setSelectedBannerDetail] = useState<AdminBanner | null>(null);

  // Package editing state
  const [isEditingPackage, setIsEditingPackage] = useState(false);
  const [editingPackageId, setEditingPackageId] = useState<number | null>(null);
  const [packageForm, setPackageForm] = useState({
    name: '',
    description: '',
    amount_vnd: 0,
    tokens: 0,
    is_active: true
  });

  // User management state
  const [selectedUserForTokens, setSelectedUserForTokens] = useState<AdminUser | null>(null);
  const [tokenDepositAmount, setTokenDepositAmount] = useState<number>(0);
  const [selectedUserForHistory, setSelectedUserForHistory] = useState<AdminUser | null>(null);
  const [userBanners, setUserBanners] = useState<AdminBanner[]>([]);
  const [isDeletingUser, setIsDeletingUser] = useState<number | null>(null);

  // Confirmation modal state
  const [confirmConfig, setConfirmConfig] = useState<{
    isOpen: boolean;
    title: string;
    message: string;
    onConfirm: () => void;
  }>({
    isOpen: false,
    title: '',
    message: '',
    onConfirm: () => {},
  });

  const menuItems = [
    { id: 'stats', label: 'TỔNG QUAN', icon: BarChart },
    { id: 'users', label: 'NGƯỜI DÙNG', icon: Users },
    { id: 'banners', label: 'LỊCH SỬ', icon: Image },
    { id: 'payments', label: 'HOÁ ĐƠN', icon: CreditCard },
    { id: 'packages', label: 'GÓI NẠP', icon: Package },
    { id: 'seo', label: 'SEO', icon: Globe },
    { id: 'settings', label: 'CẤU HÌNH HỆ THỐNG', icon: Settings },
  ];

  const handleDepositTokens = async () => {
    if (!selectedUserForTokens) return;
    try {
      await apiService.addTokensToUser(selectedUserForTokens.id, tokenDepositAmount);
      toast.success(`Đã nạp ${tokenDepositAmount} tokens cho ${selectedUserForTokens.email}`);
      setSelectedUserForTokens(null);
      fetchUsers();
    } catch (error) {
      toast.error("Nạp tiền thất bại");
    }
  };

  const handleDeleteUser = (userId: number) => {
    setConfirmConfig({
      isOpen: true,
      title: "Xác nhận xoá người dùng",
      message: "Bạn có chắc chắn muốn xoá người dùng này? Toàn bộ dữ liệu liên quan sẽ bị xoá vĩnh viễn.",
      onConfirm: async () => {
        try {
          await apiService.deleteUser(userId);
          toast.success("Đã xoá người dùng");
          fetchUsers();
        } catch (error) {
          toast.error("Xoá người dùng thất bại");
        }
      }
    });
  };

  const viewUserHistory = async (user: AdminUser) => {
    setSelectedUserForHistory(user);
    setIsLoading(true);
    try {
      const history = await apiService.getUserBanners(user.id);
      setUserBanners(history);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (activeTab === 'users') {
      fetchUsers();
    } else if (activeTab === 'payments') {
      fetchPayments();
    } else if (activeTab === 'banners') {
      fetchBanners();
    } else if (activeTab === 'stats') {
      fetchStats();
    } else if (activeTab === 'packages') {
      fetchPackages();
    } else if (activeTab === 'settings') {
      fetchSettings();
    }
  }, [activeTab]);

  const fetchSettings = async () => {
    try {
      const data = await apiService.getConfig();
      setBannerCost(data.banner_cost);
      setReferenceImageCost(data.reference_image_cost);
      setAiModel(data.ai_model || 'gemini-2.5-flash');
      setImageModel(data.image_model || 'gemini-3.0-fast-image-preview');
      setSystemPrompt(data.system_prompt || '');
      setGoogleApiKey(data.google_api_key || '');
      setGeminiSafeMode(data.gemini_safe_mode || 'OFF');
    } catch (error) {
       console.error("Error fetching settings", error);
    }
  }

  const handleUpdateCost = async () => {
    try {
      await apiService.updateBannerCost(bannerCost);
      toast.success("Cập nhật chi phí tạo ảnh thành công");
    } catch (error) {
      toast.error("Cập nhật thất bại");
    }
  }

  const handleUpdateRefCost = async () => {
    try {
      await apiService.updateReferenceImageCost(referenceImageCost);
      toast.success("Cập nhật chi phí ảnh tham chiếu thành công");
    } catch (error) {
      toast.error("Cập nhật thất bại");
    }
  }

  const handleUpdateImageModel = async () => {
    try {
      await apiService.updateImageModel(imageModel);
      toast.success("Cập nhật Model sinh ảnh thành công");
    } catch (error) {
      toast.error("Cập nhật thất bại");
    }
  }

  const handleUpdateSystemPrompt = async () => {
    try {
      await apiService.updateSystemPrompt(systemPrompt);
      toast.success("Cập nhật System Prompt thành công");
    } catch (error) {
      toast.error("Cập nhật thất bại");
    }
  }

  const handleUpdateGoogleApiKey = async () => {
    try {
      await apiService.updateGoogleApiKey(googleApiKey);
      toast.success("Cập nhật API Key thành công");
    } catch (error) {
      toast.error("Cập nhật thất bại");
    }
  }

  const handleUpdateAiModel = async () => {
    try {
      await apiService.updateAiModel(aiModel);
      toast.success("Cập nhật AI Model thành công");
    } catch (error) {
      toast.error("Cập nhật AI Model thất bại");
    }
  };

  const handleUpdateGeminiSafeMode = async () => {
    try {
      await apiService.updateGeminiSafeMode(geminiSafeMode);
      toast.success("Cập nhật Gemini Safe Mode thành công");
    } catch (error) {
      toast.error("Cập nhật Gemini Safe Mode thất bại");
    }
  };

  // ... existing code ...

  const fetchUsers = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`${__API_URL__}/admin/users`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem(__TOKEN_KEY__)}`
        }
      });
      const data = await response.json();
      setUsers(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error fetching users:', error);
      setUsers([]);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchPayments = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`${__API_URL__}/admin/payments`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem(__TOKEN_KEY__)}`
        }
      });
      const data = await response.json();
      setPayments(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error fetching payments:', error);
      setPayments([]);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchBanners = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`${__API_URL__}/admin/banners`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem(__TOKEN_KEY__)}`
        }
      });
      const data = await response.json();
      setBanners(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error fetching banners:', error);
      setBanners([]);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchStats = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`${__API_URL__}/admin/stats`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem(__TOKEN_KEY__)}`
        }
      });
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchPackages = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`${__API_URL__}/admin/packages`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem(__TOKEN_KEY__)}`
        }
      });
      const data = await response.json();
      setPackages(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error fetching packages:', error);
      setPackages([]);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleAdmin = async (userId: number, currentStatus: number) => {
    try {
      const response = await fetch(`${__API_URL__}/admin/users/${userId}/toggle-admin`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem(__TOKEN_KEY__)}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        fetchUsers();
      }
    } catch (error) {
      console.error('Error toggling admin:', error);
    }
  };

  const handleSavePackage = async () => {
    try {
      const url = editingPackageId 
        ? `${__API_URL__}/admin/packages/${editingPackageId}`
        : `${__API_URL__}/admin/packages`;
      
      const method = editingPackageId ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method,
        headers: {
          'Authorization': `Bearer ${localStorage.getItem(__TOKEN_KEY__)}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(packageForm)
      });

      if (response.ok) {
        setIsEditingPackage(false);
        setEditingPackageId(null);
        setPackageForm({
          name: '',
          description: '',
          amount_vnd: 0,
          tokens: 0,
          is_active: true
        });
        fetchPackages();
      } else {
        const error = await response.json();
        toast.error(`Lỗi: ${error.detail}`);
      }
    } catch (error) {
      console.error('Error saving package:', error);
    }
  };

  const handleDeletePackage = (id: number) => {
    setConfirmConfig({
      isOpen: true,
      title: "Xác nhận xoá gói cước",
      message: "Bạn có chắc chắn muốn xóa gói này không?",
      onConfirm: async () => {
        try {
          const response = await fetch(`${__API_URL__}/admin/packages/${id}`, {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${localStorage.getItem(__TOKEN_KEY__)}`
            }
          });

          if (response.ok) {
            toast.success("Đã xoá gói cước");
            fetchPackages();
          } else {
            const error = await response.json();
            toast.error(`Lỗi: ${error.detail}`);
          }
        } catch (error) {
          console.error('Error deleting package:', error);
          toast.error("Lỗi hệ thống khi xoá gói cước");
        }
      }
    });
  };

  const startEditPackage = (pkg?: Package) => {
    if (pkg) {
      setEditingPackageId(pkg.id);
      setPackageForm({
        name: pkg.name,
        description: pkg.description,
        amount_vnd: pkg.amount_vnd,
        tokens: pkg.tokens,
        is_active: pkg.is_active === 1
      });
    } else {
      setEditingPackageId(null);
      setPackageForm({
        name: '',
        description: '',
        amount_vnd: 0,
        tokens: 0,
        is_active: true
      });
    }
    setIsEditingPackage(true);
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(amount);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('vi-VN');
  };

  const filteredUsers = users.filter(user => 
    (user.email || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
    (user.full_name || '').toLowerCase().includes(searchTerm.toLowerCase())
  );

  const filteredPayments = payments.filter(payment =>
    (payment.package_name || 'Gói đã xóa').toLowerCase().includes(searchTerm.toLowerCase())
  );

  const filteredBanners = banners.filter(banner =>
    (banner.request_description || '').toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (!currentUser.is_admin) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <Shield className="h-16 w-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-slate-800 mb-2">Truy cập bị từ chối</h2>
          <p className="text-slate-600">Bạn không có quyền truy cập trang này.</p>
          <button 
            onClick={() => onNavigate(__APP_ROUTES__.DASHBOARD)}
            className="mt-4 px-4 py-2 bg-slate-200 text-slate-700 rounded-lg hover:bg-slate-300 transition-colors"
          >
            Về Trang Chủ
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      {/* Admin Lite Header & Tabs */}
      <div className="bg-white border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-10">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-3 bg-indigo-50 text-indigo-600 rounded-xl">
              <Shield className="h-8 w-8" />
            </div>
            <div>
              <h1 className="text-2xl md:text-3xl font-bold text-slate-800 tracking-tight">BẢNG QUẢN TRỊ</h1>
              <p className="text-sm md:text-base text-slate-500 font-medium">Quản lý hệ thống AI</p>
            </div>
            <button
              onClick={() => onNavigate(__APP_ROUTES__.DASHBOARD)}
              className="ml-auto flex items-center gap-2 px-4 py-2 text-sm font-medium text-slate-600 hover:text-indigo-600 bg-slate-50 hover:bg-indigo-50 rounded-lg transition-colors border border-slate-200"
            >
              <ArrowLeft className="h-4 w-4" />
              <span>Thoát</span>
            </button>
          </div>
          
          <div className="flex overflow-x-auto no-scrollbar border-b border-slate-200">
            {menuItems.map((item) => {
              const Icon = item.icon;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id as any)}
                  className={`flex items-center gap-2 px-4 py-3 font-bold transition-all whitespace-nowrap text-sm uppercase ${
                    activeTab === item.id
                      ? 'text-indigo-600 border-b-2 border-indigo-600 bg-indigo-50/30'
                      : 'text-slate-500 hover:text-slate-700 hover:bg-slate-50'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  {item.label}
                </button>
              );
            })}
          </div>
        </div>
      </div>

      <div className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-6">
          <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
            {/* Search Bar */}
            {activeTab !== 'stats' && activeTab !== 'packages' && activeTab !== 'settings' && activeTab !== 'seo' && (
              <div className="p-4 border-b border-slate-200 bg-white">
                <div className="relative max-w-md">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-slate-400" />
                  <input
                    type="text"
                    placeholder={`Tìm kiếm trong ${activeTab === 'users' ? 'người dùng' : activeTab === 'payments' ? 'hóa đơn' : 'lịch sử'}...`}
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 border border-slate-200 bg-slate-50 rounded-lg focus:bg-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-colors"
                  />
                </div>
              </div>
            )}

            {/* Content */}
            <div className="p-6">
              {isLoading ? (
                <div className="flex justify-center py-12">
                  <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-600"></div>
                </div>
              ) : (
                <>
                  {/* Statistics Tab */}
                  {activeTab === 'stats' && (
                    <div className="space-y-6">
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        <div className="bg-gradient-to-br from-indigo-500 to-indigo-600 rounded-xl p-6 text-white shadow-md">
                          <div className="flex items-center justify-between mb-4">
                            <Users className="h-8 w-8 opacity-80" />
                            <Activity className="h-5 w-5 opacity-60" />
                          </div>
                          <div className="text-3xl font-bold mb-1">{stats.total_users}</div>
                        <div className="text-indigo-100">Tổng Người Dùng</div>
                      </div>

                      <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl p-6 text-white shadow-md">
                        <div className="flex items-center justify-between mb-4">
                          <Shield className="h-8 w-8 opacity-80" />
                          <Activity className="h-5 w-5 opacity-60" />
                        </div>
                        <div className="text-3xl font-bold mb-1">{stats.total_admins}</div>
                        <div className="text-purple-100">Tổng Quản Trị Viên</div>
                      </div>

                      <div className="bg-gradient-to-br from-emerald-500 to-emerald-600 rounded-xl p-6 text-white shadow-md">
                        <div className="flex items-center justify-between mb-4">
                          <DollarSign className="h-8 w-8 opacity-80" />
                          <TrendingUp className="h-5 w-5 opacity-60" />
                        </div>
                        <div className="text-3xl font-bold mb-1">{formatCurrency(stats.total_revenue)}</div>
                        <div className="text-emerald-100">Tổng Doanh Thu</div>
                      </div>

                      <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-6 text-white shadow-md">
                        <div className="flex items-center justify-between mb-4">
                          <Image className="h-8 w-8 opacity-80" />
                          <Activity className="h-5 w-5 opacity-60" />
                        </div>
                        <div className="text-3xl font-bold mb-1">{stats.total_banners}</div>
                        <div className="text-blue-100">Banner Đã Tạo</div>
                      </div>

                      <div className="bg-gradient-to-br from-orange-500 to-orange-600 rounded-xl p-6 text-white shadow-md">
                        <div className="flex items-center justify-between mb-4">
                          <CreditCard className="h-8 w-8 opacity-80" />
                          <TrendingUp className="h-5 w-5 opacity-60" />
                        </div>
                        <div className="text-3xl font-bold mb-1">{stats.total_tokens_sold}</div>
                        <div className="text-orange-100">Token Đã Bán</div>
                      </div>

                      <div className="bg-gradient-to-br from-rose-500 to-rose-600 rounded-xl p-6 text-white shadow-md">
                        <div className="flex items-center justify-between mb-4">
                          <Activity className="h-8 w-8 opacity-80" />
                          <TrendingUp className="h-5 w-5 opacity-60" />
                        </div>
                        <div className="text-3xl font-bold mb-1">{formatCurrency(stats.api_cost_estimate || 0)}</div>
                        <div className="text-rose-100">Chi Phí API (Ước tính)</div>
                      </div>
                    </div>

                    {/* Charts & Recent Activities */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
                      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex flex-col">
                        <h3 className="text-lg font-bold text-slate-800 mb-4">Lưu Lượng & Doanh Thu (7 Ngày)</h3>
                        <div className="flex-1 min-h-[300px] w-full">
                          <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={stats.chart_data || []} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                              <CartesianGrid stroke="#f1f5f9" strokeDasharray="5 5" />
                              <XAxis dataKey="date" stroke="#94a3b8" fontSize={12} tickMargin={10} />
                              <YAxis yAxisId="left" stroke="#6366f1" fontSize={12} />
                              <YAxis yAxisId="right" orientation="right" stroke="#10b981" fontSize={12} />
                              <RechartsTooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
                              <Legend wrapperStyle={{ paddingTop: '20px' }} />
                              <Line yAxisId="left" type="monotone" dataKey="banners" name="Số Banner" stroke="#6366f1" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} />
                              <Line yAxisId="right" type="monotone" dataKey="revenue" name="Doanh Thu (VNĐ)" stroke="#10b981" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} />
                            </LineChart>
                          </ResponsiveContainer>
                        </div>
                      </div>

                      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">
                        <h3 className="text-lg font-bold text-slate-800 mb-4">Hoạt Động Mới Nhất</h3>
                        <div className="flex-1 overflow-auto pr-2 no-scrollbar">
                          {stats.recent_payments?.length || stats.recent_banners?.length ? (
                            <div className="space-y-3">
                              {stats.recent_payments?.map((payment: any, idx: number) => (
                                <div key={`p-${idx}`} className="flex items-center justify-between p-3 rounded-lg border border-slate-100 bg-emerald-50/50">
                                  <div className="flex items-center gap-3">
                                    <div className="h-10 w-10 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center font-bold">
                                      <DollarSign className="h-5 w-5" />
                                    </div>
                                    <div className="max-w-[150px] sm:max-w-[200px]">
                                      <p className="text-sm font-bold text-slate-800 truncate">{payment.user_email || 'Khách'}</p>
                                      <p className="text-xs text-slate-500">Nạp hạng: {payment.package_name || 'Gói nạp'}</p>
                                    </div>
                                  </div>
                                  <div className="text-right">
                                    <p className="text-sm font-bold text-emerald-600">+{formatCurrency(payment.amount_vnd)}</p>
                                    <p className="text-[10px] text-slate-400">{formatDate(payment.created_at)}</p>
                                  </div>
                                </div>
                              ))}
                              
                              {stats.recent_banners?.map((banner: any, idx: number) => (
                                <div key={`b-${idx}`} className="flex items-center justify-between p-3 rounded-lg border border-slate-100 bg-indigo-50/50">
                                  <div className="flex items-center gap-3">
                                    <div className="h-10 w-10 bg-indigo-100 text-indigo-600 rounded-full flex items-center justify-center font-bold">
                                      <Image className="h-5 w-5" />
                                    </div>
                                    <div className="max-w-[150px] sm:max-w-[200px]">
                                      <p className="text-sm font-bold text-slate-800 truncate">{banner.request_description || 'Tạo hình ảnh'}</p>
                                      <p className="text-xs text-slate-500 truncate">{banner.user_email}</p>
                                    </div>
                                  </div>
                                  <div className="text-right">
                                    <p className="text-[10px] text-slate-400">{formatDate(banner.created_at)}</p>
                                  </div>
                                </div>
                              ))}
                            </div>
                          ) : (
                            <p className="text-sm text-slate-500 text-center py-8">Chưa có giao dịch nào</p>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                  )}

{/* Users Tab */}
                  {activeTab === 'users' && (
                    <div className="space-y-4">
                      {/* Desktop Table */}
                      <div className="hidden md:block overflow-x-auto">
                        <table className="w-full">
                          <thead>
                            <tr className="border-b border-slate-200 text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                              <th className="text-left py-3 px-4">ID</th>
                              <th className="text-left py-3 px-4">Thông tin</th>
                              <th className="text-left py-3 px-4">Token</th>
                              <th className="text-left py-3 px-4">Vai trò</th>
                              <th className="text-left py-3 px-4">Ngày tham gia</th>
                              <th className="text-right py-3 px-4">Hành động</th>
                            </tr>
                          </thead>
                          <tbody>
                            {filteredUsers.map((user) => (
                              <tr key={user.id} className="border-b border-slate-100 hover:bg-slate-50 transition-colors">
                                <td className="py-4 px-4 text-slate-400 text-xs font-mono cursor-pointer hover:text-indigo-600" onClick={() => setSelectedUserDetail(user)}>#{user.id}</td>
                                <td className="py-4 px-4 cursor-pointer" onClick={() => setSelectedUserDetail(user)}>
                                  <div>
                                    <p className="font-bold text-slate-800 text-sm">{user.full_name}</p>
                                    <p className="text-xs text-slate-500">{user.email}</p>
                                  </div>
                                </td>
                                <td className="py-4 px-4">
                                  <span className="px-2.5 py-1 bg-indigo-50 text-indigo-700 rounded-full text-xs font-bold border border-indigo-100">
                                    {user.tokens} tokens
                                  </span>
                                </td>
                                <td className="py-4 px-4">
                                  {user.is_admin === 1 ? (
                                    <span className="px-2.5 py-1 bg-purple-50 text-purple-700 rounded-full text-xs font-bold border border-purple-100 flex items-center gap-1 w-fit">
                                      <Shield className="h-3 w-3" /> Admin
                                    </span>
                                  ) : (
                                    <span className="px-2.5 py-1 bg-slate-50 text-slate-600 rounded-full text-xs font-bold border border-slate-100">User</span>
                                  )}
                                </td>
                                <td className="py-4 px-4 text-slate-500 text-xs">{formatDate(user.created_at)}</td>
                                <td className="py-4 px-4 text-right">
                                  <div className="flex items-center justify-end gap-1.5">
                                    <button onClick={() => toggleAdmin(user.id, user.is_admin)} className={`p-2 rounded-lg transition-colors ${user.is_admin === 1 ? 'bg-red-50 text-red-600 hover:bg-red-100' : 'bg-green-50 text-green-600 hover:bg-green-100'}`}>
                                      {user.is_admin === 1 ? <ShieldOff className="h-4 w-4" /> : <Shield className="h-4 w-4" />}
                                    </button>
                                    <button onClick={() => setSelectedUserForTokens(user)} className="p-2 bg-indigo-50 text-indigo-600 rounded-lg hover:bg-indigo-100 transition-colors"><Plus className="h-4 w-4" /></button>
                                    <button onClick={() => viewUserHistory(user)} className="p-2 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 transition-colors"><HistoryIcon className="h-4 w-4" /></button>
                                    <button onClick={() => handleDeleteUser(user.id)} className="p-2 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition-colors"><Trash2 className="h-4 w-4" /></button>
                                  </div>
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>

                      {/* Mobile Card List */}
                      <div className="md:hidden space-y-3">
                        {filteredUsers.map((user) => (
                          <div key={user.id} className="bg-white p-4 rounded-xl border border-slate-200 space-y-3">
                            <div className="flex justify-between items-start">
                              <div>
                                <p className="font-bold text-slate-800">{user.full_name}</p>
                                <p className="text-xs text-slate-500">{user.email}</p>
                              </div>
                              <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${user.is_admin === 1 ? 'bg-purple-50 text-purple-700 border border-purple-100' : 'bg-slate-50 text-slate-600 border border-slate-100'}`}>
                                {user.is_admin === 1 ? 'Admin' : 'User'}
                              </span>
                            </div>
                            <div className="flex justify-between items-center py-2 border-y border-slate-50">
                              <span className="text-xs font-bold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded-full">{user.tokens} Tokens</span>
                              <span className="text-[10px] text-slate-400 font-mono">#{user.id}</span>
                            </div>
                            <div className="flex justify-between items-center pt-2">
                              <span className="text-[10px] text-slate-400">{formatDate(user.created_at)}</span>
                              <div className="flex gap-2">
                                <button onClick={() => setSelectedUserForTokens(user)} className="p-2 bg-indigo-50 text-indigo-600 rounded-lg"><Plus className="h-4 w-4" /></button>
                                <button onClick={() => viewUserHistory(user)} className="p-2 bg-blue-50 text-blue-600 rounded-lg"><HistoryIcon className="h-4 w-4" /></button>
                                <button onClick={() => handleDeleteUser(user.id)} className="p-2 bg-red-50 text-red-600 rounded-lg"><Trash2 className="h-4 w-4" /></button>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>

                      {filteredUsers.length === 0 && (
                        <div className="text-center py-12 text-slate-500">Không tìm thấy người dùng</div>
                      )}
                    </div>
                  )}

{/* Payments Tab */}
                  {activeTab === 'payments' && (
                    <div className="space-y-4">
                      <div className="hidden md:block overflow-x-auto">
                        <table className="w-full">
                          <thead>
                            <tr className="border-b border-slate-200 text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                              <th className="text-left py-3 px-4">Mã GD</th>
                              <th className="text-left py-3 px-4">User ID</th>
                              <th className="text-left py-3 px-4">Gói</th>
                              <th className="text-left py-3 px-4">Số tiền</th>
                              <th className="text-left py-3 px-4">Token</th>
                              <th className="text-left py-3 px-4">Trạng thái</th>
                              <th className="text-left py-3 px-4">Ngày tạo</th>
                            </tr>
                          </thead>
                          <tbody>
                            {filteredPayments.map((payment) => (
                              <tr key={payment.id} className="border-b border-slate-100 hover:bg-slate-50 transition-colors">
                                <td className="py-4 px-4 text-slate-400 text-xs font-mono cursor-pointer hover:text-indigo-600" onClick={() => setSelectedPaymentDetail(payment)}>#{payment.id}</td>
                                <td className="py-4 px-4 text-slate-600 text-xs font-medium cursor-pointer hover:text-indigo-600" onClick={() => setSelectedPaymentDetail(payment)}>#{payment.user_id}</td>
                                <td className="py-4 px-4 font-bold text-slate-800 text-sm cursor-pointer hover:text-indigo-600" onClick={() => setSelectedPaymentDetail(payment)}>{payment.package_name}</td>
                                <td className="py-4 px-4 text-slate-900 font-bold text-sm">{formatCurrency(payment.amount_vnd)}</td>
                                <td className="py-4 px-4"><span className="px-2 py-0.5 bg-indigo-50 text-indigo-700 rounded-full text-xs font-bold">+{payment.tokens_received}</span></td>
                                <td className="py-4 px-4">
                                  <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold border ${payment.status === 'completed' ? 'bg-green-50 text-green-700 border-green-100' : payment.status === 'pending' ? 'bg-yellow-50 text-yellow-700 border-yellow-100' : 'bg-red-50 text-red-700 border-red-100'}`}>
                                    {payment.status === 'completed' ? 'Thành công' : payment.status === 'pending' ? 'Đang chờ' : 'Thất bại'}
                                  </span>
                                </td>
                                <td className="py-4 px-4 text-slate-500 text-xs">{formatDate(payment.created_at)}</td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>

                      {/* Mobile Payment List */}
                      <div className="md:hidden space-y-3">
                        {filteredPayments.map((payment) => (
                          <div key={payment.id} className="bg-white p-4 rounded-xl border border-slate-200 space-y-3">
                            <div className="flex justify-between items-start">
                              <p className="font-bold text-slate-800">{payment.package_name}</p>
                              <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold border ${payment.status === 'completed' ? 'bg-green-50 text-green-700 border-green-100' : 'bg-yellow-50 text-yellow-700 border-yellow-100'}`}>
                                {payment.status === 'completed' ? 'Xong' : 'Chờ'}
                              </span>
                            </div>
                            <div className="flex justify-between text-xs">
                              <span className="text-slate-500">Số tiền: <strong className="text-slate-800">{formatCurrency(payment.amount_vnd)}</strong></span>
                              <span className="text-indigo-600 font-bold">+{payment.tokens_received} Token</span>
                            </div>
                            <div className="flex justify-between items-center text-[10px] pt-2 border-t border-slate-50 text-slate-400">
                               <span>Hội viên: #{payment.user_id}</span>
                               <span>{formatDate(payment.created_at)}</span>
                            </div>
                          </div>
                        ))}
                      </div>

                      {filteredPayments.length === 0 && (
                        <div className="text-center py-12 text-slate-500">Không tìm thấy thanh toán</div>
                      )}
                    </div>
                  )}

{/* Banners Tab */}
                  {activeTab === 'banners' && (
                    <div className="space-y-4">
                      <div className="hidden md:block overflow-x-auto">
                        <table className="w-full text-left">
                          <thead>
                            <tr className="border-b border-slate-200 text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                              <th className="py-3 px-4">Mã</th>
                              <th className="py-3 px-4">User</th>
                              <th className="py-3 px-4">Mô tả</th>
                              <th className="py-3 px-4">Thông tin</th>
                              <th className="py-3 px-4">Chi phí</th>
                              <th className="py-3 px-4">Ngày tạo</th>
                            </tr>
                          </thead>
                          <tbody>
                            {filteredBanners.map((banner) => (
                              <tr key={banner.id} className="border-b border-slate-100 hover:bg-slate-50 transition-colors">
                                <td className="py-4 px-4 text-xs font-mono text-slate-400 cursor-pointer hover:text-indigo-600" onClick={() => setSelectedBannerDetail(banner)}>#{banner.id}</td>
                                <td className="py-4 px-4 text-xs font-bold text-slate-700 cursor-pointer hover:text-indigo-600" onClick={() => setSelectedBannerDetail(banner)}>#{banner.user_id}</td>
                                <td className="py-4 px-4 text-sm text-slate-700 max-w-xs truncate cursor-pointer hover:text-indigo-600" title={banner.request_description} onClick={() => setSelectedBannerDetail(banner)}>{banner.request_description}</td>
                                <td className="py-4 px-4 text-xs text-slate-500">{banner.aspect_ratio} • {banner.resolution}</td>
                                <td className="py-4 px-4"><span className="px-2 py-0.5 bg-orange-50 text-orange-700 rounded-full text-xs font-bold">{banner.token_cost} tok</span></td>
                                <td className="py-4 px-4 text-xs text-slate-400">{formatDate(banner.created_at)}</td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>

                      {/* Mobile Banner List */}
                      <div className="md:hidden space-y-3">
                         {filteredBanners.map((banner) => (
                           <div key={banner.id} className="bg-white p-4 rounded-xl border border-slate-200 space-y-2">
                             <div className="flex justify-between items-start">
                               <p className="text-xs font-bold text-slate-800 line-clamp-1">{banner.request_description}</p>
                               <span className="bg-orange-50 text-orange-600 px-2 py-0.5 rounded-full text-[10px] font-bold">{banner.token_cost} Token</span>
                             </div>
                             <p className="text-[10px] text-slate-500">{banner.aspect_ratio} • {banner.resolution}</p>
                             <div className="flex justify-between items-center text-[9px] text-slate-400 pt-2 border-t border-slate-50">
                                <span>Tạo bởi: #{banner.user_id}</span>
                                <span>{formatDate(banner.created_at)}</span>
                             </div>
                           </div>
                         ))}
                      </div>

                      {filteredBanners.length === 0 && (
                        <div className="text-center py-12 text-slate-500">Không tìm thấy banner</div>
                      )}
                    </div>
                  )}

                  {/* Packages Tab */}
                  {activeTab === 'packages' && (
                    <div>
                      {/* ... existing packages content ... */}
                      {!isEditingPackage && (
                        <div className="mb-6 flex justify-end">
                          <button
                            onClick={() => startEditPackage()}
                            className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors shadow-sm"
                          >
                            <Plus className="h-5 w-5" />
                            Thêm Gói Mới
                          </button>
                        </div>
                      )}

                      {isEditingPackage ? (
                        <div className="max-w-2xl mx-auto bg-slate-50 p-6 rounded-xl border border-slate-200">
                          <h3 className="text-lg font-bold text-slate-800 mb-4">{editingPackageId ? 'Chỉnh Sửa Gói' : 'Tạo Gói Mới'}</h3>
                          <div className="space-y-4">
                            <div>
                              <label className="block text-sm font-medium text-slate-700 mb-1">Tên gói</label>
                              <input
                                type="text"
                                value={packageForm.name}
                                onChange={(e) => setPackageForm({ ...packageForm, name: e.target.value })}
                                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                placeholder="Ví dụ: Gói Cơ Bản"
                              />
                            </div>
                            <div>
                              <label className="block text-sm font-medium text-slate-700 mb-1">Mô tả</label>
                              <textarea
                                value={packageForm.description}
                                onChange={(e) => setPackageForm({ ...packageForm, description: e.target.value })}
                                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                placeholder="Mô tả ưu đãi của gói"
                                rows={3}
                              />
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                              <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Giá (VND)</label>
                                <input
                                  type="number"
                                  value={packageForm.amount_vnd}
                                  onChange={(e) => setPackageForm({ ...packageForm, amount_vnd: parseInt(e.target.value) || 0 })}
                                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                />
                              </div>
                              <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Token nhận được</label>
                                <input
                                  type="number"
                                  value={packageForm.tokens}
                                  onChange={(e) => setPackageForm({ ...packageForm, tokens: parseInt(e.target.value) || 0 })}
                                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                />
                              </div>
                            </div>
                            <div className="flex items-center gap-2">
                              <input
                                type="checkbox"
                                id="isActive"
                                checked={packageForm.is_active}
                                onChange={(e) => setPackageForm({ ...packageForm, is_active: e.target.checked })}
                                className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                              />
                              <label htmlFor="isActive" className="text-sm font-medium text-slate-700">Kích hoạt (Hiển thị cho người dùng)</label>
                            </div>
                            <div className="flex justify-end gap-3 mt-6">
                              <button
                                onClick={() => setIsEditingPackage(false)}
                                className="px-4 py-2 text-slate-600 hover:bg-slate-200 rounded-lg transition-colors"
                              >
                                Hủy
                              </button>
                              <button
                                onClick={handleSavePackage}
                                className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors flex items-center gap-2"
                              >
                                <Save className="h-4 w-4" />
                                Lưu Gói
                              </button>
                            </div>
                          </div>
                        </div>
                      ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                          {packages.map((pkg) => (
                            <div key={pkg.id} className={`bg-white rounded-xl shadow-sm border p-6 relative group ${pkg.is_active ? 'border-indigo-100' : 'border-slate-200 opacity-75'}`}>
                              <div className="absolute top-4 right-4 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                <button
                                  onClick={() => startEditPackage(pkg)}
                                  className="p-1 text-blue-600 hover:bg-blue-50 rounded"
                                  title="Sửa"
                                >
                                  <Edit className="h-4 w-4" />
                                </button>
                                <button
                                  onClick={() => handleDeletePackage(pkg.id)}
                                  className="p-1 text-red-600 hover:bg-red-50 rounded"
                                  title="Xóa"
                                >
                                  <Trash2 className="h-4 w-4" />
                                </button>
                              </div>
                              <div className="flex items-start justify-between mb-4">
                                <div className={`p-3 rounded-lg ${pkg.is_active ? 'bg-indigo-100 text-indigo-600' : 'bg-slate-100 text-slate-500'}`}>
                                  <Package className="h-6 w-6" />
                                </div>
                                {!pkg.is_active && (
                                  <span className="px-2 py-1 bg-slate-100 text-slate-600 text-xs rounded-full font-medium">Ngừng hoạt động</span>
                                )}
                              </div>
                              <h3 className="text-lg font-bold text-slate-900 mb-1">{pkg.name}</h3>
                              <p className="text-slate-500 text-sm mb-4 h-10 line-clamp-2">{pkg.description}</p>
                              
                              <div className="flex items-center justify-between pt-4 border-t border-slate-100">
                                <div className="text-indigo-600 font-bold">{formatCurrency(pkg.amount_vnd)}</div>
                                <div className="text-sm font-medium bg-green-50 text-green-700 px-2 py-1 rounded-full">
                                  {pkg.tokens} Token
                                </div>
                              </div>
                            </div>
                          ))}
                          {packages.length === 0 && (
                            <div className="col-span-full text-center py-12 text-slate-500 bg-slate-50 rounded-xl border border-dashed border-slate-300">
                              <Package className="h-12 w-12 mx-auto text-slate-300 mb-3" />
                              <p>Chưa có gói cước nào. Hãy tạo mới.</p>
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  )}

                  {/* SEO Tab */}
                  {activeTab === 'seo' && (
                    <AdminSeoSettings />
                  )}

                  {/* Settings Tab */}
                  {activeTab === 'settings' && (
                    <div className="max-w-2xl mx-auto bg-white rounded-xl shadow-sm border p-4 md:p-6">
                      <div className="flex items-center gap-3 mb-6">
                        <div className="bg-indigo-50 p-2 rounded-lg text-indigo-600">
                          <Settings className="h-6 w-6" />
                        </div>
                        <div>
                          <h3 className="text-xl font-bold text-slate-900">Cấu Hình Dịch Vụ</h3>
                          <p className="text-sm text-slate-500">Giới hạn, mô hình AI, và cấu hình chung</p>
                        </div>
                      </div>
                      
                      <div className="space-y-6">
                          <div className="p-4 bg-slate-50 rounded-lg border border-slate-200">
                            <label className="block text-sm font-bold text-slate-700 mb-1">Mô hình ngôn ngữ (Text Model)</label>
                            <p className="text-xs text-slate-500 mb-3">Tuỳ chỉnh mô hình xử lý Text Prompt và Logic (Dòng Gemini 2.x hoặc 3.x Flash).</p>
                            <div className="flex flex-col sm:flex-row gap-3">
                              <select 
                                value={aiModel}
                                onChange={(e) => setAiModel(e.target.value)}
                                className="w-full px-3 py-2 border border-slate-300 rounded-lg outline-none focus:ring-2 focus:ring-indigo-500 bg-white"
                              >
                                <option value="gemini-3.1-pro-preview">Gemini 3.1 Pro (Bộ não mạnh nhất)</option>
                                <option value="gemini-2.5-flash">Gemini 2.5 Flash</option>
                                <option value="gemini-2.5-pro">Gemini 2.5 Pro (Nâng cao)</option>
                                <option value="gemini-2.0-flash">Gemini 2.0 Flash</option>
                              </select>
                              <button
                                onClick={handleUpdateAiModel}
                                className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 whitespace-nowrap font-bold text-sm"
                              >
                                Lưu Text Model
                              </button>
                            </div>
                          </div>

                          <div className="p-4 bg-slate-50 rounded-lg border border-slate-200">
                            <label className="block text-sm font-bold text-slate-700 mb-1">Mô hình tạo ảnh (Image Model)</label>
                            <p className="text-xs text-slate-500 mb-3">Mô hình chuyên biệt dùng để sinh banner/vẽ ảnh từ hệ thống.</p>
                            <div className="flex flex-col sm:flex-row gap-3">
                              <select 
                                value={imageModel}
                                onChange={(e) => setImageModel(e.target.value)}
                                className="w-full px-3 py-2 border border-slate-300 rounded-lg outline-none focus:ring-2 focus:ring-indigo-500 bg-white"
                              >
                                <option value="gemini-3.1-flash-image-preview">Gemini 3.1 Flash Image (Vẽ chữ VIP)</option>
                                <option value="imagen-4.0-generate-001">Imagen 4.0 Ultra (Đẳng cấp nhất)</option>
                                <option value="gemini-3.0-fast-image-preview">Gemini 3.0 Fast Image (Preview)</option>
                                <option value="gemini-2.5-flash-image">Gemini 2.5 Flash Image</option>
                                <option value="gemini-2.5-pro-image">Gemini 2.5 Pro Image</option>
                                <option value="gemini-2.0-flash-exp">Gemini 2.0 Flash EXP (Preview)</option>
                              </select>
                              <button
                                onClick={handleUpdateImageModel}
                                className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 whitespace-nowrap font-bold text-sm"
                              >
                                Lưu Image Model
                              </button>
                            </div>
                          </div>

                          <div className="p-4 bg-slate-50 rounded-lg border border-slate-200">
                            <label className="block text-sm font-bold text-slate-700 mb-1">Google API Key</label>
                            <p className="text-xs text-slate-500 mb-3">Thay thế Key gốc để không bị gián đoạn dịch vụ khi hết hạn ngạch. Xoá trắng để dùng lại biến môi trường.</p>
                            <div className="flex flex-col sm:flex-row gap-3">
                              <input 
                                type="password"
                                value={googleApiKey}
                                onChange={(e) => setGoogleApiKey(e.target.value)}
                                placeholder="AIzaSyB..."
                                className="w-full px-3 py-2 border border-slate-300 rounded-lg outline-none focus:ring-2 focus:ring-indigo-500 bg-white"
                              />
                              <button
                                onClick={handleUpdateGoogleApiKey}
                                className="px-4 py-2 bg-rose-600 text-white rounded-lg hover:bg-rose-700 whitespace-nowrap font-bold text-sm"
                              >
                                Lưu API Key
                              </button>
                            </div>
                          </div>

                          <div className="p-4 bg-slate-50 rounded-lg border border-slate-200">
                            <label className="block text-sm font-bold text-slate-700 mb-1">System Prompt (Kiểm soát cấu trúc Prompt Hệ Thống)</label>
                            <p className="text-xs text-slate-500 mb-3">Đính kèm tự động vào đuôi các lệnh tạo Banner. Người dùng chỉ cần ghi ý tưởng mộc mạc nhất, mô hình tự động tuân thủ System Prompt này.</p>
                            <div className="flex flex-col gap-3">
                              <textarea
                                value={systemPrompt}
                                onChange={(e) => setSystemPrompt(e.target.value)}
                                rows={5}
                                placeholder="VD: Bắt buộc chừa một dải trống màu rỗng bên trái để nhúng Text Quảng Cáo. Ánh sáng phải là studio light ngầu đét. Màu sắc Vibrant. Phong cách Riot Games..."
                                className="w-full px-3 py-2 border border-slate-300 rounded-lg outline-none focus:ring-2 focus:ring-indigo-500 bg-white resize-none text-sm"
                              />
                              <div className="flex justify-end">
                                <button
                                  onClick={handleUpdateSystemPrompt}
                                  className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-bold text-sm"
                                >
                                  Lưu System Prompt
                                </button>
                              </div>
                            </div>
                          </div>

                          <div className="p-4 bg-slate-50 rounded-lg border border-slate-200">
                            <label className="block text-sm font-bold text-slate-700 mb-1">Cấu hình an toàn (Gemini Safe Mode)</label>
                            <p className="text-xs text-slate-500 mb-3">Tốc độ chặn/từ chối từ khóa nhạy cảm (Google Safety Settings).</p>
                            <div className="flex flex-col sm:flex-row gap-3">
                              <select 
                                value={geminiSafeMode}
                                onChange={(e) => setGeminiSafeMode(e.target.value)}
                                className="w-full px-3 py-2 border border-slate-300 rounded-lg outline-none focus:ring-2 focus:ring-indigo-500 bg-white"
                              >
                                <option value="OFF">Tắt giám sát (OFF)</option>
                                <option value="BLOCK_LOW_AND_ABOVE">Nghiêm ngặt (BLOCK_LOW)</option>
                                <option value="BLOCK_MEDIUM_AND_ABOVE">Vừa phải (BLOCK_MEDIUM)</option>
                                <option value="BLOCK_ONLY_HIGH">Thoáng (BLOCK_HIGH)</option>
                              </select>
                              <button
                                onClick={handleUpdateGeminiSafeMode}
                                className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 whitespace-nowrap font-bold text-sm"
                              >
                                Lưu Safe Mode
                              </button>
                            </div>
                          </div>

                          <div className="p-4 bg-slate-50 rounded-lg border border-slate-200">
                            <label className="block text-sm font-bold text-slate-700 mb-1">Chi phí tạo ảnh (Token)</label>
                            <p className="text-xs text-slate-500 mb-3">Số token bị trừ cho mỗi lần tạo banner.</p>
                            <div className="flex flex-col sm:flex-row gap-3">
                              <input 
                                type="number" 
                                min="1"
                                value={bannerCost}
                                onChange={(e) => setBannerCost(parseInt(e.target.value) || 1)}
                                className="w-full px-3 py-2 border border-slate-300 rounded-lg outline-none focus:ring-2 focus:ring-indigo-500"
                              />
                              <button
                                onClick={handleUpdateCost}
                                className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 whitespace-nowrap font-bold text-sm"
                              >
                                Lưu Chi Phí
                              </button>
                            </div>
                          </div>

                          <div className="p-4 bg-slate-50 rounded-lg border border-slate-200">
                            <label className="block text-sm font-bold text-slate-700 mb-1">Chi phí ảnh tham chiếu (Token/Ảnh)</label>
                            <p className="text-xs text-slate-500 mb-3">Số token tính thêm cho mỗi ảnh bạn tải lên để làm mẫu.</p>
                            <div className="flex flex-col sm:flex-row gap-3">
                              <input 
                                type="number" 
                                step="0.1"
                                min="0"
                                value={referenceImageCost}
                                onChange={(e) => setReferenceImageCost(parseFloat(e.target.value) || 0)}
                                className="w-full px-3 py-2 border border-slate-300 rounded-lg outline-none focus:ring-2 focus:ring-indigo-500"
                              />
                              <button
                                onClick={handleUpdateRefCost}
                                className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 whitespace-nowrap font-bold text-sm"
                              >
                                Lưu Chi Phí
                              </button>
                            </div>
                          </div>
                      </div>
                    </div>
                  )}
                </>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Deposit Modal */}
      {selectedUserForTokens && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
          <div className="bg-white rounded-2xl w-full max-w-md p-6 shadow-2xl animate-in zoom-in-95">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-lg font-bold text-slate-900">Nạp Token Thủ Công</h3>
              <button onClick={() => setSelectedUserForTokens(null)} className="p-2 hover:bg-slate-100 rounded-full">
                <X className="h-5 w-5 text-slate-500" />
              </button>
            </div>
            
            <div className="space-y-4">
              <div className="p-4 bg-slate-50 rounded-xl border border-slate-100">
                <p className="text-sm text-slate-500">Người dùng</p>
                <p className="font-bold text-slate-900">{selectedUserForTokens.full_name}</p>
                <p className="text-xs text-slate-400">{selectedUserForTokens.email}</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Số lượng Token</label>
                <input 
                  type="number"
                  value={tokenDepositAmount}
                  onChange={(e) => setTokenDepositAmount(parseInt(e.target.value) || 0)}
                  className="w-full px-4 py-2 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div className="flex gap-3 pt-4">
                <button 
                  onClick={() => setSelectedUserForTokens(null)}
                  className="flex-1 px-4 py-2 border border-slate-200 text-slate-600 rounded-xl hover:bg-slate-50"
                >
                  Hủy
                </button>
                <button 
                  onClick={handleDepositTokens}
                  className="flex-1 px-4 py-2 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 font-bold"
                >
                  Xác Nhận Nạp
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* User History Modal */}
      {selectedUserForHistory && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-2 md:p-4 bg-black/60 backdrop-blur-sm">
          <div className="bg-white rounded-2xl w-full max-w-5xl max-h-[95vh] md:max-h-[90vh] flex flex-col shadow-2xl animate-in zoom-in-95">
            <div className="px-4 md:px-6 py-3 md:py-4 border-b border-slate-100 flex justify-between items-center">
              <div className="truncate pr-4">
                <h3 className="font-bold text-slate-900 text-sm md:text-base">Lịch sử tạo Banner</h3>
                <p className="text-[10px] md:text-xs text-slate-500 truncate">{selectedUserForHistory.email}</p>
              </div>
              <button onClick={() => setSelectedUserForHistory(null)} className="p-2 hover:bg-slate-100 rounded-full flex-shrink-0">
                <X className="h-4 w-4 md:h-5 md:w-5 text-slate-500" />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-4 md:p-6">
              {isLoading ? (
                <div className="flex justify-center py-12">
                   <div className="animate-spin rounded-full h-10 w-10 md:h-12 md:w-12 border-t-2 border-b-2 border-indigo-600"></div>
                </div>
              ) : userBanners.length === 0 ? (
                <div className="text-center py-12 text-slate-500 text-sm">
                  Người dùng chưa tạo banner nào.
                </div>
              ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
                  {userBanners.map((item) => (
                    <div key={item.id} className="bg-slate-50 rounded-xl overflow-hidden border border-slate-200 group relative">
                      <img src={item.image_url} alt="Banner" className="w-full aspect-video object-cover" />
                      <div className="p-3">
                        <p className="text-[10px] md:text-xs font-medium text-slate-800 line-clamp-2 mb-1">{item.request_description}</p>
                        <div className="flex justify-between items-center">
                          <span className="text-[9px] md:text-[10px] text-slate-400">{formatDate(item.created_at)}</span>
                          <span className="text-[9px] md:text-[10px] font-bold text-indigo-600">{item.token_cost} tokens</span>
                        </div>
                      </div>
                      <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                          <a href={item.image_url} target="_blank" rel="noreferrer" className="p-2 bg-white rounded-full text-indigo-600 hover:scale-110 transition-transform shadow-lg">
                             <Maximize2 className="h-4 w-4" />
                          </a>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* User Detail Modal */}
      {selectedUserDetail && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
          <div className="bg-white rounded-2xl w-full max-w-lg p-6 shadow-2xl animate-in zoom-in-95">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-bold text-slate-900">Chi tiết Người dùng</h3>
              <button onClick={() => setSelectedUserDetail(null)} className="p-2 hover:bg-slate-100 rounded-full">
                <X className="h-5 w-5 text-slate-500" />
              </button>
            </div>
            <div className="space-y-4">
              <div className="p-4 bg-slate-50 rounded-xl border border-slate-100 flex items-center gap-4">
                <img src={selectedUserDetail.avatar_url || `https://ui-avatars.com/api/?name=${encodeURIComponent(selectedUserDetail.full_name)}&background=random`} alt="Avatar" className="w-16 h-16 rounded-full shadow-sm" />
                <div>
                  <h4 className="font-bold text-slate-900 text-lg">{selectedUserDetail.full_name}</h4>
                  <p className="text-sm text-slate-500">{selectedUserDetail.email}</p>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 bg-indigo-50 rounded-xl border border-indigo-100">
                  <p className="text-xs text-indigo-600 font-medium mb-1">Số dư Token</p>
                  <p className="text-2xl font-black text-indigo-700">{selectedUserDetail.tokens}</p>
                </div>
                <div className="p-4 bg-slate-50 rounded-xl border border-slate-200">
                  <p className="text-xs text-slate-500 font-medium mb-1">Trạng thái Admin</p>
                  <p className={`text-sm font-bold ${selectedUserDetail.is_admin ? 'text-green-600' : 'text-slate-700'}`}>
                    {selectedUserDetail.is_admin ? 'Quản trị viên' : 'Người dùng'}
                  </p>
                </div>
              </div>
              <div className="p-4 bg-slate-50 rounded-xl border border-slate-100">
                  <p className="text-xs text-slate-500 mb-1">ID Hệ thống: <span className="font-mono text-slate-700">{selectedUserDetail.id}</span></p>
                  <p className="text-xs text-slate-500">Google ID: <span className="font-mono text-slate-700">{selectedUserDetail.google_id || 'N/A'}</span></p>
                  <p className="text-xs text-slate-500 mt-2">Ngày tham gia: <span className="text-slate-700">{formatDate(selectedUserDetail.created_at)}</span></p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Payment Detail Modal */}
      {selectedPaymentDetail && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
          <div className="bg-white rounded-2xl w-full max-w-lg p-6 shadow-2xl animate-in zoom-in-95">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-bold text-slate-900">Chi tiết Hóa đơn</h3>
              <button onClick={() => setSelectedPaymentDetail(null)} className="p-2 hover:bg-slate-100 rounded-full">
                <X className="h-5 w-5 text-slate-500" />
              </button>
            </div>
            <div className="space-y-4">
              <div className={`p-4 rounded-xl border flex items-center gap-4 ${selectedPaymentDetail.status === 'completed' ? 'bg-green-50 border-green-200 text-green-700' : selectedPaymentDetail.status === 'pending' ? 'bg-yellow-50 border-yellow-200 text-yellow-700' : 'bg-red-50 border-red-200 text-red-700'}`}>
                <div className="p-2 rounded-full bg-white bg-opacity-50">
                  <CreditCard className="h-6 w-6" />
                </div>
                <div>
                  <h4 className="font-bold text-lg">{formatCurrency(selectedPaymentDetail.amount_vnd)}</h4>
                  <p className="text-sm font-medium uppercase tracking-wide">{selectedPaymentDetail.status === 'completed' ? 'Thành công' : selectedPaymentDetail.status === 'pending' ? 'Đang chờ m.toán' : 'Thất bại'}</p>
                </div>
              </div>
              
              <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-3">
                <div className="flex justify-between">
                  <span className="text-sm text-slate-500">Người dùng ID:</span>
                  <span className="text-sm font-bold text-slate-900">#{selectedPaymentDetail.user_id}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-slate-500">Gói nạp:</span>
                  <span className="text-sm font-bold text-slate-900">{selectedPaymentDetail.package_name}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-slate-500">Token nhận:</span>
                  <span className="text-sm font-bold text-indigo-600">+{selectedPaymentDetail.tokens_received}</span>
                </div>
              </div>

              <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-3">
                <div className="flex justify-between">
                  <span className="text-sm text-slate-500">Mã giao dịch (SePay):</span>
                  <span className="text-xs font-mono text-slate-700">{selectedPaymentDetail.sepay_transaction_id || 'Chưa có'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-slate-500">Nội dung CK:</span>
                  <span className="text-xs font-mono text-slate-700">{selectedPaymentDetail.payment_code}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-slate-500">Tạo lúc:</span>
                  <span className="text-sm text-slate-700">{formatDate(selectedPaymentDetail.created_at)}</span>
                </div>
                {selectedPaymentDetail.completed_at && (
                  <div className="flex justify-between">
                    <span className="text-sm text-slate-500">Hoàn thành lúc:</span>
                    <span className="text-sm text-slate-700">{formatDate(selectedPaymentDetail.completed_at || '')}</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Banner Detail Modal */}
      {selectedBannerDetail && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
          <div className="bg-white rounded-2xl w-full max-w-4xl max-h-[95vh] flex flex-col shadow-2xl animate-in zoom-in-95 overflow-hidden">
            <div className="px-6 py-4 border-b border-slate-100 flex justify-between items-center bg-slate-50">
              <div>
                <h3 className="font-bold text-slate-900 text-lg">Chi tiết Banner</h3>
                <p className="text-xs text-slate-500">ID: #{selectedBannerDetail.id} - Người dùng: #{selectedBannerDetail.user_id}</p>
              </div>
              <button onClick={() => setSelectedBannerDetail(null)} className="p-2 hover:bg-slate-200 rounded-full flex-shrink-0 bg-white shadow-sm border border-slate-200">
                <X className="h-5 w-5 text-slate-500" />
              </button>
            </div>
            <div className="flex-1 overflow-y-auto p-6 md:flex gap-6">
              <div className="w-full md:w-1/2 mb-6 md:mb-0">
                 <div className="bg-slate-100 rounded-xl overflow-hidden border border-slate-200 flex items-center justify-center h-full min-h-[300px]">
                    <img src={selectedBannerDetail.image_url} alt="Banner Preview" className="max-w-full max-h-[60vh] object-contain shadow-md" />
                 </div>
              </div>
              <div className="w-full md:w-1/2 space-y-4">
                 <div className="p-4 bg-indigo-50 rounded-xl border border-indigo-100">
                   <h4 className="text-xs font-bold text-indigo-800 uppercase mb-2">Yêu cầu từ người dùng</h4>
                   <p className="text-sm text-indigo-900 leading-relaxed font-medium">"{selectedBannerDetail.request_description}"</p>
                 </div>
                 <div className="p-4 bg-slate-50 rounded-xl border border-slate-200">
                   <h4 className="text-xs font-bold text-slate-500 uppercase mb-1">Cấu hình sử dụng</h4>
                   <div className="grid grid-cols-2 gap-4 mt-3">
                     <div>
                       <span className="block text-[10px] text-slate-400">Tỷ lệ khung hình</span>
                       <span className="font-bold text-slate-700">{selectedBannerDetail.aspect_ratio}</span>
                     </div>
                     <div>
                       <span className="block text-[10px] text-slate-400">Độ phân giải</span>
                       <span className="font-bold text-slate-700">{selectedBannerDetail.resolution}</span>
                     </div>
                     <div>
                       <span className="block text-[10px] text-slate-400">Chi phí tiêu hao</span>
                       <span className="font-bold text-orange-600">{selectedBannerDetail.token_cost} Tokens</span>
                     </div>
                     <div>
                       <span className="block text-[10px] text-slate-400">Thời gian tạo</span>
                       <span className="font-bold text-slate-700 text-xs">{formatDate(selectedBannerDetail.created_at)}</span>
                     </div>
                   </div>
                 </div>
                 
                 <div className="p-4 bg-slate-50 rounded-xl border border-slate-200">
                   <h4 className="text-xs font-bold text-slate-500 uppercase mb-2">System LLM Prompt đã dùng</h4>
                   <div className="bg-slate-800 text-slate-300 p-3 rounded-lg text-xs font-mono max-h-48 overflow-y-auto">
                     {selectedBannerDetail.prompt_used}
                   </div>
                 </div>
                 
                 <div className="flex gap-3 pt-2">
                    <a href={selectedBannerDetail.image_url} target="_blank" rel="noreferrer" className="flex-1 text-center py-2.5 bg-indigo-600 text-white font-bold rounded-xl hover:bg-indigo-700 transition-colors">
                      Mở Ảnh Gốc Chi Tiết
                    </a>
                 </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Confirm Modal */}
      <ConfirmModal 
        isOpen={confirmConfig.isOpen}
        title={confirmConfig.title}
        message={confirmConfig.message}
        onConfirm={confirmConfig.onConfirm}
        onCancel={() => setConfirmConfig(prev => ({ ...prev, isOpen: false }))}
      />
    </div>
  );
};

export default AdminPanel;
