
from django.core.management.base import BaseCommand
from faker import Faker
import random
from django.utils import timezone
from datetime import timedelta
from analytics.models import User, Video, WatchSession

class Command(BaseCommand):
    help = "Generate sample data for analytics demo"

    def handle(self, *args, **options):
        fake = Faker()
        devices = ['mobile','web','tv','tablet']
        genres = ['Drama','Comedy','Action','Sci-Fi','Documentary']

        # create users
        for i in range(20):
            User.objects.create(
                name=fake.name(),
                email=fake.unique.email(),
                registration_date=fake.date_time_this_year(tzinfo=timezone.utc)
            )

        # create videos
        for i in range(50):
            Video.objects.create(
                title=fake.sentence(nb_words=3),
                genre=random.choice(genres),
                duration=random.randint(300, 7200)
            )

        users = list(User.objects.all())
        videos = list(Video.objects.all())
        # create sessions
        for i in range(500):
            user = random.choice(users)
            video = random.choice(videos)
            start = timezone.now() - timedelta(days=random.randint(0, 10), hours=random.randint(0,23), minutes=random.randint(0,59))
            watch_seconds = random.randint(30, min(video.duration, 3600))
            end = start + timedelta(seconds=watch_seconds)
            WatchSession.objects.create(
                user=user,
                video=video,
                start_time=start,
                end_time=end,
                device_type=random.choice(devices),
                ip_address=fake.ipv4(),
                is_rewatch=random.choice([True, False, False])
            )
        self.stdout.write(self.style.SUCCESS('Seed data created.'))
