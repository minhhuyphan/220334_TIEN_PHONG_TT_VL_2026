 <main class="main">

     <!-- Page Title -->
     <div class="page-title" data-aos="fade">
         <div class="heading">
             <div class="container">
                 <div class="row d-flex justify-content-center text-center">
                     <div class="col-lg-8">
                         <h1>Khám Phá Tạo Banner Tự Động<br></h1>
                         <p class="mb-0">Hệ thống Tạo Banner Tự Động của chúng tôi mang đến giải pháp sáng tạo nhanh chóng và tiện lợi. Với công nghệ hiện đại, bạn có thể thiết kế banner độc đáo chỉ trong vài bước. Không cần kỹ năng chuyên sâu, chỉ cần ý tưởng – chúng tôi sẽ biến nó thành hiện thực. Hãy trải nghiệm ngay hôm nay!</p>
                     </div>
                 </div>
             </div>
         </div>
         <nav class="breadcrumbs">
             <div class="container">
                 <ol>
                     <li><a href="{{ route('homepage') }}">Home</a></li>
                     <li class="current">About Us<br></li>
                 </ol>
             </div>
         </nav>
     </div><!-- End Page Title -->

     <!-- About Us Section -->
     <section id="about-us" class="section about-us">

         <div class="container">

             <div class="row gy-4">

                 <div class="col-lg-6 order-1 order-lg-2" data-aos="fade-up" data-aos-delay="100">
                     <img src="{{ asset('assets/images/backgrounds/about-1.png') }}" class="img-fluid" alt="">
                 </div>

                 <div class="col-lg-6 order-2 order-lg-1 content" data-aos="fade-up" data-aos-delay="200">
                     <h3>Tập trung vào sự sáng tạo và cá nhân hóa</h3>
                     <p class="fst-italic">Biến ý tưởng thành banner độc đáo với hệ thống của chúng tôi.
                     </p>
                     <ul>
                         <li><i class="bi bi-check-circle"></i> <span>Trải nghiệm giao diện thân thiện, dễ sử dụng.</span></li>
                         <li><i class="bi bi-check-circle"></i> <span>Sáng tạo không giới hạn, không cần kỹ năng thiết kế.</span></li>
                         <li><i class="bi bi-check-circle"></i> <span>Tùy chỉnh linh hoạt, từ ý tưởng đến thành phẩm.</span></li>
                         <li><i class="bi bi-check-circle"></i> <span>Tạo banner đẹp mắt chỉ trong tích tắc!</span></li>
                         <li><i class="bi bi-check-circle"></i> <span>Banner ấn tượng, sẵn sàng thu hút mọi ánh nhìn!</span></li>
                     </ul>
                 </div>

             </div>

         </div>

     </section><!-- /About Us Section -->

     <!-- Counts Section -->
     <section id="counts" class="section counts light-background">

         <div class="container" data-aos="fade-up" data-aos-delay="100">

             <div class="row gy-4">

                 <div class="col-lg-6 col-md-12">
                     <div class="stats-item text-center w-100 h-100">
                         <span data-purecounter-start="0" data-purecounter-end="{{ $userCount }}" data-purecounter-duration="1" class="purecounter"></span>
                         <p>Số lượng người dùng</p>
                     </div>
                 </div><!-- End Stats Item -->

                 <div class="col-lg-6 col-md-12">
                     <div class="stats-item text-center w-100 h-100">
                         <span data-purecounter-start="0" data-purecounter-end="{{ $bannerCount }}" data-purecounter-duration="1" class="purecounter"></span>
                         <p>Số lượng banner đã được tạo</p>
                     </div>
                 </div><!-- End Stats Item -->

             </div>

         </div>

     </section><!-- /Counts Section -->

 </main>