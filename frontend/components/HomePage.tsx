import React, { useEffect, useState, useRef } from 'react';
import { apiService } from '../services/api';
import { PublicBannerItem, User } from '../types';

declare const __GOOGLE_CLIENT_ID__: string;

interface HomePageProps {
  onLoginSuccess: (user: User, token: string) => void;
  user?: User | null;
  onNavigate?: (route: string) => void;
}

const V = '#7C3AED';       // violet-700 — màu chính
const VL = '#8B5CF6';      // violet-500 — lighter accent
const BG = '#ffffff';      // nền trắng
const BG2 = '#f5f3ff';     // tím nhạt cho section xen kẽ
const TXT = '#1e1b4b';     // text tối (indigo-950)
const TXT2 = '#6b7280';    // text muted

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

const renderDynamic = (
  value: any, 
  defaultColor: string, 
  renderFn: (text: string, color: string, index: number) => React.ReactNode
) => {
  const items = Array.isArray(value) ? value : [{ id: 'default', text: value, color: value?.color || defaultColor }];
  return items.map((item, index) => {
    if (!item.text && item.text !== 0) return null; // hide if empty
    return <React.Fragment key={item.id}>{renderFn(String(item.text), item.color || defaultColor, index)}</React.Fragment>;
  });
};

const HomePage: React.FC<HomePageProps> = ({ onLoginSuccess, user, onNavigate }) => {
  const [config, setConfig] = useState<any>(defaultHomeConfig);
  const [publicPages, setPublicPages] = useState<any[]>([]);
  const [banners, setBanners] = useState<PublicBannerItem[]>([]);
  const [heroBanners, setHeroBanners] = useState<PublicBannerItem[]>([]);
  const [loadingBanners, setLoadingBanners] = useState(true);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [loginError, setLoginError] = useState<string | null>(null);
  const [loginLoading, setLoginLoading] = useState(false);
  const googleBtnRef = useRef<HTMLDivElement>(null);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const link = document.createElement('link');
    link.href = 'https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;900&family=Inter:wght@300;400;500;600;700&display=swap';
    link.rel = 'stylesheet';
    document.head.appendChild(link);
    const handleScroll = () => setScrolled(window.scrollY > 50);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    fetch(`${__API_URL__}/config/homepage`)
      .then(res => res.json())
      .then(data => {
         if (Object.keys(data).length > 0) setConfig({ ...defaultHomeConfig, ...data });
      })
      .catch((e) => console.log('Không tải được config trang chủ', e));

    fetch(`${__API_URL__}/pages`)
      .then(res => res.json())
      .then(data => setPublicPages(Array.isArray(data) ? data : []))
      .catch(e => console.error("Fetch pages error:", e));

    apiService.getPublicBanners(20).then(data => {
      setBanners(data);
      setLoadingBanners(false);
      // Lọc ảnh landscape (tỉ lệ >= 1.5) cho hero slideshow
      const landscapeItems: PublicBannerItem[] = [];
      let checked = 0;
      if (data.length === 0) return;
      data.forEach(item => {
        const img = new Image();
        img.onload = () => {
          if (img.naturalWidth / img.naturalHeight >= 1.5) {
            landscapeItems.push(item);
          }
          checked++;
          if (checked === data.length) {
            // Giữ thứ tự gốc
            const ordered = data.filter(b => landscapeItems.find(l => l.id === b.id));
            setHeroBanners(ordered.length > 0 ? ordered : data);
          }
        };
        img.onerror = () => {
          checked++;
          if (checked === data.length) {
            const ordered = data.filter(b => landscapeItems.find(l => l.id === b.id));
            setHeroBanners(ordered.length > 0 ? ordered : data);
          }
        };
        img.src = item.image_url;
      });
    });
  }, []);

  // Slideshow hero — CSS crossfade, chỉ đổi index mỗi 3 giây (chỉ dùng heroBanners)
  useEffect(() => {
    if (heroBanners.length <= 1) return;
    setCurrentIndex(0);
    const timer = setInterval(() => {
      setCurrentIndex(i => (i + 1) % heroBanners.length);
    }, 3000);
    return () => clearInterval(timer);
  }, [heroBanners.length]);

  useEffect(() => {
    if (!showLoginModal) return;
    const tryInit = () => {
      /* @ts-ignore */
      if (window.google && googleBtnRef.current) {
        /* @ts-ignore */
        window.google.accounts.id.initialize({ client_id: __GOOGLE_CLIENT_ID__, callback: handleGoogleResponse });
        /* @ts-ignore */
        window.google.accounts.id.renderButton(googleBtnRef.current, { theme: 'outline', size: 'large', shape: 'pill', width: 280 });
      } else { setTimeout(tryInit, 200); }
    };
    setTimeout(tryInit, 150);
  }, [showLoginModal]);

  const handleGoogleResponse = async (response: any) => {
    setLoginLoading(true); setLoginError(null);
    try {
      const data = await apiService.loginWithGoogle(response.credential);
      onLoginSuccess(data.user, data.access_token);
    } catch { setLoginError('Đăng nhập thất bại. Vui lòng thử lại.'); }
    finally { setLoginLoading(false); }
  };

  const features = [
    { tag: '01', icon: '✨', title: 'AI Tạo Banner Thông Minh', desc: 'Dùng mô hình AI tiên tiến nhất để tạo banner chất lượng cao chỉ trong vài giây từ mô tả văn bản.' },
    { tag: '02', icon: '⚡', title: 'Tốc Độ Nhanh Chóng', desc: 'Hệ thống xử lý nền, bạn có thể làm việc khác trong khi banner đang được tạo.' },
    { tag: '03', icon: '🎨', title: 'Tùy Chỉnh Linh Hoạt', desc: 'Chọn kích thước, tỉ lệ, phong cách. Thêm ảnh tham chiếu để AI hiểu đúng thương hiệu.' },
    { tag: '04', icon: '☁️', title: 'Lưu Trữ Đám Mây', desc: 'Tất cả banner được lưu vĩnh viễn trên Cloudinary. Không mất dữ liệu dù server restart.' },
  ];

  return (
    <div style={{ fontFamily: "'Inter', sans-serif", background: BG, color: TXT, minHeight: '100vh', overflowX: 'hidden' }}>

      {/* STYLE */}
      <style>{`
        @keyframes spin { to { transform: rotate(360deg); } }
        @keyframes bounce { 0%,100%{transform:translateY(0)}50%{transform:translateY(8px)} }
        @keyframes fadeUp { from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)} }
        @keyframes fadeInCard { from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)} }
        * { margin:0; padding:0; box-sizing:border-box; }
        .gallery-cols { columns:4; column-gap:14px; }
        @media(max-width:1100px){.gallery-cols{columns:3}}
        @media(max-width:720px){.gallery-cols{columns:2}}
        @media(max-width:480px){.gallery-cols{columns:1}}
        .nav-link:hover{color:#7C3AED!important}
        .feat-card:hover{background:#f5f3ff!important;border-color:rgba(124,58,237,0.3)!important;transform:translateY(-4px)}
        .btn-ghost:hover{background:rgba(124,58,237,0.08)!important;border-color:rgba(124,58,237,0.4)!important;color:#7C3AED!important}
        .btn-violet:hover{filter:brightness(1.08);box-shadow:0 8px 30px rgba(124,58,237,0.45)!important;transform:translateY(-1px)}
        .gallery-card:hover{box-shadow:0 12px 36px rgba(124,58,237,0.15)!important;transform:translateY(-4px)}
        .footer-link:hover{color:#7C3AED!important}
      `}</style>

      {/* NAVBAR */}
      <nav style={{
        position: 'fixed', top: 0, left: 0, right: 0, zIndex: 100,
        backdropFilter: 'blur(20px)', WebkitBackdropFilter: 'blur(20px)',
        background: scrolled ? 'rgba(255,255,255,0.95)' : 'rgba(255,255,255,0.1)',
        borderBottom: scrolled ? '1px solid rgba(124,58,237,0.12)' : '1px solid transparent',
        boxShadow: scrolled ? '0 2px 20px rgba(0,0,0,0.06)' : 'none',
        transition: 'all 0.4s ease', padding: '0 48px', height: '64px',
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <img src="/logo.png" alt="Zephyr" style={{ height: '30px', width: '30px', objectFit: 'contain' }} onError={(e) => { (e.target as HTMLImageElement).style.display = 'none'; }} />
          <span style={{ fontWeight: 700, fontSize: '18px', color: V, letterSpacing: '-0.3px' }}>Zephyr</span>
        </div>
        <div style={{ display: 'flex', gap: '32px' }}>
          {[['#features', 'Tính năng'], ['#gallery', 'Gallery'], ['#about', 'Về chúng tôi']].map(([href, label]) => (
            <a key={href} href={href} className="nav-link" style={{ color: TXT2, fontSize: '14px', fontWeight: 500, textDecoration: 'none', transition: 'color 0.2s' }}>{label}</a>
          ))}
        </div>
        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          {user ? (
            <button className="btn-violet" onClick={() => onNavigate && onNavigate('/dashboard')}
              style={{ background: `linear-gradient(135deg, ${V}, #6D28D9)`, color: '#fff', fontWeight: 700, fontSize: '14px', padding: '9px 22px', borderRadius: '24px', border: 'none', cursor: 'pointer', transition: 'all 0.25s', boxShadow: '0 4px 18px rgba(124,58,237,0.35)' }}
            >Bảng điều khiển</button>
          ) : (
            <>
              <button id="navbar-login-btn" onClick={() => setShowLoginModal(true)}
                style={{ color: TXT2, fontSize: '14px', fontWeight: 500, background: 'transparent', border: 'none', cursor: 'pointer', padding: '8px 14px', borderRadius: '24px', transition: 'all 0.2s' }}
                onMouseEnter={e => { (e.currentTarget as HTMLElement).style.color = V; }}
                onMouseLeave={e => { (e.currentTarget as HTMLElement).style.color = TXT2; }}
              >Đăng nhập</button>
              <button className="btn-violet" onClick={() => setShowLoginModal(true)}
                style={{ background: `linear-gradient(135deg, ${V}, #6D28D9)`, color: '#fff', fontWeight: 700, fontSize: '14px', padding: '9px 22px', borderRadius: '24px', border: 'none', cursor: 'pointer', transition: 'all 0.25s', boxShadow: '0 4px 18px rgba(124,58,237,0.35)' }}
              >Tạo ngay</button>
            </>
          )}
        </div>
      </nav>

      {/* HERO — full screen, ảnh thư viện đổi mỗi 2s */}
      {config.hero.visible && (
      <section style={{ height: '100vh', position: 'relative', display: 'flex', alignItems: 'flex-end', overflow: 'hidden' }}>
        {/* Stack chỉ ảnh landscape — CSS transition tự crossfade mượt mà */}
        {heroBanners.length > 0 ? heroBanners.map((b, i) => (
          <img
            key={b.id}
            src={b.image_url}
            alt="Zephyr Hero"
            onError={(e) => { (e.target as HTMLImageElement).style.display = 'none'; }}
            style={{
              position: 'absolute', inset: 0, width: '100%', height: '100%',
              objectFit: 'cover', objectPosition: 'center',
              opacity: i === currentIndex ? 1 : 0,
              transition: 'opacity 1.2s cubic-bezier(0.4,0,0.2,1)',
              zIndex: i === currentIndex ? 1 : 0,
              willChange: 'opacity',
            }}
          />
        )) : (
          <img src="/hero.png" alt="Zephyr Hero" style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover' }} />
        )}
        {/* Gradient overlay — dày hơn ở dưới để text dễ đọc */}
        <div style={{ position: 'absolute', inset: 0, zIndex: 5, background: 'linear-gradient(to right, rgba(15,10,30,0.88) 0%, rgba(15,10,30,0.3) 60%, transparent 100%)' }} />
        <div style={{ position: 'absolute', inset: 0, zIndex: 5, background: 'linear-gradient(to top, rgba(15,10,30,1) 0%, rgba(15,10,30,0.4) 40%, transparent 70%)' }} />

        <div style={{ position: 'relative', zIndex: 10, padding: '0 64px 80px', maxWidth: '750px', animation: 'fadeUp 1s ease both' }}>
          {renderDynamic(config.hero.subtitle, 'rgba(255,255,255,0.6)', (text, color) => (
            <span style={{ display: 'inline-block', marginBottom: '22px', fontSize: '11px', letterSpacing: '3px', color: color, textTransform: 'uppercase', border: '1px solid rgba(255,255,255,0.2)', padding: '5px 16px', borderRadius: '20px', background: 'rgba(124,58,237,0.15)' }}>
              {text}
            </span>
          ))}
          {renderDynamic(config.hero.title, '#fff', (text, color) => (
            <h1 
              style={{ fontFamily: "'Playfair Display', Georgia, serif", fontSize: 'clamp(40px, 5.5vw, 78px)', fontWeight: 700, lineHeight: 1.1, marginBottom: '30px', color: color }}
              dangerouslySetInnerHTML={{ __html: text.replace('Zephyr', `<span style="background: linear-gradient(135deg,#a78bfa,#7C3AED); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Zephyr</span>`).replace(/\n/g, '<br />') }}
            />
          ))}
          <div style={{ display: 'flex', gap: '14px', flexWrap: 'wrap' }}>
            {renderDynamic(config.hero.btn_primary, '#fff', (text, color) => (
              <button className="btn-violet" onClick={() => user ? (onNavigate && onNavigate('/generate')) : setShowLoginModal(true)}
                style={{ background: `linear-gradient(135deg, ${V}, #6D28D9)`, color: color, fontWeight: 700, fontSize: '16px', padding: '14px 34px', borderRadius: '32px', border: 'none', cursor: 'pointer', boxShadow: '0 8px 32px rgba(124,58,237,0.5)', transition: 'all 0.3s' }}
              >✦ {text}</button>
            ))}
            {renderDynamic(config.hero.btn_secondary, 'rgba(255,255,255,0.75)', (text, color) => (
              <a href="#gallery" className="btn-ghost"
                style={{ color: color, fontSize: '15px', textDecoration: 'none', padding: '14px 26px', borderRadius: '32px', border: '1px solid rgba(255,255,255,0.25)', transition: 'all 0.2s', display: 'flex', alignItems: 'center', backdropFilter: 'blur(8px)', background: 'rgba(255,255,255,0.08)' }}
              >{text}</a>
            ))}
          </div>
        </div>
        <div style={{ position: 'absolute', bottom: '28px', right: '48px', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '6px', color: 'rgba(255,255,255,0.4)', fontSize: '10px', letterSpacing: '2px', textTransform: 'uppercase', animation: 'bounce 2.5s infinite' }}>
          <span>Cuộn xuống</span>
          <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" /></svg>
        </div>
      </section>
      )}

      {/* FEATURES */}
      {config.features.visible && (
      <section id="features" style={{ padding: '120px 64px', background: BG }}>
        <div style={{ maxWidth: '1240px', margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: '72px' }}>
            {renderDynamic(config.features.subtitle, V, (text, color) => (
              <span style={{ fontSize: '12px', letterSpacing: '3px', color: color, textTransform: 'uppercase', display: 'block', marginBottom: '16px', fontWeight: 600 }}>✦ {text}</span>
            ))}
            {renderDynamic(config.features.title, TXT, (text, color) => (
              <h2 style={{ fontFamily: "'Playfair Display', Georgia, serif", fontSize: 'clamp(30px, 4vw, 52px)', fontWeight: 700, color: color, lineHeight: 1.2, marginBottom: '14px' }} dangerouslySetInnerHTML={{ __html: text.replace('bằng AI', `<span style="background: linear-gradient(135deg,${VL},${V}); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">bằng AI</span>`) }} />
            ))}
            {renderDynamic(config.features.desc, TXT2, (text, color) => (
              <p style={{ color: color, fontSize: '16px', maxWidth: '480px', margin: '0 auto', lineHeight: 1.7 }}>{text}</p>
            ))}
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(260px,1fr))', gap: '20px' }}>
            {features.map((f, i) => (
              <div key={i} className="feat-card" style={{ padding: '32px', borderRadius: '20px', background: '#fff', border: '1px solid rgba(124,58,237,0.1)', boxShadow: '0 2px 16px rgba(0,0,0,0.05)', transition: 'all 0.3s', cursor: 'default' }}>
                <span style={{ fontSize: '11px', color: V, letterSpacing: '2px', display: 'block', marginBottom: '18px', fontWeight: 600 }}>[{f.tag}]</span>
                <div style={{ fontSize: '34px', marginBottom: '14px' }}>{f.icon}</div>
                <h3 style={{ fontWeight: 700, fontSize: '17px', color: TXT, marginBottom: '10px' }}>{f.title}</h3>
                <p style={{ color: TXT2, fontSize: '14px', lineHeight: 1.75 }}>{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
      )}

      {/* HOW IT WORKS */}
      {config.workflow.visible && (
      <section style={{ padding: '100px 64px', background: BG2 }}>
        <div style={{ maxWidth: '1100px', margin: '0 auto', display: 'flex', alignItems: 'center', gap: '80px', flexWrap: 'wrap' }}>
          <div style={{ flex: '1', minWidth: '290px' }}>
            <div style={{ borderRadius: '24px', background: '#fff', border: '1px solid rgba(124,58,237,0.12)', padding: '36px', boxShadow: '0 4px 24px rgba(124,58,237,0.08)' }}>
              {[
                { step: '01', icon: '✍️', title: 'Mô tả ý tưởng', desc: 'Gõ mô tả bằng tiếng Việt hoặc tiếng Anh' },
                { step: '02', icon: '🤖', title: 'AI xử lý', desc: 'Hệ thống AI tạo ảnh chất lượng cao tự động' },
                { step: '03', icon: '📥', title: 'Tải về & dùng ngay', desc: 'Download banner độ phân giải cao' },
              ].map((item, i, arr) => (
                <div key={i} style={{ display: 'flex', gap: '18px', marginBottom: i < arr.length - 1 ? '26px' : 0, paddingBottom: i < arr.length - 1 ? '26px' : 0, borderBottom: i < arr.length - 1 ? '1px solid rgba(124,58,237,0.08)' : 'none' }}>
                  <div style={{ width: '46px', height: '46px', borderRadius: '14px', background: `linear-gradient(135deg,${VL},${V})`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '20px', flexShrink: 0 }}>{item.icon}</div>
                  <div>
                    <span style={{ fontSize: '10px', color: V, letterSpacing: '2px', display: 'block', marginBottom: '4px', fontWeight: 600 }}>{item.step}</span>
                    <h4 style={{ fontWeight: 700, color: TXT, fontSize: '15px', marginBottom: '4px' }}>{item.title}</h4>
                    <p style={{ color: TXT2, fontSize: '13px' }}>{item.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
          <div style={{ flex: '1', minWidth: '290px' }}>
            {renderDynamic(config.workflow.subtitle, V, (text, color) => (
              <span style={{ fontSize: '12px', letterSpacing: '3px', color: color, textTransform: 'uppercase', display: 'block', marginBottom: '20px', fontWeight: 600 }}>✦ {text}</span>
            ))}
            {renderDynamic(config.workflow.title, TXT, (text, color) => (
              <h2 style={{ fontFamily: "'Playfair Display', Georgia, serif", fontSize: 'clamp(28px,3.5vw,46px)', fontWeight: 700, color: color, lineHeight: 1.2, marginBottom: '18px' }} dangerouslySetInnerHTML={{ __html: text.replace('3 bước', `<span style="color: ${V}">3 bước</span>`) }} />
            ))}
            {renderDynamic(config.workflow.desc, TXT2, (text, color) => (
              <p style={{ color: color, fontSize: '16px', lineHeight: 1.8, marginBottom: '34px' }}>{text}</p>
            ))}
            {user ? (
              <button className="btn-ghost" onClick={() => onNavigate && onNavigate('/generate')}
                style={{ background: 'transparent', color: V, fontWeight: 600, fontSize: '15px', padding: '13px 28px', borderRadius: '28px', border: `1.5px solid ${V}`, cursor: 'pointer', transition: 'all 0.2s' }}
              >✦ Thử công cụ ngay →</button>
            ) : (
              <button className="btn-ghost" onClick={() => setShowLoginModal(true)}
                style={{ background: 'transparent', color: V, fontWeight: 600, fontSize: '15px', padding: '13px 28px', borderRadius: '28px', border: `1.5px solid ${V}`, cursor: 'pointer', transition: 'all 0.2s' }}
              >✦ Dùng thử miễn phí →</button>
            )}
          </div>
        </div>
      </section>
      )}

      {/* GALLERY */}
      {config.gallery.visible && (
      <section id="gallery" style={{ padding: '120px 64px', background: BG }}>
        <div style={{ maxWidth: '1280px', margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: '56px' }}>
            {renderDynamic(config.gallery.subtitle, V, (text, color) => (
              <span style={{ fontSize: '12px', letterSpacing: '3px', color: color, textTransform: 'uppercase', display: 'block', marginBottom: '16px', fontWeight: 600 }}>✦ {text}</span>
            ))}
            {renderDynamic(config.gallery.title, TXT, (text, color) => (
              <h2 style={{ fontFamily: "'Playfair Display', Georgia, serif", fontSize: 'clamp(28px,4vw,52px)', fontWeight: 700, color: color, marginBottom: '14px' }}>
                {text}
              </h2>
            ))}
            {renderDynamic(config.gallery.desc, TXT2, (text, color) => (
              <p style={{ color: color, maxWidth: '440px', margin: '0 auto', lineHeight: 1.7 }}>{text}</p>
            ))}
          </div>
          {loadingBanners ? (
            <div style={{ display: 'flex', justifyContent: 'center', padding: '80px 0' }}>
              <div style={{ width: '40px', height: '40px', border: `2px solid rgba(124,58,237,0.15)`, borderTopColor: V, borderRadius: '50%', animation: 'spin 1s linear infinite' }} />
            </div>
          ) : banners.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '80px 0' }}>
              <div style={{ fontSize: '52px', marginBottom: '16px' }}>🎨</div>
              <p style={{ color: TXT2, fontSize: '18px', marginBottom: '8px' }}>Chưa có banner nào</p>
              <p style={{ color: TXT2, fontSize: '14px', marginBottom: '28px', opacity: 0.7 }}>Hãy là người đầu tiên tạo và chia sẻ banner!</p>
              {user ? (
                <button className="btn-violet" onClick={() => onNavigate && onNavigate('/generate')}
                  style={{ background: `linear-gradient(135deg,${V},#6D28D9)`, color: '#fff', fontWeight: 700, padding: '12px 28px', borderRadius: '24px', border: 'none', cursor: 'pointer', transition: 'all 0.25s', boxShadow: '0 4px 20px rgba(124,58,237,0.35)' }}
                >✦ Tạo banner ngay</button>
              ) : (
                <button className="btn-violet" onClick={() => setShowLoginModal(true)}
                  style={{ background: `linear-gradient(135deg,${V},#6D28D9)`, color: '#fff', fontWeight: 700, padding: '12px 28px', borderRadius: '24px', border: 'none', cursor: 'pointer', transition: 'all 0.25s', boxShadow: '0 4px 20px rgba(124,58,237,0.35)' }}
                >✦ Đăng nhập & Tạo ảnh</button>
              )}
            </div>
          ) : (
            <div className="gallery-cols">
              {banners.map((banner, i) => <GalleryCard key={banner.id} banner={banner} index={i} />)}
            </div>
          )}
          <div style={{ textAlign: 'center', marginTop: '48px' }}>
            {user ? (
              <button className="btn-ghost" onClick={() => onNavigate && onNavigate('/generate')}
                style={{ background: 'transparent', color: V, fontWeight: 600, fontSize: '15px', padding: '13px 32px', borderRadius: '32px', border: `1.5px solid ${V}`, cursor: 'pointer', transition: 'all 0.2s' }}
              >✦ Thoả mãn đam mê sáng tạo →</button>
            ) : (
              <button className="btn-ghost" onClick={() => setShowLoginModal(true)}
                style={{ background: 'transparent', color: V, fontWeight: 600, fontSize: '15px', padding: '13px 32px', borderRadius: '32px', border: `1.5px solid ${V}`, cursor: 'pointer', transition: 'all 0.2s' }}
              >✦ Tham gia cùng chúng tôi →</button>
            )}
          </div>
        </div>
      </section>
      )}

      {/* ABOUT / CTA */}
      {config.about.visible && (
      <section id="about" style={{ padding: '120px 64px', background: `linear-gradient(135deg, ${V} 0%, #6D28D9 50%, #4C1D95 100%)`, textAlign: 'center' }}>
        <div style={{ maxWidth: '780px', margin: '0 auto' }}>
          {renderDynamic(config.about.subtitle, 'rgba(255,255,255,0.7)', (text, color) => (
            <span style={{ fontSize: '12px', letterSpacing: '3px', color: color, textTransform: 'uppercase', display: 'block', marginBottom: '20px', fontWeight: 600 }}>✦ {text}</span>
          ))}
          {renderDynamic(config.about.title, '#fff', (text, color) => (
            <h2 style={{ fontFamily: "'Playfair Display', Georgia, serif", fontSize: 'clamp(28px,4vw,54px)', fontWeight: 700, color: color, marginBottom: '24px', lineHeight: 1.2 }}>
              <span dangerouslySetInnerHTML={{ __html: text }} />
            </h2>
          ))}
          {renderDynamic(config.about.desc, 'rgba(255,255,255,0.8)', (text, color) => (
            <p style={{ color: color, fontSize: '16px', lineHeight: 1.85, marginBottom: '16px' }}>
              {text}
            </p>
          ))}
          {renderDynamic(config.about.company_info, 'rgba(255,255,255,0.55)', (text, color, idx) => (
            <React.Fragment>
              {text.split('\n').map((line, i, arr) => (
                <p key={`${idx}-${i}`} style={{ color: color, fontSize: '14px', marginBottom: i === (arr.length - 1) ? '48px' : '6px' }}>{line}</p>
              ))}
            </React.Fragment>
          ))}
          {user ? (
            <button id="about-cta-btn" className="btn-violet" onClick={() => onNavigate && onNavigate('/dashboard')}
              style={{ background: '#fff', color: V, fontWeight: 700, fontSize: '17px', padding: '16px 46px', borderRadius: '36px', border: 'none', cursor: 'pointer', boxShadow: '0 8px 32px rgba(0,0,0,0.2)', transition: 'all 0.3s' }}
            >✦ Bảng điều khiển</button>
          ) : (
            <button id="about-cta-btn" className="btn-violet" onClick={() => setShowLoginModal(true)}
              style={{ background: '#fff', color: V, fontWeight: 700, fontSize: '17px', padding: '16px 46px', borderRadius: '36px', border: 'none', cursor: 'pointer', boxShadow: '0 8px 32px rgba(0,0,0,0.2)', transition: 'all 0.3s' }}
            >✦ Bắt đầu ngay</button>
          )}
          <p style={{ color: 'rgba(255,255,255,0.45)', fontSize: '13px', marginTop: '16px' }}>Không cần thẻ tín dụng · 5 token miễn phí khi đăng ký</p>
        </div>
      </section>
      )}

      {/* FOOTER */}
      <footer style={{ borderTop: '1px solid rgba(124,58,237,0.1)', padding: '32px 64px', background: BG }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
             <img src="/logo.png" alt="Zephyr" style={{ height: '24px', width: '24px', objectFit: 'contain' }} onError={(e) => { (e.target as HTMLImageElement).style.display = 'none'; }} />
             <span style={{ fontWeight: 700, color: V, fontSize: '15px' }}>Zephyr</span>
             <span style={{ color: TXT2, fontSize: '12px', marginLeft: '12px', paddingLeft: '12px', borderLeft: '1px solid rgba(124,58,237,0.2)' }}>
               © {new Date().getFullYear()} Công nghệ AI tiên phong
             </span>
          </div>
          <div style={{ display: 'flex', gap: '20px' }}>
            {[['#features', 'Tính năng'], ['#gallery', 'Gallery']].map(([href, label]) => (
              <a key={href} href={href} style={{ color: TXT2, fontSize: '13px', textDecoration: 'none', transition: 'color 0.2s' }} onMouseEnter={e => { (e.currentTarget as HTMLElement).style.color = V; }} onMouseLeave={e => { (e.currentTarget as HTMLElement).style.color = TXT2; }}>{label}</a>
            ))}
            {publicPages.map(page => (
              <a 
                key={page.slug} 
                href={`/page/${page.slug}`}
                onClick={(e) => { e.preventDefault(); onNavigate && onNavigate(`/page/${page.slug}`); }}
                style={{ color: TXT2, fontSize: '13px', textDecoration: 'none', transition: 'color 0.2s', cursor: 'pointer' }} 
                onMouseEnter={e => { (e.currentTarget as HTMLElement).style.color = V; }} 
                onMouseLeave={e => { (e.currentTarget as HTMLElement).style.color = TXT2; }}
              >
                {page.title}
              </a>
            ))}
            {user ? (
              <button 
                onClick={() => onNavigate && onNavigate('/dashboard')} 
                style={{ color: V, fontSize: '13px', background: 'none', border: 'none', cursor: 'pointer', fontWeight: 600 }}
              >Bảng điều khiển</button>
            ) : (
              <button 
                onClick={() => setShowLoginModal(true)} 
                style={{ color: V, fontSize: '13px', background: 'none', border: 'none', cursor: 'pointer', fontWeight: 600 }}
              >Đăng nhập</button>
            )}
          </div>
        </div>
      </footer>

      {/* LOGIN MODAL */}
      {showLoginModal && (
        <div style={{ position: 'fixed', inset: 0, zIndex: 200, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '16px', background: 'rgba(0,0,0,0.5)', backdropFilter: 'blur(12px)' }}
          onClick={(e) => { if (e.target === e.currentTarget) setShowLoginModal(false); }}
        >
          <div style={{ width: '100%', maxWidth: '420px', background: '#fff', border: '1px solid rgba(124,58,237,0.15)', borderRadius: '28px', boxShadow: '0 40px 80px rgba(0,0,0,0.2)' }}>
            <div style={{ padding: '40px' }}>
              <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '12px' }}>
                <button id="modal-close-btn" onClick={() => setShowLoginModal(false)}
                  style={{ color: TXT2, background: '#f5f3ff', border: 'none', cursor: 'pointer', width: '32px', height: '32px', borderRadius: '50%', fontSize: '15px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}
                >✕</button>
              </div>
              <div style={{ textAlign: 'center', marginBottom: '28px' }}>
                <img src="/logo.png" alt="Zephyr" style={{ height: '52px', width: '52px', objectFit: 'contain', marginBottom: '14px' }} onError={(e) => { (e.target as HTMLImageElement).style.display = 'none'; }} />
                <h2 style={{ fontSize: '22px', fontWeight: 700, color: TXT, marginBottom: '8px' }}>Đăng nhập</h2>
                <p style={{ color: TXT2, fontSize: '14px' }}>Dùng tài khoản Google để tạo banner AI ngay</p>
              </div>
              <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '20px' }}>
                <div id="homeGoogleBtn" ref={googleBtnRef} style={{ display: 'flex', justifyContent: 'center' }} />
              </div>
              {loginLoading && (
                <div style={{ textAlign: 'center', color: TXT2, fontSize: '14px', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
                  <div style={{ width: '14px', height: '14px', border: `2px solid rgba(124,58,237,0.2)`, borderTopColor: V, borderRadius: '50%', animation: 'spin 1s linear infinite' }} />
                  Đang xác thực...
                </div>
              )}
              {loginError && (
                <div style={{ color: '#dc2626', fontSize: '14px', background: '#fef2f2', border: '1px solid #fecaca', borderRadius: '12px', padding: '12px', textAlign: 'center', marginTop: '8px' }}>{loginError}</div>
              )}
              <div style={{ marginTop: '24px', paddingTop: '22px', borderTop: '1px solid rgba(124,58,237,0.08)', textAlign: 'center' }}>
                <p style={{ fontSize: '11px', color: TXT2, letterSpacing: '1.5px', textTransform: 'uppercase', marginBottom: '6px' }}>Zephyr · MST 1801526082</p>
                <p style={{ fontSize: '12px', color: TXT2 }}>Bảo mật thông tin theo chính sách Google OAuth 2.0</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Gallery Card — light version
const GalleryCard: React.FC<{ banner: PublicBannerItem; index: number }> = ({ banner, index }) => {
  const [loaded, setLoaded] = useState(false);
  const [error, setError] = useState(false);

  const timeAgo = (dateStr: string) => {
    const diff = Date.now() - new Date(dateStr).getTime();
    const d = Math.floor(diff / 86400000);
    const h = Math.floor(diff / 3600000);
    if (d > 0) return `${d} ngày trước`;
    if (h > 0) return `${h} giờ trước`;
    return 'Vừa xong';
  };

  if (error) return null;

  return (
    <div className="gallery-card" style={{
      breakInside: 'avoid', marginBottom: '14px', borderRadius: '16px', overflow: 'hidden',
      background: '#fff', border: '1px solid rgba(124,58,237,0.1)',
      boxShadow: '0 2px 12px rgba(0,0,0,0.06)',
      animation: 'fadeInCard 0.5s ease both',
      position: 'relative', cursor: 'pointer', transition: 'all 0.3s',
      animationDelay: `${index * 40}ms`,
    }}>
      {!loaded && <div style={{ width: '100%', height: '240px', background: '#f5f3ff', animation: 'pulse 1.5s infinite' }} />}
      <img
        src={banner.image_url} alt={banner.request_description || 'Banner'}
        style={{ width: '100%', maxHeight: '420px', objectFit: 'cover', display: loaded ? 'block' : 'none' }}
        onLoad={() => setLoaded(true)} onError={() => setError(true)}
      />
      {/* Hover overlay */}
      <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(to top, rgba(15,10,30,0.85) 0%, transparent 55%)', opacity: 0, transition: 'opacity 0.3s', display: 'flex', flexDirection: 'column', justifyContent: 'flex-end', padding: '14px' }}
        onMouseEnter={e => { (e.currentTarget as HTMLElement).style.opacity = '1'; }}
        onMouseLeave={e => { (e.currentTarget as HTMLElement).style.opacity = '0'; }}
      >
        {banner.request_description && <p style={{ color: '#fff', fontSize: '12px', marginBottom: '8px', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>"{banner.request_description}"</p>}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          {banner.avatar_url
            ? <img src={banner.avatar_url} alt={banner.full_name} style={{ width: '18px', height: '18px', borderRadius: '50%', objectFit: 'cover' }} onError={(e) => { (e.target as HTMLImageElement).style.display = 'none'; }} />
            : <div style={{ width: '18px', height: '18px', borderRadius: '50%', background: '#8B5CF6', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '9px', fontWeight: 700, color: '#fff' }}>{(banner.full_name || 'U')[0].toUpperCase()}</div>
          }
          <span style={{ color: 'rgba(255,255,255,0.8)', fontSize: '11px', flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{banner.full_name || 'Người dùng'}</span>
          <span style={{ color: 'rgba(255,255,255,0.5)', fontSize: '10px', flexShrink: 0 }}>{timeAgo(banner.created_at)}</span>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
