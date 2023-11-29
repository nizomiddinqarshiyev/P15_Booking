from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email(emails: list, blog):
    send_mail(
        subject='Uploaded new Blog',
        message=f'''
Title: {blog['title']}
Description: {blog['description']}
Link: http://10.10.4.251:8000/api/blog-update/{blog['id']}
        ''',
        from_email='From Programmers Team',
        recipient_list=emails,
        fail_silently=True
    )
    return 'Done'
