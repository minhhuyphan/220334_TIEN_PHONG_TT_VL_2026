# PHÂN TÍCH ĐẦU ĐỦ DỰ ÁN - BANNER AI GENERATOR

**Ngày phân tích**: 10/02/2026  
**Phiên bản**: Laravel 12.3.0  
**Trạng thái**: Đang phát triển

---

## 📋 MỤC LỤC

1. [Tổng quan dự án](#tổng-quan)
2. [Mục đích & Tính năng chính](#mục-đích--tính-năng-chính)
3. [Công nghệ sử dụng](#công-nghệ-sử-dụng)
4. [Kiến trúc hệ thống](#kiến-trúc-hệ-thống)
5. [Luồng xử lý chi tiết](#luồng-xử-lý-chi-tiết)
6. [Cơ sở dữ liệu](#cơ-sở-dữ-liệu)
7. [Quy trình AI](#quy-trình-ai)
8. [Hướng phát triển](#hướng-phát-triển)

---

## 🎯 TỔNG QUAN

Dự án **Banner AI Generator** là một ứng dụng web hiện đại cho phép người dùng:

- **Tạo banner quảng cáo tự động** bằng AI
- **Quản lý các banner** đã tạo ra
- **Xuất bản & chia sẻ** banner trên các nền tảng
- **Xem lịch sử & thống kê** hiệu suất banner

Đây là một **SaaS application** kết hợp giữa:

- **Backend**: Laravel 12 (PHP) - xử lý logic, database, authentication
- **Frontend**: Vue.js + Vite (JavaScript) - giao diện người dùng
- **AI Engine**: FastAPI (Python) - tạo banner bằng AI/ML
- **Real-time**: Pusher/Laravel Reverb - thông báo tức thời

---

## 🎨 MỤC ĐÍCH & TÍNH NĂNG CHÍNH

### 📌 Mục Đích Chính:

Tự động hóa việc tạo banner quảng cáo chuyên nghiệp bằng AI, giúp tiết kiệm thời gian và chi phí thiết kế.

### 🚀 Các Tính Năng Chính:

#### **1. Xác thực & Quản lý người dùng**

- ✅ Đăng ký/Đăng nhập cục bộ
- ✅ Xác minh email
- ✅ Đăng nhập Google OAuth
- ✅ Quên mật khẩu & Đặt lại mật khẩu
- ✅ Quản lý hồ sơ người dùng

#### **2. Tạo Banner với AI**

- 📝 Nhập mô tả, chủ đề, kích thước banner
- 🤖 AI FastAPI xử lý & tạo hình ảnh
- 🔄 Xử lý hàng đợi (Queue) - không chặn UI
- 🎨 Cho phép chỉnh sửa/lưu banner
- 📊 Xem lịch sử các banner đã tạo

#### **3. Quản lý Banner**

- ✏️ Chỉnh sửa banner
- 🗑️ Xóa banner
- 📤 Xuất bản banner
- ⭐ Đánh dấu yêu thích
- 🔗 Tạo link chia sẻ

#### **4. Admin Dashboard**

- 📊 Xem tổng quan hệ thống
- 👥 Quản lý người dùng
- 🔐 Quản lý quyền Admin
- ⚙️ Cấu hình hệ thống
- 🤖 Quản lý AI Models

#### **5. Real-time Notifications**

- ⏱️ Thông báo khi banner sinh xong
- 🔔 Cập nhật trạng thái tức thời
- 📡 Sử dụng WebSocket (Pusher/Reverb)

---

## 💻 CÔNG NGHỆ SỬ DỤNG

### **Backend Stack**

| Công nghệ    | Phiên bản | Mục đích                  |
| ------------ | --------- | ------------------------- |
| **PHP**      | 8.2+      | Ngôn ngữ lập trình server |
| **Laravel**  | 12.0      | Web framework             |
| **MySQL**    | 5.7+      | Cơ sở dữ liệu chính       |
| **Composer** | 2.x       | Package manager PHP       |

### **Frontend Stack**

| Công nghệ       | Phiên bản | Mục đích                |
| --------------- | --------- | ----------------------- |
| **Vue.js**      | 3.x       | Framework UI (tùy chọn) |
| **Vite**        | 6.2       | Build tool & Dev server |
| **TailwindCSS** | 4.0       | CSS framework           |
| **Bootstrap**   | 5.x       | UI components           |
| **jQuery**      | 3.x       | DOM manipulation        |

### **AI & External Services**

| Dịch vụ              | Mục đích                              |
| -------------------- | ------------------------------------- |
| **FastAPI**          | Xử lý AI, tạo banner (Python backend) |
| **Pusher**           | Real-time WebSocket notifications     |
| **Google OAuth 2.0** | Xác thực Google                       |
| **SMTP (Gmail)**     | Gửi email                             |

### **Package chính trong composer.json**

```json
{
    "laravel/framework": "^12.0", // Core framework
    "laravel/reverb": "^1.5", // Real-time broadcasting
    "laravel/socialite": "^5.20", // Social authentication
    "pusher/pusher-php-server": "^7.2", // Push notifications
    "spatie/laravel-sitemap": "^7.3" // SEO sitemap
}
```

---

## 🏗️ KIẾN TRÚC HỆ THỐNG

### **Kiến trúc Tổng Quan**

```
┌─────────────────────────────────────────────────────────┐
│                    USER INTERFACE                       │
│              (Vite + TailwindCSS + Vue.js)             │
│  Dashboard | Create Banner | Edit | View | Publish     │
└─────────────────┬───────────────────────────────────────┘
                  │ HTTP REST API
                  ▼
┌─────────────────────────────────────────────────────────┐
│                   LARAVEL 12 BACKEND                    │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Controllers | Routes | Middleware | Auth        │  │
│  │ - User Authentication                           │  │
│  │ - Banner Management                             │  │
│  │ - Admin Panel                                   │  │
│  │ - Job Dispatch & Queue                          │  │
│  └──────────────────────────────────────────────────┘  │
│                      │                                  │
│  ┌──────────────────┼──────────────────┐              │
│  ▼                  ▼                   ▼              │
│ MySQL          Queue Jobs         Events/Broadcast    │
│ Database       (Database)         (Real-time)        │
└─────────────────────────────────────────────────────────┘
         │                    │
         │                    ▼
         │            ┌──────────────────┐
         │            │  Pusher/Reverb   │
         │            │ WebSocket Server │
         │            └──────────────────┘
         │                    │
         ▼                    ▼
    ┌────────────────────────────────┐
    │   FastAPI AI Engine (Python)   │
    │  - Generate Banner Images      │
    │  - ML Model Integration        │
    │  - Image Processing            │
    └────────────────────────────────┘
```

### **Directory Structure**

```
laravel_12_base/
├── app/
│   ├── Http/Controllers/
│   │   ├── Admin/           → Quản lý admin
│   │   ├── Auth/            → Xác thực người dùng
│   │   └── User/            → Tính năng người dùng
│   ├── Models/              → Eloquent models (Banner, BannerDetail, User)
│   ├── Jobs/                → Queue jobs (CreateBannersJob)
│   ├── Events/              → Events (BannerJobCompleted)
│   ├── Listeners/           → Event listeners
│   ├── Notifications/       → Email notifications
│   └── Providers/           → Service providers
├── routes/
│   ├── web.php              → Web routes
│   ├── channels.php         → Broadcasting channels
│   └── console.php          → CLI commands
├── resources/
│   ├── views/               → Blade templates
│   │   ├── admin/           → Admin pages
│   │   ├── auth/            → Login/Register
│   │   ├── homepage/        → Public pages
│   │   └── user/            → User dashboard
│   ├── js/                  → JavaScript (Vue.js, Bootstrap)
│   └── css/                 → Stylesheets (Tailwind)
├── database/
│   ├── migrations/          → Database schema
│   ├── seeders/             → Test data
│   └── database.sqlite      → SQLite database
├── public/
│   ├── assets/              → CSS, JS, fonts, images
│   └── build/               → Compiled assets
└── config/
    ├── app.php              → App configuration
    ├── database.php         → Database connections
    ├── queue.php            → Queue configuration
    └── services.php         → External services (FastAPI, Pusher)
```

---

## 🔄 LUỒNG XỬ LÝ CHI TIẾT

### **1️⃣ Quy trình Đăng ký & Đăng nhập**

```
User Visits /register
    ↓
Enter Email, Password, Name
    ↓
POST /register → AuthController::register()
    ↓
Hash Password + Create User Record
    ↓
Send Verification Email (notification)
    ↓
User Check Email & Verify
    ↓
Redirect to Dashboard (Homepage)
```

**File liên quan:**

- `app/Http/Controllers/Auth/AuthController.php`
- `app/Models/User.php`
- `app/Notifications/VerifyEmail.php`

---

### **2️⃣ Quy trình Tạo Banner bằng AI**

```
┌─ START: User vào Dashboard tạo banner
│
├─ Step 1: Nhập Input
│   └─ Form: Mô tả, Chủ đề, Kích thước (width/height), Số lượng
│
├─ Step 2: Gửi Request
│   └─ POST /user/create-banners
│       → BannerController::createBanners()
│
├─ Step 3: Lưu thông tin Banner Detail vào Database
│   └─ BannerDetail::create([
│       'user_id' => auth()->id(),
│       'description' => $description,
│       'theme' => $theme,
│       'width' => $width,
│       'height' => $height,
│       'number' => $number,
│       'status' => 0  // 0 = Processing, 1 = Success, -1 = Failed
│   ])
│
├─ Step 4: Dispatch Queue Job
│   └─ CreateBannersJob::dispatch($data, $bannerDetailsId)
│       → Queue database
│
├─ Step 5: Background Job Processing
│   └─ CreateBannersJob::handle()
│       │
│       ├─ Call FastAPI: POST http://localhost:8888/generate/banners
│       │   Headers: API-Key = {FASTAPI_KEY}
│       │   Payload: description, theme, width, height, number
│       │
│       ├─ FastAPI Returns: Array of image URLs
│       │   [
│       │     "https://fastapi-server/generated/banner_1.png",
│       │     "https://fastapi-server/generated/banner_2.png"
│       │   ]
│       │
│       ├─ For each image URL:
│       │   ├─ Download image
│       │   ├─ Save to Storage/public/banners/{filename}
│       │   └─ Create Banner record in DB
│       │
│       ├─ Update BannerDetail status = 1 (Success)
│       │
│       └─ Fire Event: BannerJobCompleted($userId)
│
├─ Step 6: Real-time Notification
│   └─ BannerJobCompleted Event
│       → Broadcast to Pusher channel: banner-job.{userId}
│       → Frontend receives notification
│       → UI updates with new banners
│
└─ END: User sees generated banners in Dashboard
```

**File liên quan:**

- `app/Http/Controllers/User/BannerController.php`
- `app/Jobs/CreateBannersJob.php` (Main AI processing logic)
- `app/Events/BannerJobCompleted.php` (Real-time notification)
- `app/Models/Banner.php`
- `app/Models/BannerDetail.php`

**Flow Code:**

```php
// Controller: POST /user/create-banners
public function createBanners(Request $request) {
    // 1. Validate input
    $request->validate([
        'description' => 'required|string',
        'theme' => 'required|string',
        'width' => 'required|integer',
        'height' => 'required|integer',
        'number' => 'required|integer'
    ]);

    // 2. Create BannerDetail
    $bannerDetail = BannerDetail::create([
        'user_id' => Auth::id(),
        'description' => $request->description,
        'theme' => $request->theme,
        'width' => $request->width,
        'height' => $request->height,
        'number' => $request->number,
        'status' => 0
    ]);

    // 3. Dispatch Job to Queue
    CreateBannersJob::dispatch(
        $request->all(),
        $bannerDetail->id,
        $jobId,
        Auth::id()
    );

    return response()->json(['status' => 'processing']);
}

// Job: CreateBannersJob::handle()
public function handle() {
    try {
        // Call FastAPI
        $response = Http::post(
            config('services.fastapi.url'),
            $this->data
        );

        if ($response->successful()) {
            $bannerUrls = $response->json();

            // Save each banner
            foreach ($bannerUrls as $url) {
                $imageContent = Http::get($url)->body();
                Storage::disk('public')->put("banners/{$filename}", $imageContent);

                Banner::create([
                    'banner_details_id' => $this->bannerDetailsId,
                    'link_banner' => Storage::url("banners/{$filename}")
                ]);
            }

            // Update status
            BannerDetail::find($this->bannerDetailsId)->update(['status' => 1]);

            // Broadcast event
            event(new BannerJobCompleted($this->userId));
        }
    } catch (\Exception $e) {
        // Handle error
        BannerDetail::find($this->bannerDetailsId)->update(['status' => -1]);
    }
}
```

---

### **3️⃣ Quy trình Chỉnh sửa Banner**

```
User Click Edit Banner
    ↓
GET /user/edit-banner/{bannerId}
    ↓
Load Banner Detail Form
    ↓
User Modify Properties
    ↓
POST /user/save-banner
    ↓
Update Database
    ↓
Redirect to Dashboard
```

**Endpoints:**

- `GET /user/edit-banner/{bannerId}` - Load form
- `POST /user/save-banner` - Save changes

---

### **4️⃣ Quy trình Xuất bản Banner**

```
User Click "Publish" Button
    ↓
PUT/DELETE /banners/{id}/publish
    ↓
BannerController::publishBanner()
    ↓
Toggle is_published flag
    ↓
Update published_at timestamp
    ↓
Return success response
```

---

### **5️⃣ Admin Dashboard Quản lý**

```
Admin Login
    ↓
/admin/layout → Dashboard
    ├─ View Statistics
    ├─ Manage Users (GET /admin/user-table)
    │   ├─ View user list
    │   ├─ Change user status (PATCH /admin/change-user-status/{id})
    │   └─ View user's banners
    │
    ├─ Manage Admins (GET /admin/admin-table)
    │   ├─ View admin list
    │   ├─ Add new admin (POST /admin/add-admin)
    │   └─ Change admin status
    │
    ├─ Manage AI Models (GET /admin/models)
    │   ├─ List models
    │   ├─ View model info
    │   └─ Update model API key
    │
    └─ Website Configuration (GET /admin/configs)
        ├─ View settings
        └─ Update configuration
```

---

## 💾 CƠ SỞ DỮ LIỆU

### **Database Schema**

#### **1. users table**

```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    email_verified_at TIMESTAMP NULL,
    password VARCHAR(255) NOT NULL,
    google_id VARCHAR(255) NULLABLE UNIQUE,
    google_token VARCHAR(255) NULLABLE,
    google_refresh_token VARCHAR(255) NULLABLE,
    remember_token VARCHAR(100) NULL,
    status INT DEFAULT 1,  -- 1=active, 0=inactive
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

#### **2. banner_details table**

```sql
CREATE TABLE banner_details (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    description TEXT NOT NULL,
    theme VARCHAR(255),
    width INT,
    height INT,
    number INT,
    status INT DEFAULT 0,  -- 0=processing, 1=success, -1=failed
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

#### **3. banners table**

```sql
CREATE TABLE banners (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    banner_details_id BIGINT NOT NULL,
    link_banner VARCHAR(255),
    is_published INT DEFAULT 0,  -- 0=draft, 1=published
    published_at TIMESTAMP NULL,
    favorite_count INT DEFAULT 0,
    FOREIGN KEY (banner_details_id) REFERENCES banner_details(id)
);
```

#### **4. Other Tables**

- `web_configs` - Website settings (theme, API keys, etc.)
- `models` - AI models management
- `sessions` - User sessions
- `cache` - Cache data
- `jobs` - Queue jobs
- `migrations` - Database migration tracking

### **Relationships**

```
User (1) ──── (M) BannerDetail
     ↓
     └─────── (M) Banner

BannerDetail (1) ──── (M) Banner
```

---

## 🤖 QUY TRÌNH AI TẠO BANNER

### **FastAPI Backend (Python)**

```
FastAPI Server: http://localhost:8888

Endpoint: POST /generate/banners
Request Payload:
{
    "description": "Summer sale promotion",
    "theme": "bright, colorful",
    "width": 1200,
    "height": 600,
    "number": 3,
    "api_key": "W8t1DstjJTXvjzAYOWk848vANL4y1crY"
}

Response:
[
    "https://fastapi-server/generated/summer_1.png",
    "https://fastapi-server/generated/summer_2.png",
    "https://fastapi-server/generated/summer_3.png"
]
```

### **AI Processing Flow**

```
Input Parameters
    ↓
Text-to-Image Model (DALL-E, Stable Diffusion, custom)
    ├─ Process description & theme
    ├─ Apply style/color from theme
    ├─ Generate image with specified dimensions
    └─ Quality check & optimization
    ↓
Image Post-Processing
    ├─ Add watermark/branding
    ├─ Resize/crop to exact dimensions
    ├─ Compress for web
    └─ Save to server storage
    ↓
Return Image URLs
    ↓
Laravel Backend
    ├─ Download images
    ├─ Store locally
    └─ Save URLs to database
```

### **Configuration trong Laravel**

File: `config/services.php`

```php
'fastapi' => [
    'url' => env('FASTAPI_URL', 'http://localhost:8888/generate/banners'),
    'api_key' => env('FASTAPI_KEY'),
]
```

File: `.env`

```
FASTAPI_URL=http://localhost:8888/generate/banners
FASTAPI_KEY=W8t1DstjJTXvjzAYOWk848vANL4y1crY
```

---

## 📡 REAL-TIME NOTIFICATIONS (WebSocket)

### **Công nghệ: Pusher/Laravel Reverb**

```
Job Completes
    ↓
Fire Event: BannerJobCompleted($userId)
    ↓
Broadcast to Channel: banner-job.{userId}
    ↓
WebSocket → Pusher/Reverb Server
    ↓
Connected Clients receive update
    ↓
Frontend JavaScript updates UI
    ├─ Show toast notification
    ├─ Refresh banner list
    └─ Show generated banners
```

### **Event Structure**

```php
class BannerJobCompleted implements ShouldBroadcast {
    public function broadcastOn(): Channel {
        return new Channel('banner-job.' . $this->userId);
    }

    public function broadcastAs() {
        return 'BannerJobCompleted';
    }
}
```

### **Frontend Listener (JavaScript/Vue.js)**

```javascript
Echo.channel(`banner-job.${userId}`).listen("BannerJobCompleted", (e) => {
    console.log("Banner generation completed!");
    // Refresh banners list
    loadBanners();
    // Show notification
    showSuccessNotification("Your banners are ready!");
});
```

---

## 🔑 AUTHENTICATION & AUTHORIZATION

### **Authentication Methods**

1. **Local Authentication**
    - Email + Password (hashed with bcrypt)
    - Session-based

2. **Google OAuth 2.0**
    - Redirect to Google login
    - Get access token
    - Create/update user record

### **Authorization**

- **Middleware**: `auth` - require login
- **Middleware**: `admin` - require admin role
- **Model**: User → hasRole('admin')

### **Key Functions**

```php
Auth::check()           // Is authenticated?
Auth::user()            // Get current user
Auth::id()              // Get user ID
Auth::guard('web')      // Specify guard
Auth::logout()          // Logout
// OAuth
Socialite::driver('google')->redirect()
Socialite::driver('google')->user()
```

---

## 📊 QUEUE & JOB PROCESSING

### **Job Configuration**

File: `config/queue.php`

```php
'default' => env('QUEUE_CONNECTION', 'database'),
'connections' => [
    'database' => [
        'driver' => 'database',
        'table' => 'jobs',
        'queue' => 'default'
    ]
]
```

### **Job Processing**

```bash
# Start queue worker (process jobs)
php artisan queue:work

# Or specific queue
php artisan queue:work --queue=default

# Failed jobs
php artisan queue:failed
```

### **Job Lifecycle**

```
1. Job Dispatched → jobs table
2. Queue worker picks it up
3. Execute Job::handle()
4. Success? → Delete from jobs
5. Failed? → Retry or move to failed_jobs
```

---

## 🚀 HƯỚNG PHÁT TRIỂN

### **Tính năng đang phát triển**

- [ ] Chỉnh sửa banner trực tiếp trong giao diện (drag-drop)
- [ ] Templates banner có sẵn
- [ ] Analytics & performance tracking
- [ ] Integrations (Facebook Ads, Google Ads)
- [ ] API cho third-party
- [ ] Mobile app
- [ ] Pricing plans & payment integration

### **Cải thiện hiệu năng**

- [ ] Caching (Redis)
- [ ] Image CDN
- [ ] Database optimization
- [ ] Frontend bundle optimization

### **Security enhancements**

- [ ] Rate limiting
- [ ] CSRF token verification
- [ ] API key rotation
- [ ] Audit logging
- [ ] Data encryption
- [ ] Backup strategy

### **DevOps & Deployment**

- [ ] Docker containerization
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Kubernetes orchestration
- [ ] Load balancing
- [ ] SSL/TLS certificates
- [ ] Monitoring & logging (ELK stack)

---

## 📝 COMMAND CHẠY DỰ ÁN

### **Development Setup**

```bash
# Copy env file
cp .env.example .env

# Generate app key
php artisan key:generate

# Create database
php artisan migrate

# Seed test data
php artisan db:seed

# Start backend server
php artisan serve

# Start frontend dev server (in another terminal)
npm run dev
```

### **Production Deployment**

```bash
# Install dependencies
composer install --no-dev
npm install

# Build frontend
npm run build

# Optimize application
php artisan optimize
php artisan config:cache
php artisan route:cache

# Start queue worker
php artisan queue:work

# Serve with production server (Nginx/Apache)
# Configure .htaccess or nginx.conf
```

---

## 📚 ENVIRONMENT VARIABLES

```ini
# Application
APP_NAME="Banner AI Generator"
APP_ENV=local|production
APP_DEBUG=true|false
APP_URL=http://localhost:8000

# Database
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel_app
DB_USERNAME=root
DB_PASSWORD=

# FastAPI Integration
FASTAPI_URL=http://localhost:8888/generate/banners
FASTAPI_KEY=your_api_key

# Queue
QUEUE_CONNECTION=database

# Broadcasting (Real-time)
PUSHER_APP_ID=1975399
PUSHER_APP_KEY=2e6b262dbb81b1356260
PUSHER_APP_SECRET=cc237fe4875f4039fa58
PUSHER_APP_CLUSTER=ap1

# Google OAuth
GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=xxx
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback

# Mail
MAIL_MAILER=smtp
MAIL_HOST=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
```

---

## 🔧 TROUBLESHOOTING

### **Problem: Queue job không chạy**

```bash
# Check if queue worker is running
ps aux | grep queue:work

# Start queue worker
php artisan queue:work

# Check failed jobs
php artisan queue:failed
```

### **Problem: Banner không được tạo**

```bash
# Check logs
tail -f storage/logs/laravel.log

# Test FastAPI connection
curl -X POST http://localhost:8888/generate/banners \
  -H "API-Key: your_key" \
  -d "description=test&theme=bright"

# Check queue status
php artisan queue:failed
```

### **Problem: Real-time notification không hoạt động**

```bash
# Restart Pusher/Reverb server
php artisan reverb:start

# Check broadcasting config
php artisan config:cache
```

---

## 📖 TÀI LIỆU THAM KHẢO

- **Laravel**: https://laravel.com/docs/12
- **Vue.js**: https://vuejs.org/
- **Vite**: https://vitejs.dev/
- **Pusher**: https://pusher.com/docs
- **FastAPI**: https://fastapi.tiangolo.com/

---

## 👨‍💼 NGƯỜI PHÁT TRIỂN

- **Framework**: Laravel 12
- **Phiên bản**: 12.3.0
- **Ngôn ngữ**: Vietnamese (Tiếng Việt)
- **Last Updated**: 10/02/2026

---

## ⚠️ LƯU Ý QUAN TRỌNG

1. **Cập nhật `.env`** với thông tin FastAPI, Pusher, Google OAuth
2. **Chạy migrations** trước khi sử dụng: `php artisan migrate`
3. **Khởi động queue worker** để xử lý job: `php artisan queue:work`
4. **Kiểm tra logs** khi có lỗi: `storage/logs/laravel.log`
5. **Sử dụng HTTPS** trong production
6. **Backup database** định kỳ

---

**END OF DOCUMENT**

---

_Tài liệu này được tạo để hỗ trợ hiểu biết toàn diện về dự án Banner AI Generator.
Nếu có câu hỏi hoặc cần thêm thông tin chi tiết, vui lòng tham khảo documentation chính thức._
