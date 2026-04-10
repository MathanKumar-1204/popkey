from django.core.management.base import BaseCommand
from accounts.models import User, Admin

class Command(BaseCommand):
    help = 'Create initial admin user'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            # Create admin user with role='admin'
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                role='admin',
                name='System Admin'
            )
            
            # Create Admin model instance
            Admin.objects.create(
                user=admin_user,
                name='System Admin'
            )
            
            self.stdout.write(self.style.SUCCESS('Admin user created successfully!'))
            self.stdout.write('Username: admin')
            self.stdout.write('Password: admin123')
            self.stdout.write('Role: admin')
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))
