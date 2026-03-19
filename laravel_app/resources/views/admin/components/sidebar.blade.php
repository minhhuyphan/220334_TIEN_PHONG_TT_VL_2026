<aside class="left-sidebar">
    <!-- Sidebar scroll-->
    <div>
        <div class="brand-logo d-flex align-items-center justify-content-between">
            <a href=" {{ route('dashboard_get') }} " class="text-nowrap logo-img mt-3">
                <img src="{{ asset($logo ?? 'assets/images/logos/logo.png') }}" style="width: 200px;" alt="Logo" />
            </a>
        </div>
        <!-- Sidebar navigation-->
        <nav class="sidebar-nav scroll-sidebar" data-simplebar="">
            <ul id="sidebarnav">
                <li class="nav-small-cap">
                    <i class="ti ti-dots nav-small-cap-icon fs-4"></i>
                    <span class="hide-menu">Home</span>
                </li>
                <li class="sidebar-item">
                    <a class="sidebar-link" href=" {{ route('dashboard_get') }}" aria-expanded="false">
                        <span>
                            <i class="ti ti-layout-dashboard"></i>
                        </span>
                        <span class="hide-menu">Thống kê</span>
                    </a>
                </li>
                <li class="nav-small-cap">
                    <i class="ti ti-dots nav-small-cap-icon fs-4"></i>
                    <span class="hide-menu">Quản lý danh mục</span>
                </li>
                <li class="sidebar-item">
                    <a class="sidebar-link" href="{{ route('user_table_get') }}" aria-expanded="false">
                        <span>
                            <i class="ti ti-user"></i>
                        </span>
                        <span class="hide-menu">Nhóm người dùng</span>
                    </a>
                </li>
                <li class="sidebar-item">
                    <a class="sidebar-link" href="{{ route('admin_table_get') }}" aria-expanded="false">
                        <span>
                            <i class="ti ti-user"></i>
                        </span>
                        <span class="hide-menu">Nhóm quản trị</span>
                    </a>
                </li>

                <li class="nav-small-cap">
                    <i class="ti ti-dots nav-small-cap-icon fs-4"></i>
                    <span class="hide-menu">QUẢN LÝ THÔNG TIN</span>
                </li>
                <li class="sidebar-item">
                    <a class="sidebar-link" href=" {{ route('models_get') }} " aria-expanded="false">
                        <span>
                            <i class="ti ti-key"></i>
                        </span>
                        <span class="hide-menu">Quản lý model</span>
                    </a>
                </li>
                <li class="sidebar-item">
                    <a class="sidebar-link" href=" {{ route('configs_get') }} " aria-expanded="false">
                        <span>
                            <i class="ti ti-share"></i>
                        </span>
                        <span class="hide-menu">Cấu hình website</span>
                    </a>
                </li>

                <li class="nav-small-cap">
                    <i class="ti ti-dots nav-small-cap-icon fs-4"></i>
                    <span class="hide-menu">CÀI ĐẶT</span>
                </li>
                <li class="sidebar-item">
                    <form method="POST" action="{{ route('logout_post') }}" aria-expanded="false">
                        @csrf
                        <button type="submit" class="sidebar-link btn btn-transparent border-0">
                            <span><i class="ti ti-logout"></i></span>
                            <span class="hide-menu">Đăng xuất</span>
                        </button>
                    </form>
                </li>
            </ul>
        </nav>
        <!-- End Sidebar navigation -->
    </div>
    <!-- End Sidebar scroll-->
</aside>