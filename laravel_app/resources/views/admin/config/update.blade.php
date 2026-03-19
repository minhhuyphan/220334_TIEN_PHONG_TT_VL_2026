<div class="container-fluid">
    <div class="row">
        <div class="col-12">
            <h3 class="mb-4">THÔNG TIN CẤU HÌNH</h3>
            <!-- Hiển thị thông báo -->
            @if (session('success'))
            <div class="alert alert-success alert-dismissible fade show" role="alert">
                {{ session('success') }}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
            @endif
            <form method="POST" action="{{ route('config_update', $config->id) }}" enctype="multipart/form-data">
                @csrf
                @method('PUT')

                <div class="mb-3">
                    <label for="config_key" class="form-label">Tên cấu hình</label>
                    <input type="text" class="form-control" id="config_key" value="{{ $config->config_key }}" disabled>
                </div>

                <!-- Kiểm tra xem giá trị $config->config_key có nằm trong mảng ['favicon', 'logo', 'hero_image'] hay không -->
                @php
                $isImageConfig = in_array($config->config_key, ['favicon', 'logo', 'hero_image']);
                @endphp

                <div class="mb-3">
                    <label for="config_value" class="form-label">Giá trị</label>
                    <input type="text"
                        class="mb-3 form-control @error('config_value') is-invalid @enderror"
                        id="config_value" name="config_value"
                        value="{{ old('config_value', $config->config_value) }}"
                        @if ($isImageConfig)
                        disabled
                        @else
                        required
                        @endif>
                    @if ($isImageConfig)
                    <!-- Hiển thị ảnh cũ nếu tồn tại -->
                    @if ($config->config_value && file_exists(public_path($config->config_value)))
                    <div class="my-4">
                        <label class="form-label">Ảnh cũ:</label>
                        <img src="{{ asset($config->config_value) }}" alt="Ảnh cũ" class="img-fluid img-thumbnail" style="max-width: 150px; max-height: 150px;">
                    </div>
                    @endif
                    <!-- Input file để chọn ảnh mới -->
                    <div class="my-4">
                        <label for="image" class="form-label">Chọn ảnh mới:</label>
                        <input type="file" class="form-control @error('image') is-invalid @enderror" id="image" name="image">
                        @error('image')
                        <div class="invalid-feedback">{{ $message }}</div>
                        @endif
                    </div>
                    <!-- Hiển thị ảnh mới sau khi chọn (preview) -->
                    <div class="my-4" id="imagePreview"></div>
                    @endif
                    @error('config_value')
                    <div class="invalid-feedback">{{ $message }}</div>
                    @endif
                </div>

                <div class="mb-3">
                    <label for="description" class="form-label">Mô tả</label>
                    <textarea class="form-control @error('description') is-invalid @enderror" id="description" name="description" rows="4" placeholder="Nhập mô tả" spellcheck="false">{{ old('description', $config->description) }}</textarea>
                    @error('description')
                    <div class="invalid-feedback">{{ $message }}</div>
                    @enderror
                </div>

                <div class="d-flex justify-content-between mt-5">
                    <a href="{{ route('configs_get') }}" class="btn btn-secondary">QUAY LẠI</a>
                    <button type="submit" class="btn btn-success">CẬP NHẬT CẤU HÌNH</button>
                </div>
            </form>
        </div>
    </div>
</div>

<script>
    // JavaScript để preview ảnh mới khi chọn
    document.getElementById('image').addEventListener('change', function(e) {
        const preview = document.getElementById('imagePreview');
        preview.innerHTML = ''; // Xóa nội dung cũ

        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(event) {
                const img = document.createElement('img');
                img.src = event.target.result;
                img.alt = 'Ảnh mới';
                img.className = 'img-fluid img-thumbnail';
                img.style.maxWidth = '150px';
                img.style.maxHeight = '150px';
                preview.appendChild(document.createElement('label')).textContent = 'Ảnh mới:';
                preview.appendChild(img);
            };
            reader.readAsDataURL(file);
        }
    });
</script>