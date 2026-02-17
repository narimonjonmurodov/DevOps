## **Marshrutlash. Misol.**

<img src="../misc/images/network_route.png" alt="network_route" width="500"/>

Bir nechta quyi tarmoqlarga ega bo'lgan tuzilmaga misol sifatida rasmni ko'rib chiqamiz.

Quyidagi misoldan ko'rinib turibdiki, birinchi yozuv (satr) **128.17.75.0/24** tarmog'i uchun ko’rsatilgan, ushbu tarmoq uchun barcha paketlar xostning **IP** manzili bo'lgan **128.17.75.20** shlyuziga yuboriladi.

Ikkinchi yozuv – **asl sozlamalar bo’yicha marshrut** bo'lib, ushbu marshrutlash jadvalida ko'rsatilmagan tarmoqlarga yuboriluvchi barcha paketlarga qo'llaniladi. Bu yerda marshrut **xost papaya** (**IP 128.17.75.98**) orqali o'tadi, uni **tashqi dunyoga eshik** deb hisoblash mumkin. Ushbu marshrut **128.17.75.0/24** tarmog'idagi boshqa tarmoqlarga kirishga muhtoj bo'lgan barcha mashinalarda qayd qilinishi kerak.

Uchinchi yozuv **halqali interfeys** uchun yaratilgan. Bu manzil, agar mashina o'ziga **TCP/IP** protokoli orqali ulanishi kerak bo'lganda ishlatiladi.

Marshrutlash jadvalidagi oxirgi yozuv **IP 128.17.75.20** uchun bo'lib, **lo** interfeysiga yo'naltiriladi. Shunday qilib, mashina **128.17.75.20** da o'ziga ulanganda, barcha paketlar **127.0.0.1** interfeysiga yuboriladi.

### **Xost "eggplant" uchun marshrutlash jadvali:**
```
[root@eggplant ~]# netstat -rn
Kernel IP routing table
Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
128.17.75.0      128.17.75.20   255.255.255.0   UN        1500 0          0 eth0
default          128.17.75.98   0.0.0.0         UGN       1500 0          0 eth0
127.0.0.1        127.0.0.1      255.0.0.0       UH        3584 0          0 lo
128.17.75.20     127.0.0.1      255.255.255.0   UH        3584 0          0 lo
```

Agar **eggplant** xosti **zucchini** xostiga paket jo'natmoqchi bo'lsa (**jo'natuvchi – 128.17.75.20** va **qabul qiluvchi – 128.17.75.37**), **IP** protokoli marshrutlash jadvali asosida ikkala xost bir xil tarmoqqa tegishli ekanligini aniqlaydi va paketni to'g'ridan-to'g'ri tarmoqqa jo'natadi, u yerda uni **zucchini** qabul qiladi.

Batafsilroq aytadigan bo’lsak, tarmoq kartasi **ARP** so'rovini keng ommaga eshittirib baqiradi:

> "**IP 128.17.75.37 kim? Bu 128.17.75.20 baqiryapti**."

Ushbu xabarni olgan barcha mashinalar uni e'tiborsiz qoldiradilar, **128.17.75.37** manziliga ega bo'lgan xost esa:

> "**Bu menman, mening MAC manzilim mana shunday...**"

– deb javob beradi. Shundan so’ng ulanish va ma'lumotlar almashinuvi **IP-MAC** manzillarining mosliklari kiritilgan **ARP** jadvallari asosida amalga oshiriladi. **"Baqiruvchi" paketi** barcha xostlarga yuboriladi. 

Buning sababi, qabul qiluvchining **MAC** manzili **FF:FF:FF:FF:FF:FF** keng ommaga eshittiruvchi manzil sifatida ko'rsatilgan. Tarmoqdagi barcha xostlar bunday paketlarni qabul qiladi.

### **Masofadagi xostga paket jo'natish**

Agar **eggplant** xosti **pear** kabi yoki undan ham uzoq xostga paket jo'natmoqchi bo'lsa, bunday holda qabul qiluvchi **128.17.112.21** bo'ladi.

**IP** protokoli marshrutlash jadvalida **128.17.112.0/24** tarmog'i uchun marshrutni topishga harakat qiladi, lekin bu marshrut jadvalda yoʻq, shuning uchun **asl sozlamalar bo’yicha marshrut** tanlanadi, uning shlyuzi **papaya (128.17.75.98)** bo’ladi.

Papaya paketni olgandan so'ng, u o'zining marshrutlash jadvalida maqsad manzilini qidiradi:
```
[root@papaya ~]# netstat -rn
Kernel IP routing table
Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
128.17.75.0      128.17.75.98   255.255.255.0   UN        1500 0          0 eth0
128.17.112.0     128.17.112.3   255.255.255.0   UN        1500 0          0 eth1
default          128.17.112.40  0.0.0.0         UGN       1500 0          0 eth1
127.0.0.1        127.0.0.1      255.0.0.0       UH        3584 0          0 lo
128.17.75.98     127.0.0.1      255.255.255.0   UH        3584 0          0 lo
128.17.112.3     127.0.0.1      255.255.255.0   UH        3584 0          0 lo
```

Misolda **papaya** ikkita tarmoqqa ulanganligini ko'rishingiz mumkin:
- **128.17.75.0/24** – **eth0** qurilmasi orqali
- **128.17.112.0/24** – **eth1** qurilmasi orqali

Asl sozlamalar bo’yicha marshrut **pineapple** xosti orqali o'tadi, bu esa **tashqi tarmoqqa kirish shlyuzi** hisoblanadi.

Shunday qilib, **pear** paketini olgandan so'ng, **papaya** marshrutizatori belgilangan manzil **128.17.112.0/24** ga tegishli ekanligini ko'radi va marshrutlash jadvalidagi ikkinchi yozuvga muvofiq paketni yo'naltiradi.

Paketlar marshrutizatordan marshrutizatorga belgilangan manzilga yetgunga qadar shu tarzda uzatiladi.

## **ICMP protokoli**

**ICMP** – bu **xato haqida xabar berish protokoli**.

Marshrutizatorlar tarmoq uzellarini xatolar yoki g'ayritabiiy vaziyatlar haqida xabardor qilishlari uchun **TCP/IP** stekiga maxsus xabarlarni yuborish mexanizmi joriy etilgan. 
Bu **Internet Control Message Protocol (ICMP)** deb nomlanadi.
