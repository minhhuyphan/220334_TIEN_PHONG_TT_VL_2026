import { User, AuthResponse, Package, CreatePaymentResponse, PaymentStatusResponse, PaymentHistoryItem, SeoSettings, PublicBannerItem } from '../types';

const getAuthHeaders = () => {
  const token = localStorage.getItem(__TOKEN_KEY__);
  return token ? { 'Authorization': `Bearer ${token}` } : {};
};

export const apiService = {
  async loginWithGoogle(idToken: string): Promise<AuthResponse> {
    const response = await fetch(`${__API_URL__}/auth/google`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token: idToken })
    });
    if (!response.ok) throw new Error('Login failed');
    return response.json();
  },

  async getMe(): Promise<User> {
    const response = await fetch(`${__API_URL__}/auth/me`, {
      headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error('Failed to fetch user profile');
    return response.json();
  },

  async getPackages(): Promise<Package[]> {
    const response = await fetch(`${__API_URL__}/payment/packages`);
    if (!response.ok) throw new Error('Failed to fetch packages');
    return response.json();
  },

  async createPayment(packageId: number): Promise<CreatePaymentResponse> {
    const formData = new FormData();
    formData.append("package_id", packageId.toString());

    const response = await fetch(`${__API_URL__}/payment/create`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: formData
    });
    if (!response.ok) throw new Error('Failed to create payment');
    return response.json();
  },

  async checkPaymentStatus(paymentId: number): Promise<PaymentStatusResponse> {
    const response = await fetch(`${__API_URL__}/payment/check-status/${paymentId}`, {
      method: "POST",
      headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error('Failed to check payment status');
    return response.json();
  },

  async getPaymentHistory(): Promise<PaymentHistoryItem[]> {
    const response = await fetch(`${__API_URL__}/payment/history`, {
      headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error('Failed to fetch payment history');
    return response.json();
  },

  async generateBanners(params: { width: number; height: number; number: number; user_request: string } | FormData): Promise<any> {
    let formData: FormData;

    // Nếu params là FormData thì dùng trực tiếp, nếu không thì tạo FormData mới
    if (params instanceof FormData) {
      formData = params;
    } else {
      formData = new FormData();
      formData.append("width", params.width.toString());
      formData.append("height", params.height.toString());
      formData.append("number", params.number.toString());
      formData.append("user_request", params.user_request);
    }

    const response = await fetch(`${__API_URL__}/generate/banners`, {
      method: 'POST',
      headers: {
        ...getAuthHeaders(),
      },
      body: formData
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to generate banners');
    }

    return response.json();
  },

  async getTaskStatus(taskId: string): Promise<any> {
    const response = await fetch(`${__API_URL__}/generate/tasks/${taskId}`, {
      headers: getAuthHeaders()
    });
    if (!response.ok) {
      throw new Error('Failed to get task status');
    }
    return response.json();
  },

  async getHistory(): Promise<any[]> {
    const response = await fetch(`${__API_URL__}/generate/history`, {
      headers: getAuthHeaders()
    });
    if (!response.ok) return [];
    return response.json();
  },

  async deleteHistoryItem(id: number): Promise<void> {
    const response = await fetch(`${__API_URL__}/generate/history/${id}`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error('Failed to delete history item');
  },

  async clearHistory(): Promise<void> {
    const response = await fetch(`${__API_URL__}/generate/history`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error('Failed to clear history');
  },

  async getDashboardStats(): Promise<DashboardStats> {
    const response = await fetch(`${__API_URL__}/generate/stats`, {
      headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error('Failed to fetch dashboard stats');
    return response.json();
  },

  async getBannerCost(): Promise<{ cost: number }> {
    const response = await fetch(`${__API_URL__}/generate/cost`, {
      headers: getAuthHeaders()
    });
    if (!response.ok) return { cost: 1 };
    return response.json();
  },

  async getConfig(): Promise<{ banner_cost: number; reference_image_cost: number; gemini_safe_mode: string; ai_model: string; image_model: string; system_prompt: string; google_api_key: string }> {
    const response = await fetch(`${__API_URL__}/admin/config`, {
      headers: getAuthHeaders()
    });
    if (!response.ok) return { banner_cost: 1, reference_image_cost: 0.5, gemini_safe_mode: 'OFF', ai_model: 'gemini-2.5-flash', image_model: 'gemini-3.0-fast-image-preview', system_prompt: '', google_api_key: '' };
    return response.json();
  },

  async updateBannerCost(cost: number): Promise<void> {
    const response = await fetch(`${__API_URL__}/admin/config/cost`, {
      method: "POST",
      headers: {
        ...getAuthHeaders(),
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ cost })
    });
    if (!response.ok) throw new Error('Failed to update banner cost');
  },

  async updateReferenceImageCost(cost: number): Promise<void> {
    const response = await fetch(`${__API_URL__}/admin/config/reference-image-cost`, {
      method: "POST",
      headers: {
        ...getAuthHeaders(),
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ cost })
    });
    if (!response.ok) throw new Error('Failed to update reference image cost');
  },

  async updateGeminiSafeMode(mode: string): Promise<void> {
    const response = await fetch(`${__API_URL__}/admin/config/gemini-safe-mode`, {
      method: "POST",
      headers: {
        ...getAuthHeaders(),
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ mode })
    });
    if (!response.ok) throw new Error('Failed to update Gemini Safe Mode');
  },

  async updateAiModel(model: string): Promise<void> {
    const response = await fetch(`${__API_URL__}/admin/config/ai-model`, {
      method: "POST",
      headers: {
        ...getAuthHeaders(),
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ model })
    });
    if (!response.ok) throw new Error('Failed to update AI Model');
  },

  async updateImageModel(model: string): Promise<void> {
    const response = await fetch(`${__API_URL__}/admin/config/image-model`, {
      method: "POST",
      headers: {
        ...getAuthHeaders(),
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ model })
    });
    if (!response.ok) throw new Error('Failed to update Image Model');
  },

  async updateSystemPrompt(prompt: string): Promise<void> {
    const response = await fetch(`${__API_URL__}/admin/config/system-prompt`, {
      method: "POST",
      headers: {
        ...getAuthHeaders(),
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ prompt })
    });
    if (!response.ok) throw new Error('Failed to update System Prompt');
  },

  async updateGoogleApiKey(api_key: string): Promise<void> {
    const response = await fetch(`${__API_URL__}/admin/config/google-api-key`, {
      method: "POST",
      headers: {
        ...getAuthHeaders(),
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ api_key })
    });
    if (!response.ok) throw new Error('Failed to update Google API Key');
  },

  async addTokensToUser(userId: number, tokens: number): Promise<void> {
    const response = await fetch(`${__API_URL__}/admin/users/${userId}/add-tokens`, {
      method: "POST",
      headers: {
        ...getAuthHeaders(),
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ tokens })
    });
    if (!response.ok) throw new Error('Failed to add tokens');
  },

  async deleteUser(userId: number): Promise<void> {
    const response = await fetch(`${__API_URL__}/admin/users/${userId}`, {
      method: "DELETE",
      headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error('Failed to delete user');
  },

  async getUserBanners(userId: number): Promise<any[]> {
    const response = await fetch(`${__API_URL__}/admin/users/${userId}/banners`, {
      headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error('Failed to fetch user banners');
    return response.json();
  },

  async getSeoSettings(): Promise<SeoSettings> {
    const response = await fetch(`${__API_URL__}/admin/seo`, {
      headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error('Failed to fetch SEO settings');
    return response.json();
  },

  async updateSeoSettings(settings: SeoSettings): Promise<void> {
    const response = await fetch(`${__API_URL__}/admin/seo`, {
      method: "PUT",
      headers: {
        ...getAuthHeaders(),
        "Content-Type": "application/json"
      },
      body: JSON.stringify(settings)
    });
    if (!response.ok) throw new Error('Failed to update SEO settings');
  },

  async syncSeoSettings(): Promise<SeoSettings> {
    const response = await fetch(`${__API_URL__}/admin/seo/sync`, {
      method: "POST",
      headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error('Failed to sync SEO settings');
    return response.json();
  },

  async getPublicBanners(limit = 20): Promise<PublicBannerItem[]> {
    const response = await fetch(`${__API_URL__}/generate/public-banners?limit=${limit}`);
    if (!response.ok) return [];
    return response.json();
  },

  async toggleBannerPublic(bannerId: number, isPublic: boolean): Promise<void> {
    const response = await fetch(`${__API_URL__}/generate/history/${bannerId}/public`, {
      method: 'PATCH',
      headers: { ...getAuthHeaders(), 'Content-Type': 'application/json' },
      body: JSON.stringify({ is_public: isPublic })
    });
    if (!response.ok) throw new Error('Failed to toggle banner public status');
  },

  async adminToggleBannerVisibility(bannerId: number, isHidden: boolean): Promise<void> {
    const response = await fetch(`${__API_URL__}/admin/banners/${bannerId}/visibility`, {
      method: 'PATCH',
      headers: { ...getAuthHeaders(), 'Content-Type': 'application/json' },
      body: JSON.stringify({ is_hidden: isHidden })
    });
    if (!response.ok) throw new Error('Failed to toggle banner visibility');
  },

  async adminDeleteBanner(bannerId: number): Promise<void> {
    const response = await fetch(`${__API_URL__}/admin/banners/${bannerId}`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error('Failed to delete banner');
  },

  async uploadFile(file: File): Promise<{ filename: string; url: string }> {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${__API_URL__}/upload-file/upload`, {
      method: "POST",
      headers: getAuthHeaders(), // Optional depending on backend auth for upload
      body: formData
    });

    if (!response.ok) throw new Error('Failed to upload file');
    return response.json();
  }
};

export interface DashboardStats {
  total_banners: number;
  token_balance: number;
  total_spent: number;
  generation_score: string;
  recent_projects: {
    id: number;
    image_url: string;
    request_description: string;
    created_at: string;
  }[];
}
