from django.core.management.base import BaseCommand
from faker import Faker
from ...models import Branch

class Command(BaseCommand):
    help = "create fake data for library models"

    def handle(self, *args, **options):
        fake = Faker(['ka_GE'])
        for i in range(10):
            address = fake.unique.address()
            work_days = 'ორშაბათი პარასკევი 09 - 20:00'
            tel_number = fake.unique.building_number()
            branch = Branch.objects.create(
                address = address,
                work_day = work_days,
                tel_number = tel_number
            )
            branch.save()
        