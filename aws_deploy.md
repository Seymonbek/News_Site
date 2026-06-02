# AWS EC2 ga joylash — To'liq qo'llanma

## Kerakli narsalar
- AWS akkaunt (aws.amazon.com)
- Domain nom (ixtiyoriy, bo'lmasa EC2 public IP ishlatiladi)

---

## 1-QADAM: EC2 Instance yaratish

1. AWS Console → EC2 → **Launch Instance**
2. Quyidagilarni tanlang:
   - **Name:** `biznews-server`
   - **OS:** Ubuntu Server 22.04 LTS (Free tier eligible)
   - **Instance type:** `t2.micro` (Free tier) yoki `t3.small` (ko'proq RAM)
   - **Key pair:** Yangi yarating → `biznews-key.pem` yuklab oling
   - **Security Group — quyidagi portlarni oching:**

| Port | Protocol | Source    | Maqsad               |
|------|----------|-----------|----------------------|
| 22   | TCP      | My IP     | SSH kirish           |
| 80   | TCP      | 0.0.0.0/0 | HTTP                 |
| 443  | TCP      | 0.0.0.0/0 | HTTPS                |

3. **Storage:** 20 GB gp3 (rasmlar va DB uchun yetarli)
4. **Launch Instance** tugmasini bosing

---

## 2-QADAM: Serverga SSH orqali ulanish

```bash
# Key faylini himoyalang
chmod 400 biznews-key.pem

# Ulanish (EC2 Public IP ni AWS Console dan oling)
ssh -i biznews-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

---

## 3-QADAM: Server muhitini sozlash

```bash
# Tizimni yangilash
sudo apt update && sudo apt upgrade -y

# Kerakli paketlar
sudo apt install -y python3-pip python3-venv nginx git certbot python3-certbot-nginx

# Loyiha papkasi
sudo mkdir -p /var/www/biznews
sudo chown ubuntu:ubuntu /var/www/biznews
```

---

## 4-QADAM: Loyihani serverga yuklash

### Variant A — GitHub orqali (tavsiya etiladi)
```bash
cd /var/www/biznews
git clone https://github.com/YOUR_USERNAME/News_Site.git .
```

### Variant B — SCP orqali (GitHub yo'q bo'lsa)
```bash
# Mahalliy kompyuterda (loyiha papkasida)
scp -i biznews-key.pem -r /home/seymonbek/Downloads/News_Site/* ubuntu@YOUR_EC2_IP:/var/www/biznews/
```

---

## 5-QADAM: Python muhitini sozlash

```bash
cd /var/www/biznews

# Virtual environment
python3 -m venv venv
source venv/bin/activate

# Paketlarni o'rnatish
pip install -r requirements.txt
```

---

## 6-QADAM: .env faylini yaratish

```bash
cp .env.example .env
nano .env
```

Quyidagilarni to'ldiring:
```
SECRET_KEY=yangi-maxfiy-kalit-bu-yerga
DEBUG=False
ALLOWED_HOSTS=YOUR_EC2_IP,yourdomain.com,www.yourdomain.com

DB_ENGINE=django.db.backends.sqlite3

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=sizning@gmail.com
EMAIL_HOST_PASSWORD=gmail-app-parolingiz
DEFAULT_FROM_EMAIL=sizning@gmail.com
```

**SECRET_KEY yaratish:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 7-QADAM: Django sozlash

```bash
source venv/bin/activate
cd /var/www/biznews

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

---

## 8-QADAM: Gunicorn sozlash (systemd service)

```bash
sudo nano /etc/systemd/system/biznews.service
```

Quyidagini yozing:
```ini
[Unit]
Description=BizNews Django Application
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/var/www/biznews
ExecStart=/var/www/biznews/venv/bin/gunicorn \
    config.wsgi:application \
    --bind 127.0.0.1:8000 \
    --workers 3 \
    --timeout 120 \
    --access-logfile /var/log/biznews/access.log \
    --error-logfile /var/log/biznews/error.log
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

```bash
# Log papkasini yaratish
sudo mkdir -p /var/log/biznews
sudo chown ubuntu:ubuntu /var/log/biznews

# Serviceni yoqish
sudo systemctl daemon-reload
sudo systemctl enable biznews
sudo systemctl start biznews
sudo systemctl status biznews
```

---

## 9-QADAM: Nginx sozlash

```bash
sudo nano /etc/nginx/sites-available/biznews
```

Quyidagini yozing:
```nginx
server {
    listen 80;
    server_name YOUR_EC2_IP yourdomain.com www.yourdomain.com;

    # Static fayllar — Nginx to'g'ridan-to'g'ri beradi (tez)
    location /static/ {
        alias /var/www/biznews/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media fayllar
    location /media/ {
        alias /var/www/biznews/media/;
        expires 7d;
    }

    # Django ilova
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_read_timeout 120s;
    }

    # Max upload size (rasm yuklash uchun)
    client_max_body_size 10M;
}
```

```bash
# Nginx ni yoqish
sudo ln -s /etc/nginx/sites-available/biznews /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 10-QADAM: SSL (HTTPS) — Let's Encrypt bilan bepul

> Domain nom bo'lsa bajarish mumkin. IP bilan ishlamaydi.

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Certbot avtomatik Nginx konfiguratsiyasini HTTPS ga o'tkazadi.

---

## 11-QADAM: Media fayllar uchun AWS S3 (ixtiyoriy, lekin tavsiya)

EC2 restart bo'lsa yoki instance o'chirilsa media fayllar yo'qolmasligi uchun S3 ishlatish kerak.

```bash
pip install django-storages boto3
```

`.env` ga qo'shing:
```
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=biznews-media
AWS_S3_REGION_NAME=us-east-1
```

`settings.py` ga qo'shing (DEBUG=False bo'lganda):
```python
if not DEBUG:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/'
```

---

## Monitoring — Server tekshirish

```bash
# Gunicorn holati
sudo systemctl status biznews

# Nginx holati
sudo systemctl status nginx

# Loglar
sudo tail -f /var/log/biznews/error.log
sudo tail -f /var/log/nginx/error.log

# Gunicorn qayta ishga tushirish
sudo systemctl restart biznews
```

---

## Yangilik chiqarilganda kod yangilash (deploy)

```bash
cd /var/www/biznews
source venv/bin/activate

# Yangi kod yuklash
git pull origin main

# Yangi paketlar (agar bo'lsa)
pip install -r requirements.txt

# Migratsiyalar
python manage.py migrate

# Static fayllar
python manage.py collectstatic --noinput

# Serverni qayta ishga tushirish
sudo systemctl restart biznews
```

---

## Xarajat hisob-kitobi (AWS Free Tier)

| Xizmat | Free Tier | Narx (keyinchalik) |
|--------|-----------|---------------------|
| EC2 t2.micro | 750 soat/oy (1 yil) | ~$10/oy |
| EBS 20GB | 30 GB/oy (1 yil) | ~$2/oy |
| Bandwidth | 15 GB/oy | $0.09/GB |
| Elastic IP | 1 ta bepul (instance yoqiq) | $3.6/oy |
| **Jami** | **1 yil bepul** | **~$15/oy** |

---

## Deployment checklist

- [ ] EC2 instance yaratildi (Ubuntu 22.04)
- [ ] Security Group portlari ochildi (22, 80, 443)
- [ ] SSH orqali ulandi
- [ ] Loyiha yuklandi
- [ ] `.env` to'ldirildi (`DEBUG=False`, `SECRET_KEY`, `ALLOWED_HOSTS`)
- [ ] `migrate`, `collectstatic`, `createsuperuser` bajarildi
- [ ] Gunicorn service ishlayapti
- [ ] Nginx sozlandi va ishlayapti
- [ ] SSL o'rnatildi (domain bo'lsa)
- [ ] Media fayllar S3 da (ixtiyoriy)
