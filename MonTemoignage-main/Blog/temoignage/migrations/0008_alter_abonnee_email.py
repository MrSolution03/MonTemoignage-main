# Generated by Django 4.2 on 2023-06-07 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temoignage', '0007_remove_abonnee_confirmation_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abonnee',
            name='email',
            field=models.EmailField(max_length=255),
        ),
    ]
