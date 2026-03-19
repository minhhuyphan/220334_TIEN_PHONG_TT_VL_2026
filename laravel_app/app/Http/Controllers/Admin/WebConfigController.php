<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Models\WebConfig;
use Illuminate\Http\Request;
use Illuminate\Support\Str;
use Illuminate\Support\Facades\File;

class WebConfigController extends Controller
{
    public function __construct()
    {
        @session_start();
    }

    public function index()
    {
        $logo = WebConfig::where('config_key', 'logo')->value('config_value');
        $favicon = WebConfig::where('config_key', 'favicon')->value('config_value');
        $title = 'Thông tin cấu hình';
        // Load tất cả cấu hình từ bảng web_config
        $configs = WebConfig::all();
        $template = 'admin.config.index';
        // Truyền dữ liệu vào view
        return view('admin.layout', compact(
            'logo',
            'favicon',
            'title',
            'template',
            'configs'
        ));
    }

    public function getInfoConfig($id)
    {
        $logo = WebConfig::where('config_key', 'logo')->value('config_value');
        $favicon = WebConfig::where('config_key', 'favicon')->value('config_value');
        $title = 'Chỉnh sửa cấu hình';
        // Logic để hiển thị form chỉnh sửa (nếu cần)
        $config = WebConfig::findOrFail($id);
        $template = 'admin.config.update';
        // Truyền dữ liệu vào view
        return view('admin.layout', compact(
            'logo',
            'favicon',
            'title',
            'template',
            'config'
        ));
    }

    public function updateConfig(Request $request, $id)
    {
        $config = WebConfig::findOrFail($id);
        // Validate dữ liệu
        $request->validate([
            'config_value' => ['string'],
            'description' => ['nullable', 'string'],
            'image' => ['nullable', 'file', 'mimes:jpg,jpeg,png,webp,gif,ico,svg', 'max:2048'], // Kiểm tra nếu có ảnh (tối đa 2MB)
        ]);
        // Xử lý trường config_value
        $newConfigValue = $request->input('config_value');
        if ($request->hasFile('image') && in_array($config->config_key, ['favicon', 'logo', 'hero_image'])) {
            // Xóa ảnh cũ nếu tồn tại
            // if (File::exists(public_path($config->config_value))) {
            //     File::delete(public_path($config->config_value));
            // }
            // Lưu ảnh mới với tên duy nhất
            $image = $request->file('image');
            $imageName = Str::uuid() . '.' . $image->getClientOriginalExtension();
            $image->move(public_path('assets/images/logos'), $imageName);
            $newConfigValue = 'assets/images/logos/' . $imageName;
        }
        // Cập nhật bản ghi
        $config->update([
            'config_value' => $newConfigValue,
            'description' => $request->input('description'),
        ]);
        // Chuyển hướng với thông báo thành công
        return redirect()->back()->with('success', 'Đã cập nhật cấu hình thành công!');
    }

}