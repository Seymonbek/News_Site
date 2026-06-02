from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse


class PublishedManager(models.Manager):
    """Faqat chop etilgan (Published) yangiliklarni qaytaradi."""
    def get_queryset(self):
        return super().get_queryset().filter(status=News.Status.PUBLISHED)


class Category(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'

    def __str__(self):
        return self.name


class News(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Qoralama'
        PUBLISHED = 'PB', 'Chop etilgan'

    title = models.CharField(max_length=300, verbose_name='Sarlavha')
    slug = models.SlugField(max_length=300, unique=True, verbose_name='Slug')
    body = models.TextField(verbose_name='Matn')
    image = models.ImageField(upload_to='news/images', null=True, blank=True, verbose_name='Rasm')
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='news',
        verbose_name='Kategoriya'
    )
    publish_time = models.DateTimeField(default=timezone.now, verbose_name='Chop etish vaqti')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='Yangilangan vaqt')
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name='Holat'
    )

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish_time']
        verbose_name = 'Yangilik'
        verbose_name_plural = 'Yangiliklar'
        indexes = [
            models.Index(fields=['-publish_time']),
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail_page', args=[self.slug])

class ContactData(models.Model):
    address = models.CharField(max_length=150, verbose_name='Manzil')
    phone = models.CharField(max_length=50, verbose_name='Telefon')
    email = models.EmailField(verbose_name='Email')

    class Meta:
        verbose_name = 'Aloqa ma\'lumoti'
        verbose_name_plural = 'Aloqa ma\'lumotlari'

    def __str__(self):
        return self.address


class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name='Ism')
    email = models.EmailField(max_length=100, verbose_name='Email')
    subject = models.CharField(max_length=150, verbose_name='Mavzu')
    message = models.TextField(verbose_name='Xabar')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='Yuborilgan vaqt')

    class Meta:
        verbose_name = 'Xabar'
        verbose_name_plural = 'Xabarlar'
        ordering = ['-created_time']

    def __str__(self):
        return f"{self.name} — {self.subject}"


class Comment(models.Model):
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Yangilik'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Foydalanuvchi'
    )
    body = models.TextField(max_length=300, verbose_name='Izoh')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='Vaqt')
    active = models.BooleanField(default=True, verbose_name='Faol')

    class Meta:
        ordering = ['created_time']
        verbose_name = 'Izoh'
        verbose_name_plural = 'Izohlar'

    def __str__(self):
        return f"{self.user.username}: {self.body[:50]}"
