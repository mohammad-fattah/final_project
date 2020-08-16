<div dir="rtl">

# موضوع پروژه

هدف از این پروژه، تحلیل فروش محصولات مختلف در استان ها و شهرهای مختلف می‌باشد. ورودی برنامه وارد یک
برنامه به زبان C خواهد شد. این برنامه وظیفه دارد تا اطلاعات محصولات مختلف را برای یک شهر تجمیع کند. در
واقع ، هر شهر دارای فروشگاه های مختلفی می‌باشد که اطلاعات فروش محصولات خود را در این سامانه وارد می‌کنند.
برنامه نوشته شده به زبان C این اطلاعات را برای هر شهر تجمیع می‌کند و در داخل پایگاه داده ذخیره می‌کند.
در مرحله بعد، برنامه نوشته شده به زبان پایتون این اطلاعات را از پایگاه داده خوانده و تحلیل های مختلفی برای آن ایجاد
می‌کند.

## نصب موارد مورد نیاز

برای نصب پایگاه داده postgresql از دستور زیر استفاده می کنیم:
```
sudo apt-get install postgresql
```
سپس برای استفاده از postgresql در زبان c کتابخانه زیر را نصب می‌کنیم:

```
sudo apt-get install libpq-dev
```
برای مسائل امنیتی postgresql فقط به کاربری که به اسم سیستم عامل باشد اجازه می دهد تا به پایگاه داده های مختلف متصل شود برای اجتناب از این امر در فایل pg_hba.conf که در مسیر etc/postgresql/'your postgresql version'/main قرار دارد رفته و در خط اول و دوم بدون در نظر گرفتن کامنت ها peer را به md5 تبدیل می‌کنیم.
سپس برای استفاده از postgresql در زبان python کتابخانه زیر را نصب می‌کنیم:
```
pip install psycopg2
```
برای این که کد پایتون در هر نیم ساعت اجرا شود کتابخانه زیر را نصب می‌کنیم:

```
pip install schedule
```
## نحوه اجرا پروژه

برای اجرای پروژه فایل run_30_minute را اجرا کرده و این فایل، فایل query.py را در هر ۳۰ دقیقه اجرا کرده و این فایل نیز فایل c و bash را اجرا می‌کند.
</div>
