# Generated by Django 4.2.7 on 2023-12-17 17:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('places', '0005_alter_place_city_alter_place_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='image',
            field=models.ImageField(blank=True, upload_to='positive/place_pictures/'),
        ),
        migrations.AlterField(
            model_name='place',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]