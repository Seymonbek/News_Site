from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    # null=True olib tashlandi: har bir foydalanuvchining profili bo'lishi shart
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/', null=True, blank=True, verbose_name='Rasm')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Tug\'ilgan sana')
    # IntegerField → CharField: telefon raqamlar "+" va "-" belgilarini ham qabul qilishi kerak
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Telefon')

    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profillar'

    def __str__(self):
        return f"{self.user.username}"
