<div class="container-fluid">
    <div class="row">
        <div class="col-12">
            @if (session('success'))
            <div class="alert alert-success alert-dismissible fade show" role="alert">
                {{ session('success') }}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
            @endif
            <h3 class="text-center mb-4">THÔNG TIN QUẢN TRỊ VIÊN</h3>
            <form method="POST" action="{{ route('add_admin_post') }}">
                @csrf
                <div class="mb-3">
                    <label for="username" class="form-label">Name</label>
                    <input type="text" class="form-control {{ $errors->has('username') ? 'is-invalid' : '' }}" id="username" name="username" required>
                    @if ($errors->has('username'))
                    <div class="invalid-feedback">
                        {{ $errors->first('username') }}
                    </div>
                    @endif
                </div>
                <div class="mb-3">
                    <label for="phone_number" class="form-label">Phone number</label>
                    <input type="tel" class="form-control {{ $errors->has('phone_number') ? 'is-invalid' : '' }}" id="phone_number" name="phone_number" required>
                    @if ($errors->has('phone_number'))
                    <div class="invalid-feedback">
                        {{ $errors->first('phone_number') }}
                    </div>
                    @endif
                </div>
                <div class="mb-3">
                    <label for="address" class="form-label">Address</label>
                    <input type="text" class="form-control {{ $errors->has('address') ? 'is-invalid' : '' }}" id="address" name="address" required>
                    @if ($errors->has('address'))
                    <div class="invalid-feedback">
                        {{ $errors->first('address') }}
                    </div>
                    @endif
                </div>
                <div class="mb-3">
                    <label for="email" class="form-label">Email</label>
                    <input type="email" class="form-control {{ $errors->has('email') ? 'is-invalid' : '' }}" id="email" name="email" required>
                    @if ($errors->has('email'))
                    <div class="invalid-feedback">
                        {{ $errors->first('email') }}
                    </div>
                    @endif
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label">Password</label>
                    <input type="password" class="form-control {{ $errors->has('password') ? 'is-invalid' : '' }}" id="password" name="password" required>
                    @if ($errors->has('password'))
                    <div class="invalid-feedback">
                        {{ $errors->first('password') }}
                    </div>
                    @endif
                </div>
                <div class="mb-3">
                    <label for="password_confirmation" class="form-label">Confirm Password</label>
                    <input type="password" class="form-control {{ $errors->has('password_confirmation') ? 'is-invalid' : '' }}" id="password_confirmation" name="password_confirmation" required>
                    @if ($errors->has('password_confirmation'))
                    <div class="invalid-feedback">
                        {{ $errors->first('password_confirmation') }}
                    </div>
                    @endif
                </div>
                <div class="d-flex justify-content-between mt-5">
                    <a href="{{ route('admin_table_get') }}" class="btn btn-secondary">QUAY LẠI</a>
                    <button type="submit" class="btn btn-success">THÊM QUẢN TRỊ VIÊN</button>
                </div>
            </form>
        </div>
    </div>
</div>