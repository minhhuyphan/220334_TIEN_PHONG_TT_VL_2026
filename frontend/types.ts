
export interface User {
  id: number;
  email: string;
  full_name: string;
  avatar: string;
  tokens: number;
  is_admin: boolean;
  created_at?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface Package {
  id: number;
  name: string;
  tokens: number;
  amount_vnd: number;
  is_active: number;
}

export interface CreatePaymentResponse {
  payment_id: number;
  amount_vnd: number;
  tokens_received: number;
  transaction_content: string;
  bank_account: string;
  bank_brand: string;
  qr_url: string;
}

export enum PaymentStatus {
  PENDING = 'pending',
  COMPLETED = 'completed',
  FAILED = 'failed'
}

export interface PaymentStatusResponse {
  status: PaymentStatus;
  message: string;
}

export interface PaymentHistoryItem {
  id: number;
  package_name: string;
  amount_vnd: number;
  tokens: number;
  status: string;
  created_at: string;
}

export interface SeoSettings {
  site_title: string;
  description: string;
  keywords: string;
  author: string;
  favicon_url: string;
  logo_url: string;
  canonical_url: string;
  robots: string;
}


export interface ReferenceImage {
  path: string;
  label: string;
  url: string;
}

export interface BannerHistoryItem {
  id: number;
  user_id: number;
  request_description: string;
  aspect_ratio: string;
  resolution: string;
  prompt_used: string;
  image_url: string;
  token_cost: number;
  created_at: string;
  reference_images?: string;
  reference_images_list?: ReferenceImage[];
}
