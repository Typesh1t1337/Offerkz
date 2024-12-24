from django.core.mail import send_mail,EmailMessage
from OFFERKZ.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model


def send_html_message(email,username):
    subject = "Добро пожаловать OFFERKZ"
    from_email = EMAIL_HOST_USER
    recipient = [email]


    user = get_user_model().objects.filter(email=email).first()

    token = default_token_generator.make_token(user)

    uid = urlsafe_base64_encode(force_bytes(user.pk))

    confirmation_url = f"http://127.0.0.1:8000/accounts/confirm/{uid}/{token}"



    credentials = {
        'user': username,
        'link': 'link',
        'confirmation_url': confirmation_url,
    }

    html_content = render_to_string("email.html",credentials)

    email = EmailMessage(subject, html_content, from_email, recipient)
    email.content_subtype = "html"
    email.send()


