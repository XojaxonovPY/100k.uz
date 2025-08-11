# 🏆 💼 100k.uz

## 📌 Loyihaning qisqacha tavsifi

**💼 100k.uz** - bu Django va Jinja2 shablonlari yordamida ishlab chiqilgan mustaqil ish platformasi. 
Bu foydalanuvchilarga frilanser ish joylarini joylashtirish, ularga ariza berish va ish jarayonlarini boshqarish imkonini beradi. 
Platforma fon vazifalari uchun Seldereydan va ma'lumotlar bazasi sifatida PostgreSQL-dan foydalanadi va[100.uz](https://100k.uz/) sayti asosida yaratigan .

## ⚙️ Asosiy xususiyatlar

- **Django**: Yuqori samaradorlikka ega va ko‘p imkoniyatli Python web-framework. Kengaytirilgan ORM, autentifikatsiya, admin panel va boshqa ko‘plab tayyor funksiyalarni taqdim etadi.
- **Redis**: Xotirada ishlovchi tezkor ma’lumotlar bazasi. Kesh, navbat va xabar brokeri sifatida keng qo‘llanadi.
- **Celery**: Asinxron fon vazifalarini bajarish va periodik ishlarni rejalashtirish uchun Python kutubxonasi.
- **Docker**: Ilovani konteynerlash va uni turli muhitlarda barqaror ishlashini ta’minlaydi
- **Frontend**: Foydalanuvchi interfeysini yaratish qismi. HTML, CSS, JavaScript va frontend freymvorklar yordamida ishlanadi.

## 🛠 Texnologiyalar

| Texnologiya  | Tavsifi                                                              |
|--------------|----------------------------------------------------------------------|
| Python 3.12  | Asosiy dasturlash tili                                               |
| Django       | Yuqori samaradorlikka ega va ko‘p imkoniyatli Python web-framework   |
| PostgreSQL   | Ma’lumotlar bazasi                                                   |
| Docker       | Konteynerizatsiya                                                    |
| Frontend     | HTML, CSS, JavaScript va frontend freymvorklar yordamida ishlanadi   |

## 🛠️ O'rnatish va ishga tushirish

1. Repositoriyani klonlash

```bash
git clone https://github.com/XojaxonovPY/100k.uz.git
cd 100k.uz
```

2. Virtual muhit yaratish va kutubxonalarni o'rnatish

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

3. Docker yordamida ishga tushirish

```bash
docker-compose up --build
```

4. Ma'lumotlar bazasini migratsiya qilish

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Ilovani ishga tushirish

```bash
python manage.py runserver 0.0.0.0:8000
```
Ilova http://127.0.0.1:8000 manzilida ishga tushadi.
Ilov hozir ishlayotgan url https://one00k-uz.onrender.com/

## 🔧 .env konfiguratsiyasi

Ilova ishlashi uchun `.env` faylida quyidagi parametrlarni sozlash kerak:

```env
DB_DJANGO=Your_db_url
DP_NAME=Your_db_name
DP_USER=Your_db_username
DP_PASSWORD=Your_db_password
DP_HOST=Your_db_host
DP_PORT=Your_db_port
EMAIL=your_email
PASSWORD=your_password
REDIS_URL=redis://host:port/0
```

## 📄 Litsenziya

Loyiha MIT litsenziyasi asosida tarqatiladi.
