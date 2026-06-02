# Serverga joylash qo'llanmasi

## 1. Serverga ulanish va loyihani yuklash

```bash
# Serverga SSH orqali ulaning
ssh user@your-server-ip

# Loyihani klonlash
git clone https://github.com/sizning-repo/News_Site.git
cd News_Site
```

---

## 2. Virtual environment va paketlarni o'rnatish

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 3. `.env` faylini yaratish

```bash
cp .env.example .env
nano .env
```

`.env` faylini to'ldiring:

```
SECRET_KEY=bu-yerga-uzun-tasodifiy-kalit-yozing
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DB_ENGINE=django.db.backends.sqlite3

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=sizning@gmail.com
EMAIL_HOST_PASSWORD=gmail-app-password
DEFAULT_FROM_EMAIL=sizning@gmail.com
```

> **SECRET_KEY yaratish:** Python'da quyidagini ishga tushiring:
> ```python
> python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

> **Gmail App Password:** Gmail → Sozlamalar → Xavfsizlik → 2FA yoqing → App passwords → yangi parol oling

---

## 4. Django buyruqlari

```bash
# Migratsiyalarni bajarish
python manage.py migrate

# Static fayllarni yig'ish (WhiteNoise uchun)
python manage.py collectstatic --noinput

# Superuser yaratish
python manage.py createsuperuser

# Tarjimalarni compile qilish
python manage.py compilemessages
```

---

## 5. Gunicorn bilan ishga tushirish

```bash
# Test uchun
gunicorn config.wsgi:application --bind 0.0.0.0:8000

# Fon rejimida
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --daemon
```

---

## 6. Nginx sozlash (tavsiya etiladi)

`/etc/nginx/sites-available/newssite` faylini yarating:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Static fayllar
    location /static/ {
        alias /path/to/News_Site/staticfiles/;
    }

    # Media fayllar
    location /media/ {
        alias /path/to/News_Site/media/;
    }

    # Django ilovasi
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Nginx'ni yoqish
sudo ln -s /etc/nginx/sites-available/newssite /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 7. Systemd service (server restart bo'lsa avtomatik ishga tushadi)

`/etc/systemd/system/newssite.service` faylini yarating:

```ini
[Unit]
Description=News Site Gunicorn
After=network.target

[Service]
User=your-linux-user
WorkingDirectory=/path/to/News_Site
ExecStart=/path/to/News_Site/venv/bin/gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 3
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable newssite
sudo systemctl start newssite
sudo systemctl status newssite
```

---

## 8. SSL (HTTPS) — Let's Encrypt bilan bepul

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## Tekshirish ro'yxati (Deploy oldidan)

- [ ] `.env` fayli yaratildi va to'ldirildi
- [ ] `DEBUG=False` qilingan
- [ ] `ALLOWED_HOSTS` to'g'ri domen yozilgan
- [ ] `SECRET_KEY` yangi va maxfiy
- [ ] `python manage.py migrate` bajarildi
- [ ] `python manage.py collectstatic` bajarildi
- [ ] `python manage.py compilemessages` bajarildi
- [ ] Superuser yaratildi
- [ ] Gunicorn ishlayapti
- [ ] Nginx sozlangan
- [ ] SSL sertifikat o'rnatildi
