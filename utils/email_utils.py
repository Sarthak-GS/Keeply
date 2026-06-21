import logging
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from html import escape
from datetime import datetime, timezone
import aiosmtplib
from config.settings import settings

logger = logging.getLogger(__name__)


async def send_password_reset_email(to_email: str, username: str, reset_link: str):
    
    safe_username = escape(username)
    safe_link = escape(reset_link)
    txn_id = uuid.uuid4().hex[:8].upper()
    current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    
    message = MIMEMultipart("alternative")
    message["Subject"] = "Reset Your Keeply Password"
    message["From"] = settings.SMTP_FROM_EMAIL
    message["To"] = to_email
    message["Reply-To"] = settings.SMTP_FROM_EMAIL
    
    domain = settings.SMTP_FROM_EMAIL.split("@")[-1]
    message["Message-ID"] = f"<{txn_id}.{uuid.uuid4().hex[:8]}@{domain}>"
    message["List-Unsubscribe"] = f"<mailto:{settings.SMTP_FROM_EMAIL}?subject=unsubscribe>"
    message["List-Unsubscribe-Post"] = "List-Unsubscribe=One-Click"
    message["X-Mailer"] = "Keeply Password Manager"
    message["X-Priority"] = "3"  # Normal priority
    message["X-Entity-ID"] = txn_id  # For tracking
    
    text_content = f"""\
Hello {safe_username},

We received a request to reset your Keeply account password.

==============================
RESET YOUR PASSWORD
==============================
Click this secure link to set a new password (valid for 60 minutes):

{reset_link}

WHAT TO EXPECT:
• You'll be redirected to a secure page to create your new password
• Your new password must be at least 8 characters
• Once reset, you can log in immediately

IF YOU DIDN'T REQUEST THIS:
You can safely ignore this email. Your account is still secure and your 
password remains unchanged. No action is needed.

NEED HELP?
Contact our support team at support@keeply.com

==============================
Keeply Security Team
Automated security notification - Please do not reply to this email
© {datetime.now().year} Keeply. All rights reserved.
==============================

Transaction ID: {txn_id}
Sent: {current_time}
"""

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reset Your Password</title>
    </head>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f8fafc; margin: 0; padding: 0; -webkit-font-smoothing: antialiased;">
        <div style="max-width: 600px; margin: 40px auto; background-color: #ffffff; border-radius: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; overflow: hidden;">
            <div style="background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%); padding: 40px 20px; text-align: center;">
                <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 700; letter-spacing: -0.025em;">Keeply</h1>
            </div>
            <div style="padding: 40px 30px; color: #334155; line-height: 1.6;">
                <p style="margin: 0 0 20px 0; font-size: 16px;">Hello <strong>{safe_username}</strong>,</p>
                <p style="margin: 0 0 20px 0; font-size: 16px;">We received a request to reset the password for your Keeply account. Click the button below to set a new password:</p>
                <div style="text-align: center; margin: 35px 0;">
                    <a href="{safe_link}" style="background-color: #4f46e5; color: #ffffff; text-decoration: none; padding: 14px 30px; font-weight: 600; font-size: 16px; border-radius: 8px; display: inline-block; box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.2);">Reset Password</a>
                </div>
                <p style="margin: 0 0 20px 0; font-size: 16px;">If you prefer, you can copy and paste the following link directly into your browser:</p>
                <p style="word-break: break-all; font-size: 14px; color: #6366f1; margin: 0 0 20px 0;"><a href="{safe_link}" style="color: #6366f1; text-decoration: underline;">{safe_link}</a></p>
                <div style="font-size: 13px; color: #64748b; background-color: #f8fafc; border-left: 4px solid #cbd5e1; padding: 12px 16px; margin: 24px 0 0 0; border-radius: 0 8px 8px 0;">
                    <strong>Note:</strong> This link is only valid for <strong>60 minutes</strong>. If you did not request a password reset, please ignore this email. Your password will remain unchanged.
                </div>
            </div>
            <div style="background-color: #f1f5f9; padding: 24px; text-align: center; font-size: 13px; color: #64748b; border-top: 1px solid #e2e8f0;">
                <p style="margin: 0 0 8px 0;">&copy; {datetime.now().year} Keeply. Secure Password Manager.</p>
                <p style="margin: 0 0 8px 0;">Transaction ID: {txn_id}</p>
                <p style="margin: 0;">This is an automated security transmission. Please do not reply directly.</p>
            </div>
        </div>
    </body>
    </html>
    """

    message.attach(MIMEText(text_content, "plain", "utf-8"))
    message.attach(MIMEText(html_content, "html", "utf-8"))

    try:
        if settings.SMTP_PORT == 465:
            use_tls, start_tls = True, False
        elif settings.SMTP_PORT == 587:
            use_tls, start_tls = False, True
        else:
            raise ValueError("SMTP_PORT must be 465 or 587")

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
        logger.info(f"Password reset email sent to {to_email} [TxnID: {txn_id}]")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        raise