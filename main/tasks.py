from celery import shared_task
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy


@shared_task
def send_email(emails: list, blog):
    send_mail(
        subject='Uploaded new Todo',
        message=f'''
Title: {blog['title']}
Description: {blog['description']}
Price: {blog['price']}
Link: http://127.0.0.1:8000/api/blog-update/{blog['id']}
        ''',
        from_email='From Programmers Team',
        recipient_list=emails,
        fail_silently=True
    )
    return 'Done'
