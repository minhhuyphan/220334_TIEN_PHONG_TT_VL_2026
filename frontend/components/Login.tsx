import React, { useEffect, useState } from 'react';
import { apiService } from '../services/api';
import { User } from '../types';

declare const __GOOGLE_CLIENT_ID__: string;

interface LoginProps {
  onLoginSuccess: (user: User, token: string) => void;
}

const Login: React.FC<LoginProps> = ({ onLoginSuccess }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    /* @ts-ignore */
    if (window.google) {
      /* @ts-ignore */
      /* @ts-ignore */
      window.google.accounts.id.initialize({
        client_id: __GOOGLE_CLIENT_ID__,
        callback: handleGoogleResponse
      });
      /* @ts-ignore */
      window.google.accounts.id.renderButton(
        document.getElementById("googleBtn"),
        { theme: "outline", size: "large", shape: "pill" }
      );
    }
  }, []);

  const handleGoogleResponse = async (response: any) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await apiService.loginWithGoogle(response.credential);
      onLoginSuccess(data.user, data.access_token);
    } catch (err) {
      setError("Login failed. Please try again.");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };



  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 p-6">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-3xl shadow-xl shadow-slate-200/50 border border-slate-100 overflow-hidden">
          <div className="p-8 md:p-12">
            <div className="flex flex-col items-center mb-10">
              <div className="mb-6">
                <img src="/logo.png" alt="AutoBanner Logo" className="h-20 w-20 object-contain animate-in zoom-in duration-700" />
              </div>
              <h1 className="text-3xl font-extrabold text-slate-900 mb-2">AutoBanner</h1>
              <p className="text-slate-500 text-center text-sm">
                Đăng nhập để bắt đầu tạo banner chuyên nghiệp với trí tuệ nhân tạo
              </p>
            </div>

            <div className="space-y-6">
              <div id="googleBtn" className="w-full flex justify-center"></div>
              
              {error && (
                <div className="text-red-500 text-sm bg-red-50 p-3 rounded-xl border border-red-100 text-center animate-in fade-in slide-in-from-top-2">
                  {error}
                </div>
              )}
            </div>

            <div className="mt-12 pt-8 border-t border-slate-50 text-center">
              <p className="text-[10px] text-slate-400 uppercase tracking-widest font-bold mb-2">
                Trí Tuệ Nhân Tạo & Thiết Kế Hiện Đại
              </p>
              <a 
                href="#" 
                target="_blank" 
                rel="noreferrer"
                className="text-xs text-indigo-600 hover:text-indigo-700 font-medium transition-colors"
              >
                Fanpage: Adhightech Ltd. Co.
              </a>
            </div>
          </div>
        </div>
        
        <p className="mt-8 text-center text-slate-400 text-[10px] uppercase tracking-wider">
          © {new Date().getFullYear()} Adhightech Ltd. Co. - AutoBanner. Bảo lưu mọi quyền.
        </p>
      </div>
    </div>
  );
};

export default Login;
