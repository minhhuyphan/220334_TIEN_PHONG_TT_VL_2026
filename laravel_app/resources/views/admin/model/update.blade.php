<div class="container-fluid">
    <div class="row">
        <div class="col-12">
            <h3 class="mb-4">THÔNG TIN MODEL</h3>
            <!-- Hiển thị thông báo -->
            @if (session('success'))
            <div class="alert alert-success alert-dismissible fade show" role="alert">
                {{ session('success') }}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
            @endif
            <form method="POST" action="{{ route('model_update', $model->id) }}">
                @csrf
                @method('PUT')

                <div class="mb-3">
                    <label for="model_name" class="form-label">Tên model</label>
                    <input type="text" class="form-control" id="model_name" value="{{ $model->model_name }}" disabled>
                </div>

                <div class="mb-3">
                    <label for="model_key" class="form-label">Key</label>
                    <input type="text" class="form-control @error('model_key') is-invalid @enderror" id="model_key" name="model_key" value="{{ old('model_key', $model->model_key) }}" required>
                    @error('model_key')
                    <div class="invalid-feedback">{{ $message }}</div>
                    @enderror
                </div>

                <div class="mb-3">
                    <label for="description" class="form-label">Mô tả</label>
                    <input type="text" class="form-control @error('description') is-invalid @enderror" id="description" name="description" value="{{ old('description', $model->description) }}" rows="4" placeholder="Nhập mô tả" spellcheck="false" required>
                    @error('description')
                    <div class="invalid-feedback">{{ $message }}</div>
                    @enderror
                </div>

                <div class="d-flex justify-content-between mt-5">
                    <a href="{{ route('models_get') }}" class="btn btn-secondary">QUAY LẠI</a>
                    <button type="submit" class="btn btn-success">CẬP NHẬT MODEL</button>
                </div>
            </form>
        </div>
    </div>
</div>