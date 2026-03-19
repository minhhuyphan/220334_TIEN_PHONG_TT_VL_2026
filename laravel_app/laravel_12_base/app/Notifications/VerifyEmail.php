<?php

namespace App\Notifications;

use Illuminate\Notifications\Notification;
use Illuminate\Notifications\Messages\MailMessage;
use Illuminate\Support\Str;
use Illuminate\Support\Facades\DB;

class VerifyEmail extends Notification
{
    public function via($notifiable)
    {
        return ['mail'];
    }

    public function toMail($notifiable)
    {
        $token = Str::random(60);

        // Lưu token vào bảng email_verification_tokens
        DB::table('email_verification_tokens')->updateOrInsert(
            ['email' => $notifiable->email],
            ['token' => $token, 'created_at' => now()]
        );

        $url = url(route('verify.email', [
            'token' => $token,
            'email' => $notifiable->email,
        ], false));

        return (new MailMessage)
            ->subject('Xác thực địa chỉ email')
            ->greeting('Xin chào!')
            ->line('Vui lòng nhấp vào nút dưới đây để xác thực địa chỉ email của bạn.')
            ->action('Xác thực email', $url)
            ->line('Nếu bạn không tạo tài khoản, vui lòng bỏ qua email này.')
            ->salutation('Trân trọng, ' . config('app.name'));
    }
}