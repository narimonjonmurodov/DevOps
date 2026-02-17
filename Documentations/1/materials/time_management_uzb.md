## Vaqt xizmatini o'rnatish va sozlash
Unix-ga o'xshash operatsion tizimlarning ko'plab distributivlarida maxsus utilita sana va vaqtni sinxronlashtirish uchun javob beradi. U asl sozlamalar bo'yicha faol bo’lib, shuning uchun foydalanuvchilar uni biror tarzda sozlashlari yoki o'zgartirishlari shart emas. Biroq, ba'zida bunday ehtiyoj baribir turli sabablarga ko'ra paydo bo'ladi, masalan, tasodifiy to’xtab qolishlarda. \
Butun dunyodagi kompyuterlar NTP serverlari ierarxiyasidan foydalangan holda vaqtlarini Internet orqali standart etalon soatlari bilan sinxronlashtirish uchun NTP (tarmoqli vaqt protokoli) dan foydalanadilar. \
Avtomatik vaqt sinxronizatsiyasini sozlash, masalan, asl sozlamalar bo’yicha vaqt sinxronizatsiyasi uchun mas'ul bo'lgan timesyncd utilitasidan yanada ishonchliroq NTPD protokoliga o'tishda talab qilinishi mumkin. Buning uchun quyidagilar bajarilishi lozim:
- Standart utilitani o'chirish
- Tizim eng so'nggi versiyasigacha yangilanganligini ta'minlash tavsiya etiladi
- Avtomatik ravishda faollashtiriladigan NTP ni o'rnatish, shuning uchun hech qanday qo'shimcha buyruqlar kiritish shart emas.
