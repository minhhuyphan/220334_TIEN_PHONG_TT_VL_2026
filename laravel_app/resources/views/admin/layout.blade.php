<!doctype html>
<html lang="en">

<head>
  @include('admin.components.head')
</head>

<body>
  <!--  Body Wrapper -->
  <div class="page-wrapper" id="main-wrapper" data-layout="vertical" data-navbarbg="skin6" data-sidebartype="full"
    data-sidebar-position="fixed" data-header-position="fixed">
    <!-- Sidebar -->
    @include('admin.components.sidebar')
    <!--  Main wrapper -->
    <div class="body-wrapper">
      <!--  Header -->
      @include('admin.components.nav')
      <!-- Body -->
      @include($template)
    </div>
  </div>
  @include('admin.components.script')
</body>

</html>