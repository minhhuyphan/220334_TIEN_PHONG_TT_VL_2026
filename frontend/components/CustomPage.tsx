import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Header from './Header';

interface Page {
  slug: string;
  title: string;
  content: string;
  is_published: boolean;
  created_at: string;
  updated_at: string;
}

const CustomPage: React.FC<{ user: any, onNavigate: (path: string) => void }> = ({ user, onNavigate }) => {
  const { slug } = useParams<{ slug: string }>();
  const navigate = useNavigate();
  const [page, setPage] = useState<Page | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPage = async () => {
      setIsLoading(true);
      try {
        const response = await fetch(`${__API_URL__}/pages/${slug}`);
        if (!response.ok) {
          throw new Error('Page not found');
        }
        const data = await response.json();
        setPage(data);
        document.title = `${data.title} | Cổng Nội Dung`;
      } catch (err: any) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };
    
    if (slug) fetchPage();
  }, [slug]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-slate-50 flex flex-col">
        <Header user={user} onMenuClick={() => {}} hideMenuButton={true} />
        <div className="flex-1 flex justify-center items-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-indigo-600"></div>
        </div>
      </div>
    );
  }

  if (error || !page) {
    return (
      <div className="min-h-screen bg-slate-50 flex flex-col">
        <Header user={user} onMenuClick={() => {}} hideMenuButton={true} />
        <div className="flex-1 flex flex-col justify-center items-center p-6 text-center">
          <h1 className="text-6xl font-black text-slate-300 mb-4">404</h1>
          <h2 className="text-2xl font-bold text-slate-800 mb-2">Không tìm thấy nội dung</h2>
          <p className="text-slate-500 mb-6 max-w-md mx-auto">Trang bạn đang tìm kiếm có thể đã bị xóa, đổi tên hoặc tạm thời không thể truy cập.</p>
          <button 
            onClick={() => navigate('/')}
            className="px-6 py-3 bg-indigo-600 text-white rounded-xl font-bold"
          >
            Quay về Trang chủ
          </button>
        </div>
      </div>
    );
  }

  // Render the page
  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <Header user={user} onMenuClick={() => {}} hideMenuButton={true} />
      
      <main className="flex-1 max-w-4xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-12 md:py-20">
        <div className="bg-white rounded-3xl shadow-sm border border-slate-100 overflow-hidden">
          <div className="bg-slate-50 border-b border-slate-100 p-8 md:p-12 text-center">
             <h1 className="text-3xl md:text-5xl font-black text-slate-900 tracking-tight leading-tight mb-4">
               {page.title}
             </h1>
             <p className="text-slate-500 text-sm font-medium">
               Cập nhật lần cuối: {new Date(page.updated_at).toLocaleDateString('vi-VN')}
             </p>
          </div>
          
          <div className="p-8 md:p-12">
            <div 
              className="prose prose-slate prose-indigo max-w-none md:prose-lg custom-page-content"
              dangerouslySetInnerHTML={{ __html: page.content }}
            />
          </div>
        </div>
      </main>
      
      {/* Footer Minimalist */}
      <footer className="mt-auto py-8 bg-white border-t border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="flex items-center gap-2 text-slate-900 font-bold opacity-75">
            <span className="text-xl">⚡</span>
            <span>Zephyr</span>
          </div>
          <p className="text-slate-500 text-sm">© {new Date().getFullYear()} Zephyr. Đã đăng ký bản quyền.</p>
          <div className="flex gap-4 text-sm font-medium">
             <button onClick={() => navigate('/')} className="text-slate-600 hover:text-indigo-600 transition-colors">Trang chủ</button>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default CustomPage;
