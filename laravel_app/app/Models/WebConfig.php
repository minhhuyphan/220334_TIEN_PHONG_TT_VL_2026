<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class WebConfig extends Model
{
    protected $table = 'web_configs';

    protected $primaryKey = "id";

    protected $fillable = ['config_key', 'config_value', 'description'];

    public $timestamps = true;
}
