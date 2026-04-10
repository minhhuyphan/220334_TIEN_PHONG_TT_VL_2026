# HỒ SƠ PHÂN TÍCH KỸ THUẬT CHI TIẾT DỰ ÁN: BANNERAI STUDIO

## 1. Kiến trúc Hệ thống (System Architecture)

Dự án được xây dựng theo mô hình **Client-Server** hiện đại, tách biệt hoàn toàn giữa Frontend và Backend.

### 1.1. Sơ đồ luồng dữ liệu (Data Flow)
1. **Frontend (React)**: Gửi các yêu cầu (HTTP Requests) mang theo JWT Token.
2. **Backend (FastAPI)**: 
   - Kiểm tra xác thực qua Middleware.
   - Nhận yêu cầu tạo banner, đẩy vào **Queue (Task Manager)**.
   - Gọi **Gemini AI API** kết hợp với ảnh tham chiếu (Layering).
   - Xử lý ảnh bằng **Pillow/OpenCV**.
   - Lưu trữ song song: Local Storage + **Cloudinary**.
3. **Database (SQLite/MySQL)**: Lưu trữ trạng thái và lịch sử.

---

## 2. Cấu trúc Cơ sở dữ liệu (Database Schema)

Dưới đây là chi tiết các thực thể dữ liệu được định nghĩa trong `app/utils/database.py`:

### 2.1. Bảng `users` (Quản lý người dùng)
| Cột | Kiểu dữ liệu | Mô tả |
| :--- | :--- | :--- |
| `id` | INT (PK) | Định danh duy nhất |
| `email` | VARCHAR | Email đăng nhập (Unique) |
| `full_name` | VARCHAR | Tên hiển thị |
| `tokens` | REAL | Số dư token hiện tại (Mặc định tặng 5) |
| `is_admin` | BOOLEAN | Quyền quản trị |
| `google_id` | VARCHAR | Liên kết đăng nhập Google |

### 2.2. Bảng `banner_history` (Lịch sử tạo ảnh)
| Cột | Kiểu dữ liệu | Mô tả |
| :--- | :--- | :--- |
| `id` | INT (PK) | Định danh banner |
| `user_id` | INT (FK) | Liên kết tới bảng users |
| `request_description`| TEXT | Mô tả gốc của người dùng |
| `aspect_ratio` | VARCHAR | Tỷ lệ khung hình (16:9, 1:1, ...) |
| `image_url` | TEXT | Link ảnh (Cloudinary hoặc Local) |
| `prompt_used` | TEXT | Prompt AI cuối cùng (đã tối ưu) |
| `reference_images` | TEXT | Lưu JSON các ảnh tham chiếu đã dùng |

### 2.3. Bảng `payments` (Lịch sử nạp tiền)
| Cột | Kiểu dữ liệu | Mô tả |
| :--- | :--- | :--- |
| `id` | INT (PK) | Mã giao dịch |
| `payment_code` | VARCHAR | Mã chuyển khoản tự động (XOR encoded) |
| `status` | VARCHAR | Trạng thái: `pending`, `completed` |
| `amount_vnd` | INT | Số tiền nạp |
| `tokens_received` | REAL | Số token tương ứng |

---

## 3. Các Giải pháp Kỹ thuật Đặc biệt (Core Logic Deep-dive)

### 3.1. Thuật toán "Green Mask Technology" cho Text Layout
Hệ thống sử dụng file `app/utils/image_processing.py` để giải quyết bài toán khó nhất: **Làm sao để AI viết chữ đúng vị trí?**
- **Cơ chế**: Hệ thống tạo một ảnh "mồi" (Reference Image) có nền xanh lá cây thuần khiết (`#00FF00`).
- **Render chữ**: Chữ được vẽ lên nền xanh này bằng thư viện Pillow với các tính năng:
  - `add_text_overlay`: Tự động tính toán tọa độ (Center, Top, Bottom).
  - `create_text_reference_image`: Tự động ngắt dòng (Word wrap) và chọn font phù hợp.
- **AI Fusion**: Khi gửi ảnh này cho Gemini Imagen 3, hệ thống kèm theo lệnh: "Focus on the white text in the green area". AI sẽ bóc tách chữ và vẽ lại một cách nghệ thuật nhất.

### 3.2. Hệ thống Background Task & Polling
Vì AI sinh ảnh mất từ 10-30 giây, hệ thống không để người dùng chờ đợi (block request):
- **Backend**: Nhận request -> Trả về `task_id` ngay lập tức -> Đẩy xử lý vào `ram_task_manager.py`.
- **Frontend**: Trong file `App.tsx`, có một useEffect lắng nghe `current_banner_task_id`. Nếu có, nó sẽ gọi API `/tasks/{id}` liên tục:
  - Nếu `status == 'processing'`: Hiển thị animation AI đang thiết kế.
  - Nếu `status == 'completed'`: Tải ảnh về và thông báo qua `react-hot-toast`.

### 3.3. Bảo mật & Thanh toán XOR
- **Mã hóa thanh toán**: Trong `payment.py`, hệ thống dùng một `SECRET_XOR_KEY` để biến đổi `payment_id` thành một mã HEX khó đoán. Điều này ngăn chặn việc người dùng đoán mã nạp tiền của người khác.
- **Sepay Integration**: Webhook/API check tự động khớp nội dung chuyển khoản với `payment_code` trong DB để cộng tiền tự động 24/7.

---

## 4. Tài liệu API (API Endpoints)

Hệ thống cung cấp bộ API chuẩn RESTful tại prefix `/api/v1`:

### 4.1. Nhóm Banner (`/generate`)
- `POST /banners`: Tạo nhiệm vụ sinh ảnh mới (Hỗ trợ multipart/form-data cho upload ảnh tham chiếu).
- `GET /tasks/{task_id}`: Kiểm tra trạng thái nhiệm vụ.
- `GET /history`: Lấy toàn bộ lịch sử ảnh của User.
- `GET /public-banners`: Lấy ảnh cho Gallery (không cần đăng nhập).
- `GET /view/{file_id}`: Xem/Tải ảnh trực tiếp.

### 4.2. Nhóm Auth & Admin
- `POST /auth/login`: Đăng nhập cấp JWT Token.
- `GET /admin/users`: Quản lý danh sách người dùng (Chỉ Admin).
- `POST /admin/config`: Thay đổi cấu hình hệ thống (Giá token, System Prompt).

---

## 5. Danh sách Công nghệ (Tech Stack Toàn diện)

| Thành phần | Công nghệ sử dụng |
| :--- | :--- |
| **Giao diện** | React 19, Vite, Tailwind CSS, Lucide |
| **Logic Frontend** | TypeScript, React Router 6, Recharts |
| **Server** | FastAPI, Uvicorn, Python 3.12 |
| **Xử lý ảnh** | Pillow, OpenCV, Rembg, Cloudinary SDK |
| **AI** | Gemini 3.1 Flash, Imagen 3, LangChain |
| **Cơ sở dữ liệu** | SQLAlchemy, SQLite, MySQL |
| **DevOps** | Docker, Docker Compose, Nginx |

---

## 6. Các điểm nhấn để viết báo cáo (Key Selling Points)
1. **Khả năng điều khiển AI**: Không chỉ là prompt thô, mà có sự can thiệp của thuật toán xử lý ảnh truyền thống để tối ưu kết quả (Hybrid AI).
2. **Trải nghiệm người dùng**: Tích hợp Voice-to-Text và cơ chế @-mention như mạng xã hội để tham chiếu hình ảnh.
3. **Tính sẵn sàng cao**: Hệ thống có khả năng tự phục hồi task bị lỗi khi restart server.
4. **Mô hình kinh doanh hoàn chỉnh**: Có sẵn hệ thống nạp tiền, quản lý gói dịch vụ và thống kê doanh thu.

---
*Tài liệu này được trích xuất trực tiếp từ cấu trúc logic của dự án 220334_TIEN_PHONG.*
