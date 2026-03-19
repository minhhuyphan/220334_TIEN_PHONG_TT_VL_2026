import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { User, PaymentHistoryItem, BannerHistoryItem } from '../types';
import { apiService } from '../services/api';
import { 
  Download, 
  Calendar, 
  Activity, 
  Trash2, 
  Layers, 
  Maximize2,
  CreditCard,
  CheckCircle,
  Clock,
  X,
  Image as ImageIcon,
  History as HistoryIcon,
  RefreshCcw
} from 'lucide-react';
import toast from 'react-hot-toast';
import ConfirmModal from './ConfirmModal';

interface HistoryProps {
  user: User;
  onNavigate?: (route: string, state?: any) => void;
}

const History: React.FC<HistoryProps> = ({ user, onNavigate }) => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<'banners' | 'payments'>('banners');
  const [bannerHistory, setBannerHistory] = useState<BannerHistoryItem[]>([]);
  const [paymentHistory, setPaymentHistory] = useState<PaymentHistoryItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  
  // Modal state
  const [selectedBanner, setSelectedBanner] = useState<BannerHistoryItem | null>(null);

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

  useEffect(() => {
    fetchData();
  }, [user, activeTab]);

  const fetchData = async () => {
    setIsLoading(true);
    try {
      if (activeTab === 'banners') {
        const data = await apiService.getHistory();
        setBannerHistory(Array.isArray(data) ? data : []);
      } else {
        const data = await apiService.getPaymentHistory();
        setPaymentHistory(Array.isArray(data) ? data : []);
      }
    } catch (error) {
      console.error('Error fetching history:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteBanner = (id: number, e: React.MouseEvent) => {
    e.stopPropagation();
    setConfirmConfig({
      isOpen: true,
      title: "Xác nhận xoá banner",
      message: "Bạn có chắc chắn muốn xoá banner này không?",
      onConfirm: async () => {
        try {
          await apiService.deleteHistoryItem(id);
          toast.success("Đã xoá banner thành công");
          setBannerHistory(prev => prev.filter(item => item.id !== id));
          if (selectedBanner?.id === id) setSelectedBanner(null);
        } catch (error) {
          toast.error("Xoá thất bại");
        }
      }
    });
  };

  const handleClearAllBanners = () => {
    setConfirmConfig({
      isOpen: true,
      title: "Xác nhận xoá toàn bộ lịch sử",
      message: "CẢNH BÁO: Bạn có chắc chắn muốn xoá TOÀN BỘ lịch sử banner không?",
      onConfirm: async () => {
        try {
          await apiService.clearHistory();
          setBannerHistory([]);
          toast.success("Đã xoá toàn bộ lịch sử");
        } catch (error) {
          toast.error("Xoá thất bại");
        }
      }
    });
  };

  const handleDownload = (imageUrl: string) => {
    const downloadUrl = imageUrl.includes('?') 
      ? `${imageUrl}&download=true` 
      : `${imageUrl}?download=true`;
    
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.setAttribute('download', 'banner.png');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    toast.success('Đang bắt đầu tải xuống...');
  };

  const handleRegenerate = () => {
    if (!selectedBanner) return;
    
    const targetRoute = (__APP_ROUTES__ as any).GENERATE;
    const state = { regenerateData: selectedBanner };

    if (onNavigate) {
      onNavigate(targetRoute, { state });
    } else {
      navigate(targetRoute, { state });
    }
    
    toast.success('Đã tải lên thông tin banner cũ');
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('vi-VN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatCurrency = (val: number) => {
    return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(val);
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6 animate-in fade-in duration-500 pb-12">
      {/* Header & Tabs */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-800">Lịch Sử Hoạt Động</h2>
          <p className="text-slate-500">Quản lý banner đã tạo và lịch sử giao dịch</p>
        </div>
        
        <div className="flex bg-slate-100 p-1 rounded-xl w-full md:w-auto">
          <button
            onClick={() => setActiveTab('banners')}
            className={`flex-1 md:flex-none flex items-center justify-center gap-2 px-3 md:px-6 py-2 md:py-2.5 rounded-lg font-medium transition-all text-xs md:text-sm ${
              activeTab === 'banners' 
                ? 'bg-white text-indigo-600 shadow-sm' 
                : 'text-slate-500 hover:text-slate-700'
            }`}
          >
            <ImageIcon className="h-4 w-4" />
            <span className="truncate">Lịch sử Tạo Ảnh</span>
          </button>
          <button
            onClick={() => setActiveTab('payments')}
            className={`flex-1 md:flex-none flex items-center justify-center gap-2 px-3 md:px-6 py-2 md:py-2.5 rounded-lg font-medium transition-all text-xs md:text-sm ${
              activeTab === 'payments' 
                ? 'bg-white text-indigo-600 shadow-sm' 
                : 'text-slate-500 hover:text-slate-700'
            }`}
          >
            <CreditCard className="h-4 w-4" />
            <span className="truncate">Lịch sử Giao Dịch</span>
          </button>
        </div>
      </div>

      {/* Main Content */}
      {isLoading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-600"></div>
        </div>
      ) : (
        <>
          {/* BANNER TAB */}
          {activeTab === 'banners' && (
            <div className="space-y-4">
              {bannerHistory.length > 0 && (
                <div className="flex justify-end">
                  <button 
                    onClick={handleClearAllBanners}
                    className="flex items-center gap-2 px-4 py-2 text-red-600 bg-red-50 hover:bg-red-100 rounded-lg transition-colors text-xs md:text-sm font-medium"
                  >
                    <Trash2 className="h-4 w-4" />
                    Xoá tất cả
                  </button>
                </div>
              )}

              {bannerHistory.length === 0 ? (
                <div className="bg-white rounded-2xl p-8 md:p-12 text-center border border-slate-200 shadow-sm">
                  <Layers className="h-12 w-12 md:h-16 md:w-16 text-slate-300 mx-auto mb-4" />
                  <h3 className="text-lg md:text-xl font-bold text-slate-700 mb-2">Chưa có banner nào</h3>
                  <p className="text-sm md:text-base text-slate-500">Bạn chưa tạo banner nào. Hãy thử công cụ AI ngay!</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
                  {bannerHistory.map((item) => (
                    <div 
                      key={item.id} 
                      className="bg-white rounded-xl overflow-hidden border border-slate-200 shadow-sm hover:shadow-md transition-all cursor-pointer group"
                      onClick={() => setSelectedBanner(item)}
                    >
                      <div className="aspect-video bg-slate-100 relative overflow-hidden">
                        <img 
                          src={item.image_url} 
                          alt="Banner" 
                          className="w-full h-full object-cover transition-transform group-hover:scale-105"
                          loading="lazy"
                        />
                        <div className="absolute inset-0 bg-black/5 md:bg-black/0 md:group-hover:bg-black/10 transition-colors" />
                        <div className="absolute top-2 right-2 flex gap-2 md:opacity-0 md:group-hover:opacity-100 transition-opacity">
                           <button
                              onClick={(e) => handleDeleteBanner(item.id, e)}
                              className="p-2 bg-white/90 text-red-600 rounded-lg md:rounded-full hover:bg-red-50 shadow-sm backdrop-blur-sm"
                              title="Xoá"
                           >
                             <Trash2 className="h-4 w-4" />
                           </button>
                        </div>
                      </div>
                      
                      <div className="p-4">
                        <div className="flex justify-between items-start mb-2">
                          <span className="text-[10px] md:text-xs text-slate-500">{formatDate(item.created_at)}</span>
                          <span className="text-[10px] md:text-xs px-2 py-0.5 bg-indigo-50 text-indigo-700 rounded-full font-bold">
                            {item.token_cost} tokens
                          </span>
                        </div>
                        <p className="text-sm font-medium text-slate-800 line-clamp-2 leading-relaxed">
                          {item.request_description || "Không có mô tả"}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* PAYMENT TAB */}
          {activeTab === 'payments' && (
            <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
              {paymentHistory.length === 0 ? (
                <div className="p-12 text-center text-slate-500">
                  <CreditCard className="h-12 w-12 mx-auto mb-4 opacity-20" />
                  <p>Chưa có giao dịch nào.</p>
                </div>
              ) : (
                <>
                  <div className="hidden md:block overflow-x-auto">
                    <table className="w-full text-left">
                      <thead>
                        <tr className="bg-slate-50 border-b border-slate-200">
                          <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Mã GD</th>
                          <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Gói nhận</th>
                          <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Số tiền</th>
                          <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Trạng thái</th>
                          <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Thời gian</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-100">
                        {paymentHistory.map((item) => (
                          <tr key={item.id} className="hover:bg-slate-50 transition-colors">
                            <td className="px-6 py-4 text-sm text-slate-600 font-mono">#{item.id}</td>
                            <td className="px-6 py-4">
                              <div>
                                 <p className="text-sm font-semibold text-slate-900">{item.package_name}</p>
                                 <p className="text-xs text-slate-500">+{item.tokens} tokens</p>
                              </div>
                            </td>
                            <td className="px-6 py-4 text-sm font-bold text-slate-700">
                              {formatCurrency(item.amount_vnd)}
                            </td>
                            <td className="px-6 py-4">
                              {item.status === 'completed' ? (
                                <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 border border-green-200">
                                  <CheckCircle className="h-3 w-3" />
                                  Thành công
                                </span>
                              ) : item.status === 'pending' ? (
                                <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800 border border-yellow-200">
                                  <Clock className="h-3 w-3" />
                                  Đang chờ
                                </span>
                              ) : (
                                <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800 border border-red-200">
                                  <X className="h-3 w-3" />
                                  Thất bại
                                </span>
                              )}
                            </td>
                            <td className="px-6 py-4 text-xs text-slate-500">
                              {formatDate(item.created_at)}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>

                  <div className="md:hidden divide-y divide-slate-100">
                    {paymentHistory.map((item) => (
                      <div key={item.id} className="p-4 space-y-3">
                        <div className="flex justify-between items-start">
                          <div>
                             <p className="text-xs font-mono text-slate-400 mb-1">#{item.id}</p>
                             <p className="text-sm font-bold text-slate-900">{item.package_name}</p>
                             <p className="text-xs text-indigo-600 font-medium">+{item.tokens} tokens</p>
                          </div>
                          <div className="text-right">
                            <p className="text-sm font-bold text-slate-900 mb-1">{formatCurrency(item.amount_vnd)}</p>
                            {item.status === 'completed' ? (
                              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-green-50 text-green-700 border border-green-100">
                                Thành công
                              </span>
                            ) : item.status === 'pending' ? (
                              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-yellow-50 text-yellow-700 border border-yellow-101">
                                Đang chờ
                              </span>
                            ) : (
                              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-red-50 text-red-700 border border-red-101">
                                Thất bại
                              </span>
                            )}
                          </div>
                        </div>
                        <div className="flex items-center gap-1 text-[10px] text-slate-400">
                           <Clock className="h-3 w-3" />
                           {formatDate(item.created_at)}
                        </div>
                      </div>
                    ))}
                  </div>
                </>
              )}
            </div>
          )}
        </>
      )}

      {/* DETAIL MODAL */}
      {selectedBanner && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
          <div 
            className="bg-white rounded-2xl w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col shadow-2xl animate-in zoom-in-50 duration-200"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Modal Header */}
            <div className="px-6 py-4 border-b border-slate-100 flex justify-between items-center bg-white sticky top-0 z-10">
              <div className="flex items-center gap-2">
                <ImageIcon className="h-5 w-5 text-indigo-600" />
                <h3 className="font-bold text-slate-800">Chi tiết Banner</h3>
              </div>
              <button 
                onClick={() => setSelectedBanner(null)}
                className="p-2 hover:bg-slate-100 rounded-full transition-colors text-slate-500"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {/* Modal Content - Scrollable */}
            <div className="overflow-y-auto flex-1 p-6">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Image Section */}
                <div className="space-y-4">
                   <div className="bg-slate-100 rounded-xl overflow-hidden border border-slate-200 shadow-inner">
                     <img 
                       src={selectedBanner.image_url} 
                       alt="Full Banner" 
                       className="w-full h-auto object-contain"
                     />
                   </div>
                   
                   <div className="flex gap-3">
                      <button 
                        onClick={() => handleDownload(selectedBanner.image_url)}
                        className="flex-1 flex justify-center items-center gap-2 bg-indigo-600 text-white px-4 py-3 rounded-xl font-medium hover:bg-indigo-700 transition-colors shadow-lg shadow-indigo-100"
                      >
                        <Download className="h-5 w-5" />
                        Tải xuống
                      </button>
                     <button
                        onClick={(e) => handleDeleteBanner(selectedBanner.id, e)}
                        className="flex items-center gap-2 px-4 py-3 border border-red-200 text-red-600 rounded-xl font-medium hover:bg-red-50 transition-colors"
                     >
                       <Trash2 className="h-5 w-5" />
                       Xoá
                     </button>
                   </div>
                </div>

                {/* Info Section */}
                <div className="space-y-6">
                  <div>
                    <h4 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-2">Thông tin cơ bản</h4>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                        <span className="text-xs text-slate-500 block mb-1">Thời gian tạo</span>
                        <span className="text-sm font-medium text-slate-900">{formatDate(selectedBanner.created_at)}</span>
                      </div>
                      <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                        <span className="text-xs text-slate-500 block mb-1">Chi phí</span>
                        <span className="text-sm font-medium text-indigo-600">{selectedBanner.token_cost} Token</span>
                      </div>
                      <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                         <span className="text-xs text-slate-500 block mb-1">Kích thước</span>
                         <span className="text-sm font-medium text-slate-900">{selectedBanner.resolution}</span>
                      </div>
                      <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                         <span className="text-xs text-slate-500 block mb-1">Tỷ lệ</span>
                         <span className="text-sm font-medium text-slate-900">{selectedBanner.aspect_ratio}</span>
                      </div>
                    </div>
                  </div>

                  <div>
                     <h4 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-2">Yêu cầu gốc (Prompt)</h4>
                     <div className="p-4 bg-indigo-50/50 rounded-xl border border-indigo-100 text-slate-700 text-sm leading-relaxed">
                       {selectedBanner.request_description}
                     </div>
                  </div>

                  <div>
                     <h4 className="flex items-center gap-2 text-sm font-bold text-slate-400 uppercase tracking-wider mb-2">
                       <Activity className="h-4 w-4" />
                       Prompt AI Chi Tiết
                     </h4>
                     <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 text-slate-600 text-sm font-mono leading-relaxed max-h-40 overflow-y-auto">
                       {selectedBanner.prompt_used}
                     </div>
                  </div>

                  {selectedBanner.reference_images_list && selectedBanner.reference_images_list.length > 0 && (
                    <div>
                      <h4 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-3">Ảnh tham chiếu đã dùng</h4>
                      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                        {selectedBanner.reference_images_list.map((ref, idx) => (
                          <div key={idx} className="relative group rounded-lg overflow-hidden border border-slate-200">
                            <img 
                              src={ref.url} 
                              alt={ref.label} 
                              className="w-full aspect-square object-cover"
                            />
                            <div className="absolute bottom-0 left-0 right-0 bg-black/60 text-white text-[10px] px-2 py-1 text-center truncate">
                              @{ref.label}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  <div className="pt-4 border-t border-slate-100">
                      <button
                        onClick={handleRegenerate}
                        className="w-full flex justify-center items-center gap-2 bg-amber-500 text-white px-4 py-3 rounded-xl font-bold hover:bg-amber-600 transition-colors shadow-lg shadow-amber-100"
                      >
                        <RefreshCcw className="h-5 w-5" />
                        Sử dụng lại Prompt & Ảnh này
                      </button>
                      <p className="text-[10px] text-slate-400 text-center mt-2">
                        Hệ thống sẽ điền lại toàn bộ thông tin gốc cho bạn
                      </p>
                  </div>
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

export default History;
