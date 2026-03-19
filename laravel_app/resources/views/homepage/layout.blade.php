<!DOCTYPE html>
<html lang="en">

<head>
    @include('homepage.components.head')
</head>

<body class="index-page">

    @include('homepage.components.nav')

    @include($template)

    @include('homepage.components.foot')

    <!-- Scroll Top -->
    <a href="#" id="scroll-top" class="scroll-top d-flex align-items-center justify-content-center"><i class="bi bi-arrow-up-short"></i></a>

    <!-- Preloader -->
    <div id="preloader"></div>

    @include('homepage.components.script')

</body>

</html>