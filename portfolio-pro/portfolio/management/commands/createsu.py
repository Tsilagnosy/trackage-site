from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **options):

        User = get_user_model()

        username = settings.DJANGO_SUPERUSER_USERNAME

        email = settings.DJANGO_SUPERUSER_EMAIL

        password = settings.DJANGO_SUPERUSER_PASSWORD

        if not User.objects.filter(
            username=username
        ).exists():

            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )

            self.stdout.write(
                self.style.SUCCESS(
                    'Superuser created successfully'
                )
            )

        else:

            self.stdout.write(
                'Superuser already exists'
            )
	
	
	
	
	
	
	
	
	