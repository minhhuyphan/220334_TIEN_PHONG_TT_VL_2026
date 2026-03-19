<main class="main">

    <!-- Hero Section -->
    <section id="hero" class="hero section dark-background">

        <img src="{{ asset($configs['hero_image'] ??'assets/images/blog-detail.webp') }}" alt="Hero image" data-aos="fade-in">

        <div class="container">
            <h2 data-aos="fade-up" data-aos-delay="100">{{ $configs['hero_title'] ?? 'Từ ý tưởng đến banner - nhanh chóng, đẹp mắt, đúng mục tiêu' }}</h2>
            <p data-aos="fade-up" data-aos-delay="200">{{ $configs['hero_subtitle'] ?? 'Chỉ cần nhập nội dung, hệ thống lo phần còn lại' }}</p>
            <div class="d-flex mt-4" data-aos="fade-up" data-aos-delay="300">
                <a href="{{ route('load_view_create_banners') }}" class="btn-get-started fw-bold">Bắt đầu tạo banner</a>
            </div>
        </div>

    </section><!-- /Hero Section -->

    <!-- About Section -->
    <section id="about" class="about section">

        <div class="container">

            <div class="row gy-4">

                <div class="col-lg-6 order-1 order-lg-2" data-aos="fade-up" data-aos-delay="100">
                    <img src="{{ asset('assets/images/backgrounds/about-1.png') }}" class="img-fluid" alt="">
                </div>

                <div class="col-lg-6 order-2 order-lg-1 content" data-aos="fade-up" data-aos-delay="200">
                    <h3>Tập trung vào sự sáng tạo</h3>
                    <p class="fst-italic">Biến ý tưởng thành banner độc đáo với hệ thống của chúng tôi.
                    </p>
                    <ul>
                        <li><i class="bi bi-check-circle"></i> <span>Trải nghiệm giao diện thân thiện, dễ sử dụng.</span></li>
                        <li><i class="bi bi-check-circle"></i> <span>Sáng tạo không giới hạn, không cần kỹ năng thiết kế.</span></li>
                        <li><i class="bi bi-check-circle"></i> <span>Tùy chỉnh linh hoạt, từ ý tưởng đến thành phẩm.</span></li>
                        <li><i class="bi bi-check-circle"></i> <span>Tạo banner đẹp mắt chỉ trong tích tắc!</span></li>
                        <li><i class="bi bi-check-circle"></i> <span>Banner ấn tượng, sẵn sàng thu hút mọi ánh nhìn!</span></li>
                    </ul>
                    <a href="{{ route('load_site_about') }}" class="read-more"><span>Đọc thêm</span><i class="bi bi-arrow-right"></i></a>
                </div>

            </div>

        </div>

    </section><!-- /About Section -->


    <!-- Features Section -->
    <section id="features" class="features section">

        <div class="container">

            <div class="row gy-4">

                <div class="col-lg-3 col-md-4" data-aos="fade-up" data-aos-delay="100">
                    <div class="features-item">
                        <i class="bi bi-eye" style="color: #ffbb2c;"></i>
                        <h3><a href="#" class="stretched-link">Xem trước banner</a></h3>
                    </div>
                </div><!-- End Feature Item -->

                <div class="col-lg-3 col-md-4" data-aos="fade-up" data-aos-delay="200">
                    <div class="features-item">
                        <i class="bi bi-infinity" style="color: #5578ff;"></i>
                        <h3><a href="#" class="stretched-link">Prompt linh hoạt</a></h3>
                    </div>
                </div><!-- End Feature Item -->

                <div class="col-lg-3 col-md-4" data-aos="fade-up" data-aos-delay="300">
                    <div class="features-item">
                        <i class="bi bi-mortarboard" style="color: #e80368;"></i>
                        <h3><a href="#" class="stretched-link">Học hỏi AI nâng cao</a></h3>
                    </div>
                </div><!-- End Feature Item -->

                <div class="col-lg-3 col-md-4" data-aos="fade-up" data-aos-delay="400">
                    <div class="features-item">
                        <i class="bi bi-nut" style="color: #e361ff;"></i>
                        <h3><a href="#" class="stretched-link">Bảo mật dữ liệu</a></h3>
                    </div>
                </div><!-- End Feature Item -->

                <div class="col-lg-3 col-md-4" data-aos="fade-up" data-aos-delay="500">
                    <div class="features-item">
                        <i class="bi bi-shuffle" style="color: #47aeff;"></i>
                        <h3><a href="#" class="stretched-link">Tùy chọn đa dạng</a></h3>
                    </div>
                </div><!-- End Feature Item -->

                <div class="col-lg-3 col-md-4" data-aos="fade-up" data-aos-delay="600">
                    <div class="features-item">
                        <i class="bi bi-star" style="color: #ffa76e;"></i>
                        <h3><a href="#" class="stretched-link">Banner nổi bật</a></h3>
                    </div>
                </div><!-- End Feature Item -->


                <div class="col-lg-3 col-md-4" data-aos="fade-up" data-aos-delay="900">
                    <div class="features-item">
                        <i class="bi bi-command" style="color: #b2904f;"></i>
                        <h3><a href="#" class="stretched-link">Quản lý thông minh</a></h3>
                    </div>
                </div><!-- End Feature Item -->

                <div class="col-lg-3 col-md-4" data-aos="fade-up" data-aos-delay="1200">
                    <div class="features-item">
                        <i class="bi bi-brightness-high" style="color: #29cc61;"></i>
                        <h3><a href="#" class="stretched-link">Giao diện thân thiện</a></h3>
                    </div>
                </div><!-- End Feature Item -->

            </div>

        </div>

    </section><!-- /Features Section -->

    <!-- Courses Section -->
    @if(!$banners->isEmpty())
    <section id="courses" class="courses section">

        <!-- Section Title -->
        <div class="container section-title" data-aos="fade-up">
            <h2>Phổ biến</h2>
            <p>Sáng tạo của cộng đồng</p>
        </div><!-- End Section Title -->

        <div class="container">

            <div class="row overflow-auto vh-100">

                @foreach($banners as $banner)
                <div class="col-lg-4 col-md-6 d-flex align-items-stretch mb-4" data-aos="zoom-in" data-aos-delay="100">
                    <div class="course-item">
                        <!-- Hiển thị ảnh banner -->
                        <img src="{{ asset($banner->link_banner) }}" class="img-fluid" alt="Banner Image">

                        <div class="course-content">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <a href="{{ route('load_view_create_banners', ['description' => urlencode($banner->bannerDetail->description), 'theme' => urlencode($banner->bannerDetail->theme)]) }}" class="category">
                                    Tạo banner với mẫu này
                                </a>
                            </div>

                            <!-- Mô tả từ BannerDetail -->
                            <h3>Mô tả</h3>
                            <p class="description">{{ $banner->bannerDetail->description ?? 'Không có mô tả' }}</p>

                            <div class="trainer d-flex justify-content-between align-items-center">
                                <div class="trainer-profile d-flex align-items-center">
                                    <img src="{{ asset('assets/images/profile/user-1.jpg') }}" class="img-fluid" alt="">
                                    <p class="trainer-link">{{ $banner->bannerDetail->user->username ?? 'N/A' }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div> <!-- End Course Item-->
                @endforeach

            </div>

        </div>

    </section><!-- /Courses Section -->
    @endif

</main>