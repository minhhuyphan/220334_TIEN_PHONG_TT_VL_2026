<?php

namespace App\Http\Controllers\User;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\User;
use Illuminate\Support\Facades\Hash;

class UserController extends Controller
{
    public function __construct()
    {
        @session_start();
    }


    public function getInfo(Request $request, $id)
    {
        $title = 'Thông tin cá nhân';
        $user = User::findOrFail($id); 
        $template = 'user.info.index';
        return view('homepage.layout', compact(
            'template',
            'title',
            'user'
        ));
    }

    public function updateInfo(Request $request, $id)
    {
        $user = User::findOrFail($id); // Tìm người dùng theo ID
        if (!empty($request->password)) {
            $request->validate([
                'password' => 'required|string|min:8|max:255',
            ]);
            $user->password = Hash::make($request->password);
        }
        $request->validate([
            'username' => 'required|string|max:255',
            'phone_number' => 'nullable|regex:/^[0-9]{10,11}$/',
            'address' => 'max:255',
        ]);
        $now = date('Y-m-d H:i:s');
        $user->username = $request->username;
        $user->phone_number = $request->phone_number;
        $user->address = $request->address;
        $user->updated_at = $now;
        $user->created_at = $user->create_at;
        $user->save();
        return redirect()->route('info_user_get', ['id' => $id])->with('success', 'Cập nhật thông tin thành công!');
    }
}
