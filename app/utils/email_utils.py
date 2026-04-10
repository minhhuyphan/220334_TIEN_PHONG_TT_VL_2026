import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings
import logging

logger = logging.getLogger(__name__)

def send_reset_email(to_email: str, token: str):
    """
    Gửi email khôi phục mật khẩu thông qua SMTP Gmail.
    """
    if not all([settings.MAIL_USER, settings.MAIL_PASS]):
        logger.warning("Cấu hình Email trống. Không thể gửi mail.")
        return False

    # Cấu tạo link reset (Điều chỉnh URL theo môi trường deploy)
    base_url = "http://localhost:3000" # Mặc định local
    
    if hasattr(settings, "FRONTEND_URL") and settings.FRONTEND_URL:
        base_url = settings.FRONTEND_URL
    elif hasattr(settings, "API_URL") and settings.API_URL:
        if "localhost" not in settings.API_URL:
            # Nếu API_URL là domain thật, thử đoán domain frontend
            base_url = settings.API_URL.replace("api.", "").replace(":8000", "").replace(":5000", "")
            # Nếu vẫn là domain run.app, đây có lẽ là backend đơn thuần, 
            # nên dùng FRONTEND_URL đã cấu hình (ở bước trên đã check) 
            # hoặc để mặc định localhost nếu không đoán được.

    reset_link = f"{base_url}/reset-password?token={token}"

    # Nội dung Email HTML (Giao diện chuyên nghiệp)
    html_content = f"""
    <html>
    <body style="font-family: 'Inter', sans-serif; line-height: 1.6; color: #334155; margin: 0; padding: 0; background-color: #f8fafc;">
        <div style="max-width: 600px; margin: 40px auto; background: #ffffff; border-radius: 24px; overflow: hidden; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);">
            <div style="background: linear-gradient(135deg, #4f46e5, #7c3aed); padding: 40px 20px; text-align: center;">
                <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 800;">Khôi phục mật khẩu</h1>
            </div>
            <div style="padding: 40px;">
                <p style="font-size: 16px; margin-bottom: 24px;">Xin chào,</p>
                <p style="font-size: 16px; margin-bottom: 32px;">Chúng tôi nhận được yêu cầu khôi phục mật khẩu cho tài khoản của bạn. Vui lòng nhấn vào nút bên dưới để tiến hành thay đổi mật khẩu mới:</p>
                
                <div style="text-align: center; margin-bottom: 32px;">
                    <a href="{reset_link}" style="display: inline-block; padding: 16px 36px; background-color: #4f46e5; color: #ffffff; text-decoration: none; border-radius: 14px; font-weight: 700; font-size: 16px; box-shadow: 0 4px 14px rgba(79, 70, 229, 0.4);">
                        Đặt lại mật khẩu
                    </a>
                </div>

                <p style="font-size: 14px; color: #64748b; margin-bottom: 24px;">Link này sẽ hết hạn sau 15 phút. Nếu bạn không yêu cầu hành động này, vui lòng bỏ qua email này.</p>
                
                <div style="border-top: 1px solid #e2e8f0; padding-top: 24px;">
                    <p style="font-size: 13px; color: #94a3b8; margin: 0;">Trân trọng,</p>
                    <p style="font-size: 13px; color: #4f46e5; font-weight: 700; margin: 4px 0 0 0;">Đội ngũ {settings.NAME_WEB}</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    try:
        msg = MIMEMultipart()
        msg['From'] = settings.MAIL_FROM or settings.MAIL_USER
        msg['To'] = to_email
        msg['Subject'] = f"[{settings.NAME_WEB}] Khôi phục mật khẩu"

        msg.attach(MIMEText(html_content, 'html'))

        with smtplib.SMTP(settings.MAIL_HOST, settings.MAIL_PORT) as server:
            server.starttls()
            server.login(settings.MAIL_USER, settings.MAIL_PASS)
            server.send_message(msg)
            
        logger.info(f"Đã gửi email reset mật khẩu tới {to_email}")
        return True
    except Exception as e:
        logger.error(f"Lỗi khi gửi email: {e}")
        return False
