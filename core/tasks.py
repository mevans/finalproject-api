from celery import shared_task
from django.utils import timezone
from fcm_django.models import FCMDevice

from core.models import VariableNotification
from core.utils import get_next_notification_time


@shared_task
def send_variable_notifications():
    ready_notifications = VariableNotification.objects.filter(scheduled_for__lte=timezone.now())
    for notification in ready_notifications:
        instance = notification.instance
        user = instance.patient.user
        preferences = instance.notification_preference
        if preferences.enabled:
            # send notification
            device = FCMDevice.objects.filter(user=user).first()
            if device is not None:
                device.send_message(title="Friendly Reminder", body=f"Time to log your {instance.variable.name}")
        # create new notification
        schedule = instance.schedule
        time = instance.notification_preference.time
        if schedule is not None and time is not None:
            new_scheduled_for = get_next_notification_time(schedule, time, inc=False)
            new_notification = VariableNotification(instance=instance, scheduled_for=new_scheduled_for)
            new_notification.save()
        # delete notification
        notification.delete()
