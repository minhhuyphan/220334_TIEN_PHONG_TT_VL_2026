<div class="container-fluid">
    <div class="row">
        <div class="col-12">
            <h3 class="mb-4">DANH SÁCH CẤU HÌNH</h3>
            <table class="table table-bordered table-hover" id="myTable">
                <thead>
                    <tr>
                        <th>STT</th>
                        <th>Tên cấu hình</th>
                        <th>Giá trị</th>
                        <th>Mô tả</th>
                        <th>Thời gian cập nhật</th>
                        <th>Thao tác</th>
                    </tr>
                </thead>
                <tbody>
                    @foreach ($configs as $config)
                    <tr>
                        <td>{{ $loop->iteration }}</td>
                        <td>{{ $config->config_key }}</td>
                        <td>
                            @if (in_array($config->config_key, ['favicon', 'logo', 'hero_image']) && $config->config_value && file_exists(public_path($config->config_value)))
                            <img src="{{ asset($config->config_value) }}" alt="Ảnh" class="img-fluid img-thumbnail" style="max-width: 150px; max-height: 150px;">
                            @else
                            {{ $config->config_value }}
                            @endif
                        </td>
                        <td>{{ $config->description ?? 'Không có mô tả' }}</td>
                        <td>{{ $config->updated_at->format('d/m/Y') }}</td>
                        <td>
                            <a href="{{ route('info_config_get', $config->id) }}" class="btn btn-warning">Chỉnh sửa</a>
                        </td>
                    </tr>
                    @endforeach
                </tbody>
            </table>
        </div>
    </div>
</div>