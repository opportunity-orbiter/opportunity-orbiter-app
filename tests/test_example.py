from orbiter.core.models import User
from django.core import mail
from django.test import TestCase


def test_create_user_username(db):
    user = User.objects.create_user("Mark")
    assert user.username == "Mark"


class EmailTest(TestCase):
    """_summary_

    Args:
        TestCase (_type_): _description_
    """

    def test_send_email(self):
        mail.send_mail(
            "Subject here",
            "Here is the message.",
            "hey@opportunity-orbiter.com",
            ["quirin.koch@gmail.com"],
            fail_silently=False,
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Subject here")
