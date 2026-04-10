from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import CustomUser
from events.models import Category, Event

class Command(BaseCommand):
    help = 'Seeds the database with sample data'

    def handle(self, *args, **kwargs):
        # Create categories
        cats = ['Technology', 'Music', 'Sports', 'Workshop', 'Conference', 'Art']
        for cat in cats:
            Category.objects.get_or_create(name=cat)
        self.stdout.write(self.style.SUCCESS('Categories created.'))

        # Create organizer user
        if not CustomUser.objects.filter(username='organizer1').exists():
            org = CustomUser.objects.create_user(
                username='organizer1', email='organizer1@example.com',
                password='organizer123', role='organizer'
            )
            self.stdout.write(self.style.SUCCESS('Organizer user created: organizer1 / organizer123'))

        # Create participant user
        if not CustomUser.objects.filter(username='user1').exists():
            CustomUser.objects.create_user(
                username='user1', email='user1@example.com',
                password='user12345', role='participant'
            )
            self.stdout.write(self.style.SUCCESS('Participant user created: user1 / user12345'))

        org = CustomUser.objects.get(username='organizer1')
        tech_cat = Category.objects.get(name='Technology')
        music_cat = Category.objects.get(name='Music')

        # Create sample events
        today = timezone.now().date()
        import datetime
        events_data = [
            {
                'title': 'Python Workshop 2025',
                'description': 'An intensive Python programming workshop for beginners and intermediates.',
                'venue': 'Tech Hub, Bangalore',
                'category': tech_cat,
                'date': today + datetime.timedelta(days=10),
                'time': datetime.time(10, 0),
                'total_seats': 50,
                'ticket_price': 500,
                'status': 'upcoming',
            },
            {
                'title': 'Web Dev Bootcamp',
                'description': 'Full-stack web development bootcamp covering Django, React and more.',
                'venue': 'Innovation Centre, Chennai',
                'category': tech_cat,
                'date': today + datetime.timedelta(days=20),
                'time': datetime.time(9, 0),
                'total_seats': 30,
                'ticket_price': 1200,
                'status': 'upcoming',
            },
            {
                'title': 'Free Music Festival',
                'description': 'A free outdoor music festival featuring local bands.',
                'venue': 'City Park, Hyderabad',
                'category': music_cat,
                'date': today + datetime.timedelta(days=5),
                'time': datetime.time(17, 0),
                'total_seats': 200,
                'ticket_price': 0,
                'status': 'upcoming',
            },
        ]
        for ed in events_data:
            if not Event.objects.filter(title=ed['title']).exists():
                Event.objects.create(organizer=org, available_seats=ed['total_seats'], **ed)
        self.stdout.write(self.style.SUCCESS('Sample events created.'))
        self.stdout.write(self.style.SUCCESS('\nDone! Run: python manage.py createsuperuser to create admin.'))
