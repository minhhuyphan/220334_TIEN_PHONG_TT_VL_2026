  <script src="{{ asset('assets/libs/jquery/dist/jquery.min.js') }}"></script>
  <script src="{{ asset('assets/libs/bootstrap/dist/js/bootstrap.bundle.min.js') }}"></script>
  <script src="{{ asset('assets/js/sidebarmenu.js') }}"></script>
  <script src="{{ asset('assets/js/app.min.js') }}"></script>
  <script src="{{ asset('assets/libs/apexcharts/dist/apexcharts.min.js') }}"></script>
  <script src="{{ asset('assets/libs/simplebar/dist/simplebar.js') }}"></script>
  <script src="{{ asset('assets/js/dashboard.js') }}"></script>
  <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>

  <script>
    document.addEventListener('DOMContentLoaded', function() {
      const containers = document.querySelectorAll('.image-container');

      containers.forEach(container => {
        const overlay = container.querySelector('.icon-overlay');

        container.addEventListener('click', function(e) {
          // Nếu đang active rồi, thì không toggle nữa
          const isActive = overlay.classList.contains('active');

          // Ẩn tất cả overlay khác
          document.querySelectorAll('.icon-overlay').forEach(o => o.classList.remove('active'));

          if (!isActive) {
            overlay.classList.add('active');
          }

          e.stopPropagation();
        });
      });

      // Chạm ngoài overlay thì ẩn tất cả
      document.addEventListener('click', function() {
        document.querySelectorAll('.icon-overlay').forEach(o => o.classList.remove('active'));
      });
    });
  </script>


  <script src="{{ asset('build/assets/app-DkQbcbQ4.js') }}" defer></script>