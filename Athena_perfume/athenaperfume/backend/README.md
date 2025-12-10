# Athena Perfume — Backend (Django)

فروشگاه آنلاین عطر و ادکلن با امکانات کامل

## ویژگی‌های بک‌اند
- احراز هویت با JWT + httpOnly Cookie
- سیستم کامل محصولات با حجم‌های مختلف (هر حجم قیمت و موجودی جداگانه)
- تگ‌های هوشمند و گروه‌بندی شده (نت‌ها، فصل، ماندگاری)
- سبد خرید → ثبت سفارش مستقیم
- پنل ادمین کامل و حرفه‌ای
- API کاملاً RESTful و آماده تولید

## راه‌اندازی سریع (Development)

```bash
# نصب وابستگی‌ها
pip install -r requirements.txt

# اعمال migrationها
python manage.py migrate

# ساخت سوپریوزر
python manage.py createsuperuser

# اجرای سرور
python manage.py runserver