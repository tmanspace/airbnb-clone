# Generated by Django 2.2.5 on 2020-12-21 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_email_secret'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='login_method',
            field=models.CharField(choices=[('email', 'Email'), ('github', 'Github')], default='email', max_length=20),
        ),
    ]
