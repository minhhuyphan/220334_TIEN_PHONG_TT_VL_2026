<div class="container-fluid" id="bannerList">
    <div class="row">
        <div class="col-2 mb-4">
            <a href="{{ route('user_table_get') }}" class="btn btn-secondary">QUAY LẠI</a>
        </div>
        <div class="col-12">
            <!-- Chưa có banner nào. -->
            @if (empty($data))
            <div class="text-center mt-4">
                <h3 style=" background: linear-gradient(122deg, rgb(250, 85, 96) 0.01%, rgb(177, 75, 244) 49.9%, rgb(77, 145, 255) 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-size: 48px;
                font-weight: bold;">
                    CHƯA CÓ BANNER NÀO!
                </h3>
            </div>

            @else
            <h3>BANNER ĐÃ ĐƯỢC TẠO</h3>
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
                        <div class="col-md-2">
                            <label for="created_at_{{ $bannerDetail->id }}" class="form-label">Ngày tạo</label>
                            <input type="text" class="form-control" id="created_at_{{ $bannerDetail->id }}" value="{{ $bannerDetail->created_at->format('d/m/Y') }}" readonly>
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