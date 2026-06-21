import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import aiosmtplib
from config.settings import settings

logger = logging.getLogger(__name__)


async def send_password_reset_email(to_email: str, username: str, reset_link: str):
    """Sends a professional, responsive HTML password reset email using aiosmtplib."""
    
    # 1. Create message container
    message = MIMEMultipart("alternative")
    message["Subject"] = "Reset Your Keeply Password"
    message["From"] = settings.SMTP_FROM_EMAIL
    message["To"] = to_email

    # 2. Design high-end HTML layout
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reset Your Password</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                background-color: #f8fafc;
                margin: 0;
                padding: 0;
                -webkit-font-smoothing: antialiased;
            }}
            .container {{
                max-width: 600px;
                margin: 40px auto;
                background-color: #ffffff;
                border-radius: 16px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
                overflow: hidden;
                border: 1px solid #e2e8f0;
            }}
            .header {{
                background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
                padding: 40px 20px;
                text-align: center;
            }}
            .header h1 {{
                color: #ffffff;
                margin: 0;
                font-size: 28px;
                font-weight: 700;
                letter-spacing: -0.025em;
            }}
            .content {{
                padding: 40px 30px;
                color: #334155;
                line-height: 1.6;
            }}
            .content p {{
                margin: 0 0 20px 0;
                font-size: 16px;
            }}
            .button-container {{
                text-align: center;
                margin: 35px 0;
            }}
            .btn {{
                background-color: #4f46e5;
                color: #ffffff !important;
                text-decoration: none;
                padding: 14px 30px;
                font-weight: 600;
                font-size: 16px;
                border-radius: 8px;
                display: inline-block;
                box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.2), 0 2px 4px -1px rgba(79, 70, 229, 0.1);
            }}
            .footer {{
                background-color: #f1f5f9;
                padding: 24px;
                text-align: center;
                font-size: 13px;
                color: #64748b;
                border-top: 1px solid #e2e8f0;
            }}
            .warning {{
                font-size: 13px;
                color: #64748b;
                background-color: #f8fafc;
                border-left: 4px solid #cbd5e1;
                padding: 12px 16px;
                margin: 24px 0 0 0;
                border-radius: 0 8px 8px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Keeply</h1>
            </div>
            <div class="content">
                <p>Hello <strong>{username}</strong>,</p>
                <p>We received a request to reset the password for your Keeply account. Click the button below to set a new password:</p>
                <div class="button-container">
                    <a href="{reset_link}" class="btn" style="color: #ffffff;">Reset Password</a>
                </div>
                <p>If you prefer, you can copy and paste the following link directly into your browser:</p>
                <p style="word-break: break-all; font-size: 14px; color: #6366f1;"><a href="{reset_link}">{reset_link}</a></p>
                <div class="warning">
                    <strong>Note:</strong> This link is only valid for <strong>60 minutes</strong>. If you did not request a password reset, please ignore this email. Your password will remain unchanged.
                </div>
            </div>
            <div class="footer">
                <p>&copy; {datetime.now().year} Keeply. Secure Password Manager.</p>
                <p>This is an automated security transmission. Please do not reply directly.</p>
            </div>
        </div>
    </body>
    </html>
    """

    message.attach(MIMEText(html_content, "html"))

    try:
        # Port 465 requires direct SSL/TLS (use_tls=True), port 587 requires STARTTLS (start_tls=True)
        use_tls = True if settings.SMTP_PORT == 465 else False
        start_tls = False if settings.SMTP_PORT == 465 else settings.SMTP_USE_TLS

        smtp_client = aiosmtplib.SMTP(
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            use_tls=use_tls,
            start_tls=start_tls,
        )
        await smtp_client.connect()
        
        if settings.SMTP_USERNAME and settings.SMTP_PASSWORD:
            await smtp_client.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            
        await smtp_client.send_message(message)
        await smtp_client.quit()
        logger.info(f"Password reset email successfully sent to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send password reset email to {to_email}: {e}")
