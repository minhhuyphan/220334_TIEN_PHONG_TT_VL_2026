<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class Banner extends Model
{
    use HasFactory;

    protected $table = "banners";

    protected $primaryKey = "id";

    protected $fillable = ['banner_details_id', 'link_banner', 'is_published', 'published_at', 'favorite_count'];

    public $timestamps = false; // Tắt timestamps hoàn toàn

    public function bannerDetail()
    {
        return $this->belongsTo(BannerDetail::class, 'banner_details_id');
    }
}
