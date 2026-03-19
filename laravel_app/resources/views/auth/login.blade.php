<!doctype html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Banner Blitz - Đăng nhập</title>
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
                <form method="POST" action="{{ route('login_post') }}">
                  @csrf
                  <div class="mb-3">
                    <label for="email" class="form-label">Email</label>
                    <input type="email" class="form-control" name="email" id="email" require>
                  </div>
                  <div class="mb-4">
                    <label for="password" class="form-label">Mật khẩu</label>
                    <input type="password" class="form-control" name="password" id="password" require>
                  </div>
                  <div class="d-flex align-items-center justify-content-between mb-4">
                    <a class="text-primary fw-bold ms-2" href="{{ route('register_get') }}">Tạo tài khoản</a>
                    <a class="text-primary fw-bold" href="{{ route('password.request') }}">Quên mật khẩu ?</a>
                  </div>
                  <!-- Hiển thị lỗi chung nếu có -->
                  @if ($errors->any())
                  <div class="alert alert-danger">
                    <ul>
                      @foreach ($errors->all() as $error)
                      <li>{{ $error }}</li>
                      @endforeach
                    </ul>
                  </div>
                  @endif
                  <button type="submit" class="btn btn-auth text-white w-100 py-8 fs-4 mb-3">Đăng nhập</button>
                  <p class="text-center mb-3 fw-bold">Hoặc</p>
                  <a class="btn btn-light w-100 py-8 fs-4 mb-4 fw-bold d-flex justify-content-center align-items-center gap-2" href="{{ route('auth.google') }}">
                    <img src="../assets/images/logos/google.svg" alt="img">
                    <span>Google</span>
                  </a>
                  <a href="{{ route('homepage') }}" class="btn btn-light py-8 mb-4 w-100 fs-4">Hủy đăng nhập</a>
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