## VirtualBox yordamida tarmoqni qanday emulyatsiyalash kerak

#### Asosiy virtual mashinalarni yaratish

Tarmoq topologiyasini bajarish uchun avvalo yangi virtual mashina yaratish lozim, masalan Ubuntu Server 20.04 LTS.

Virtual mashinani klonlash – xost kompyuterda qo'shimcha mehmon virtual mashinalarini yaratishning eng oson usuli hisoblanadi.

Tarmoq emulyatsiyasi uchun PK va marshrutizatorlarni bajarish maqsadida avvalgi bosqichda yaratilgan Ubuntu server virtual mashinasini klonlang. Ubuntu serveriga sichqonchaning o'ng tugmasini bosing va menyudan Clone bandini tanlang.

Muloqot oynasida yangi VM nomini kiriting va barcha tarmoq kartalarining MAC manzillarini qayta ishga tushirishni unutmang. Har bir klonlangan VMda MAC manzillari boshqacha ekanligiga ishonch hosil qilishingiz kerak.

Keyingi dialog oynasida klonlangan VM fayl hajmini kichik saqlash uchun Linked Clone -ni tanlang.

Clone tugmasini bosing va yangi VM VirtualBox Manager oynasida paydo bo'ladi.

Har bir talab qilinadigan VM uchun ushbu amallarni takrorlang. Sizga kerak bo'lgan uzel nomlariga mos keladigan virtual mashina nomlarini tanlang.

Har bir VM tarmoq topologiyasini yaratish uchun tarmoq interfeyslarini sozlashi va ularni VirtualBox ichki tarmoqlariga ulashi kerak.

#### VirtualBox ichki tarmoqlarini yaratish

VirtualBox grafik interfeysi har bir VM uchun faqat to'rtta tarmoq adapterini qo'llab-quvvatlaydi. Shu sababli, mumkin bo'lgan tarmoq ssenariylarining murakkabligi cheklanadi.

Har bir tarmoq adapterini yoqish yoki o'chirish mumkin. Agar adapter yoqilgan bo'lsa, u VirtualBox tomonidan taqdim etiluvchi juda ko'p turli xil interfeys turlaridan biriga ulanish uchun sozlanishi mumkin.

Ikki virtual mashinani bir-biriga ulash uchun Internal Network interfeysi turidan foydalaning.

VirtualBox Manager oynasida virtual mashinalardan birini tanlang va Settings (Sozlamalar) ni bosing. Keyin sozlamalar oynasida Network (tarmoq) ni bosing.

Agar u allaqachon o’rnatilmagan bo'lsa, Enable Network Adapter ga bayroqcha qo'ying. Keyin Attached То ni bosing va Internal Network ni tanlang.

Shundan so’ng, ichki tarmoqqa nom bering. Nom ushbu VMga ulanadigan boshqa VMdagi tegishli tarmoq adapterida sozlangan tarmoq nomiga mos kelishi kerak.

Har bir uzel uchun takrorlang.

Marshrutizatorlar ichki tarmoqlarga ulanish uchun mavjud to'rtta tarmoq adapterlaridan uchtasidan foydalanadilar. PK bitta tarmoq adapteridan foydalanadilar.

## Ubuntu Linuxda statik marshrutlarni qanday qo'shish mumkin

Linuxda statik marshrutlarni qo'shish quyidagi buyruq yordamida amalga oshirilishi mumkin:
`ip r add [address we want to connect to] dev [network name]`
 
Biroq, ushbu buyruq bilan yaratilgan ulanish tarmoq yoki tizim qayta ishga tushirilgandan so'ng yo'qoladi.

Ubuntu Linuxda statik marshrutlarni doimiy qilish uchun routes xususiyatidan foydalanib tarmoq interfeysi fayliga marshrut yozuvlarini qo'shish lozim.

Yodda tutingki, YAML fayliga yangi marshrut yozuvini qo'shganingizda `netplan apply` buyrug'i yordamida **netplan** konfiguratsiyasini qayta yuklashingiz kerak.
