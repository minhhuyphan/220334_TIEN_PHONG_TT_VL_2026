<!doctype html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Banner Blitz - Đăng ký</title>
  <!-- Favicons -->
  <link href="{{ asset($favicon ?? 'assets/images/favicon.png') }}" rel="icon">
  <!-- CSS -->
  <link rel="stylesheet" href="{{ asset('assets/css/styles.min.css') }}" />

  <style>
    .btn-auth {
      background: linear-gradient(122deg, rgb(250, 85, 96) 0.01%, rgb(177, 75, 244) 49.9%, rgb(77, 145, 255) 100%);
      font-weight: bold;
    }
  </style>
</head>

<body>
  <!--  Body Wrapper -->
  <div class="page-wrapper" id="main-wrapper" data-layout="vertical" data-navbarbg="skin6" data-sidebartype="full"
    data-sidebar-position="fixed" data-header-position="fixed">
    <div
      class="position-relative overflow-hidden radial-gradient min-vh-100 d-flex align-items-center justify-content-center">
      <div class="d-flex align-items-center justify-content-center w-100">
        <div class="row justify-content-center w-100">
          <div class="col-md-8 col-lg-6 col-xxl-3">
            <div class="card mb-0">
              <div class="card-body">
                <div class="text-nowrap logo-img text-center d-block py-3 w-100 mb-3">
                  <img src="{{ asset($logo ?? 'assets/images/logos/logo.png') }}" style="width: 200px;" alt="Logo">
                </div>
                @if (session('status'))
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                  {{ session('status') }}
                  <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
                @endif
                <form method="POST" action="{{ route('register_post') }}">
                  @csrf
                  <div class="mb-3">
                    <label for="username" class="form-label">Tên người dùng</label>
                    <input type="text" class="form-control" id="username" name="username" require>
                    @error('username')
                    <span class="text-danger">{{ $message }}</span>
                    @enderror
                  </div>
                  <div class="mb-3">
                    <label for="email" class="form-label">Email</label>
                    <input type="email" class="form-control" id="email" name="email" require>
                    @error('email')
                    <span class="text-danger">{{ $message }}</span>
                    @enderror
                  </div>
                  <div class="mb-3">
                    <label for="password" class="form-label">Mật khẩu</label>
                    <input type="password" class="form-control" id="password" name="password" require>
                    @error('password')
                    <span class="text-danger">{{ $message }}</span>
                    @enderror
                  </div>
                  <div class="mb-4">
                    <label for="password_confirmation" class="form-label">Xác nhận mật khẩu</label>
                    <input type="password" class="form-control" id="password_confirmation" name="password_confirmation" require>
                  </div>
                  <button type="submit" class="btn btn-auth text-white w-100 py-8 fs-4 mb-4">Đăng ký</button>
                  <div class="d-flex align-items-center justify-content-center mb-4">
                    <p class="fs-4 mb-0 fw-bold">Bạn đã có tài khoản?</p>
                    <a class="text-primary fw-bold ms-2" href="{{ route('login') }}">Đăng nhập</a>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <script src="{{ asset('assets/libs/jquery/dist/jquery.min.js') }}"></script>
  <script src="{{ asset('assets/libs/bootstrap/dist/js/bootstrap.bundle.min.js') }}"></script>
</body>

</html>