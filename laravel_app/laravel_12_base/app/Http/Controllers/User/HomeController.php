<?php

namespace App\Http\Controllers\User;

use App\Http\Controllers\Controller;
use App\Models\Banner;
use Illuminate\Support\Facades\Auth;
use App\Models\BannerDetail;
use App\Models\User;
use App\Models\WebConfig;
use Illuminate\Http\Request;

class HomeController extends Controller
{
    public function __construct()
    {
        @session_start();
    }


    public function index()
    {
        // Tạo mảng với config_key làm key và config_value làm value
        $configs = WebConfig::all()->pluck('config_value', 'config_key')->all();
        // Tên trang
        $title = 'Trang chủ';
        // Lấy các banner đã publish, sắp xếp theo thời gian publish mới nhất
        $banners = Banner::where('is_published', true)
            ->with('bannerDetail.user') // Load BannerDetail và User
            ->orderBy('published_at', 'desc')
            ->get();
        $template = 'homepage.main.index';
        return view('homepage.layout', compact(
            'template',
            'configs',
            'title',
            'banners'
        ));
    }

    public function loadSiteAbout()
    {
        $configs = WebConfig::all()->pluck('config_value', 'config_key')->all();
        $title = 'Giới thiệu';
        $userCount = User::count();
        $bannerCount = Banner::count();
        $template = 'homepage.main.about';
        return view('homepage.layout', compact(
            'template',
            'configs',
            'title',
            'userCount',
            'bannerCount'
        ));
    }

    public function loadSitePricing()
    {
        $configs = WebConfig::all()->pluck('config_value', 'config_key')->all();
        $title = 'Chi phí';
        $template = 'homepage.main.pricing';
        return view('homepage.layout', compact(
            'template',
            'configs',
            'title'
        ));
    }

    public function loadSiteContact()
    {
        $configs = WebConfig::all()->pluck('config_value', 'config_key')->all();
        $title = 'Liên hệ';
        $template = 'homepage.main.contact';
        return view('homepage.layout', compact(
            'template',
            'configs',
            'title'
        ));
    }

    public function loadViewCreateBanners(Request $request)
    {
        $logo = WebConfig::where('config_key', 'logo')->value('config_value');
        $favicon = WebConfig::where('config_key', 'favicon')->value('config_value');
        $title = 'Tạo banner';
        $userId = Auth::user()->id;
        $data = BannerDetail::with('banners')
            ->where('user_id', $userId)
            ->orderBy('created_at', 'desc')
            ->get();
        $data = $data->isEmpty() ? [] : $data;

        // Lấy description và theme từ query string
        $description = urldecode($request->query('description'));

        return view('user.body.banner', compact(
            'favicon',
            'title',
            'logo',
            'data',
            'description',
        ));
    }

    public function loadBannerEditForm($bannerId)
    {
        $banner = Banner::findOrFail($bannerId);
        $favicon = WebConfig::where('config_key', 'favicon')->value('config_value');
        $title = 'Chỉnh sửa';
        return view('user.body.edit', compact(
            'title',
            'favicon',
            'banner'
        ));
    }
}
