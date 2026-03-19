<?php

namespace App\Events;

use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Support\Facades\Log;
use Illuminate\Broadcasting\PresenceChannel;
use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Contracts\Broadcasting\ShouldBroadcastNow;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;
use App\Models\BannerDetail;

class BannerJobCompleted implements ShouldBroadcast
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    public $userId;

    public function __construct($userId)
    {
        $this->userId = $userId;
        Log::info('Broadcasting for BannerJobCompleted...');
    }

    public function broadcastOn(): Channel
    {
        Log::debug('Channel name: banner-job.' . $this->userId);
        return new Channel('banner-job.' . $this->userId);
    }

    public function broadcastAs()
    {
        return 'BannerJobCompleted';
    }
}
