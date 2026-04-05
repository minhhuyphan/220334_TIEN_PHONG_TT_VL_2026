import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { User, BannerHistoryItem, ReferenceImage } from '../types';
import { apiService } from '../services/api';
import { 
  Wand2, 
  Settings2, 
  Layers, 
  Download, 
  RefreshCcw,
  AlertCircle,
  CheckCircle2,
  Maximize2,
  Sparkles as SparklesIcon, 
  Image as ImageIcon,
  Mic,
  MicOff
} from 'lucide-react';
import toast from 'react-hot-toast';

// Extend Window interface for Speech Recognition
declare global {
  interface Window {
    SpeechRecognition: any;
    webkitSpeechRecognition: any;
  }
}

interface BannerGeneratorProps {
  user: User;
  refreshUser: () => void;
}

interface ReferenceImageWithLabel {
  file?: File;
  label: string;
  previewUrl: string; // Lưu URL cố định để tránh lag khi render
  path?: string; // Tên file trên server nếu đã có
}

const ASPECT_RATIO_PRESETS = [
  { label: '1:1', width: 1024, height: 1024, app: 'Ảnh Đại Diện, Bài Đăng Instagram' },
  { label: '2:3', width: 832, height: 1248, app: 'Poster, Portrait Mobile' },
  { label: '3:2', width: 1248, height: 832, app: 'Nhiếp Ảnh, Ảnh Blog' },
  { label: '3:4', width: 864, height: 1184, app: 'Tạp Chí, Social Media Portrait' },
  { label: '4:3', width: 1184, height: 864, app: 'Máy Tính Bảng, Màn Hình Cũ' },
  { label: '4:5', width: 896, height: 1152, app: 'Instagram Portrait' },
  { label: '5:4', width: 1152, height: 896, app: 'In Ấn, Mỹ Thuật' },
  { label: '9:16', width: 768, height: 1344, app: 'TikTok, Instagram Story' },
  { label: '16:9', width: 1344, height: 768, app: 'Thumbnail YouTube, Banner Điện Ảnh' },
  { label: '21:9', width: 1536, height: 672, app: 'Màn Hình Siêu Rộng, Cinema Scope' },
];

const BannerGenerator: React.FC<BannerGeneratorProps> = ({ user, refreshUser }) => {
  const [prompt, setPrompt] = useState('');
  const [width, setWidth] = useState(ASPECT_RATIO_PRESETS[0].width);
  const [height, setHeight] = useState(ASPECT_RATIO_PRESETS[0].height);
  const [count, setCount] = useState(1);
  const [costPerImage, setCostPerImage] = useState(1);
  const [referenceImageCost, setReferenceImageCost] = useState(0.5);
  const [referenceImages, setReferenceImages] = useState<ReferenceImageWithLabel[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [suggestionQuery, setSuggestionQuery] = useState('');
  const [isListening, setIsListening] = useState(false);

  const location = useLocation();
  const navigate = useNavigate();

  // Task polling state
  const [currentTaskId, setCurrentTaskId] = useState<string | null>(() => {
    return localStorage.getItem('current_banner_task_id');
  });

  // Handle regeneration from history
  useEffect(() => {
    const state = location.state as { regenerateData?: BannerHistoryItem };
    if (state?.regenerateData) {
      const data = state.regenerateData;
      setPrompt(data.request_description || '');
      
      const normalizedRatio = data.aspect_ratio?.replace(/\s+/g, '');
      const preset = ASPECT_RATIO_PRESETS.find(p => p.label.replace(/\s+/g, '') === normalizedRatio);
      
      if (preset) {
        setWidth(preset.width);
        setHeight(preset.height);
      } else {
        // Fallback or attempt to parse from resolution if aspect_ratio label doesn't match
        console.warn(`Aspect ratio ${data.aspect_ratio} not found in presets`);
      }
      
      if (data.reference_images_list) {
        const refs: ReferenceImageWithLabel[] = data.reference_images_list.map(r => ({
          label: r.label,
          previewUrl: r.url,
          path: r.path
        }));
        setReferenceImages(refs);
      }
      
      // Clear state after reading to prevent re-fill on refresh
      navigate(location.pathname, { replace: true, state: {} });
    }
  }, [location.state]);

  useEffect(() => {
    if (currentTaskId) {
      localStorage.setItem('current_banner_task_id', currentTaskId);
      setIsLoading(true);
    }
  }, [currentTaskId]);

  useEffect(() => {
    const loadCost = async () => {
        try {
            const data = await apiService.getConfig();
            setCostPerImage(data.banner_cost);
            setReferenceImageCost(data.reference_image_cost);
        } catch (e) {
            console.error(e);
            const fallbackData = await apiService.getBannerCost();
            setCostPerImage(fallbackData.cost);
        }
    }
    loadCost();
  }, []);

  // Clean up Object URLs when component unmounts or images change
  // Actually we only need to revoke when images are removed (handled in handleRemove)
  // or when component unmounts
  useEffect(() => {
    return () => {
      // Use the latest referenceImages from ref or closure to be safe, 
      // but simple unmount cleanup is usually enough
    };
  }, []);

  // Polling effect
  useEffect(() => {
    let intervalId: any;
    let pollCount = 0;
    const MAX_POLLS = 150; // 150 × 2s = 5 phút timeout

    if (currentTaskId) {
      intervalId = setInterval(async () => {
        pollCount++;

        // Timeout sau 5 phút
        if (pollCount > MAX_POLLS) {
          clearInterval(intervalId);
          setError('Yêu cầu tạo banner đã quá thời gian chờ (5 phút). Vui lòng thử lại.');
          setIsLoading(false);
          setCurrentTaskId(null);
          localStorage.removeItem('current_banner_task_id');
          return;
        }

        try {
          const task = await apiService.getTaskStatus(currentTaskId);
          
          if (task.status === 'completed') {
            setResults(task.result || []);
            setIsLoading(false);
            setCurrentTaskId(null);
            localStorage.removeItem('current_banner_task_id');
            refreshUser();
          } else if (task.status === 'failed') {
            setError(task.error || "Tạo banner thất bại");
            setIsLoading(false);
            setCurrentTaskId(null);
            localStorage.removeItem('current_banner_task_id');
          } else if (task.status === 'processing') {
            if (task.result && task.result.length > 0) {
              setResults(task.result);
            }
          }
        } catch (err) {
          console.error("Polling error", err);
        }
      }, 2000);
    }

    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [currentTaskId, refreshUser]);

  const handlePromptChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value;
    setPrompt(value);

    // Xử lý gợi ý @
    const cursorPosition = e.target.selectionStart;
    const textBeforeCursor = value.substring(0, cursorPosition);
    const lastAtIndex = textBeforeCursor.lastIndexOf('@');

    if (lastAtIndex !== -1 && !textBeforeCursor.substring(lastAtIndex).includes(' ')) {
      setShowSuggestions(true);
      setSuggestionQuery(textBeforeCursor.substring(lastAtIndex + 1).toLowerCase());
    } else {
      setShowSuggestions(false);
    }
  };

  const selectSuggestion = (label: string) => {
    const lastAtIndex = prompt.lastIndexOf('@', prompt.length);
    const newValue = prompt.substring(0, lastAtIndex) + '@' + label + ' ' + prompt.substring(prompt.length);
    setPrompt(newValue);
    setShowSuggestions(false);
  };

  // Tính toán chi phí bao gồm ảnh tham chiếu
  const referenceCostPerBanner = referenceImages.length * referenceImageCost;
  const totalCostPerBanner = costPerImage + referenceCostPerBanner;
  const totalCost = count * totalCostPerBanner;

  const handleDownload = async (imageUrl: string) => {
    try {
      toast.loading('Đang chuẩn bị tải xuống...', { id: 'downloading' });
      
      const response = await fetch(imageUrl);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `banner-${Date.now()}.png`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      // Clean up the object URL
      window.URL.revokeObjectURL(url);
      
      toast.success('Đã tải xuống thành công!', { id: 'downloading' });
    } catch (error) {
      console.error('Download error:', error);
      toast.error('Tải xuống thất bại. Hãy thử lại!', { id: 'downloading' });
      // Fallback
      window.open(imageUrl, '_blank');
    }
  };

  const handleViewLarge = (imageUrl: string) => {
    window.open(imageUrl, '_blank');
  };

  const handleReferenceImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    const imageFiles = files.filter(file => file.type.startsWith('image/'));
    
    if (imageFiles.length + referenceImages.length > 5) {
      toast.error('Tối đa 5 ảnh tham chiếu');
      return;
    }
    
    // Tạo label mặc định từ tên file (bỏ extension) và tạo URL preview một lần duy nhất
    const newImages = imageFiles.map(file => ({
      file,
      label: file.name.replace(/\.[^/.]+$/, ''), 
      previewUrl: URL.createObjectURL(file) // Tạo ở đây
    }));
    
    setReferenceImages(prev => [...prev, ...newImages]);
    toast.success(`Đã thêm ${imageFiles.length} ảnh tham chiếu`);
  };

  const handleRemoveReferenceImage = (index: number) => {
    setReferenceImages(prev => {
      const imgToRemove = prev[index];
      if (imgToRemove && imgToRemove.previewUrl.startsWith('blob:')) {
        URL.revokeObjectURL(imgToRemove.previewUrl); // Giải phóng bộ nhớ blob
      }
      return prev.filter((_, i) => i !== index);
    });
  };

  const handleUpdateImageLabel = (index: number, newLabel: string) => {
    setReferenceImages(prev => prev.map((img, i) => 
      i === index ? { ...img, label: newLabel } : img
    ));
  };

  const toggleListening = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
      toast.error("Trình duyệt của bạn không hỗ trợ nhận diện giọng nói.");
      return;
    }

    if (isListening) {
      setIsListening(false);
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = 'vi-VN'; // Mặc định tiếng Việt
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => {
      setIsListening(true);
      toast.success("Đang nghe... Mời bạn nói mô tả banner.");
    };

    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      setPrompt(prev => prev + (prev ? " " : "") + transcript);
      setIsListening(false);
    };

    recognition.onerror = (event: any) => {
      console.error("Speech recognition error", event.error);
      setIsListening(false);
      
      if (event.error === 'audio-capture') {
        toast.error("Không tìm thấy Micro hoặc bạn chưa cho phép trình duyệt truy cập Micro.");
      } else if (event.error === 'not-allowed') {
        toast.error("Bạn đã chặn quyền truy cập Micro. Hãy kiểm tra cài đặt trình duyệt.");
      } else {
        toast.error("Lỗi nhận diện giọng nói: " + event.error);
      }
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.start();
  };

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    if (user.tokens < totalCost) {
       setError(`Không đủ token. Cần ${totalCost.toFixed(1)} tokens.`);
       return;
    }

    setIsLoading(true);
    setResults([]);
    setError(null);
    
    try {
      // Create FormData to send files
      const formData = new FormData();
      formData.append('width', width.toString());
      formData.append('height', height.toString());
      formData.append('number', count.toString());
      
      // Thêm thông tin về các ảnh tham chiếu vào prompt để AI dễ nhận diện
      let enhancedPrompt = prompt;
      if (referenceImages.length > 0) {
        const labelsInfo = referenceImages.map((img, i) => `@${img.label}`).join(', ');
        enhancedPrompt += `\n\n(Tham chiếu các ảnh: ${labelsInfo})`;
      }
      formData.append('user_request', enhancedPrompt);
      
      // Seprate new files from existing paths
      const newFiles = referenceImages.filter(img => img.file);
      const existingRefs = referenceImages.filter(img => img.path).map(img => ({
        path: img.path,
        label: img.label
      }));

      // Append new files
      newFiles.forEach((img) => {
        if (img.file) {
          formData.append('reference_images', img.file);
          formData.append('reference_labels', img.label);
        }
      });

      // Append existing refs as JSON
      if (existingRefs.length > 0) {
        formData.append('existing_reference_images', JSON.stringify(existingRefs));
      }
      
      // Call API to create task
      const response: any = await apiService.generateBanners(formData);
      
      if (response && response.task_id) {
        localStorage.setItem('current_banner_task_id', response.task_id);
        setCurrentTaskId(response.task_id);
        
        // Trigger global listener by dispatching storage event if needed 
        // (though same-window storage event doesn't fire, but our App.tsx will pick it up on next poll)
        window.dispatchEvent(new Event('storage')); 
        
        const message = response.reference_images_count > 0 
          ? `Đang xếp hàng tạo banner với ${response.reference_images_count} ảnh tham chiếu...`
          : "Đang xếp hàng tạo banner...";
        toast.loading(message, { duration: 3000 });
      } else {
        throw new Error("Không nhận được Task ID");
      }
      
    } catch (err: any) {
      setError(err.message || "Đã có lỗi xảy ra");
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8 animate-in slide-in-from-bottom-4 duration-500">
      <div className="flex flex-col md:flex-row gap-8">
        {/* Settings Panel */}
        <div className="w-full md:w-80 space-y-4">
          <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <Settings2 className="h-4 w-4 text-indigo-600" />
                <h3 className="font-bold text-slate-800 text-sm">Cấu hình Banner</h3>
              </div>
              <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Thiết lập</span>
            </div>
            
            <div className="space-y-5">
              <div>
                <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">Tỷ lệ khung hình</label>
                <div className="grid grid-cols-2 gap-3">
                  {ASPECT_RATIO_PRESETS.map((preset) => {
                    const isActive = width === preset.width && height === preset.height;
                    const isPortrait = preset.height > preset.width;
                    const isSquare = preset.width === preset.height;
                    
                    return (
                      <button
                        key={preset.label}
                        type="button"
                        onClick={() => {
                          setWidth(preset.width);
                          setHeight(preset.height);
                        }}
                        className={`group relative flex flex-col items-center justify-center p-4 rounded-2xl border transition-all duration-300 ${
                          isActive 
                            ? 'border-indigo-600 bg-indigo-50/50 ring-2 ring-indigo-500/20 shadow-lg shadow-indigo-100' 
                            : 'border-slate-100 bg-white hover:border-indigo-200 hover:shadow-md hover:-translate-y-0.5'
                        }`}
                      >
                        {/* Visual Shape Indicator */}
                        <div className="mb-3 h-10 w-full flex items-center justify-center">
                          <div 
                            className={`rounded-md border-2 transition-all duration-300 ${
                              isActive 
                                ? 'border-indigo-500 bg-indigo-100 scale-110' 
                                : 'border-slate-200 bg-slate-50 group-hover:border-indigo-300 group-hover:bg-indigo-50/30'
                            }`}
                            style={{
                              width: isSquare ? '24px' : isPortrait ? '18px' : '36px',
                              height: isSquare ? '24px' : isPortrait ? '30px' : '20px',
                              boxShadow: isActive ? '0 0 15px rgba(99, 102, 241, 0.2)' : 'none'
                            }}
                          />
                        </div>
                        
                        <div className="flex flex-col items-center gap-0.5">
                          <span className={`text-xs font-bold leading-none ${isActive ? 'text-indigo-700' : 'text-slate-700'}`}>
                            {preset.label}
                          </span>
                          <span className="text-[9px] font-medium text-slate-400">
                             {preset.width}x{preset.height}
                          </span>
                        </div>
                        
                        {isActive && (
                          <div className="absolute -top-1 -right-1">
                            <div className="bg-indigo-600 text-white rounded-full p-0.5 shadow-md">
                              <CheckCircle2 className="h-3 w-3" />
                            </div>
                          </div>
                        )}
                        
                        {/* Premium Tooltip (Bottom/Top) */}
                        <div className="absolute -top-10 left-1/2 -translate-x-1/2 bg-slate-900/95 backdrop-blur-sm text-white text-[10px] px-3 py-1.5 rounded-lg opacity-0 group-hover:opacity-100 group-focus:opacity-100 transition-all duration-200 -translate-y-2 group-hover:translate-y-0 whitespace-nowrap z-50 pointer-events-none shadow-2xl border border-white/10 font-bold scale-90 group-hover:scale-100 origin-bottom">
                          {preset.app}
                          <div className="absolute -bottom-1 left-1/2 -translate-x-1/2 w-2 h-2 bg-slate-900 rotate-45" />
                        </div>
                      </button>
                    );
                  })}
                </div>
              </div>

              <div className="pt-4 border-t border-slate-100">
                <div className="flex items-center justify-between mb-3">
                  <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">Số lượng</label>
                  <span className="text-[11px] font-bold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded-full">
                    {totalCost} Token
                  </span>
                </div>
                <div className="flex gap-2">
                  {[1, 2, 4].map((num) => (
                    <button
                      key={num}
                      type="button"
                      onClick={() => setCount(num)}
                      className={`flex-1 py-2 rounded-lg text-xs font-bold border transition-all ${
                        count === num 
                          ? 'bg-indigo-600 border-indigo-600 text-white shadow-md' 
                          : 'bg-white border-slate-200 text-slate-600 hover:border-indigo-300'
                      }`}
                    >
                      {num} {num === 1 ? 'Ảnh' : 'Ảnh'}
                    </button>
                  ))}
                </div>
                <p className="mt-2 text-[10px] text-center text-slate-400">
                  {costPerImage} token mỗi ảnh tạo mới
                </p>
              </div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-indigo-600 to-indigo-700 rounded-2xl p-5 text-white shadow-lg shadow-indigo-100 relative overflow-hidden">
            <div className="absolute top-0 right-0 -mr-4 -mt-4 opacity-10">
              <SparklesIcon className="h-24 w-24" />
            </div>
            <h4 className="font-bold flex items-center gap-2 mb-2 text-sm">
              <SparklesIcon className="h-4 w-4" />
              Mẹo Pro
            </h4>
            <p className="text-[11px] text-indigo-100 leading-relaxed relative z-10">
              Mô tả chi tiết ánh sáng, góc chụp và cảm xúc. Càng chi tiết, kết quả càng ấn tượng.
            </p>
          </div>
        </div>

        {/* Main Interface */}
        <div className="flex-1 space-y-6">
          <form onSubmit={handleGenerate} className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
            <div className="relative">
              <textarea 
                value={prompt}
                onChange={handlePromptChange}
                maxLength={1000}
                placeholder='Mô tả banner bạn muốn tạo... Dùng dấu " " để viết chữ lên ảnh, ví dụ: "SALE 50%" màu đỏ to ở giữa. (Gõ @ để tham chiếu ảnh đã tải)'
                className="w-full h-32 p-4 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-indigo-500 resize-none text-slate-700"
              />
              
              {/* Voice Input Button */}
              <button
                type="button"
                onClick={toggleListening}
                className={`absolute bottom-4 left-4 p-2 rounded-full transition-all flex items-center gap-2 group ${
                  isListening 
                    ? 'bg-red-500 text-white animate-pulse shadow-lg shadow-red-200' 
                    : 'bg-white text-slate-400 hover:text-indigo-600 border border-slate-100 hover:border-indigo-100 shadow-sm'
                }`}
                title={isListening ? "Đang nghe..." : "Nhập bằng giọng nói"}
              >
                {isListening ? <Mic className="h-4 w-4" /> : <Mic className="h-4 w-4" />}
                {isListening && <span className="text-[10px] font-bold mr-1">Đang nghe...</span>}
              </button>

              {/* @ Suggestions Popup */}
              {showSuggestions && referenceImages.length > 0 && (
                <div className="absolute left-4 bottom-4 bg-white border border-slate-200 rounded-lg shadow-xl z-50 overflow-hidden min-w-[150px]">
                  <div className="bg-slate-50 px-3 py-1.5 border-b border-slate-100 text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                    Tham chiếu ảnh
                  </div>
                  <div className="max-h-40 overflow-y-auto">
                    {referenceImages
                      .filter(img => img.label.toLowerCase().includes(suggestionQuery))
                      .map((img, idx) => (
                        <button
                          key={idx}
                          type="button"
                          onClick={() => selectSuggestion(img.label)}
                          className="w-full text-left px-3 py-2 text-sm hover:bg-indigo-50 flex items-center gap-2 transition-colors border-b border-slate-50 last:border-none"
                        >
                          <span className="text-indigo-600 font-bold">@</span>
                          <span className="text-slate-700 truncate">{img.label}</span>
                        </button>
                      ))}
                  </div>
                </div>
              )}

              <div className={`absolute bottom-4 right-4 text-xs font-medium ${
                prompt.length > 900 ? 'text-red-400' : prompt.length > 700 ? 'text-amber-400' : 'text-slate-400'
              }`}>
                {prompt.length}/1000
              </div>
            </div>

            {/* Reference Images Upload Section */}
            <div className="border-t border-slate-100 pt-4">
              <div className="flex items-center justify-between mb-3 px-1">
                <label className="text-xs font-bold text-slate-500 uppercase tracking-wider flex items-center gap-2">
                  <ImageIcon className="h-4 w-4" />
                  Ảnh tham chiếu
                </label>
                {referenceImages.length > 0 && (
                  <span className="text-[10px] md:text-[11px] font-bold text-amber-600 bg-amber-50 px-2 py-0.5 rounded-full">
                    +{(referenceCostPerBanner).toFixed(1)} Token
                  </span>
                )}
              </div>
              
              <div className="space-y-3">
                {/* Upload Button */}
                <label className="flex items-center justify-center gap-2 p-3 md:p-4 border-2 border-dashed border-slate-200 rounded-xl hover:border-indigo-300 hover:bg-indigo-50/30 transition-all cursor-pointer group">
                  <input
                    type="file"
                    multiple
                    accept="image/*"
                    onChange={handleReferenceImageUpload}
                    className="hidden"
                    disabled={referenceImages.length >= 5}
                  />
                  <ImageIcon className="h-5 w-5 text-slate-400 group-hover:text-indigo-600" />
                  <span className="text-xs md:text-sm text-slate-600 group-hover:text-indigo-700 font-medium">
                    {referenceImages.length >= 5 ? 'Đã đạt giới hạn (5 ảnh)' : 'Tải ảnh lên (Tối đa 5)'}
                  </span>
                </label>

                {/* Preview Images */}
                {referenceImages.length > 0 && (
                  <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-2">
                    {referenceImages.map((img, index) => (
                      <div key={index} className="relative group">
                        <div className="aspect-square rounded-lg overflow-hidden border border-slate-200 bg-slate-50">
                          <img
                            src={img.previewUrl}
                            alt={img.label}
                            className="w-full h-full object-cover"
                          />
                        </div>
                        <button
                          type="button"
                          onClick={() => handleRemoveReferenceImage(index)}
                          className="absolute -top-1 -right-1 bg-red-500 text-white rounded-full p-1.5 md:p-1 opacity-100 md:opacity-0 md:group-hover:opacity-100 transition-opacity shadow-lg hover:bg-red-600 z-10"
                          title="Xóa ảnh"
                        >
                          <svg className="h-3 w-3 md:h-2 md:w-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                          </svg>
                        </button>
                        <div className="absolute bottom-0 left-0 right-0 p-0.5">
                          <input
                            type="text"
                            value={img.label}
                            onChange={(e) => handleUpdateImageLabel(index, e.target.value)}
                            className="w-full bg-black/60 text-white text-[8px] md:text-[9px] px-1 py-0.5 rounded outline-none focus:bg-indigo-600/80 transition-colors border-none text-center"
                            placeholder="Tên..."
                            title="Đặt tên để gọi trong prompt bằng @tên"
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                )}
                
                {referenceImages.length > 0 && (
                  <p className="text-[10px] text-slate-500 text-center">
                    {referenceImages.length} ảnh tham chiếu • {referenceImageCost} token/ảnh
                  </p>
                )}
              </div>
            </div>

            <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
              <div className="flex items-center gap-2 text-xs text-slate-500 order-2 sm:order-1">
                <CheckCircle2 className="h-3 w-3 text-green-500" />
                <span>Số dư: <strong>{user.tokens} tokens</strong></span>
              </div>
              <button 
                type="submit"
                disabled={isLoading || !prompt.trim() || user.tokens < totalCost}
                className="w-full sm:w-auto bg-indigo-600 text-white px-8 py-3.5 rounded-xl font-bold flex items-center justify-center gap-2 hover:bg-indigo-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-indigo-100 order-1 sm:order-2"
              >
                {isLoading ? (
                  <>
                    <RefreshCcw className="h-5 w-5 animate-spin" />
                    Đang tạo...
                  </>
                ) : (
                  <>
                    <Wand2 className="h-5 w-5" />
                    Tạo Banner
                  </>
                )}
              </button>
            </div>
          </form>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-600 p-4 rounded-xl flex items-center gap-3">
              <AlertCircle className="h-5 w-5 shrink-0" />
              <p className="text-sm font-medium">{error}</p>
            </div>
          )}

          {/* Results Area */}
          <div className="bg-white rounded-2xl p-4 md:p-8 border border-slate-200 shadow-sm min-h-[300px] md:min-h-[400px] flex flex-col">
            <div className="flex items-center gap-2 mb-6">
              <Layers className="h-5 w-5 text-indigo-600" />
              <h3 className="font-bold text-slate-900">Kết quả</h3>
            </div>

            {!results.length && !isLoading && (
              <div className="flex-1 flex flex-col items-center justify-center text-slate-400">
                <ImageIcon className="h-12 w-12 md:h-16 md:w-16 mb-4 opacity-20" />
                <p className="text-sm md:text-base">Banner AI sẽ xuất hiện ở đây.</p>
              </div>
            )}

            {isLoading && (
              <div className="flex-1 flex flex-col items-center justify-center space-y-4 py-8">
                <div className="relative h-20 w-20 md:h-24 md:w-24">
                  <div className="absolute inset-0 border-4 border-indigo-100 rounded-full"></div>
                  <div className="absolute inset-0 border-4 border-indigo-600 rounded-full border-t-transparent animate-spin"></div>
                  <SparklesIcon className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-6 w-6 md:h-8 md:w-8 text-indigo-600" />
                </div>
                <div className="text-center px-4">
                  <p className="font-bold text-slate-900">Đang xử lý yêu cầu</p>
                  <p className="text-xs md:text-sm text-slate-500">AI đang thiết kế banner cho bạn...</p>
                </div>
              </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6">
              {results.map((url, idx) => (
                <div key={idx} className="group relative bg-slate-50 rounded-2xl overflow-hidden border border-slate-200 aspect-video shadow-sm">
                  <img src={url} alt={`Banner ${idx + 1}`} className="w-full h-full object-cover" />
                  <div className="absolute inset-0 bg-black/40 opacity-100 md:opacity-0 md:group-hover:opacity-100 transition-opacity flex items-end md:items-center justify-center gap-3 p-3 md:p-0 backdrop-blur-[1px] md:backdrop-blur-none">
                    <button 
                      onClick={() => handleDownload(url)}
                      className="flex-1 md:flex-none p-2.5 md:p-3 bg-white rounded-xl md:rounded-full text-indigo-600 hover:scale-110 transition-transform flex items-center justify-center gap-2 md:gap-0 shadow-lg"
                      title="Tải xuống"
                    >
                      <Download className="h-5 w-5 md:h-6 md:w-6" />
                      <span className="md:hidden font-bold text-sm">Tải về</span>
                    </button>
                    <button 
                      onClick={() => handleViewLarge(url)}
                      className="p-2.5 md:p-3 bg-white rounded-xl md:rounded-full text-indigo-600 hover:scale-110 transition-transform shadow-lg"
                      title="Xem ảnh lớn"
                    >
                      <Maximize2 className="h-5 w-5 md:h-6 md:w-6" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BannerGenerator;
