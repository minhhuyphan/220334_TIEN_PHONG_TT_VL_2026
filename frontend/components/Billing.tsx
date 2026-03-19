import React, { useState, useEffect } from 'react';
import { User, Package } from '../types';
import { apiService } from '../services/api';
import { Check, Star, Zap, X, Copy, RefreshCw, CheckCircle2, CreditCard } from 'lucide-react';
import toast from 'react-hot-toast';

interface BillingProps {
    user: User;
    refreshUser: () => void;
}

const Billing: React.FC<BillingProps> = ({ user, refreshUser }) => {
    const [packages, setPackages] = useState<Package[]>([]);
    const [selectedPackage, setSelectedPackage] = useState<Package | null>(null);
    const [loading, setLoading] = useState(false);
    const [paymentData, setPaymentData] = useState<any>(null);
    const [checkStatusLoading, setCheckStatusLoading] = useState(false);
    const [paymentSuccess, setPaymentSuccess] = useState(false);

    useEffect(() => {
        const fetchPackages = async () => {
            try {
                const data = await apiService.getPackages();
                setPackages(data);
            } catch (error) {
                console.error("Failed to fetch packages", error);
            }
        };
        fetchPackages();
    }, []);

    const handleBuy = async (pkg: Package) => {
        setLoading(true);
        setSelectedPackage(pkg);
        try {
            const data = await apiService.createPayment(pkg.id);
            setPaymentData(data);
        } catch (error) {
            console.error(error);
            toast.error("Lỗi tạo thanh toán");
        } finally {
            setLoading(false);
        }
    };

    // Auto-polling for payment status
    useEffect(() => {
        let intervalId: any;
        if (paymentData && !paymentSuccess) {
            intervalId = setInterval(async () => {
                await handleCheckStatus(true); // silent check
            }, 5000);
        }
        return () => {
            if (intervalId) clearInterval(intervalId);
        };
    }, [paymentData, paymentSuccess]);

    const handleCheckStatus = async (silent = false) => {
         if (!paymentData) return;
         if (!silent) setCheckStatusLoading(true);
         
         try {
             const res = await apiService.checkPaymentStatus(paymentData.payment_id);
             if (res.status === 'completed') {
                 setPaymentSuccess(true);
                 refreshUser();
                 if (!silent) toast.success("Thanh toán thành công! Tokens đã được cộng.");
                 
                 // Close modal after 3s
                 setTimeout(() => {
                     setPaymentData(null);
                     setPaymentSuccess(false);
                     setSelectedPackage(null);
                 }, 3000);
             } else {
                 if (!silent) toast.error("Thanh toán chưa hoàn tất hoặc đang xử lý.");
             }
         } catch (error) {
             console.error(error);
             if (!silent) toast.error("Lỗi kiểm tra trạng thái");
         } finally {
             if (!silent) setCheckStatusLoading(false);
         }
    };


    const formatCurrency = (val: number) => {
        return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(val);
    };

    return (
        <div className="max-w-5xl mx-auto space-y-6 md:space-y-8 animate-in zoom-in-50 duration-500 pb-10">
            <div className="text-center space-y-3 md:space-y-4">
                <h2 className="text-2xl md:text-3xl font-bold text-slate-900">Gói Cước Dịch Vụ</h2>
                <p className="text-sm md:text-base text-slate-500 max-w-2xl mx-auto px-4">
                    Chọn gói cước phù hợp với nhu cầu của bạn. Tỷ lệ quy đổi: 1.000 VND = 1 Token. 
                    Nạp càng nhiều, ưu đãi càng lớn.
                </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8 pt-4 md:pt-8 px-4 md:px-0">
                {packages.map((pkg) => {
                    const isPopular = pkg.tokens >= 500; // Example logic for popular
                    return (
                        <div 
                            key={pkg.id} 
                            className={`relative bg-white rounded-2xl md:rounded-3xl p-6 md:p-8 border ${isPopular ? 'border-indigo-600 shadow-xl md:scale-105 z-10' : 'border-slate-200 shadow-sm hover:shadow-md'} transition-all flex flex-col`}
                        >
                            {isPopular && (
                                <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-indigo-600 text-white px-3 py-0.5 md:py-1 rounded-full text-[10px] md:text-sm font-bold flex items-center gap-1 shadow-lg shadow-indigo-200 whitespace-nowrap">
                                    <Star className="h-3 w-3 md:h-4 md:w-4 fill-current" />
                                    Phổ biến nhất
                                </div>
                            )}
                            
                            <div className="mb-4 md:mb-6">
                                <h3 className="text-base md:text-lg font-bold text-slate-600 mb-1 md:mb-2">{pkg.name}</h3>
                                <div className="flex items-baseline gap-1">
                                    <span className="text-3xl md:text-4xl font-bold text-slate-900">
                                        {formatCurrency(pkg.amount_vnd).replace('₫', '')}
                                    </span>
                                    <span className="text-xs md:text-sm text-slate-500">VND</span>
                                </div>
                                <p className="text-xs md:text-sm text-indigo-600 font-bold mt-1 md:mt-2">
                                    nhận {pkg.tokens} Token
                                </p>
                            </div>

                            <ul className="space-y-3 md:space-y-4 mb-6 md:mb-8 flex-1">
                                <li className="flex items-center gap-3 text-slate-600">
                                   <div className="p-1 rounded-full bg-green-100 text-green-600 flex-shrink-0">
                                     <Check className="h-3 w-3" />
                                   </div>
                                   <span className="text-xs md:text-sm">Mở khóa tất cả tỷ lệ khung hình</span>
                                </li>
                                <li className="flex items-center gap-3 text-slate-600">
                                   <div className="p-1 rounded-full bg-green-100 text-green-600 flex-shrink-0">
                                     <Check className="h-3 w-3" />
                                   </div>
                                   <span className="text-xs md:text-sm">Tốc độ ưu tiên cao</span>
                                </li>
                                <li className="flex items-center gap-3 text-slate-600">
                                   <div className="p-1 rounded-full bg-green-100 text-green-600 flex-shrink-0">
                                     <Check className="h-3 w-3" />
                                   </div>
                                   <span className="text-xs md:text-sm">Hỗ trợ 24/7</span>
                                </li>
                            </ul>

                            <button
                                onClick={() => handleBuy(pkg)}
                                disabled={loading}
                                className={`w-full py-3 md:py-3.5 rounded-xl font-bold flex items-center justify-center gap-2 transition-all text-sm md:text-base ${
                                    isPopular 
                                    ? 'bg-indigo-600 text-white hover:bg-indigo-700 shadow-lg shadow-indigo-100' 
                                    : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                                }`}
                            >
                                {loading && selectedPackage?.id === pkg.id ? (
                                    <>
                                        <RefreshCw className="h-4 w-4 md:h-5 md:w-5 animate-spin" />
                                        Đang xử lý...
                                    </>
                                ) : (
                                    <>
                                        <Zap className="h-4 w-4 md:h-5 md:w-5" />
                                        Mua Ngay
                                    </>
                                )}
                            </button>
                        </div>
                    );
                })}
            </div>

            {/* Payment Modal */}
            {paymentData && (
                <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in overflow-y-auto">
                    <div className="bg-white rounded-2xl md:rounded-3xl max-w-lg w-full p-4 md:p-8 shadow-2xl relative my-auto animate-in zoom-in-95">
                        <button 
                            onClick={() => setPaymentData(null)}
                            className="absolute top-3 right-3 md:top-4 md:right-4 p-2 bg-slate-100 rounded-full hover:bg-slate-200 z-10"
                        >
                            <X className="h-4 w-4 md:h-5 md:w-5 text-slate-500" />
                        </button>

                        {paymentSuccess ? (
                            <div className="text-center py-6 md:py-8">
                                <div className="mx-auto w-16 h-16 md:w-20 md:h-20 bg-green-100 rounded-full flex items-center justify-center mb-4 md:mb-6">
                                    <CheckCircle2 className="h-8 w-8 md:h-10 md:w-10 text-green-600" />
                                </div>
                                <h3 className="text-xl md:text-2xl font-bold text-slate-900 mb-2">Thành công!</h3>
                                <p className="text-sm md:text-base text-slate-500">Đã cộng token vào tài khoản của bạn.</p>
                            </div>
                        ) : (
                            <>
                                <h3 className="text-lg md:text-xl font-bold text-slate-900 mb-4 md:mb-6 flex items-center gap-2">
                                    <CreditCard className="h-5 w-5 md:h-6 md:w-6 text-indigo-600" />
                                    Thông Tin Chuyển Khoản
                                </h3>

                                <div className="space-y-4 md:space-y-6">
                                    <div className="flex justify-center bg-slate-50 p-2 md:p-4 rounded-xl border border-slate-100">
                                        <img src={paymentData.qr_url} alt="QR Code" className="w-40 h-40 md:w-48 md:h-48 mix-blend-multiply" />
                                    </div>

                                    <div className="space-y-2 md:space-y-3">
                                        <div className="flex justify-between items-center py-2 border-b border-slate-50">
                                            <span className="text-slate-500 text-xs md:text-sm">Ngân hàng</span>
                                            <span className="font-bold text-slate-900 text-sm md:text-base">{paymentData.bank_brand}</span>
                                        </div>
                                        <div className="flex justify-between items-center py-2 border-b border-slate-50">
                                            <span className="text-slate-500 text-xs md:text-sm">Số tài khoản</span>
                                            <div className="flex items-center gap-2">
                                                <span className="font-bold text-slate-900 font-mono tracking-wider text-sm md:text-base">{paymentData.bank_account}</span>
                                                <button 
                                                    onClick={() => {
                                                        navigator.clipboard.writeText(paymentData.bank_account);
                                                        toast.success("Đã sao chép STK");
                                                    }}
                                                    className="text-indigo-600 hover:text-indigo-700"
                                                >
                                                    <Copy className="h-4 w-4" />
                                                </button>
                                            </div>
                                        </div>
                                        <div className="flex justify-between items-center py-2 border-b border-slate-50">
                                            <span className="text-slate-500 text-xs md:text-sm">Số tiền</span>
                                            <span className="font-bold text-slate-900 text-base md:text-lg text-indigo-600">
                                                {formatCurrency(paymentData.amount_vnd)}
                                            </span>
                                        </div>
                                        <div className="flex justify-between items-start md:items-center py-2 border-b border-slate-50">
                                            <span className="text-slate-500 text-xs md:text-sm mt-1 md:mt-0">Nội dung</span>
                                            <div className="flex items-center gap-2">
                                                <span className="font-bold text-slate-900 bg-yellow-100 px-2 py-0.5 md:py-1 rounded text-xs md:text-sm">{paymentData.transaction_content}</span>
                                                <button 
                                                    onClick={() => {
                                                        navigator.clipboard.writeText(paymentData.transaction_content);
                                                        toast.success("Đã sao chép nội dung");
                                                    }}
                                                    className="text-indigo-600 hover:text-indigo-700"
                                                >
                                                    <Copy className="h-4 w-4" />
                                                </button>
                                            </div>
                                        </div>
                                    </div>

                                    <button
                                        onClick={() => handleCheckStatus()}
                                        disabled={checkStatusLoading}
                                        className="w-full bg-indigo-600 text-white py-3 md:py-4 rounded-xl font-bold text-base md:text-lg hover:bg-indigo-700 transition-colors flex items-center justify-center gap-2 shadow-lg shadow-indigo-200"
                                    >
                                        {checkStatusLoading ? (
                                            <>
                                                <RefreshCw className="h-4 w-4 md:h-5 md:w-5 animate-spin" />
                                                Đang kiểm tra...
                                            </>
                                        ) : (
                                            "Đã chuyển khoản"
                                        )}
                                    </button>
                                    
                                    <p className="text-[10px] md:text-xs text-center text-slate-400">
                                        Hệ thống sẽ tự động cập nhật token sau khi nhận được thanh toán.
                                    </p>
                                </div>
                            </>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default Billing;
