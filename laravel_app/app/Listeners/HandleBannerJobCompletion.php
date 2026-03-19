<?php

namespace App\Listeners;

use App\Http\Controllers\User\BannerController;
use App\Jobs\CreateBannersJob;
use App\Events\BannerJobCompleted;
use Illuminate\Support\Facades\Log;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;

class HandleBannerJobCompletion
{
    public function __construct()
    {
        
    }

    public function handle(object $event): void
    {
        
    }
}
