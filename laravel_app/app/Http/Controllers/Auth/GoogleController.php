<?php

namespace App\Http\Controllers\Auth;

use App\Http\Controllers\Controller;
use App\Models\User;
use Laravel\Socialite\Facades\Socialite;
use Illuminate\Support\Facades\Auth;

class GoogleController extends Controller
{
    // Chuyển hướng người dùng đến trang đăng nhập Google
    public function redirectToGoogle()
    {
        return Socialite::driver('google')->redirect();
    }

    public function handleGoogleCallback()
    {
        try {
            $googleUser = Socialite::driver('google')->user();
            $email = $googleUser->getEmail();

            $user = User::where('email', $email)->first();

            if (!$user) {
                $user = User::create([
                    'username' => $googleUser->getName(),
                    'email' => $email,
                    'google_id' => $googleUser->getId(),
                    'password' => bcrypt(uniqid()),
                    'level' => 0, // Mặc định không phải admin
                ]);
            } else {
                // Cập nhật google_id nếu cần
                $user->update(['google_id' => $googleUser->getId()]);
            }

            Auth::login($user, true);

            // Kiểm tra quyền admin trước khi chuyển hướng
            if ($user->level == 1) {
                return redirect()->intended('/admin/layout');
            }
            
            return redirect()->intended('/');
        } catch (\Exception $e) {
            return redirect('/')->with('error', 'Đăng nhập bằng Google thất bại.');
        }
    }
}