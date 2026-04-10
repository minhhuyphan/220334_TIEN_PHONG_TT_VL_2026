import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiService } from '../services/api';
import { toast } from 'react-hot-toast';

const Register: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState({
    full_name: '',
    username: '',
    email: '',
    password: '',
    confirm_password: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (formData.password !== formData.confirm_password) {
      setError("Mật khẩu xác nhận không khớp");
      return;
    }

    setIsLoading(true);
    setError(null);
    try {
      await apiService.register({
        full_name: formData.full_name,
        username: formData.username,
        email: formData.email,
        password: formData.password
      });
      toast.success("Đăng ký thành công! Hãy đăng nhập.");
      navigate('/login');
    } catch (err: any) {
      setError(err.message || "Đăng ký thất bại");
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
            <div className="flex flex-col items-center mb-8">
              <div className="mb-4">
                <img src="/logo.png" alt="Logo" className="h-16 w-16 object-contain" />
              </div>
              <h1 className="text-2xl font-bold text-[#1e293b] mb-1">Tạo tài khoản</h1>
              <p className="text-slate-500 text-center text-sm">
                Đăng ký để trải nghiệm công nghệ banner AI
              </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4 mb-6">
              <div>
                <input
                  type="text"
                  placeholder="Họ và tên"
                  className="w-full px-5 py-4 bg-slate-50 border border-slate-100 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all text-slate-700"
                  value={formData.full_name}
                  onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                  required
                />
              </div>
              <div>
                <input
                  type="text"
                  placeholder="Tên đăng nhập (Username)"
                  className="w-full px-5 py-4 bg-slate-50 border border-slate-100 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all text-slate-700"
                  value={formData.username}
                  onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                  required
                />
              </div>
              <div>
                <input
                  type="email"
                  placeholder="Email (Để khôi phục mật khẩu)"
                  className="w-full px-5 py-4 bg-slate-50 border border-slate-100 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all text-slate-700"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  required
                />
              </div>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  placeholder="Mật khẩu"
                  className="w-full px-5 py-4 bg-slate-50 border border-slate-100 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all text-slate-700"
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-indigo-600 transition-colors"
                >
                  {showPassword ? (
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9.88 9.88 3.62 3.62"/><path d="M2 2l20 20"/><path d="M10.37 4.37a9 9 0 0 1 8.87 5.25"/><path d="M16 4v1.5"/><path d="m15.5 15.5 1 1"/><path d="M22 12c-1.5 3-4.5 5-8 5-1.08 0-2.13-.19-3.1-.53"/><path d="M6.33 6.33Q4.17 7.96 2 12c1.5 3 4.5 5 8 5"/><path d="M8 8q.5-.5 1-1"/><path d="M14.12 14.12q-.5.5-1.12.88"/></svg>
                  ) : (
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>
                  )}
                </button>
              </div>
              <div className="relative">
                <input
                  type={showConfirmPassword ? "text" : "password"}
                  placeholder="Xác nhận mật khẩu"
                  className="w-full px-5 py-4 bg-slate-50 border border-slate-100 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all text-slate-700"
                  value={formData.confirm_password}
                  onChange={(e) => setFormData({ ...formData, confirm_password: e.target.value })}
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-indigo-600 transition-colors"
                >
                  {showConfirmPassword ? (
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9.88 9.88 3.62 3.62"/><path d="M2 2l20 20"/><path d="M10.37 4.37a9 9 0 0 1 8.87 5.25"/><path d="M16 4v1.5"/><path d="m15.5 15.5 1 1"/><path d="M22 12c-1.5 3-4.5 5-8 5-1.08 0-2.13-.19-3.1-.53"/><path d="M6.33 6.33Q4.17 7.96 2 12c1.5 3 4.5 5 8 5"/><path d="M8 8q.5-.5 1-1"/><path d="M14.12 14.12q-.5.5-1.12.88"/></svg>
                  ) : (
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>
                  )}
                </button>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full py-4 bg-indigo-600 hover:bg-slate-900 text-white font-bold rounded-2xl transition-all shadow-lg shadow-indigo-200 disabled:opacity-50"
              >
                {isLoading ? "Đang xử lý..." : "Đăng ký ngay"}
              </button>
            </form>

            {error && (
              <div className="mb-6 text-red-500 text-sm bg-red-50 p-3 rounded-xl border border-red-100 text-center">
                {error}
              </div>
            )}

            <div className="text-center">
              <p className="text-slate-500 text-sm">
                Đã có tài khoản?{" "}
                <button 
                  onClick={() => navigate('/login')}
                  className="font-bold text-indigo-600 hover:underline"
                >
                  Đăng nhập
                </button>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;
