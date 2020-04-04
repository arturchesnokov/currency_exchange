from account.models import Contact
from currency.models import Rate
from django.urls import reverse


# python manage.py test -v 2
class DbHelpers:

    @staticmethod
    def create_rate(currency, buy_rate, sale_rate, source):
        r = Rate(currency=currency, buy=buy_rate, sale=sale_rate, source=source)
        r.save()
        return r.id

    @staticmethod
    def get_rate(_id):
        try:
            return Rate.objects.get(id=_id)
        except Rate.DoesNotExist:
            return None

    @staticmethod
    def create_contact(email, title, text):
        c = Contact(email=email, title=title, text=text)
        c.save()
        return c.id

    @staticmethod
    def get_contact(_id):
        try:
            return Contact.objects.get(id=_id)
        except Contact.DoesNotExist:
            return None
