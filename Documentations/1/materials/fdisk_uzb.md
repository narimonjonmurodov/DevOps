## fdisk utilitasidan foydalanish
Qattiq disklar katta hajmga ega bo'lganligi sababli, ularning maydoni odatda bir nechta qismlarga – disk bo'limlariga bo'linadi va ular bilan tizimdagi mustaqil disklar kabi ishlash mumkin. \
fdisk - qattiq disk bo'limlarini boshqarish va ular haqida ma'lumot olish buyrug'i.

fdisk buyrug'i bilan ishlashning ba'zi misollari quyida keltirilgan:
- Siz uchun mavjud bo'lgan disklar va bo'limlar ro'yxatini ko'rish uchun -l opsiyasidan foydalaning: \
  <img src="../misc/images/fdisk1.png" alt="fdisk1" width="500"/>
- Disk belgilari bo’yicha ko'pgina fdisk operatsiyalari interaktiv rejimda amalga oshiriladi. Interaktiv rejimda fdiskni ishga tushirish uchun belgilanishi kerak bo'lgan blokli qurilmani utilitaga o'tkazing. \
    Ushbu misolda u /dev/nvme0n1: \
  <img src="../misc/images/fdisk2.png" alt="fdisk2" width="500"/>
- Joriy bo'limlar jadvali turini, shuningdek diskdagi mavjud bo'limlarni ko'rish uchun p buyrug'idan foydalaning:\
  <img src="../misc/images/fdisk3.png" alt="fdisk3" width="500"/>
- m -- xotira ma'lumotlarini ko'rsatish rejimini o'chirish yoki o’zgartirish buyrug'i
- w -- diskka yangi bo'limlar jadvalini yozish buyrug'i (mazmunan -- o'zgarishlarni saqlash)
- q -- saqlamasdan chiqish buyrug’i

