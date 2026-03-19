<header class="app-header" style="position: fixed; right: 0; ">
    <nav class="navbar navbar-expand-lg navbar-light">
        <div class="navbar-collapse justify-content-end px-0" id="navbarNav">
            <ul class="navbar-nav flex-row ms-auto align-items-center justify-content-end">
                <li class="nav-item dropdown">
                    <a class="nav-link nav-icon-hover" href="javascript:void(0)" id="drop2" data-bs-toggle="dropdown"
                        aria-expanded="false">
                        <img src="{{ asset('assets/images/profile/user-1.jpg') }}" width=" 35" height="35" class="rounded-circle">
                    </a>
                    <div class="dropdown-menu dropdown-menu-end dropdown-menu-animate-up" aria-labelledby="drop2">
                        <div class="message-body">
                            <a href="{{ route('info_user_get', Auth::user()->id) }}" class="d-flex align-items-center gap-2 dropdown-item">
                                <i class="ti ti-user fs-6"></i>
                                <p class="mb-0 fs-3">Thông tin cá nhân</p>
                            </a>
                            <form method="POST" action="{{ route('logout_post') }}">
                                @csrf
                                <button type="submit" class="d-flex align-items-center gap-2 dropdown-item">
                                    <i class="ti ti-logout fs-6"></i>
                                    <p class="mb-0 fs-3">Đăng xuất</p>
                                </button>
                            </form>
                        </div>
                    </div>
                </li>
            </ul>
        </div>
    </nav>
</header>