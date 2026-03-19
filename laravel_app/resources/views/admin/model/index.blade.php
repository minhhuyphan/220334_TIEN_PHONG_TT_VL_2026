<div class="container-fluid">
    <div class="row">
        <div class="col-12">
            <h3 class="mb-4">DANH SÁCH MODEL</h3>
            <table class="table table-bordered table-hover" id="myTable">
                <thead>
                    <tr>
                        <th>STT</th>
                        <th>Tên model</th>
                        <th>Key</th>
                        <th>Mô tả</th>
                        <th>Thời gian cập nhật</th>
                        <th>Thao tác</th>
                    </tr>
                </thead>
                <tbody>
                    @foreach ($models as $model)
                    <tr>
                        <td>{{ $loop->iteration }}</td>
                        <td>{{ $model->model_name }}</td>
                        <td>{{ $model->model_key }}</td>
                        <td>{{ $model->description }}</td>
                        <td>{{ $model->updated_at->format('d/m/Y') }}</td>
                        <td>
                            <a href=" {{ route('info_model_get', $model->id) }} " class="btn btn-warning">Chỉnh sửa</a>
                        </td>
                    </tr>
                    @endforeach
                </tbody>
            </table>
        </div>
    </div>
</div>