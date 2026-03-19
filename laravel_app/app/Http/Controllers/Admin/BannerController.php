<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Models\WebConfig;
use App\Models\BannerDetail;

class BannerController extends Controller
{
    public function __construct()
    {
        @session_start();
    }

    public function getUserBanners($userId)
    {
        $logo = WebConfig::where('config_key', 'logo')->value('config_value');
        $favicon = WebConfig::where('config_key', 'favicon')->value('config_value');
        $title = 'Banner người dùng tạo';
        $data = BannerDetail::with('banners')
            ->where('user_id', $userId)
            ->orderBy('created_at', 'desc')
            ->get();
        $data = $data->isEmpty() ? [] : $data;
        $template = 'admin.banner.index';
        return view('admin.layout', compact(
            'logo',
            'favicon',
            'title',
            'template',
            'data'
        ));
    }
}