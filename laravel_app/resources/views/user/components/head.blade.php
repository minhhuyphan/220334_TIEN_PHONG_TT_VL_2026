<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="csrf-token" content="{{ csrf_token() }}">
<title>Banner Blitz - {{ $title }}</title>
<!-- Favicons -->
<link href="{{ asset($favicon ?? 'assets/images/favicon.png') }}" rel="icon">

<!-- Sử dụng các directive để tạo thẻ meta chuẩn SEO. -->
<!-- @seoTitle($title ?? 'Trang Chủ')
@seoDescription($description ?? 'Mô tả trang chủ')
@seoKeywords($keywords ?? 'từ khóa, laravel')
@seoOgTitle($title ?? 'Trang Chủ')
@seoOgDescription($description ?? 'Mô tả trang chủ')
@seoOgImage(asset('images/og-image.jpg'))
@seoOgUrl(url()->current())
@seoOgType('website') -->

<link rel="stylesheet" href="{{ asset('build/assets/app-isrLMXsH.css') }}" />
<link rel="stylesheet" href="{{ asset('assets/css/styles.min.css') }}" />
<!-- Datatable js -->
<link rel="stylesheet" href="//cdn.datatables.net/2.2.2/css/dataTables.dataTables.min.css" />
<link rel="stylesheet" href="https://cdn.datatables.net/buttons/3.2.0/css/buttons.dataTables.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">

<style>
    /* Container bao quanh ảnh */
    .image-container {
        position: relative;
    }

    /* Khi hover vào container, hiển thị con trỏ click */
    .image-container:hover {
        cursor: pointer;
    }

    /* Lớp phủ icon */
    .icon-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.4);
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    /* Hiển thị khi hover */
    .image-container:hover .icon-overlay {
        opacity: 1;
    }

    /* Style cho icon */
    .icon-style {
        font-size: 24px;
        color: white;
        background: rgba(255, 255, 255, 0.2);
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .icon-style:hover {
        background: rgba(255, 255, 255, 0.4);
        color: white;
    }

    .loading-placeholder {
        z-index: 2;
        background: #f8f9fa;
    }

    .main-image {
        display: block;
        width: 100%;
        height: auto;
        z-index: 1;
    }

    /* Mobile: ngăn tương tác khi chưa hiện */
    @media (max-width: 768px) {
        .icon-overlay {
            pointer-events: none;
        }

        .icon-overlay.active {
            opacity: 1 !important;
            pointer-events: auto !important;
        }
    }
    
</style>