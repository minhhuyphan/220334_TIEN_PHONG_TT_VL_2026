@extends('user.layout')

@section('content')

<div class="container-fluid mt-5 overflow-auto vh-100" id="bannerList">
    <div class="row">
        <div class="col-12 mt-3">
            <!-- Chưa có banner nào. -->
            @if (empty($data))
            <div class="text-center mt-4">
                <h1 style=" background: linear-gradient(122deg, rgb(250, 85, 96) 0.01%, rgb(177, 75, 244) 49.9%, rgb(77, 145, 255) 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-size: 48px;
                font-weight: bold;">
                    TẠO NHỮNG BANNER CUỐN HÚT
                </h1>
            </div>

            @else
            <h3 style=" background: linear-gradient(122deg, rgb(250, 85, 96) 0.01%, rgb(177, 75, 244) 49.9%, rgb(77, 145, 255) 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-size: 24px;
                font-weight: bold;">BANNER ĐÃ ĐƯỢC TẠO</h3>
            @foreach ($data as $bannerDetail)
            <!-- THÔNG TIN BANNER -->
            <div class="card mt-4">
                <div class="card-header">
                    <div class="row">
                        <div class="col-md-12">
                            <label for="description_{{ $bannerDetail->id }}" class="form-label text-truncate">Mô tả</label>
                            <input type="text" class="form-control fs-4" id="description_{{ $bannerDetail->id }}" value="{{ $bannerDetail->description }}" readonly>
                        </div>
                    </div>
                    <div class="row mt-2">
                        <div class="col-md-2">
                            <label for="width_{{ $bannerDetail->id }}" class="form-label">Chiều dài</label>
                            <input type="text" class="form-control" id="width_{{ $bannerDetail->id }}" value="{{ $bannerDetail->width }}px" readonly>
                        </div>
                        <div class="col-md-2">
                            <label for="height_{{ $bannerDetail->id }}" class="form-label">Chiều cao</label>
                            <input type="text" class="form-control" id="height_{{ $bannerDetail->id }}" value="{{ $bannerDetail->height }}px" readonly>
                        </div>
                        <div class="col-md-2">
                            <label for="quantity_{{ $bannerDetail->id }}" class="form-label">Số lượng</label>
                            <input type="text" class="form-control" id="quantity_{{ $bannerDetail->id }}" value="{{ $bannerDetail->number }}" readonly>
                        </div>
                        <div class="col-md-2 mb-2">
                            <label for="created_at_{{ $bannerDetail->id }}" class="form-label">Ngày tạo</label>
                            <input type="text" class="form-control" id="created_at_{{ $bannerDetail->id }}" value="{{ $bannerDetail->created_at->format('d/m/Y') }}" readonly>
                        </div>
                        <div class=" col-md-2 d-flex pt-4">
                            <form class="align-self-center" id="delete-banner-details-form-{{ $bannerDetail->id }}" action="{{ route('banner_details_delete', $bannerDetail->id) }}" method="POST">
                                @csrf
                                @method('DELETE')
                                <button type="button" class="btn btn-outline-dark" onclick="confirmDeleteBannerDetails('{{ $bannerDetail->id }}')">
                                    <i class="ti ti-trash"></i> Xóa
                                </button>
                            </form>
                        </div>
                    </div>
                </div>

                <!-- BANNER -->
                <div class="card-body py-1">
                    <div class="row mt-3">

                        <!-- Banner bị lỗi -->
                        @if ($bannerDetail->status == -1)
                        @foreach ($bannerDetail->banners as $banner)
                        <div class="col-md-4 mb-3">
                            <div class="image-container position-relative">
                                <!-- Ảnh loading giả -->
                                <div class="loading-placeholder position-absolute top-0 start-0 w-100 h-100 bg-light d-flex justify-content-center align-items-center">
                                    <i class="fas fa-eye-slash fa-2x"></i>
                                </div>
                                <!-- Banner -->
                                <img src="{{ asset($banner->link_banner) }}"
                                    alt="Banner {{ $banner->id }}"
                                    class="img-fluid main-image img-{{ $banner->id }}"
                                    data-banner-id="{{ $banner->id }}">
                            </div>
                        </div>
                        @endforeach

                        <!-- Banner đang load -->
                        @elseif ($bannerDetail->status == 0)
                        @for ($i = 0; $i < $bannerDetail->number; $i++)
                            <div class="col-md-4 mb-3">
                                <div class="image-container position-relative">
                                    <!-- Ảnh loading giả -->
                                    <div class="loading-placeholder position-absolute top-0 start-0 w-100 h-100 bg-light d-flex justify-content-center align-items-center">
                                        <div class="spinner-border text-secondary" role="status"></div>
                                    </div>
                                    <!-- Banner -->
                                    <img src="{{ asset('assets\images\banners\Flux_Dev_An_artistic_representation_of_smart_devices_featuring_0.jpeg') }}"
                                        alt=""
                                        class="img-fluid main-image">
                                </div>
                            </div>
                            @endfor

                            <!-- Banner đã tạo -->
                            @elseif ($bannerDetail->status == 1)
                            @foreach ($bannerDetail->banners as $banner)
                            <div class="col-md-4 mb-3">
                                <div class="image-container">
                                    <img src="{{ asset($banner->link_banner) }}" alt="Banner {{ $banner->id }}" class="img-fluid">
                                    <div class="icon-overlay d-flex justify-content-center align-items-center">

                                        <!-- Edit banenr -->
                                        <a href="{{ route('edit_banner_get', $banner->id) }}" class="icon-style mx-2" title="Chỉnh sửa"><i class="ti ti-edit"></i></a>

                                        <!-- Download  -->
                                        <button class="icon-style mx-2 download-btn" data-image="{{ asset($banner->link_banner) }}" title="Tải về"><i class="ti ti-download"></i></button>

                                        <!-- Publish -->
                                        @if($banner->is_published)
                                        <form action="{{ route('banners_publish', $banner->id) }}" method="POST">
                                            @csrf
                                            @method('DELETE') <!-- Sử dụng DELETE để hủy công khai -->
                                            <button type="submit" class="icon-style mx-2" title="Hủy công khai"><i class="fa fa-close"></i></button>
                                        </form>
                                        @else
                                        <form action="{{ route('banners_publish', $banner->id) }}" method="POST">
                                            @csrf
                                            @method('PUT') <!-- Sử dụng PUT để công khai -->
                                            <button type="submit" class="icon-style mx-2" title="Công khai mẫu"><i class="fa fa-share-alt"></i></button>
                                        </form>
                                        @endif

                                        <!-- Delete -->
                                        <form id="delete-banner-form-{{ $banner->id }}" action="{{ route('banner_delete', $banner->id) }}" method="POST">
                                            @csrf
                                            @method('DELETE')
                                            <button type="button" class="icon-style mx-2" title="Xóa" onclick="confirmDeleteBanner('{{ $banner->id }}')"><i class="ti ti-trash"></i></button>
                                        </form>
                                    </div>
                                </div>
                            </div>
                            @endforeach
                            @endif
                    </div>
                </div>
            </div>
            @endforeach
            @endif
        </div>
    </div>
</div>
@section('scripts')
<script script>
    // Lắng nghe sự kiện BannerJobCompleted
    window.onload = function() {
        Echo.channel('banner-job.{{ auth()->user()->id }}')
            .listen('.BannerJobCompleted', (e) => {
                console.log('Banner job completed:', e);
                // Tải lại nội dung của #bannerList
                fetch('{{ route("load_view_create_banners") }}')
                    .then(response => response.text())
                    .then(html => {
                        const parser = new DOMParser();
                        const doc = parser.parseFromString(html, 'text/html');
                        const newBannerList = doc.querySelector('#bannerList');
                        if (newBannerList) {
                            document.querySelector('#bannerList').innerHTML = newBannerList.innerHTML;
                        }
                    })
                    .catch(error => console.error('Error reloading banner list:', error));
            });
    }
</script>


<!-- Download banenr -->
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const downloadButtons = document.querySelectorAll('.download-btn');
        downloadButtons.forEach(button => {
            button.addEventListener('click', function() {
                const imageUrl = this.getAttribute('data-image');
                const fileName = imageUrl.split('/').pop(); // tên file từ URL
                const link = document.createElement('a');
                link.href = imageUrl;
                link.download = fileName;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            });
        });
    });
</script>

@endsection
@endsection


<!-- Form xác nhận xóa banner details -->
<script>
    function confirmDeleteBannerDetails(id) {
        Swal.fire({
            title: 'Bạn có chắc chắn muốn?',
            text: 'Banner liên quan sẽ bị xóa!',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            confirmButtonText: 'Xóa',
            cancelButtonText: 'Hủy'
        }).then((result) => {
            if (result.isConfirmed) {
                document.getElementById(`delete-banner-details-form-${id}`).submit();
            }
        });
    }
</script>

<!-- Form xác nhận xóa banner -->
<script>
    function confirmDeleteBanner(id) {
        Swal.fire({
            title: 'Bạn có chắc chắn muốn?',
            text: 'Banner liên quan sẽ bị xóa!',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            confirmButtonText: 'Xóa',
            cancelButtonText: 'Hủy'
        }).then((result) => {
            if (result.isConfirmed) {
                document.getElementById(`delete-banner-form-${id}`).submit();
            }
        });
    }
</script>