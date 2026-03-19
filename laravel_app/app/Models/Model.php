<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model as EloquentModel;

class Model extends EloquentModel
{
    use HasFactory;

    protected $table = "models";

    protected $primaryKey = 'id'; 

    protected $fillable = [
        'model_name',
        'model_key',
        'description',
        'updated_at',
    ];
}
