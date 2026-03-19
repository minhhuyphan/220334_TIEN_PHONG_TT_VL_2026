<?php

namespace App\Http\Controllers\Auth;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Password;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;
use App\Models\User;
use App\Models\WebConfig;

class AuthController extends Controller
{
    public function __construct()
    {
        @session_start();
    }

    // Show login form
    public function showLoginForm()
    {
        $logo = WebConfig::where('config_key', 'logo')->value('config_value');
        $favicon = WebConfig::where('config_key', 'favicon')->value('config_value');
        return view('auth.login', compact(
            'logo',
            'favicon'
        ));
    }

    // Handel login
    public function login(Request $request)
    {
        $credentials = $request->validate([
            'email' => 'required|email',
            'password' => 'required',
        ]);
        if (Auth::attempt($credentials)) {
            // Kiểm tra trạng thái của người dùng
            $user = Auth::user();
            if ($user->status != 1) {
                // Nếu status không phải 1, đăng xuất ngay lập tức
                Auth::logout();
                $request->session()->invalidate();
                $request->session()->regenerateToken();
                return back()->withErrors([
                    'email' => 'Tài khoản của bạn đã bị khóa. Vui lòng liên hệ quản trị viên.',
                ])->withInput();
            }
            if($user->level == 0){
                // Kiểm tra xác thực email
                if (is_null(Auth::user()->email_verified_at)) {
                    Auth::logout();
                    return redirect()->route('login')
                        ->withErrors(['email' => 'Vui lòng xác thực email trước khi đăng nhập.']);
                }
                // Đăng nhập người dùng
                $request->session()->regenerate();
                return redirect()->intended('/');
            }
            else if($user->level == 1){
                // Đăng nhập admin
                $request->session()->regenerate();
                return redirect()->intended('/admin/layout');
            }
        }
        // Nếu thông tin đăng nhập không hợp lệ
        return back()->withErrors([
            'email' => 'Email hoặc mật khẩu không đúng.',
        ])->withInput();
    }

    // Show register form
    public function showRegistrationForm()
    {
        $logo = WebConfig::where('config_key', 'logo')->value('config_value');
        $favicon = WebConfig::where('config_key', 'favicon')->value('config_value');
        return view('auth.register', compact(
            'logo',
            'favicon'
        ));
    }

    // Handle register
    public function register(Request $request)
    {
        $request->validate([
            'username' => 'required|string|max:255',
            'email' => 'required|string|email|max:255|unique:users',
            'password' => 'required|string|min:8|max:255|confirmed',
        ]);
        $user = User::create([
            'username' => $request->username,
            'email' => $request->email,
            'password' => Hash::make($request->password),
        ]);
        // Gửi email xác thực
        $user->sendEmailVerificationNotification();
        return redirect()->route('register_get')->with('status', 'Vui lòng kiểm tra email để xác thực tài khoản.');
    }


    /**
     * Xử lý xác thực email.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\RedirectResponse
     */
    public function verifyEmail(Request $request)
    {
        $token = $request->token;
        $email = $request->email;
        $verification = DB::table('email_verification_tokens')
            ->where('email', $email)
            ->where('token', $token)
            ->first();
        if (!$verification) {
            return redirect()->route('login')->withErrors(['email' => 'Liên kết xác thực không hợp lệ.']);
        }
        // Kiểm tra thời gian hết hạn (ví dụ: 60 phút)
        if (now()->subMinutes(60)->gt($verification->created_at)) {
            return redirect()->route('login')->withErrors(['email' => 'Liên kết xác thực đã hết hạn.']);
        }
        $user = User::where('email', $email)->first();

        if ($user && is_null($user->email_verified_at)) {
            $user->email_verified_at = now();
            $user->save();
            // Xóa token sau khi xác thực
            DB::table('email_verification_tokens')->where('email', $email)->delete();
            return redirect()->route('login')->with('status', 'Email đã được xác thực. Vui lòng đăng nhập.');
        }
        return redirect()->route('login')->withErrors(['email' => 'Email đã được xác thực hoặc không tồn tại.']);
    }

    // Handle logout
    public function logout(Request $request)
    {
        Auth::logout();
        $request->session()->invalidate();
        $request->session()->regenerateToken();
        return redirect('/');
    }

    /**
     * Hiển thị form yêu cầu đặt lại mật khẩu.
     *
     * @return \Illuminate\View\View
     */
    public function showLinkRequestForm()
    {
        $logo = WebConfig::where('config_key', 'logo')->value('config_value');
        $favicon = WebConfig::where('config_key', 'favicon')->value('config_value');
        return view('auth.forgot-password', compact(
            'logo',
            'favicon'
        ));
    }

    /**
     * Xử lý gửi email đặt lại mật khẩu.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\RedirectResponse
     */
    public function sendResetLinkEmail(Request $request)
    {
        $request->validate(['email' => 'required|email']);

        $status = Password::sendResetLink(
            $request->only('email')
        );

        return $status === Password::RESET_LINK_SENT
            ? back()->with('status', __($status))
            : back()->withErrors(['email' => __($status)]);
    }

    /**
     * Hiển thị form đặt lại mật khẩu.
     *
     * @param  string  $token
     * @return \Illuminate\View\View
     */
    public function showResetForm($token, Request $request)
    {
        $logo = WebConfig::where('config_key', 'logo')->value('config_value');
        $favicon = WebConfig::where('config_key', 'favicon')->value('config_value');
        return view('auth.reset-password', [
            'logo' => $logo,
            'favicon' => $favicon,
            'token' => $token,
            'email' => $request->email
        ]);
    }

    /**
     * Xử lý cập nhật mật khẩu mới.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\RedirectResponse
     */
    public function reset(Request $request)
    {
        $request->validate([
            'token' => 'required',
            'email' => 'required|email',
            'password' => 'required|confirmed|min:8',
        ]);

        $status = Password::reset(
            $request->only('email', 'password', 'password_confirmation', 'token'),
            function ($user, $password) {
                $user->forceFill([
                    'password' => Hash::make($password),
                    'remember_token' => Str::random(60),
                ])->save();
            }
        );

        return $status === Password::PASSWORD_RESET
            ? redirect()->route('login')->with('status', __($status))
            : back()->withErrors(['email' => [__($status)]]);
    }
}
