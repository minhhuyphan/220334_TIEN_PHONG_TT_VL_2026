<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        //
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        //
    }
    /**
     * Đăng ký Event và Listener
     */
    protected $listen = [
        \App\Jobs\CreateBannersJob::class => [
            \App\Listeners\HandleBannerJobCompletion::class,
        ],
    ];
}
