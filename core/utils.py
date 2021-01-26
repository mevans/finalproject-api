import datetime

from django.apps import apps
from django.utils.timezone import make_aware


def get_next_notification_time(schedule, time, inc=True):
    next_day = schedule.after(datetime.datetime.utcnow(), inc=inc)
    next_time = datetime.datetime.combine(next_day, time)
    while next_time < datetime.datetime.utcnow():
        next_time = schedule.after(next_time, inc=True)
    tz_aware = make_aware(next_time)
    return tz_aware


def rebuild_notifications(variable_instance):
    variable_notification_model = apps.get_model('core.VariableNotification')
    variable_notification_model.objects.filter(instance=variable_instance).delete()  # delete all existing notifications
    if variable_instance.schedule is not None:
        scheduled_for = get_next_notification_time(variable_instance.schedule,
                                                   variable_instance.notification_preference.time,
                                                   inc=True)
        first_notification = variable_notification_model(instance=variable_instance,
                                                         scheduled_for=scheduled_for)
        first_notification.save()
