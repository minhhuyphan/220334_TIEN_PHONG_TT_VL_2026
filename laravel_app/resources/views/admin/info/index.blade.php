<div class="container-fluid">
    <div class="row">
        <div class="col-12">
      
            <h3 class="mb-4">THÔNG TIN CÁ NHÂN</h3>
            <form method="POST" action="{{ route('info_admin_update', $user->id) }}">
                @csrf
                <div class="mb-3">
                    <label for="username" class="form-label">Username</label>
                    <input type="text" class="form-control @error('username') is-invalid @enderror" id="username" name="username" value="{{ old('username', $user->username) }}">
                    @error('username')
                    <div class="invalid-feedback">{{ $message }}</div>
                    @enderror
                </div>

                <div class="mb-3">
                    <label for="phone_number" class="form-label">Phone Number</label>
                    <input type="text" class="form-control @error('phone_number') is-invalid @enderror" id="phone_number" name="phone_number" value="{{ old('phone_number', $user->phone_number) }}">
                    @error('phone_number')
                    <div class="invalid-feedback">{{ $message }}</div>
                    @enderror
                </div>

                <div class="mb-3">
                    <label for="address" class="form-label">Address</label>
                    <input type="text" class="form-control @error('address') is-invalid @enderror" id="address" name="address" value="{{ old('address', $user->address) }}">
                    @error('address')
                    <div class="invalid-feedback">{{ $message }}</div>
                    @enderror
                </div>

                <div class="mb-3">
                    <label for="status" class="form-label">Status</label>
                    <input type="text" class="form-control @error('status') is-invalid @enderror" id="status" name="status" value="{{ $user->status == 1 ? 'Đang hoạt động' : 'Đã khóa' }}" readonly>
                    @error('status')
                    <div class="invalid-feedback">{{ $message }}</div>
                    @enderror
                </div>

                <div class="mb-3">
                    <label for="email" class="form-label">Email</label>
                    <input type="email" class="form-control @error('email') is-invalid @enderror" id="email" name="email" value="{{ old('email', $user->email) }}">
                    @error('email')
                    <div class="invalid-feedback">{{ $message }}</div>
                    @enderror
                </div>

                <div class="mb-3">
                    <label for="password" class="form-label">Password</label>
                    <input type="password" class="form-control @error('password') is-invalid @enderror" id="password" name="password">
                    @error('password')
                    <div class="invalid-feedback">{{ $message }}</div>
                    @enderror
                </div>

                <div class="mb-3">
                    <label for="created_at" class="form-label">Created At</label>
                    <input type="text" class="form-control" id="created_at" value="{{ $user->created_at->format('d/m/Y') }}" readonly>
                </div>

                <div class="mb-3">
                    <label for="updated_at" class="form-label">Updated At</label>
                    <input type="text" class="form-control" id="updated_at" value="{{ $user->updated_at->format('d/m/Y') }}" readonly>
                </div>
                <div class="d-flex justify-content-between mt-5">
                    <a href="{{ route('dashboard_get') }}" class="btn btn-secondary">QUAY LẠI</a>
                    <button type="submit" class="btn btn-primary">CẬP NHẬT THÔNG TIN</button>
                </div>
                <!-- Hiển thị thông báo -->
                @if (session('success'))
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    {{ session('success') }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
                @endif
            </form>
        </div>
    </div>
</div>