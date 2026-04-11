import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiService } from '../services/api';
import { User } from '../types';

declare const __GOOGLE_CLIENT_ID__: string;

interface LoginProps {
  onLoginSuccess: (user: User, token: string) => void;
}

const Login: React.FC<LoginProps> = ({ onLoginSuccess }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState({ account: '', password: '' });
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    /* @ts-ignore */
    if (window.google) {
      /* @ts-ignore */
      window.google.accounts.id.initialize({
        client_id: __GOOGLE_CLIENT_ID__,
        callback: handleGoogleResponse
      });
      /* @ts-ignore */
      window.google.accounts.id.renderButton(
        document.getElementById("googleBtn"),
        { theme: "outline", size: "large", shape: "pill", width: 320 }
      );
    }
  }, []);

  const handleGoogleResponse = async (response: any) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await apiService.loginWithGoogle(response.credential);
      onLoginSuccess(data.user, data.access_token);
    } catch (err: any) {
      setError(err.message || "Google login failed");
    } finally {
      setIsLoading(false);
    }
  };

  const startHybridGoogleLogin = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const sessionId = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
      
      // 1. Khởi tạo phiên chờ trên Backend
      await apiService.createLoginSession(sessionId);

      // 2. Gửi lệnh cho Flutter mở Chrome Custom Tab
      /* @ts-ignore */
      if (window.FlutterBridge) {
        /* @ts-ignore */
        window.FlutterBridge.postMessage(`GOOGLE_LOGIN:${sessionId}`);
      } else {
        throw new Error("Không tìm thấy môi trường ứng dụng di động.");
      }

      // 3. Bắt đầu Polling
      const pollInterval = setInterval(async () => {
        try {
          const data = await apiService.checkLoginSession(sessionId);
          if (data.status === 'completed' && data.access_token) {
            clearInterval(pollInterval);
            onLoginSuccess(data.user, data.access_token);
          }
        } catch (err) {
          console.error("Polling error:", err);
        }
      }, 2000);

      // Timeout sau 5 phút
      setTimeout(() => clearInterval(pollInterval), 5 * 60 * 1000);

    } catch (err: any) {
      setError(err.message || "Hybrid login failed");
      setIsLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    try {
      const data = await apiService.login(formData);
      onLoginSuccess(data.user, data.access_token);
    } catch (err: any) {
      setError(err.message || "Đăng nhập thất bại");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#0f172a] p-6 bg-cover bg-center" style={{ backgroundImage: 'linear-gradient(rgba(15, 23, 42, 0.8), rgba(15, 23, 42, 0.9)), url("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2564&auto=format&fit=crop")' }}>
      <div className="w-full max-w-md animate-in fade-in zoom-in duration-500">
        <div className="bg-white rounded-[2.5rem] shadow-2xl overflow-hidden relative">
          <button 
            onClick={() => navigate('/')} 
            className="absolute top-6 right-6 p-2 rounded-full bg-slate-50 text-slate-400 hover:text-slate-600 transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
          </button>

          <div className="p-10 md:p-12">
            <div className="flex flex-col items-center mb-8">
              <div className="mb-4">
                <img src="/logo.png" alt="Logo" className="h-16 w-16 object-contain" />
              </div>
              <h1 className="text-2xl font-bold text-[#1e293b] mb-1">Đăng nhập</h1>
              <p className="text-slate-500 text-center text-sm">
                Dùng tài khoản của bạn để tạo banner AI ngay
              </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4 mb-6">
              <div>
                <input
                  type="text"
                  placeholder="Tên đăng nhập hoặc Email"
                  className="w-full px-5 py-4 bg-slate-50 border border-slate-100 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all text-slate-700"
                  value={formData.account}
                  onChange={(e) => setFormData({ ...formData, account: e.target.value })}
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
              
              <div className="flex justify-end">
                <button 
                  type="button"
                  onClick={() => navigate('/forgot-password')} 
                  className="text-xs font-semibold text-indigo-600 hover:text-indigo-700"
                >
                  Quên mật khẩu?
                </button>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full py-4 bg-indigo-600 hover:bg-slate-900 text-white font-bold rounded-2xl transition-all shadow-lg shadow-indigo-200 disabled:opacity-50"
              >
                {isLoading ? "Đang xử lý..." : "Đăng nhập"}
              </button>
            </form>

            <div className="relative mb-6">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-slate-100"></div>
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-white px-3 text-slate-400 font-medium">Hoặc</span>
              </div>
            </div>

            <div className="flex justify-center mb-8">
              {/* @ts-ignore */}
              {window.FlutterBridge ? (
                <button
                  onClick={startHybridGoogleLogin}
                  disabled={isLoading}
                  className="w-full flex items-center justify-center gap-3 py-4 bg-white border border-slate-200 rounded-2xl hover:bg-slate-50 transition-all text-slate-700 font-semibold shadow-sm"
                >
                  <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" alt="Google" className="w-5 h-5" />
                  {isLoading ? "Đang chờ đăng nhập..." : "Tiếp tục với Google"}
                </button>
              ) : (
                <div id="googleBtn" className="w-full flex justify-center"></div>
              )}
            </div>

            {error && (
              <div className="mb-6 text-red-500 text-sm bg-red-50 p-3 rounded-xl border border-red-100 text-center">
                {error}
              </div>
            )}

            <div className="text-center">
              <p className="text-slate-500 text-sm">
                Chưa có tài khoản?{" "}
                <button 
                  onClick={() => navigate('/register')}
                  className="font-bold text-indigo-600 hover:underline"
                >
                  Đăng ký ngay
                </button>
              </p>
            </div>

            <div className="mt-10 pt-6 border-t border-slate-50 text-center">
              <p className="text-[10px] text-slate-400 uppercase tracking-[0.2em] font-bold mb-1">
                ZEPHYR · MST 1801526082
              </p>
              <p className="text-[10px] text-slate-400">
                Bảo mật thông tin theo chính sách Google OAuth 2.0
              </p>
            </div>
          </div>
        </div>
        
        <p className="mt-8 text-center text-slate-500 text-[10px] uppercase tracking-widest opacity-60">
          © {new Date().getFullYear()} Adhightech Ltd. Co. - AutoBanner.
        </p>
      </div>
    </div>
  );
};

export default Login;
