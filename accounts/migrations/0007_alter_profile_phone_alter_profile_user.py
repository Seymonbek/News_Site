# Migration: Profile.user null=True olib tashlandi, phone IntegerField → CharField

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_profile_photo_en_remove_profile_photo_ru_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # phone: IntegerField → CharField (telefon raqamlar +, -, bo'sh joy qabul qilishi uchun)
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Telefon'),
        ),
        # user: null=True olib tashlandi — har bir profilning egasi bo'lishi shart
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
