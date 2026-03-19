<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Models\WebConfig;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class DashboardController extends Controller
{
    public function __construct()
    {
        @session_start();
    }

    public function index(Request $request)
    {
        $logo = WebConfig::where('config_key', 'logo')->value('config_value');
        $favicon = WebConfig::where('config_key', 'favicon')->value('config_value');
        $title = 'Thống kê';
        $template = 'admin.dashboard.index';
        return view('admin.layout', compact(
            'template',
            'logo',
            'favicon',
            'title'
        ));
    }
}
