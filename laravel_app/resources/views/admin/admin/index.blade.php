<div class="container-fluid">
    <div class="row">
        <div class="col-12">
            <div class="card">
                <div class="card-header">
                    <!-- Hiển thị thông báo -->
                    @if (session('success'))
                    <div class="alert alert-success alert-dismissible fade show" role="alert">
                        {{ session('success') }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>
                    @endif
                    <div class="d-flex justify-content-between align-items-center">
                        <h3 class="card-title mb-0">DANH SÁCH QUẢN TRỊ VIÊN</h3>
                        <a class="btn btn-success" href="{{ route('add_admin_get') }}">Thêm quản trị viên <i class="ti ti-plus"></i></a>
                    </div>
                </div>
                <div class="card-body">
                    <table class="table table-bordered table-hover" id="myTable">
                        <thead>
                            <tr>
                                <th>STT</th>
                                <th>Tên</th>
                                <th>Email</th>
                                <th>Số điện thoại</th>
                                <th>Địa chỉ</th>
                                <th>Cấp độ</th>
                                <th>Ngày tạo</th>
                                <th>Ngày cập nhật</th>
                                <th>Tình trạng</th>
                                <th>Thao tác</th>
                            </tr>
                        </thead>
                        <tbody>
                            @forelse ($users as $user)
                            <tr>
                                <td>{{ $loop->iteration }}</td>
                                <td>{{ $user->username }}</td>
                                <td>{{ $user->email }}</td>
                                <td>{{ $user->phone_number }}</td>
                                <td>{{ $user->address }}</td>
                                <td>
                                    @if ($user->level == 1)
                                    <span class="badge bg-success">Admin</span>
                                    @elseif ($user->level == 0)
                                    <span class="badge bg-info">Người dùng</span>
                                    @endif
                                </td>
                                <td>{{ $user->created_at->format('d/m/Y') }}</td>
                                <td>{{ $user->updated_at->format('d/m/Y') }}</td>
                                <td>
                                    @if ($user->status == 1)
                                    <span class="badge bg-success">Đang hoạt động</span>
                                    @else
                                    <span class="badge bg-danger">Đã khóa</span>
                                    @endif
                                </td>
                                <td>
                                    <!-- Nút Mở/Khóa -->
                                    <form action="{{ route('admin.change_status_admin', $user->id) }}" method="POST" style="display:inline;">
                                        @csrf
                                        @method('PATCH')
                                        @php
                                        $action = $user->status == 1 ? 'khóa tài khoản' : 'mở khóa tài khoản';
                                        $buttonClass = $user->status == 1 ? 'btn-warning' : 'btn-success';
                                        @endphp
                                        <button type="submit" class="btn btn-sm {{ $buttonClass }}"
                                            onclick="return confirm('Bạn có chắc muốn {{ $action }} này?')">
                                            {{ ucfirst($action) }}
                                        </button>
                                    </form>
                                </td>
                            </tr>
                            @empty
                            <tr>
                                <td colspan="9" class="text-center">Không có người dùng nào</td>
                            </tr>
                            @endforelse
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>