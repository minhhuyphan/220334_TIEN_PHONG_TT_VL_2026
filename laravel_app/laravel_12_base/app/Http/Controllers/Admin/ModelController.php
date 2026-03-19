<?php

namespace App\Http\Controllers\Admin;

use App\Models\Model;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\WebConfig;

class ModelController extends Controller
{
    public function __construct()
    {
        @session_start();
    }

    public function getModels()
    {
        $logo = WebConfig::where('config_key', 'logo')->value('config_value');
        $favicon = WebConfig::where('config_key', 'favicon')->value('config_value');
        $title = 'Thông tin model';
        // Load tất cả model
        $models = Model::all();
        $template = 'admin.model.index';
        return view('admin.layout', compact(
            'logo',
            'favicon',
            'title',
            'template',
            'models'
        ));
    }

    public function getInfoModel($id){
        $logo = WebConfig::where('config_key', 'logo')->value('config_value');
        $favicon = WebConfig::where('config_key', 'favicon')->value('config_value');
        $title = 'Chỉnh sửa model';
        $model = Model::findOrFail($id);
        $template = 'admin.model.update';
        return view('admin.layout', compact(
            'logo',
            'favicon',
            'title',
            'template',
            'model'
        ));
    }

    public function updateKey(Request $request, $id)
    {
        // Tìm model theo model_name
        $model = Model::findOrFail($id);

        // Validate dữ liệu đầu vào
        $request->validate([
            'model_key' => 'required|string|max:255',
            'description' => 'required|string|max:512',
        ]);

        // Cập nhật model_key
        $model->update([
            'model_key' => $request->input('model_key'),
            'description' => $request->input('description'),
        ]);

        return redirect()->back()->with('success', 'Đã cập nhật model!');
    }
}
