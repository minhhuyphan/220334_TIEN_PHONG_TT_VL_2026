import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import { SeoSettings } from '../types';
import toast from 'react-hot-toast';
import { Save, RefreshCw, Upload, Globe } from 'lucide-react';

const AdminSeoSettings: React.FC = () => {
  const [settings, setSettings] = useState<SeoSettings>({
    site_title: '',
    description: '',
    keywords: '',
    author: '',
    favicon_url: '',
    logo_url: '',
    canonical_url: '/',
    robots: 'index, follow'
  });
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [isSyncing, setIsSyncing] = useState(false);

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    setIsLoading(true);
    try {
      const data = await apiService.getSeoSettings();
      // Ensure we have default values if API returns partial data
      setSettings(prev => ({ ...prev, ...data }));
    } catch (error) {
      toast.error("Failed to load SEO settings");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSave = async () => {
    setIsSaving(true);
    try {
      await apiService.updateSeoSettings(settings);
      toast.success("SEO settings saved successfully");
    } catch (error) {
      toast.error("Failed to save settings");
    } finally {
      setIsSaving(false);
    }
  };

  const handleSync = async () => {
    setIsSyncing(true);
    try {
      const data = await apiService.syncSeoSettings();
      setSettings(prev => ({ ...prev, ...data }));
      toast.success("Synced from HTML successfully");
    } catch (error) {
      toast.error("Failed to sync from HTML");
    } finally {
      setIsSyncing(false);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>, field: 'favicon_url' | 'logo_url') => {
    if (!e.target.files || e.target.files.length === 0) return;
    
    const file = e.target.files[0];
    if (file.size > 500 * 1024) { // 500KB check
        toast.error("File size should be less than 500KB for better SEO");
        return;
    }

    const toastId = toast.loading("Uploading...");
    try {
      const result = await apiService.uploadFile(file);
      setSettings(prev => ({ ...prev, [field]: result.url }));
      toast.success("Uploaded successfully", { id: toastId });
    } catch (error) {
      toast.error("Upload failed", { id: toastId });
    }
  };

  if (isLoading) {
    return (
      <div className="flex justify-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
          <div className="flex items-center gap-2">
            <Globe className="h-5 w-5 md:h-6 md:w-6 text-indigo-600 flex-shrink-0" />
            <h2 className="text-lg md:text-xl font-bold text-slate-900">Cấu hình SEO</h2>
          </div>
          <div className="flex gap-2 w-full sm:w-auto">
            <button
              onClick={handleSync}
              disabled={isSyncing}
              className="flex-1 sm:flex-none flex items-center justify-center gap-2 px-3 py-2 text-xs md:text-sm text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors disabled:opacity-50"
              title="Pull settings from existing index.html"
            >
              <RefreshCw className={`h-3 w-3 md:h-4 md:w-4 ${isSyncing ? 'animate-spin' : ''}`} />
              <span>Đồng bộ</span>
            </button>
            <button
              onClick={handleSave}
              disabled={isSaving}
              className="flex-1 sm:flex-none flex items-center justify-center gap-2 px-3 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors shadow-sm disabled:opacity-50 text-xs md:text-sm font-bold"
            >
              <Save className="h-3 w-3 md:h-4 md:w-4" />
              <span>{isSaving ? 'Đang lưu...' : 'Lưu'}</span>
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 gap-6">
          {/* Main Info */}
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Site Title</label>
              <input
                type="text"
                value={settings.site_title}
                onChange={(e) => setSettings({ ...settings, site_title: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                placeholder="Page Title"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Meta Description</label>
              <textarea
                value={settings.description}
                onChange={(e) => setSettings({ ...settings, description: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                rows={3}
                placeholder="Brief description for search engines"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Keywords</label>
              <input
                type="text"
                value={settings.keywords}
                onChange={(e) => setSettings({ ...settings, keywords: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                placeholder="Comma separated keywords"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Author</label>
              <input
                type="text"
                value={settings.author}
                onChange={(e) => setSettings({ ...settings, author: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Canonical URL</label>
              <input
                type="text"
                value={settings.canonical_url}
                onChange={(e) => setSettings({ ...settings, canonical_url: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                placeholder="https://example.com"
              />
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-slate-700 mb-1">Robots Tag</label>
              <input
                type="text"
                value={settings.robots}
                onChange={(e) => setSettings({ ...settings, robots: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                placeholder="index, follow"
              />
            </div>
          </div>

          {/* Images */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4 border-t border-slate-100">
            {/* Favicon */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Favicon</label>
              <div className="flex items-start gap-4">
                <div className="h-16 w-16 bg-slate-100 rounded-lg border border-slate-200 flex items-center justify-center overflow-hidden">
                  {settings.favicon_url ? (
                    <img src={settings.favicon_url} alt="Favicon" className="h-full w-full object-contain" />
                  ) : (
                    <span className="text-xs text-slate-400">None</span>
                  )}
                </div>
                <div className="flex-1">
                  <div className="flex gap-2 mb-2">
                    <label className="cursor-pointer px-3 py-1.5 bg-white border border-slate-300 rounded-md text-sm font-medium text-slate-700 hover:bg-slate-50 flex items-center gap-2">
                      <Upload className="h-3 w-3" />
                      Upload
                      <input type="file" className="hidden" accept="image/*" onChange={(e) => handleFileUpload(e, 'favicon_url')} />
                    </label>
                  </div>
                  <input 
                    type="text" 
                    value={settings.favicon_url}
                    onChange={(e) => setSettings({ ...settings, favicon_url: e.target.value })}
                    className="w-full text-xs text-slate-500 border-none bg-transparent p-0 focus:ring-0" 
                    placeholder="Or paste URL..."
                  />
                </div>
              </div>
            </div>

            {/* Logo / OG Image */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Social Share Image (Logo)</label>
              <div className="flex items-start gap-4">
                <div className="h-16 w-16 bg-slate-100 rounded-lg border border-slate-200 flex items-center justify-center overflow-hidden">
                  {settings.logo_url ? (
                    <img src={settings.logo_url} alt="Logo" className="h-full w-full object-cover" />
                  ) : (
                    <span className="text-xs text-slate-400">None</span>
                  )}
                </div>
                <div className="flex-1">
                  <div className="flex gap-2 mb-2">
                    <label className="cursor-pointer px-3 py-1.5 bg-white border border-slate-300 rounded-md text-sm font-medium text-slate-700 hover:bg-slate-50 flex items-center gap-2">
                      <Upload className="h-3 w-3" />
                      Upload
                      <input type="file" className="hidden" accept="image/*" onChange={(e) => handleFileUpload(e, 'logo_url')} />
                    </label>
                  </div>
                  <input 
                    type="text" 
                    value={settings.logo_url}
                    onChange={(e) => setSettings({ ...settings, logo_url: e.target.value })}
                    className="w-full text-xs text-slate-500 border-none bg-transparent p-0 focus:ring-0" 
                    placeholder="Or paste URL..."
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminSeoSettings;
