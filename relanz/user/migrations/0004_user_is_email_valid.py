# Generated by Django 4.2.2 on 2023-06-26 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_email_valid',
            field=models.BooleanField(default=False),
        ),
    ]
