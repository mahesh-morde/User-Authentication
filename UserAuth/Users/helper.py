from django.core.mail import send_mail

def send_forgot_password_mail(user, token):
    subject = 'Password Reset Request'
    message = f'Hello {user.username},\n\nPlease click the following link to reset your password:\n\nhttp://yourdomain.com/reset_password/{token}/'
    sender = 'maheshmorde2511@gmail.com'
    recipient = [user.email]

    send_mail(subject, message, sender, recipient)
