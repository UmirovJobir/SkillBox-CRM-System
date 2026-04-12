import random

from django.core.management.base import BaseCommand
from faker import Faker

from advertisements.models import Advertisement
from contracts.models import Contract
from customers.models import Customer
from leads.models import Lead
from products.models import Product

fake = Faker("ru_RU")


class Command(BaseCommand):
    help = "Заполнить базу данных тестовыми данными"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Очистить все данные перед заполнением",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write("Очищаю базу данных...")
            Contract.objects.all().delete()
            Customer.objects.all().delete()
            Lead.objects.all().delete()
            Advertisement.objects.all().delete()
            Product.objects.all().delete()
            self.stdout.write(self.style.WARNING("База очищена."))

        self._seed_products()
        self._seed_advertisements()
        self._seed_leads()
        self._seed_customers()
        self._seed_contracts()

        self.stdout.write(self.style.SUCCESS("Готово! База заполнена тестовыми данными."))

    def _seed_products(self):
        names = [
            "Веб-разработка",
            "SEO-продвижение",
            "Контекстная реклама",
            "SMM-маркетинг",
            "Email-рассылки",
            "Мобильное приложение",
            "Дизайн сайта",
            "Техническая поддержка",
        ]
        count = 0
        for name in names:
            _, created = Product.objects.get_or_create(
                name=name,
                defaults={"description": fake.text(max_nb_chars=100)},
            )
            if created:
                count += 1
        self.stdout.write(f"  Услуги: создано {count} из {len(names)}")

    def _seed_advertisements(self):
        products = list(Product.objects.all())
        if not products:
            self.stdout.write(self.style.ERROR("  Нет услуг для рекламных кампаний"))
            return
        ad_names = [
            "Google Ads — Весна 2024",
            "VK Реклама — Квартал 1",
            "Яндекс.Директ — Лето",
            "Instagram Ads — Акция",
            "Таргет ВКонтакте",
            "Telegram Ads — Осень",
        ]
        count = 0
        for name in ad_names:
            _, created = Advertisement.objects.get_or_create(
                name=name,
                defaults={
                    "product": random.choice(products),
                    "budget": random.randint(5, 100) * 1000,
                },
            )
            if created:
                count += 1
        self.stdout.write(f"  Рекламные кампании: создано {count} из {len(ad_names)}")

    def _seed_leads(self):
        ads = list(Advertisement.objects.all())
        if not ads:
            self.stdout.write(self.style.ERROR("  Нет рекламных кампаний для лидов"))
            return
        count = 0
        for _ in range(30):
            Lead.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone=fake.phone_number(),
                email=fake.email(),
                advertisement=random.choice(ads),
            )
            count += 1
        self.stdout.write(f"  Лиды: создано {count}")

    def _seed_customers(self):
        # Берём лидов без Customer и конвертируем часть из них
        leads_without_customer = Lead.objects.filter(customer__isnull=True)
        sample = random.sample(
            list(leads_without_customer),
            min(12, leads_without_customer.count()),
        )
        count = 0
        for lead in sample:
            Customer.objects.create(lead=lead)
            count += 1
        self.stdout.write(f"  Активные клиенты: создано {count}")

    def _seed_contracts(self):
        customers = list(Customer.objects.all())
        products = list(Product.objects.all())
        if not customers or not products:
            self.stdout.write(self.style.ERROR("  Нет клиентов или услуг для контрактов"))
            return
        count = 0
        for customer in customers:
            # Каждому клиенту 1–2 контракта
            for _ in range(random.randint(1, 2)):
                start = fake.date_between(start_date="-1y", end_date="today")
                end = fake.date_between(start_date="today", end_date="+1y")
                Contract.objects.create(
                    name=f"Договор №{fake.numerify('###-####')}",
                    product=random.choice(products),
                    customer=customer,
                    start_date=start,
                    end_date=end,
                    cost=random.randint(10, 500) * 1000,
                )
                count += 1
        self.stdout.write(f"  Контракты: создано {count}")
