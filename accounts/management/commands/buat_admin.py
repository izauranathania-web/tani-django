from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Buat akun admin default (username: admin, password: admin123)'

    def handle(self, *args, **kwargs):
        if User.objects.filter(username='admin').exists():
            self.stdout.write(self.style.WARNING('Akun admin sudah ada.'))
            return
        User.objects.create_superuser(
            username='admin',
            password='admin123',
            email=''
        )
        self.stdout.write(self.style.SUCCESS(
            'Akun admin dibuat! Username: admin | Password: admin123\n'
            '⚠️  Segera ganti password setelah login pertama!'
        ))
