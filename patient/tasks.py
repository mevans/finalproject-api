from celery import shared_task
from fcm_django.models import FCMDevice


@shared_task
def send_email():
    print("wassupss")
    for device in FCMDevice.objects.all().iterator():
        device.send_message(title="Testing", body="123")
