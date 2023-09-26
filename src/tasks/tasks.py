import smtplib
from email.message import EmailMessage

from celery import Celery

from src.db.config import SMTP_USER, SMTP_PASSWORD

celery = Celery('tasks', broker='redis://localhost:6379/0')

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465


def get_email_template_dashboard(username: str, user_email: str):
    email = EmailMessage()
    email['Subject'] = 'YOUR MESSAGE'
    email['From'] = user_email
    email['To'] = SMTP_USER

    email.set_content(
        '<div>'
        f'<h1 style="color: red;">Здравствуйте, {username}, а вот и ваш отчет. Зацените 😊</h1>'
        '<img src="https://static.vecteezy.com/system/resources/previews/008/295/031/original/custom-relationship'
        '-management-dashboard-ui-design-templates-suitable-designing-application-for-android-and-ios-clean-style-app'
        '-mobile-free-vector.jpg" width="600">'
        '</div>',
        subtype='html'
    )

    return email


@celery.task
def send_email_report_dashboard(username: str, user_email: str):
    email = get_email_template_dashboard(username=username, user_email=user_email)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)


