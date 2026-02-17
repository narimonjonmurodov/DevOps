## **SNAT** va **DNAT**

**NAT** – "Network Address Translation" ning qisqartmasi, ya'ni, "tarmoq manzillarini o’zgartirish".
**NAT** IP-paket sarlavhasidagi IP-manzillardan biri o'zgarganda yuzaga keladi: yoki manba IP-manzili, yoki qabul qiluvchining IP-manzili.

<img src="../misc/images/nat.png" alt="network_route" width="500"/>

| **Parametr**            | **SNAT** | **DNAT** |
|-------------------------|----------|----------|
| **Qisqartmalar**        | Source **NAT** | Destination **NAT** |
| **Terminologiya**       | **SNAT** manba uzelining shaxsiy IP manzilini umumiy IP manzilga o'zgartiradi. TCP/UDP sarlavhalaridagi manba portini ham o'zgartirishi mumkin. Odatda, **SNAT** ichki foydalanuvchilar tomonidan Internetga kirish uchun ishlatiladi. | **DNAT** IP-paket sarlavhasidagi maqsad manzilini o'zgartiradi. Shuningdek, u TCP/UDP sarlavhalaridagi maqsad portni o'zgartirishi mumkin. **DNAT** umumiy manzil/maqsad portiga ega bo’lgan kiruvchi paketlarni tarmog'imiz ichidagi shaxsiy IP-manzil/portga yo'naltirishimiz kerak bo'lganda foydalaniladi. |
| **Foydalanish ssenariysi** | Mahalliy tarmoq ichidagi va fayervoll bilan himoyalangan mijoz Internet tarmog’iga kirishni xohlaydi. | Ma'lumotlar markazi ichida joylashtirilgan va fayervoll ortida joylashgan veb-sayt Internet foydalanuvchilari uchun ochiq bo'lishi kerak. |
| **Manzil o'zgarishi**    | **SNAT** **NAT** qurilmasi orqali yuboriluvchi paketlarning manba manzilini o'zgartiradi. | **DNAT** marshrutizator orqali yuboriluvchi paketlarning maqsad manzilini o'zgartiradi. |
| **Amalga oshirish tartibi** | **SNAT** marshrutlash qarori qabul qilingandan keyin amalga oshiriladi. | **DNAT** marshrutlash qarorlari qabul qilinishidan oldin amalga oshiriladi. |
| **Muloqot tartibi**      | **SNAT** ichki himoyalangan tarmoq tashqi dunyo bilan aloqa qila boshlaganda paydo bo'ladi. | **DNAT** tashqi, himoyalanmagan tarmoq ichki, himoyalangan tarmoq bilan o’zaro aloqani boshlaganida yuzaga keladi. |
| **Bir/bir nechta xostlar** | **SNAT** "ichki" tarmoqdagi bir nechta xostlarga "tashqi" tarmoqdagi istalgan xostgacha yetib borishga imkon beradi. | **DNAT** "tashqi" tarmoqdagi har qanday xostga "ichki" tarmoqdagi bitta xostgacha yetib borish imkonini beradi. |
