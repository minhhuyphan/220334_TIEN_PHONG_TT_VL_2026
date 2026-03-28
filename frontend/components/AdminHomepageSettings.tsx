import React, { useState, useEffect } from 'react';
import { Save, Eye, EyeOff, CheckCircle } from 'lucide-react';
import toast from 'react-hot-toast';

const defaultHomeConfig = {
  hero: {
    visible: true,
    title: "Biến cảm hứng thành nghệ thuật trên Zephyr",
    title_color: "#ffffff",
    subtitle: "[ CÔNG NGHỆ KỸ THUẬT AI TIÊN TIẾN ]",
    subtitle_color: "#e2e8f0",
    btn_primary: "Tạo banner ngay",
    btn_primary_color: "#ffffff",
    btn_secondary: "Xem Gallery ↓",
    btn_secondary_color: "#ffffff"
  },
  features: {
    visible: true,
    subtitle: "TÍNH NĂNG NỔI BẬT",
    subtitle_color: "#7C3AED",
    title: "Hiện thực hóa tác phẩm trong mơ của bạn bằng AI",
    title_color: "#1e1b4b",
    desc: "Nền tảng công nghệ kỹ thuật tiên phong hàng đầu dành cho doanh nghiệp Việt Nam",
    desc_color: "#6b7280"
  },
  workflow: {
    visible: true,
    subtitle: "ĐƠN GIẢN",
    subtitle_color: "#7C3AED",
    title: "Chỉ 3 bước để có banner hoàn hảo",
    title_color: "#1e1b4b",
    desc: "Từ ý tưởng đến banner chuyên nghiệp — nhanh chóng, không cần kỹ năng thiết kế.",
    desc_color: "#6b7280"
  },
  gallery: {
    visible: true,
    subtitle: "CỘNG ĐỒNG SÁNG TẠO",
    subtitle_color: "#7C3AED",
    title: "Tìm cảm hứng của bạn trong vô vàn ý tưởng sáng tạo",
    title_color: "#1e1b4b",
    desc: "Khám phá những banner được tạo bởi cộng đồng người dùng Zephyr.",
    desc_color: "#6b7280"
  },
  about: {
    visible: true,
    subtitle: "VỀ CHÚNG TÔI",
    subtitle_color: "#e2e8f0",
    title: "Zephyr, bộ công cụ công nghệ AI toàn diện",
    title_color: "#ffffff",
    desc: "CÔNG TY TNHH MỘT THÀNH VIÊN CÔNG NGHỆ KỸ THUẬT TIÊN PHONG — chuyên cung cấp giải pháp công nghệ kỹ thuật cao và xuất nhập khẩu các mặt hàng công nghệ tiên tiến.",
    desc_color: "#e2e8f0",
    company_info: "MST: 1801526082 · Người đại diện: NGÔ HỒ ANH KHÔI\nP16, Đường số 8, KDC lô 49, Khu đô thị Nam Cần Thơ, Phường Cái Răng, TP. Cần Thơ\n0916 416 409 · Hoạt động từ 05/04/2017",
    company_info_color: "#9ca3af"
  }
};



const SectionEditor = ({ sectionKey, label, description, fields, config, updateSection }: any) => {
  const sectionData = config[sectionKey];
  if (!sectionData) return null;

  return (
    <div className="bg-white border rounded-xl shadow-sm mb-6 overflow-hidden">
      <div className="bg-slate-50 px-6 py-4 border-b flex justify-between items-center">
        <div>
          <h3 className="font-bold text-slate-800 text-lg">{label}</h3>
          <p className="text-xs text-slate-500">{description}</p>
        </div>
        <button
          onClick={() => updateSection(sectionKey, 'visible', !sectionData.visible)}
          className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
            sectionData.visible 
              ? 'bg-indigo-50 text-indigo-700 hover:bg-indigo-100' 
              : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
          }`}
        >
          {sectionData.visible ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
          {sectionData.visible ? 'Đang hiện' : 'Đang ẩn'}
        </button>
      </div>
        
        <div className={`p-6 space-y-4 ${!sectionData.visible ? 'opacity-50 pointer-events-none' : ''}`}>
          {fields.map((field: any) => {
             const rawValue = sectionData[field.key];
             const items = Array.isArray(rawValue) ? rawValue : [{ id: 'default', text: rawValue || '', color: sectionData[`${field.key}_color`] }];

             return (
               <div key={field.key} className="mb-4">
                 <div className="flex justify-between items-center mb-2">
                   <label className="text-sm font-semibold text-slate-700">{field.label}</label>
                   <button onClick={() => updateSection(sectionKey, field.key, [...items, { id: Date.now().toString(), text: '', color: items[0]?.color || '#000000' }])} className="text-xs font-medium text-indigo-600 bg-indigo-50 px-2 py-1 rounded hover:bg-indigo-100 transition-colors">+ Thêm dòng</button>
                 </div>
                 <div className="space-y-2">
                   {items.map((item: any) => (
                     <div key={item.id} className="flex gap-2 relative">
                        <input type="color" value={item.color || '#000000'} onChange={(e) => {
                           const newItems = items.map((i: any) => i.id === item.id ? { ...i, color: e.target.value } : i);
                           updateSection(sectionKey, field.key, newItems);
                        }} className="w-10 h-10 p-1 border rounded-lg cursor-pointer flex-shrink-0" title="Chọn màu chữ" />
                        {field.type === 'textarea' ? (
                          <textarea value={item.text} onChange={(e) => {
                             const newItems = items.map((i: any) => i.id === item.id ? { ...i, text: e.target.value } : i);
                             updateSection(sectionKey, field.key, newItems);
                          }} className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none resize-y min-h-[100px]" placeholder="Nhập nội dung..." />
                        ) : (
                          <input type="text" value={item.text} onChange={(e) => {
                             const newItems = items.map((i: any) => i.id === item.id ? { ...i, text: e.target.value } : i);
                             updateSection(sectionKey, field.key, newItems);
                          }} className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none" placeholder="Nhập nội dung..." />
                        )}
                        <button onClick={() => {
                           const newItems = items.filter((i: any) => i.id !== item.id);
                           updateSection(sectionKey, field.key, newItems);
                        }} className="w-10 h-10 flex items-center justify-center text-red-500 bg-red-50 hover:bg-red-100 rounded-lg flex-shrink-0 transition-colors" title="Xóa dòng này">
                          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
                        </button>
                     </div>
                   ))}
                   {items.length === 0 && (
                     <p className="text-xs text-slate-400 italic px-2">Đã xóa dữ liệu hiển thị. Bấm "+ Thêm dòng" để tạo nội dung mới nếu cần thiết.</p>
                   )}
                 </div>
               </div>
             );
          })}
        </div>
      </div>
    );
};

export default function AdminHomepageSettings() {
  const [config, setConfig] = useState<any>(defaultHomeConfig);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    fetchConfig();
  }, []);

  const fetchConfig = async () => {
    try {
      const response = await fetch(`${__API_URL__}/config/homepage`);
      if (response.ok) {
        const data = await response.json();
        if (Object.keys(data).length > 0) {
          setConfig({ ...defaultHomeConfig, ...data });
        }
      }
    } catch (error) {
      console.error('Failed to load homepage config:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSave = async () => {
    setIsSaving(true);
    try {
      const token = localStorage.getItem(__TOKEN_KEY__);
      const response = await fetch(`${__API_URL__}/admin/config/homepage`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(config)
      });
      
      if (response.ok) {
        toast.success("Đã lưu cấu hình Trang chủ!");
      } else {
        toast.error("Lỗi khi lưu cấu hình.");
      }
    } catch (error) {
      toast.error("Không thể kết nối tới server.");
    } finally {
      setIsSaving(false);
    }
  };

  const updateSection = (section: string, key: string, value: any) => {
    setConfig((prev: any) => ({
      ...prev,
      [section]: {
        ...prev[section],
        [key]: value
      }
    }));
  };

  if (isLoading) return <div className="p-8 text-center text-slate-500">Đang tải cấu hình...</div>;

  return (
    <div className="max-w-4xl mx-auto space-y-2">
      <div className="flex justify-between items-end mb-6">
        <div>
          <h2 className="text-2xl font-bold text-slate-800 flex items-center gap-2">
            Cấu hình Giao diện Trang chủ
          </h2>
          <p className="text-slate-500 text-sm mt-1">
            Điều chỉnh nội dung chữ hoặc ẩn/hiện các phần hiển thị bên ngoài Trang chủ
          </p>
        </div>
        <button
          onClick={handleSave}
          disabled={isSaving}
          className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2.5 rounded-lg font-bold shadow-sm transition-colors disabled:opacity-50"
        >
          {isSaving ? (
            <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
          ) : (
            <Save className="w-5 h-5" />
          )}
          Lưu Giao Diện
        </button>
      </div>

      <SectionEditor
        config={config}
        updateSection={updateSection}
        sectionKey="hero"
        label="Phần Đầu Trang (Hero)"
        description="Thay đổi lời mời gọi trên cùng của trang web."
        fields={[
          { key: 'subtitle', label: 'Tiêu đề phụ nhỏ (phía trên cùng)' },
          { key: 'title', label: 'Tiêu đề chính to' },
          { key: 'btn_primary', label: 'Nút hành động chính yếu' },
          { key: 'btn_secondary', label: 'Nút hành động thứ hai' }
        ]}
      />

      <SectionEditor
        config={config}
        updateSection={updateSection}
        sectionKey="features"
        label="Phần Tính Năng Nổi Bật"
        description="Giới thiệu nhanh lý do chọn nền tảng."
        fields={[
          { key: 'subtitle', label: 'Tiêu đề phụ nhỏ' },
          { key: 'title', label: 'Tiêu đề chính to' },
          { key: 'desc', label: 'Mô tả ngắn' }
        ]}
      />

      <SectionEditor
        config={config}
        updateSection={updateSection}
        sectionKey="workflow"
        label="Phần Hướng Dẫn Kéo Thả (Chỉ 3 bước)"
        description="Giải thích nhanh cách hệ thống hoạt động."
        fields={[
          { key: 'subtitle', label: 'Tiêu đề phụ nhỏ' },
          { key: 'title', label: 'Tiêu đề chính to' },
          { key: 'desc', label: 'Mô tả ngắn' }
        ]}
      />

      <SectionEditor
        config={config}
        updateSection={updateSection}
        sectionKey="gallery"
        label="Phần Thư Viện Nổi Bật (Community Gallery)"
        description="Khoe những tác phẩm xuất sắc nhất."
        fields={[
          { key: 'subtitle', label: 'Tiêu đề phụ nhỏ' },
          { key: 'title', label: 'Tiêu đề chính to' },
          { key: 'desc', label: 'Mô tả ngắn' }
        ]}
      />

      <SectionEditor
        config={config}
        updateSection={updateSection}
        sectionKey="about"
        label="Phần Chân Trang & Về Chúng Tôi (Footer)"
        description="Thông tin liên hệ cuối website."
        fields={[
          { key: 'subtitle', label: 'Tiêu đề phụ nhỏ' },
          { key: 'title', label: 'Tiêu đề chính to' },
          { key: 'desc', label: 'Giới thiệu công ty' },
          { key: 'company_info', label: 'Mã số thuế & Địa chỉ công ty', type: 'textarea' }
        ]}
      />
      
      <div className="pb-12 text-center mt-6">
        <button
          onClick={handleSave}
          disabled={isSaving}
          className="bg-slate-900 hover:bg-black text-white px-8 py-3 rounded-full font-bold shadow-lg transition-transform active:scale-95"
        >
          {isSaving ? "Đang lưu..." : "Lưu Toàn Bộ Thay Đổi Trang Chủ"}
        </button>
      </div>
    </div>
  );
}
