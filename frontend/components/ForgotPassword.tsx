import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiService } from '../services/api';
import { toast } from 'react-hot-toast';

const ForgotPassword: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [account, setAccount] = useState('');
  const [isSuccess, setIsSuccess] = useState(false);
  const [mockLink, setMockLink] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    try {
      const resp = await apiService.forgotPassword(account);
      setIsSuccess(true);
      if (resp.mock_link) {
          setMockLink(resp.mock_link);
      }
      toast.success("Yêu cầu thành công!");
    } catch (err: any) {
      setError(err.message || "Gửi yêu cầu thất bại");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#0f172a] p-6 bg-cover bg-center" style={{ backgroundImage: 'linear-gradient(rgba(15, 23, 42, 0.8), rgba(15, 23, 42, 0.9)), url("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2564&auto=format&fit=crop")' }}>
      <div className="w-full max-w-md animate-in fade-in zoom-in duration-500">
        <div className="bg-white rounded-[2.5rem] shadow-2xl overflow-hidden relative">
          <button 
            onClick={() => navigate('/login')} 
            className="absolute top-6 right-6 p-2 rounded-full bg-slate-50 text-slate-400 hover:text-slate-600 transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m15 18-6-6 6-6"/></svg>
          </button>

          <div className="p-10 md:p-12">
            {!isSuccess ? (
              <>
                <div className="flex flex-col items-center mb-8">
                  <div className="mb-4">
                    <img src="/logo.png" alt="Logo" className="h-16 w-16 object-contain" />
                  </div>
                  <h1 className="text-2xl font-bold text-[#1e293b] mb-1">Quên mật khẩu?</h1>
                  <p className="text-slate-500 text-center text-sm">
                    Nhập tên đăng nhập hoặc email để nhận link khôi phục (Tối đa 2 lần/ngày)
                  </p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-6 mb-6">
                  <div>
                    <input
                      type="text"
                      placeholder="Username hoặc Email"
                      className="w-full px-5 py-4 bg-slate-50 border border-slate-100 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all text-slate-700"
                      value={account}
                      onChange={(e) => setAccount(e.target.value)}
                      required
                    />
                  </div>

                  <button
                    type="submit"
                    disabled={isLoading}
                    className="w-full py-4 bg-indigo-600 hover:bg-slate-900 text-white font-bold rounded-2xl transition-all shadow-lg shadow-indigo-200 disabled:opacity-50"
                  >
                    {isLoading ? "Đang xử lý..." : "Gửi yêu cầu"}
                  </button>
                </form>

                {error && (
                  <div className="text-red-500 text-sm bg-red-50 p-3 rounded-xl border border-red-100 text-center">
                    {error}
                  </div>
                )}
              </>
            ) : (
              <div className="text-center py-4">
                <div className="w-20 h-20 bg-green-50 rounded-full flex items-center justify-center mx-auto mb-6">
                  <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#10b981" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                </div>
                <h1 className="text-2xl font-bold text-[#1e293b] mb-4">Gửi thành công!</h1>
                <p className="text-slate-500 mb-8">
                  Chúng tôi đã gửi hướng dẫn khôi phục mật khẩu vào email của bạn.
                </p>
                
                {mockLink && (
                    <div className="p-4 bg-amber-50 rounded-2xl border border-amber-100 text-amber-800 text-xs mb-8">
                        <p className="font-bold mb-1">[MOCK MODE]</p>
                        <p className="mb-2">Vì chưa có SMTP, bạn có thể click vào link giả lập bên dưới:</p>
                        <button 
                            onClick={() => navigate(mockLink)}
                            className="text-indigo-600 font-bold underline"
                        >
                            Khôi phục mật khẩu ngay
                        </button>
                    </div>
                )}

                <button
                  onClick={() => navigate('/login')}
                  className="w-full py-4 bg-slate-900 text-white font-bold rounded-2xl transition-all"
                >
                  Quay lại đăng nhập
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ForgotPassword;
