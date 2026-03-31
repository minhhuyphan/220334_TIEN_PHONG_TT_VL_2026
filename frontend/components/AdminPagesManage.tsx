import React, { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, Eye, EyeOff, Save, X, Globe, FileUp } from 'lucide-react';
import toast from 'react-hot-toast';

interface Page {
  slug: string;
  title: string;
  content: string;
  is_published: number | boolean;
  created_at?: string;
  updated_at?: string;
}

export default function AdminPagesManage() {
  const [pages, setPages] = useState<Page[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  
  const [formData, setFormData] = useState<Page>({
    slug: '',
    title: '',
    content: '',
    is_published: true
  });
  const [originalSlug, setOriginalSlug] = useState('');

  useEffect(() => {
    fetchPages();
  }, []);

  const fetchPages = async () => {
    setIsLoading(true);
    try {
      const token = localStorage.getItem(__TOKEN_KEY__);
      const res = await fetch(`${__API_URL__}/pages/admin/all`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (res.ok) {
        const data = await res.json();
        setPages(data);
      }
    } catch (e) {
      toast.error('Lỗi khi tải danh sách trang');
    } finally {
      setIsLoading(false);
    }
  };

  const handleEdit = (page?: Page) => {
    if (page) {
      setOriginalSlug(page.slug);
      setFormData({
        slug: page.slug,
        title: page.title,
        content: page.content,
        is_published: page.is_published === 1 || page.is_published === true
      });
    } else {
      setOriginalSlug('');
      setFormData({
        slug: '',
        title: '',
        content: '',
        is_published: true
      });
    }
    setIsEditing(true);
  };

  const handleDelete = async (slug: string) => {
    if (!confirm(`Bạn chắc chắn muốn xoá trang "${slug}"?`)) return;
    try {
      const token = localStorage.getItem(__TOKEN_KEY__);
      const res = await fetch(`${__API_URL__}/pages/admin/${slug}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        toast.success('Đã xoá trang');
        fetchPages();
      } else {
        toast.error('Xoá nội dung thất bại');
      }
    } catch (e) {
      toast.error('Lỗi hệ thống');
    }
  };

  const handleSave = async () => {
    if (!formData.slug.trim() || !formData.title.trim()) {
      toast.error('Vui lòng nhập đường dẫn và tiêu đề');
      return;
    }
    
    // Auto format slug (url-friendly)
    const formattedSlug = formData.slug.trim().toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');
    
    try {
      const token = localStorage.getItem(__TOKEN_KEY__);
      const isCreate = !originalSlug;
      const url = isCreate 
        ? `${__API_URL__}/pages/admin/create` 
        : `${__API_URL__}/pages/admin/${originalSlug}`;
        
      const payload = {
        ...formData,
        slug: formattedSlug,
        is_published: formData.is_published
      };

      const res = await fetch(url, {
        method: isCreate ? 'POST' : 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        toast.success(isCreate ? 'Đã tạo trang mới' : 'Đã cập nhật trang');
        setIsEditing(false);
        fetchPages();
      } else {
        const error = await res.json();
        toast.error(error.detail || 'Lưu thất bại');
      }
    } catch (e) {
      toast.error('Lỗi kết nối máy chủ');
    }
  };

  const togglePublish = async (slug: string, currentStatus: any, title: string, content: string) => {
     try {
       const token = localStorage.getItem(__TOKEN_KEY__);
       const newStatus = !(currentStatus === 1 || currentStatus === true);
       const res = await fetch(`${__API_URL__}/pages/admin/${slug}`, {
         method: 'PUT',
         headers: {
           'Authorization': `Bearer ${token}`,
           'Content-Type': 'application/json'
         },
         body: JSON.stringify({ slug, title, content, is_published: newStatus })
       });
       if (res.ok) {
         toast.success(newStatus ? 'Đã hiện trang' : 'Đã ẩn trang');
         fetchPages();
       }
     } catch (e) {
       toast.error("Lỗi khi thay đổi trạng thái");
     }
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.name.toLowerCase().endsWith('.html')) {
      toast.error('Chỉ hỗ trợ tải lên tệp .html');
      return;
    }

    const reader = new FileReader();
    reader.onload = (event) => {
      const content = event.target?.result as string;
      setFormData(prev => ({ ...prev, content }));
      toast.success('Đã tải nội dung từ tệp HTML');
      // Reset input value so same file can be uploaded again if needed
      e.target.value = '';
    };
    reader.onerror = () => {
      toast.error('Lỗi khi đọc tệp');
    };
    reader.readAsText(file);
  };

  if (isEditing) {
    return (
      <div className="bg-white rounded-xl shadow-sm border p-6">
        <div className="flex justify-between items-center mb-6 border-b pb-4">
          <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">
            <Globe className="h-5 w-5 text-indigo-600" />
            {originalSlug ? 'Sửa trang' : 'Tạo trang mới'}
          </h2>
          <div className="flex gap-2">
            <button
              onClick={() => setIsEditing(false)}
              className="px-4 py-2 text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-lg font-medium transition-colors"
            >
              Hủy
            </button>
            <button
              onClick={handleSave}
              className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-medium transition-colors"
            >
              <Save className="h-4 w-4" />
              Lưu thay đổi
            </button>
          </div>
        </div>

        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-bold text-slate-700 mb-1">Đường dẫn URL (Slug)</label>
              <div className="flex items-center focus-within:ring-2 focus-within:ring-indigo-500 rounded-lg border overflow-hidden">
                <span className="bg-slate-50 text-slate-500 px-3 py-2 border-r text-sm">/page/</span>
                <input
                  type="text"
                  value={formData.slug}
                  onChange={(e) => setFormData({...formData, slug: e.target.value})}
                  className="w-full px-3 py-2 outline-none"
                  placeholder="thu-thuat, gioi-thieu..."
                />
              </div>
              <p className="text-xs text-slate-500 mt-1">Chỉ chứa chữ thường, số và dấu gạch ngang (-)</p>
            </div>
            
            <div>
              <label className="block text-sm font-bold text-slate-700 mb-1">Tiêu đề trang</label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) => setFormData({...formData, title: e.target.value})}
                className="w-full px-3 py-2 border rounded-lg outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="Nhập tiêu đề hiển thị..."
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-bold text-slate-700 mb-1 flex justify-between items-center">
              <div className="flex items-center gap-3">
                <span>Nội dung (Hỗ trợ HTML/Tuỳ biến)</span>
                <label className="flex items-center gap-1.5 px-2.5 py-1 bg-indigo-50 text-indigo-600 hover:bg-indigo-100 rounded-md cursor-pointer transition-colors text-xs font-bold border border-indigo-100">
                  <FileUp className="h-3.5 w-3.5" />
                  Tải file HTML
                  <input 
                    type="file" 
                    accept=".html" 
                    className="hidden" 
                    onChange={handleFileUpload}
                  />
                </label>
              </div>
              <div className="flex items-center gap-2">
                <label className="text-xs font-normal cursor-pointer flex items-center gap-1">
                  <input 
                    type="checkbox" 
                    checked={formData.is_published as boolean} 
                    onChange={(e) => setFormData({...formData, is_published: e.target.checked})}
                  />
                  Công khai ngay?
                </label>
              </div>
            </label>
            <textarea
              value={formData.content}
              onChange={(e) => setFormData({...formData, content: e.target.value})}
              className="w-full px-3 py-3 border rounded-lg outline-none focus:ring-2 focus:ring-indigo-500 min-h-[400px] font-mono text-sm"
              placeholder="<h1>Xin chào</h1> <p>Đây là nội dung trang mới của bạn...</p>"
            />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
      <div className="p-6 border-b border-slate-200 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">Quản lý Trang Nội Dung</h2>
          <p className="text-sm text-slate-500 mt-1">Tạo và chỉnh sửa các trang tuỳ biến như Giới thiệu, Chính sách, v.v.</p>
        </div>
        <button
          onClick={() => handleEdit()}
          className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-medium transition-colors"
        >
          <Plus className="h-4 w-4" />
          Tạo trang mới
        </button>
      </div>

      <div className="overflow-x-auto">
        {isLoading ? (
          <div className="p-12 text-center text-slate-500">Đang tải danh sách...</div>
        ) : pages.length === 0 ? (
          <div className="p-12 text-center flex flex-col items-center">
            <Globe className="h-12 w-12 text-slate-200 mb-3" />
            <p className="text-slate-500 font-medium">Chưa có trang phụ nào được tạo.</p>
            <p className="text-sm text-slate-400">Bấm "Tạo trang mới" để bắt đầu thiết kế nội dung.</p>
          </div>
        ) : (
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50 border-b border-slate-200 text-xs text-slate-500 uppercase">
                <th className="py-3 px-6 font-bold">Tiêu đề</th>
                <th className="py-3 px-6 font-bold">Đường dẫn (Slug)</th>
                <th className="py-3 px-6 font-bold">Trạng thái</th>
                <th className="py-3 px-6 font-bold text-right">Hành động</th>
              </tr>
            </thead>
            <tbody>
              {pages.map((page) => {
                const isPublished = page.is_published === 1 || page.is_published === true;
                return (
                  <tr key={page.slug} className="border-b border-slate-100 hover:bg-slate-50 transition-colors">
                    <td className="py-3 px-6 font-medium text-slate-800">{page.title}</td>
                    <td className="py-3 px-6">
                      <a href={`/page/${page.slug}`} target="_blank" rel="noreferrer" className="text-indigo-600 hover:underline font-mono text-sm">
                        /page/{page.slug}
                      </a>
                    </td>
                    <td className="py-3 px-6">
                      <button 
                        onClick={() => togglePublish(page.slug, page.is_published, page.title, page.content)}
                        className={`px-3 py-1 text-xs rounded-full font-bold flex items-center w-fit gap-1 transition-colors ${
                          isPublished ? 'bg-green-100 text-green-700 hover:bg-green-200' : 'bg-slate-100 text-slate-500 hover:bg-slate-200'
                        }`}
                      >
                        {isPublished ? <><Eye className="w-3 h-3" /> Công khai</> : <><EyeOff className="w-3 h-3" /> Đang ẩn</>}
                      </button>
                    </td>
                    <td className="py-3 px-6 text-right">
                      <div className="flex justify-end gap-2">
                        <button
                          onClick={() => handleEdit(page)}
                          className="p-1.5 text-blue-600 hover:bg-blue-50 rounded"
                          title="Chỉnh sửa nội dung"
                        >
                          <Edit className="h-4 w-4" />
                        </button>
                        <button
                          onClick={() => handleDelete(page.slug)}
                          className="p-1.5 text-red-600 hover:bg-red-50 rounded"
                          title="Xoá trang"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
