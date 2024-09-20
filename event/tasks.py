import os
from django.core.mail import EmailMessage
from django.conf import settings
from celery import shared_task
from utils.generate_pdf import generate_pdf

@shared_task
def generate_pdf_and_send_mail(user_email, payment_id, user_first_name, user_last_name, payment_amount, payment_boolean, stripe_checkout_session_id, created_at):
    print('generating pdf....')
    file_path = generate_pdf(
        payment_id, 
        user_first_name, 
        user_last_name, 
        payment_amount , 
        payment_boolean, 
        stripe_checkout_session_id,
        created_at
    )
    print('pdf generation done....')

    print('sending mail...')
    subject = 'Payment Invoice'
    message = 'Please find the attached payment invoice.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    attachment = open(file_path, 'rb')
    email = EmailMessage(subject, message, from_email, recipient_list)
    email.attach(file_path.split('/')[-1], attachment.read(), 'application/pdf')
    email.send()
    attachment.close()
    os.remove(file_path)
    print('mail sent....')

    return True


