<footer id="footer" class="footer position-relative light-background mt-4">

    <div class="container footer-top">
        <div class="row gy-4">
            <div class="col-lg-4 col-md-6 footer-about">
                <a href="index.html" class="logo d-flex align-items-center">
                    <span class="sitename">{{ $configs['name'] ?? 'Banner Blitz' }}</span>
                </a>
                <div class="footer-contact pt-3">
                    <p>{{ $configs['address'] ?? 'A108 Adam Street New York, NY 535022' }}</p>
                    <p class="mt-3"><strong>Phone:</strong> <span>{{ $configs['phone'] ?? '+1 5589 55488 55' }}</span></p>
                    <p><strong>Email:</strong> <span>{{ $configs['email'] ?? 'info@example.com' }}</span></p>
                </div>
                <div class="social-links d-flex mt-4">
                    <a href=""><i class="bi bi-twitter-x"></i></a>
                    <a href=""><i class="bi bi-facebook"></i></a>
                    <a href=""><i class="bi bi-instagram"></i></a>
                    <a href=""><i class="bi bi-linkedin"></i></a>
                </div>
            </div>

            <div class="col-lg-4 col-md-3 footer-links">
                <h4>Liên kết hữu ích</h4>
                <ul>
                    <li><a href="{{ route('homepage') }}">Trang chủ</a></li>
                    <li><a href="{{ route('load_site_about') }}">Về chúng tôi</a></li>
                    <li><a href="#">Dịch vụ</a></li>
                    <li><a href="#">Điều khoản dịch vụ</a></li>
                    <li><a href="#">Chính sách bảo mật</a></li>
                </ul>
            </div>

            <div class="col-lg-4 col-md-3 footer-links">
                <h4>Dịch vụ của chúng tôi</h4>
                <ul>
                    <li><a href="#">Web Design</a></li>
                    <li><a href="#">Web Development</a></li>
                    <li><a href="#">Product Management</a></li>
                    <li><a href="#">Marketing</a></li>
                    <li><a href="#">Graphic Design</a></li>
                </ul>
            </div>

            <!-- <div class="col-lg-4 col-md-12 footer-newsletter">
                <h4>Bản tin của chúng tôi</h4>
                <p>Đăng ký nhận bản tin của chúng tôi và nhận tin tức mới nhất về sản phẩm và dịch vụ của chúng tôi!</p>
                <form action="forms/newsletter.php" method="post" class="php-email-form">
                    <div class="newsletter-form"><input type="email" name="email"><input type="submit" value="Subscribe"></div>
                    <div class="loading">Loading</div>
                    <div class="error-message"></div>
                    <div class="sent-message">Yêu cầu đăng ký của bạn đã được gửi. Cảm ơn bạn!</div>
                </form>
            </div> -->

        </div>
    </div>
</footer>