# HƯỚNG DẪN NHANH - BANNER AI GENERATOR

## 🎯 ĐỬC ĂN LÀ GÌ?

**Banner AI Generator** - Ứng dụng web cho phép người dùng:

- Tạo banner quảng cáo tự động bằng **AI (FastAPI)**
- Quản lý, chỉnh sửa, xuất bản banner
- Xem thống kê & lịch sử
- Admin quản lý hệ thống

---

## 🏗️ KIẾN TRÚC (Architecture)

```
Frontend (Vite + Vue.js + TailwindCSS)
         ↓ HTTP REST API
Backend Laravel 12 (PHP)
         ↓
Queue Job Processing
         ↓
FastAPI AI Engine (Python) → Generate Images
         ↓
Real-time Notifications (Pusher WebSocket)
```

---

## 📊 CÁCH HOẠT ĐỘNG

### **1. Người dùng tạo banner**

- Nhập mô tả, chủ đề, kích thước
- Gửi request đến backend

### **2. Backend xử lý**

- Lưu thông tin vào database (Banner Details)
- Gửi job vào Queue
- Trả về response (không chờ)

### **3. Worker xử lý job**

- Gọi FastAPI để tạo banner
- Tải image về, lưu storage
- Lưu URL vào database

### **4. Real-time thông báo**

- Job hoàn tất → Broadcast event
- Pusher/Reverb gửi WebSocket
- Frontend cập nhật UI tức thời

### **5. Người dùng xem kết quả**

- Banner list cập nhật tự động
- Có thể chỉnh sửa, xuất bản, xóa

---

## 🗄️ DATABASE

**3 bảng chính:**

1. **users** - Người dùng
    - id, name, email, password, google_id, status

2. **banner_details** - Thông tin request tạo banner
    - id, user_id, description, theme, width, height, number, **status** (0=processing, 1=success, -1=failed)

3. **banners** - Banner được tạo ra
    - id, banner_details_id, link_banner, is_published, favorite_count

---

## 🤖 CÔNG NGHỆ

### **Backend**

- PHP 8.2+
- Laravel 12
- MySQL

### **Frontend**

- Vite (build tool)
- Vue.js (optional)
- TailwindCSS
- Bootstrap 5

### **AI & External**

- FastAPI (Generate banner images)
- Pusher (Real-time WebSocket)
- Google OAuth 2.0

### **Khác**

- Queue (database-driven)
- Sessions (database-driven)

---

## 🚀 CÁC ENDPOINT CHÍNH

### **Public Routes**

```
GET  /                          # Trang chủ
GET  /about                     # About
GET  /pricing                   # Giá cả
GET  /contact                   # Liên hệ
```

### **Auth Routes**

```
GET  /login                     # Form đăng nhập
POST /login                     # Đăng nhập
GET  /register                  # Form đăng ký
POST /register                  # Đăng ký
GET  /forgot-password           # Quên mật khẩu
POST /forgot-password           # Gửi reset link
GET  /reset-password/{token}    # Form reset
POST /reset-password            # Update password
GET  /auth/google               # Google OAuth
GET  /auth/google/callback      # Google callback
```

### **User Routes** (auth required)

```
GET  /user/layout                          # Dashboard
GET  /user/edit-banner/{bannerId}          # Form chỉnh sửa
POST /user/create-banners                  # Tạo banner
POST /user/save-banner                     # Lưu chỉnh sửa
PUT  /user/banners/{id}/publish            # Publish
DELETE /user/delete-banner/{bannerId}      # Xóa banner
GET  /user/get-info-user/{id}              # Thông tin user
POST /user/update-info-user/{id}           # Update user
```

### **Admin Routes** (auth + admin required)

```
GET  /admin/layout                         # Admin dashboard
GET  /admin/get-dashboard                  # Dashboard data
GET  /admin/get-table-user                 # Danh sách user
PATCH /admin/change-user-status/{id}       # Cập nhật user
GET  /admin/get-table-admin                # Danh sách admin
POST /admin/add-admin                      # Thêm admin
GET  /admin/get-user-banners/{userId}      # Banner của user
GET  /admin/get-models                     # Danh sách AI model
GET  /admin/get-configs                    # Cấu hình hệ thống
```

---

## 🔄 LUỒNG TẠOBANNER (Chi tiết)

```
1. User POST /user/create-banners
   ├─ Validate input
   └─ Create BannerDetail (status=0)

2. CreateBannersJob::dispatch()
   └─ Thêm vào queue (jobs table)

3. Queue Worker xử lý job
   ├─ Call FastAPI endpoint
   ├─ Nhận array URLs từ FastAPI
   ├─ For each URL:
   │   ├─ Download image
   │   ├─ Save storage/public/banners/
   │   └─ Create Banner record
   │
   ├─ Update BannerDetail status=1
   └─ Fire BannerJobCompleted event

4. BannerJobCompleted event
   └─ Broadcast to Pusher channel (banner-job.{userId})

5. Frontend WebSocket listener
   ├─ Nhận event
   ├─ Show notification
   └─ Refresh banner list
```

**File chính:** `app/Jobs/CreateBannersJob.php`

---

## 🔐 AUTHENTICATION

### **Cách đăng nhập:**

1. **Local** - Email + Password
2. **Google OAuth** - Redirect Google login

### **Quy trình:**

- User submit credentials
- AuthController xác minh
- Hash password so sánh
- Create session
- Redirect dashboard

### **File:** `app/Http/Controllers/Auth/AuthController.php`

---

## 🎨 REAL-TIME UPDATES (WebSocket)

**Công nghệ:** Pusher / Laravel Reverb

**Quy trình:**

1. Job kết thúc → Fire event
2. Event broadcast to Pusher
3. Pusher push to connected clients
4. Frontend listen & update UI

**File:** `app/Events/BannerJobCompleted.php`

---

## 📁 DIRECTORY STRUCTURE

```
app/
├── Http/Controllers/
│   ├── Auth/AuthController.php       → Xác thực
│   ├── Admin/DashboardController.php → Admin
│   └── User/BannerController.php     → Tạo banner
├── Models/
│   ├── User.php
│   ├── Banner.php
│   └── BannerDetail.php
├── Jobs/CreateBannersJob.php         → Queue job
├── Events/BannerJobCompleted.php     → Real-time event
└── Listeners/
    └── HandleBannerJobCompletion.php → Listen event

routes/
├── web.php                           → Web routes

resources/
├── views/
│   ├── auth/                         → Login/Register UI
│   ├── user/                         → User dashboard
│   └── admin/                        → Admin panel
├── js/                               → JavaScript
└── css/                              → Stylesheet

database/
├── migrations/                       → Schema
├── seeders/                          → Test data
└── database.sqlite

config/
├── database.php                      → DB connections
├── services.php                      → FastAPI, Pusher config
└── queue.php                         → Queue config
```

---

## 🚀 CÁCH CHẠY

### **Setup**

```bash
# Copy env
cp .env.example .env

# Generate key
php artisan key:generate

# Migrate database
php artisan migrate

# Seed test data
php artisan db:seed

# Install packages
npm install
```

### **Development**

```bash
# Terminal 1: Backend
php artisan serve
# http://localhost:8000

# Terminal 2: Frontend
npm run dev
# http://localhost:5173

# Terminal 3: Queue worker
php artisan queue:work

# Terminal 4: Real-time (optional)
php artisan reverb:start
```

---

## ⚙️ CONFIGURATION

### **.env Variables**

```ini
# FastAPI
FASTAPI_URL=http://localhost:8888/generate/banners
FASTAPI_KEY=W8t1DstjJTXvjzAYOWk848vANL4y1crY

# Pusher (Real-time)
PUSHER_APP_ID=1975399
PUSHER_APP_KEY=2e6b262dbb81b1356260
PUSHER_APP_SECRET=cc237fe4875f4039fa58

# Google OAuth
GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=xxx
```

---

## 🔧 TROUBLESHOOTING

| Problem               | Solution                                                         |
| --------------------- | ---------------------------------------------------------------- |
| Queue job không chạy  | `php artisan queue:work`                                         |
| Real-time không work  | Kiểm tra Pusher keys, `php artisan reverb:start`                 |
| Banner không được tạo | Check logs `storage/logs/laravel.log`, kiểm tra FastAPI endpoint |
| Database lỗi          | Run `php artisan migrate:fresh --seed`                           |

---

## 📝 GHI CHÚ QUAN TRỌNG

✅ **Cần config trước dùng:**

- FastAPI URL & API Key
- Pusher credentials
- Google OAuth keys
- Database

✅ **Phải chạy:**

- Laravel backend (`php artisan serve`)
- Frontend dev (`npm run dev`)
- Queue worker (`php artisan queue:work`)
- FastAPI server (Python backend)

✅ **Database:**

- Tự động create từ migrations
- Seeders cung cấp test data

✅ **Authentication:**

- Session-based (local)
- OAuth-based (Google)

---

**Đọc chi tiết tại:** [TRIEN_KHAI_DU_AN.md](./TRIEN_KHAI_DU_AN.md)
