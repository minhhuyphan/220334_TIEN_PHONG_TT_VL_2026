<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class BannerDetail extends Model
{
    use HasFactory;

    protected $table = "banner_details";

    protected $primaryKey = "id";

    protected $fillable = ['user_id', 'description', 'theme', 'width', 'height', 'number', 'created_at', 'updated_at', 'status'];

    public function user()
    {
        return $this->belongsTo(User::class);
    }

    public function banners()
    {
        return $this->hasMany(Banner::class, 'banner_details_id');
    }
}