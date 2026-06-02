# BizNews — O'zbek Yangiliklar Portali

Django asosida qurilgan ko'p tilli yangiliklar veb-sayti. O'zbek, Rus va Ingliz tillarini qo'llab-quvvatlaydi.

## Texnologiyalar

- **Backend:** Python 3.11, Django 5.0
- **Frontend:** Vanilla CSS, Font Awesome, jQuery
- **Ma'lumotlar bazasi:** SQLite (dev) / PostgreSQL (prod)
- **I18n:** django-modeltranslation (uz/ru/en)
- **Production:** Gunicorn + Nginx + WhiteNoise

## Xususiyatlar

- Ko'p tilli qo'llab-quvvatlash (O'zbek, Rus, Ingliz)
- Yangiliklar bo'limlari: O'zbekiston, Jahon, Sport, Fan-texnika, Iqtisodiyot
- Maqola ko'rishlar hisoblagichi (django-hitcount)
- Foydalanuvchi izohlari tizimi
- To'liq autentifikatsiya (login, ro'yxatdan o'tish, parol tiklash)
- Superuser CRUD paneli
- Qidiruv funksiyasi
- Aloqa formasi
- Responsive dizayn

## O'rnatish

### 1. Repositoriyani klonlash

```bash
git clone https://github.com/Seymonbek/News_Site.git
cd News_Site
```

### 2. Virtual muhit yaratish

```bash
python3 -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows
```

### 3. Paketlarni o'rnatish

```bash
pip install -r requirements.txt
```

### 4. Muhit o'zgaruvchilarini sozlash

```bash
cp .env.example .env
```

`.env` faylini oching va quyidagilarni to'ldiring:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_ENGINE=django.db.backends.sqlite3

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

`SECRET_KEY` yaratish:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Migratsiyalarni bajarish

```bash
python manage.py migrate
```

### 6. Superuser yaratish

```bash
python manage.py createsuperuser
```

### 7. Serverni ishga tushirish

```bash
python manage.py runserver
```

Sayt: [http://127.0.0.1:8000/uz/](http://127.0.0.1:8000/uz/)

Admin panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Production (Serverga joylash)

### Static fayllarni yig'ish

```bash
python manage.py collectstatic --noinput
```

### Tarjimalarni compile qilish

```bash
python manage.py compilemessages
```

### Gunicorn bilan ishga tushirish

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

### Production `.env` sozlamalari

```
SECRET_KEY=very-long-random-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

---

## Loyiha tuzilmasi

```
News_Site/
├── app/              # Asosiy yangiliklar ilovasi
├── accounts/         # Foydalanuvchi autentifikatsiyasi
├── config/           # Django sozlamalari
├── templates/        # HTML shablonlar
├── static/           # CSS, JS, rasmlar
├── media/            # Foydalanuvchi yuklagan fayllar
├── locale/           # Tarjima fayllari (uz/ru/en)
└── requirements.txt
```

## Kategoriyalar

| Kategoriya | URL |
|---|---|
| O'zbekiston | `/uz/Uzbekistan/` |
| Jahon | `/uz/Jahon/` |
| Sport | `/uz/Sport/` |
| Fan va texnika | `/uz/Fan_texnika/` |
| Iqtisodiyot | `/uz/Iqtisodiyot/` |

## Litsenziya

MIT License
