# Generated by Django 4.2.2 on 2023-06-23 04:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0005_alter_challenge_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='challenge',
            old_name='recommnad',
            new_name='recommand',
        ),
    ]
