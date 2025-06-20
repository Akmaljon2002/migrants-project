import calendar
from datetime import datetime, timedelta, date
from django.core.management.base import BaseCommand
from faker import Faker
import random

from apps.border.models import BorderCross
from apps.migrant.constants import GenderChoices
from apps.migrant.models import Migrant

fake = Faker('uz_UZ')

REGION_IDS = list(range(1, 15))
DISTRICT_IDS = list(range(1, 50))
COUNTRY_IDS = [100, 101, 102, 103, 104]
TRIP_PURPOSE_IDS = [1, 2, 3, 4]
TRANSPORT_TYPES = [1, 2, 3, 4]
DIRECTION_CODES = ["OUT", "IN"]
ENDPOINT_IDS = list(range(1, 20))

MONTHS = [
    (2023 + (i // 12), (i % 12) + 1)
    for i in range(23)
]

class Command(BaseCommand):
    help = "Generate fake migrants and border cross data for statistics (oyma-oy)"

    def add_arguments(self, parser):
        parser.add_argument('--migrants', type=int, default=100000, help='Number of migrants to create')
        parser.add_argument('--crosses', type=int, default=3, help='Number of border crosses per migrant')

    def handle(self, *args, **options):
        migrant_count = options['migrants']
        crosses_per_migrant = options['crosses']

        self.stdout.write(self.style.WARNING(f'Generating {migrant_count} migrants...'))
        migrants = self.generate_fake_migrants(migrant_count)

        self.stdout.write(self.style.WARNING(f'Generating border crossings for each migrant...'))
        self.generate_fake_border_crosses(migrants, crosses_per_migrant)

        self.stdout.write(self.style.SUCCESS('✅ Fake data generation completed.'))

    def generate_fake_migrants(self, n):
        migrants = []
        for i in range(n):
            birth_date = fake.date_of_birth(minimum_age=18, maximum_age=65)
            gender = random.choice([GenderChoices.MALE, GenderChoices.FEMALE])

            # Oy bo‘yicha taqsimlash (migrantlar sonini oyga mod qilish orqali)
            year, month = MONTHS[i % len(MONTHS)]
            last_day = calendar.monthrange(year, month)[1]
            day = random.randint(1, last_day)

            created_at = datetime(year, month, day, random.randint(0, 23), random.randint(0, 59), random.randint(0, 59))

            migrant = Migrant.objects.create(
                first_name=fake.first_name_male() if gender == GenderChoices.MALE else fake.first_name_female(),
                last_name=fake.last_name(),
                region_id=random.choice(REGION_IDS),
                district_id=random.choice(DISTRICT_IDS),
                pinfl=fake.unique.random_number(digits=14),
                birth_date=birth_date,
                gender=gender,
                created_at=created_at
            )
            migrants.append(migrant)
        return migrants

    def generate_fake_border_crosses(self, migrants, count_per_migrant):
        border_cross_months = [
            (2023 + (i // 12), (i % 12) + 1)
            for i in range(24)
        ]

        total_crosses = len(migrants) * count_per_migrant

        for idx, (migrant_index, migrant) in enumerate(enumerate(migrants)):
            for j in range(count_per_migrant):
                cross_idx = migrant_index * count_per_migrant + j
                year, month = border_cross_months[cross_idx % len(border_cross_months)]
                last_day = calendar.monthrange(year, month)[1]
                day = random.randint(1, last_day)

                reg_date = date(year, month, day)

                created_at = datetime(
                    year, month, day,
                    random.randint(0, 23),
                    random.randint(0, 59),
                    random.randint(0, 59)
                )

                BorderCross.objects.create(
                    reg_date=reg_date,
                    endpoint_id=random.choice(ENDPOINT_IDS),
                    direction_type_code=random.choice(DIRECTION_CODES),
                    migrant_id=migrant.id,
                    trip_purpose_id=random.choice(TRIP_PURPOSE_IDS),
                    driection_country_id=random.choice(COUNTRY_IDS),
                    transport_type_code_id=random.choice(TRANSPORT_TYPES),
                    created_at=created_at
                )

