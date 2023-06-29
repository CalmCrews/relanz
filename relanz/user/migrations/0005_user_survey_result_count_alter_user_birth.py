# Generated by Django 4.2.2 on 2023-06-26 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_user_is_email_valid'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='survey_result_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='birth',
            field=models.IntegerField(null=True),
        ),
    ]
