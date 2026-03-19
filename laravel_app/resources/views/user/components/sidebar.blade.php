<div class="brand-logo d-flex align-items-center justify-content-between p-0 mt-3">
    <a href="{{ route('homepage') }}" class="text-nowrap logo-img">
        <img src="{{ asset($logo ?? 'assets/images/logos/logo.png') }}" style="width: 200px;" alt="Logo" />
    </a>
    <a href="{{ route('homepage') }}" class="btn btn-light fs-4"><i class="fa fa-arrow-left mx-2"></i> Quay lại</a>
</div>

<nav class="sidebar-nav scroll-sidebar mt-4">
    <form id="bannerForm" class="row" method="POST" action="{{ route('create_banner_post') }}">
        @csrf
        <!-- Textarea cho mô tả -->
        <div class="mb-4">
            <label for="description" class="form-label">Mô tả</label>
            <textarea class="form-control color-input no-focus-effect @error('description') is-invalid @enderror" id="description" name="description" rows="6" placeholder="Để tạo banner chính xác hơn, bạn có thể cung cấp thông tin về màu sắc, hình ảnh, nội dung văn bản và phong cách thiết kế. Gợi ý: Tạo banner có hình ảnh sách, bút, bảng đen, học sinh cười vui. Có tiêu đề 'Chào mừng năm học mới'" spellcheck="false" required>{{ old('description', $description ?? '') }}</textarea>
            @error('description')
            <div class="invalid-feedback">{{ $message }}</div>
            @enderror
        </div>

        <!-- Chiều dài và chiều rộng (trên cùng 1 dòng) -->
        <div class="mb-3">
            <label for="width" class="form-label">Chiều rộng</label>
            <input type="number" class="px-4 form-control color-input no-focus-effect @error('width') is-invalid @enderror" id="width" name="width" step="1" value="{{ old('width', 800) }}" min="320" max="1536" placeholder="Chiều rộng" required>
            @error('width')
            <div class="invalid-feedback">{{ $message }}</div>
            @enderror
        </div>

        <div class="mb-3">
            <label for="height" class="form-label">Chiều cao</label>
            <input type="number" class="px-4 form-control color-input no-focus-effect @error('height') is-invalid @enderror" id="height" name="height" step="1" value="{{ old('height', 350) }}" min="320" max="1536" placeholder="Chiều dài" required>
            @error('height')
            <div class="invalid-feedback">{{ $message }}</div>
            @enderror
        </div>

        <!-- Số lượng -->
        <div class="mb-5">
            <label for="number" class="form-label">Số lượng</label>
            <input type="number" class="px-4 form-control color-input no-focus-effect @error('number') is-invalid @enderror" id="number" name="number" step="1" value="{{ old('number', 1) }}" min="1" max="4" placeholder="Số lượng" required>
            @error('number')
            <div class="invalid-feedback">{{ $message }}</div>
            @enderror
        </div>

        
        <!-- Nút tạo banner -->
        <div class="col-12">
            <button type="submit" class="btn w-100 text-white p-3 btn-create-banner" id="createBannerBtn"><i class="ti ti-wand mx-2 fs-6"></i> TẠO BANNER</button>
        </div>
    </form>
</nav>


<style>
    .color-input {
        box-sizing: border-box;
        background-color: rgba(22, 22, 25, 0);
        background-image: linear-gradient(90deg, #fff, #fff), linear-gradient(86deg, #fcac23 15%, #cd34ff 99%);
        background-clip: padding-box, border-box;
        background-origin: padding-box, border-box;
        border: 2px solid transparent;
        border-radius: .5rem;
        font-weight: bold;
    }

    .no-focus-effect:focus {
        box-sizing: border-box;
        background-color: rgba(22, 22, 25, 0);
        background-image: linear-gradient(90deg, #fff, #fff), linear-gradient(86deg, #fcac23 15%, #cd34ff 99%);
        background-clip: padding-box, border-box;
        background-origin: padding-box, border-box;
        border: 2px solid transparent;
        border-radius: .5rem;
    }

    .btn-create-banner {
        background: linear-gradient(122deg, rgb(250, 85, 96) 0.01%, rgb(177, 75, 244) 49.9%, rgb(77, 145, 255) 100%);
        font-weight: bold;
        border: none;
    }
</style>

<script>
    document.addEventListener('DOMContentLoaded', function() {
        const form = document.getElementById('bannerForm');
        const submitBtn = document.getElementById('createBannerBtn');

        // Khóa nút khi submit form
        form.addEventListener('submit', function(event) {
            localStorage.setItem('bannerCreating', '1'); // Lưu vào localStorage
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<div class="spinner-grow fs-6" role="status"></div>';
        });

        // Khi load lại trang, kiểm tra trạng thái
        if (localStorage.getItem('bannerCreating') === '1') {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<div class="spinner-grow fs-6" role="status"></div>';
        }

        // Lắng nghe sự kiện BannerJobCompleted để mở khóa nút
        Echo.channel('banner-job.{{ auth()->user()->id }}')
            .listen('.BannerJobCompleted', (e) => {
                console.log('Banner job completed:', e);
                // Mở khóa nút và khôi phục nội dung
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="ti ti-wand mx-2 fs-6"></i> TẠO BANNER';
                localStorage.removeItem('bannerCreating'); // Xóa trạng thái đang tạo
            });
    });
</script>