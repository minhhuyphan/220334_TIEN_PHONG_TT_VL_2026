<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Auth\AuthController;
use App\Http\Controllers\Auth\GoogleController;
use Spatie\Sitemap\Sitemap;
use Spatie\Sitemap\Tags\Url;

Route::get('/', [App\Http\Controllers\User\HomeController::class, 'index'])->name('homepage');
Route::get('/about', [App\Http\Controllers\User\HomeController::class,'loadSiteAbout'])->name('load_site_about');
Route::get('/pricing', [App\Http\Controllers\User\HomeController::class, 'loadSitePricing'])->name('load_site_pricing');
Route::get('/contact', [App\Http\Controllers\User\HomeController::class, 'loadSiteContact'])->name('load_site_contact');

// Authenticate
Route::controller(AuthController::class)->group(function () {
    Route::get('/login', 'showLoginForm')->name('login');
    Route::post('/login', 'login')->name('login_post');
    Route::get('/register', 'showRegistrationForm')->name('register_get');
    Route::post('/register', 'register')->name('register_post');
    Route::get('/verify-email', 'verifyEmail')->name('verify.email');
    Route::post('/logout', 'logout')->name('logout_post');
    Route::get('/forgot-password', 'showLinkRequestForm')->name('password.request');
    Route::post('/forgot-password', 'sendResetLinkEmail')->name('password.email');
    Route::get('/reset-password/{token}', 'showResetForm')->name('password.reset');
    Route::post('/reset-password', 'reset')->name('password.store');
});

// Thêm route cho GoogleController (không dùng middleware 'auth' hoặc prefix 'admin')
Route::controller(GoogleController::class)->group(function () {
    Route::get('auth/google', 'redirectToGoogle')->name('auth.google');
    Route::get('auth/google/callback', 'handleGoogleCallback');
});

// User
Route::middleware('auth')->prefix('user')->group(function () {
    Route::controller(App\Http\Controllers\User\HomeController::class)->group(function () {
        Route::get('/layout', 'loadViewCreateBanners')->name('load_view_create_banners');
        Route::get('/edit-banner/{bannerId}', 'loadBannerEditForm')->name('edit_banner_get');
    });

    Route::controller(App\Http\Controllers\User\UserController::class)->group(function () {
        Route::get('/get-info-user/{id}', 'getInfo')->name('info_user_get');
        Route::post('/update-info-user/{id}', 'updateInfo')->name('info_user_update');
    });

    Route::controller(App\Http\Controllers\User\BannerController::class)->group(function () {
        Route::post('/create-banners', 'createBanners')->name('create_banner_post');
        Route::delete('/delete-banners/{bannerDetailsId}', 'deleteBannerDetail')->name('banner_details_delete');
        Route::delete('/delete-banner/{bannerId}', 'deleteBanner')->name('banner_delete');
        Route::post('/save-banner', 'saveBanner')->name('save_banner');
        Route::match(['put', 'delete'], '/banners/{id}/publish', 'publishBanner')->name('banners_publish');
    });

});

// Admin
Route::middleware('auth')->prefix('admin')->group(function () {
    Route::controller(App\Http\Controllers\Admin\DashboardController::class)->group(function () {
        Route::get('/layout', 'index');
        Route::get('/get-dashboard', 'index')->name('dashboard_get');
    });

    Route::controller(App\Http\Controllers\Admin\UserController::class)->group(function () {
        Route::get('/get-table-user', 'index')->name('user_table_get');
        Route::patch('/change-user-status/{id}', 'changeStatus')->name('admin.change_status_user');
    });

    Route::controller(App\Http\Controllers\Admin\AdminController::class)->group(function () {
        Route::get('/get-info-admin/{id}', 'getInfo')->name('info_admin_get');
        Route::patch('/update-info-admin/{id}', 'updateInfo')->name('info_admin_update');
        Route::get('/get-table-admin', 'index')->name('admin_table_get');
        Route::patch('/change-admin-status/{id}', 'changeStatus')->name('admin.change_status_admin');
        Route::get('/add-admin', 'showAddAdminForm')->name('add_admin_get');
        Route::post('/add-admin', 'addAdmin')->name('add_admin_post');
    });

    Route::controller(App\Http\Controllers\Admin\BannerController::class)->group(function () {
        Route::get('/get-user-banners/{userId}', 'getUserBanners')->name('user_banners_get');
    });

    Route::controller(App\Http\Controllers\Admin\ModelController::class)->group(function () {
        Route::get('/get-models', 'getModels')->name('models_get');
        Route::get('/get-info-model/{id}', 'getInfoModel')->name('info_model_get');
        Route::put('/update-model/{id}/update-key', 'updateKey')->name('model_update');
    });

    Route::controller(App\Http\Controllers\Admin\WebConfigController::class)->group(function () {
        Route::get('/get-configs', 'index')->name('configs_get');
        Route::get('/get-info-config/{id}', 'getInfoConfig')->name('info_config_get');
        Route::put('/update-config/{id}/update-config', 'updateConfig')->name('config_update');
    });
});

// Tạo sitemap trong route
// Route::get('/sitemap.xml', function () {
//     $sitemap = Sitemap::create()
//         ->add(Url::create('/'))
//         ->add(Url::create('/about'))
//         ->add(Url::create('/contact'));
//     $sitemap->writeToFile(public_path('sitemap.xml'));
//     return response()->file(public_path('sitemap.xml'));
// });