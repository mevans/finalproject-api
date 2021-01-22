from django.core.mail import send_mail


class Mailer:
    def send_invite_email(self, invite):
        link = invite.generate_link()
        send_mail(from_email="matthew@evans99.co.uk", recipient_list=[invite.email], subject="Invitation",
                  message="You have been invited to join Canoe! Click here on your mobile device to accept your invitation " + link,
                  fail_silently=False)


mailer = Mailer()
