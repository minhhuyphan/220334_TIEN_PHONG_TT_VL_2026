<header id="header" class="header d-flex align-items-center sticky-top">
    <div class="container-fluid container-xl position-relative d-flex align-items-center">

        <a href="{{ route('homepage') }}" class="logo d-flex align-items-center me-auto">
            <!-- Uncomment the line below if you also wish to use an image logo -->
            <img src="{{ asset($configs['logo'] ?? 'assets/images/logos/logo.png') }}" style="width: 200px;" alt="Logo">
        </a>

        <nav id="navmenu" class="navmenu">
            <ul>
                <li><a href="{{ route('homepage') }}" class="{{ request()->routeIs('homepage') ? 'active' : '' }}">Trang chủ</a></li>
                <li><a href="{{ route('load_site_about') }}" class="{{ request()->routeIs('load_site_about') ? 'active' : '' }}">Về chúng tôi</a></li>
                <!-- <li><a href="{{ route('load_site_pricing') }}" class="{{ request()->routeIs('load_site_pricing') ? 'active' : '' }}">Chi phí</a></li> -->
                <li><a href="{{ route('load_site_contact') }}" class="{{ request()->routeIs('load_site_contact') ? 'active' : '' }}">Liên hệ</a></li>
                <li><a href="{{ route('load_view_create_banners') }}" class="{{ request()->routeIs('load_view_create_banners') ? 'active' : '' }}">Tạo banner</a></li>
            </ul>
            <i class="mobile-nav-toggle d-xl-none bi bi-list"></i>
        </nav>
        @if (Auth::check())
        <div class="mx-4" id="navbarNav">
            <ul class="navbar-nav flex-row ms-auto align-items-center justify-content-end">
                <li class="nav-item dropdown">
                    <a class="nav-link nav-icon-hover" href="javascript:void(0)" id="drop2" data-bs-toggle="dropdown"
                        aria-expanded="false">
                        <img src="{{ asset('assets/images/profile/user-1.jpg') }}" width=" 35" height="35" class="rounded-circle">
                    </a>
                    <div class="dropdown-menu dropdown-menu-end dropdown-menu-animate-up" aria-labelledby="drop2">
                        <div class="message-body">
                            <a href="{{ route('info_user_get', Auth::user()->id) }}" class="d-flex align-items-center gap-2 dropdown-item">
                                <i class="fa fa-user fs-6"></i>
                                <p class="mb-0 fs-6">Thông tin cá nhân</p>
                            </a>
                            <form method="POST" action="{{ route('logout_post') }}">
                                @csrf
                                <button type="submit" class="d-flex align-items-center gap-2 dropdown-item">
                                    <i class="fa fa-sign-out fs-6"></i>
                                    <p class="mb-0 fs-6">Đăng xuất</p>
                                </button>
                            </form>
                        </div>
                    </div>
                </li>
            </ul>
        </div>
        @else
        <a class="btn-getstarted" href="{{ route('login') }}">Đăng nhập</a>
        @endif

    </div>
</header>