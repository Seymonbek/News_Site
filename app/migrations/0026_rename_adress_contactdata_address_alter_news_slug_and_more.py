# Migration: adress → address (typo tuzatish), slug unique, DB indexes, Meta verbose_name

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_alter_news_image'),
    ]

    operations = [
        # "adress" → "address" typo tuzatildi
        migrations.RenameField(
            model_name='contactdata',
            old_name='adress',
            new_name='address',
        ),
        # slug unique bo'lishi kerak — bir xil slug ikki yangilikda bo'lmasligi uchun
        migrations.AlterField(
            model_name='news',
            name='slug',
            field=models.SlugField(max_length=300, unique=True, verbose_name='Slug'),
        ),
        # DB darajasida indekslar — qidiruv va saralash tezlashadi
        migrations.AddIndex(
            model_name='news',
            index=models.Index(fields=['-publish_time'], name='news_publish_time_idx'),
        ),
        migrations.AddIndex(
            model_name='news',
            index=models.Index(fields=['slug'], name='news_slug_idx'),
        ),
        migrations.AddIndex(
            model_name='news',
            index=models.Index(fields=['status'], name='news_status_idx'),
        ),
        # Contact modeliga created_time qo'shildi
        migrations.AddField(
            model_name='contact',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Yuborilgan vaqt'),
        ),
    ]
