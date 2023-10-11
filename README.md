![Logo](https://i.imgur.com/U1KBGMc.jpg)

# BookBuffet

## 👥 Anggota Kelompok C-12 👥
* [Ricardo Palungguk Natama](https://github.com/odracheer) (2206082700)
* [Faris Zhafir Faza](https://github.com/Marsupilamieu) (2206081931)
* [Fiona Ratu Maheswari]( https://github.com/fionafrm) (2206024575)
* [Muhammad Faishal Adly Nelwan](https://github.com/pesolosep) (2206030754)
* [Muhammad Andhika Prasetya](https://github.com/radityahnf) (2206031302)

## 📚 Latar Belakang BookBuffet 📚
Mengingat perkembangan teknologi yang sangat pesat saat ini sehingga terjadi perubahan pola perilaku masyarakat. Kini, masyarakat cenderung menggunakan perangkat seluler dalam mengakses informasi. Hal ini dikarenakan mudahnya proses mengakses informasi apapun dari internet melalui perangkat seluler yang mereka miliki. Namun, masih terdapat tantangan yang dialami oleh masyarakat, seperti kesulitan dalam memilih buku sesuai dengan minat pribadi. BookBuffet hadir sebagai solusi untuk tantangan ini.</br>

Dilengkapi dengan fitur Recommendation, BookBuffet hadir untuk memberikan informasi terkait buku-buku yang cocok dengan minat Anda. Fitur ini juga didasarkan oleh ulasan-ulasan pengguna lainnya. Tidak hanya itu, BookBuffet juga hadir dengan fitur My Books, di mana Anda dapat menyimpan judul buku-buku yang telah Anda baca dan Anda juga dapat memberikan ulasan terhadap buku tersebut. BookBuffet juga menyediakan sebuah forum diskusi di mana Anda dapat berdiskusi tentang buku sepuasnya. Selain itu, Anda juga dapat menambahkan buku Anda ke katalog yang kami miliki. Anda juga tidak perlu khawatir jika mendapati suatu kendala ketika menggunakan BookBuffet ini. Terdapat fitur Report Book yang siap membantu Anda dalam menyelesaikan masalah. Kami harap dengan adanya situs web BookBuffet ini dapat membantu Anda dalam memilih buku yang akan Anda baca.

## 📂 Daftar Modul 📂
Berikut ini beberapa modul yang digunakan pada web BookBuffet:

### ✨ Book Catalogue ✨
Pada tampilan _Catalogue page_, pengguna dapat melihat buku-buku yang ada pada aplikasi BookBuffet. Pengguna akan mendapat rekomendasi serta mencari buku-buku yang ada melalui _filtering_ baik berdasarkan genre, _rating_ tertinggi dan terendah, dan _most recent upload_. Ketika suatu buku dipilih, tampilannya akan berisi _cover_, judul, tanggal publikasi, deskripsi, _rating_, dan ulasan-ulasan terhadap buku tersebut.

### 🗞️ Publish a New Book 🗞️
Pada tampilan _Publish A New Book page_, pengguna _role_ `User` juga dapat meng-_upload_ suatu buku yang belum ada di katalog aplikasi BookBuffet. Akan tetapi, fitur ini akan melewati proses _screening_ dahulu oleh `Admin`. Jika proses _screening_ sudah selesai, maka buku akan di-_upload_ oleh `Admin` di web dan dapat diakses oleh semua Pengguna.

### 💬 Community Forum 💬
Pada tampilan _Community page_, Pengguna role `User` dapat melakukan diskusi dengan Pengguna lainnya tentang buku. Pengguna akan mendiskusikan buku-buku berdasarkan genre buku yang dipilih. Selain itu, Pengguna juga dapat melakukan _request_ kepada `Admin` untuk membuat diskusi baru tentang sebuah buku.

### 🔮 My Book 🔮
Pada tampilan My Books aplikasi BookBuffet, Pengguna bisa menyimpan _list_ buku yang sedang dibaca. Pengguna dapat menambahkan buku ke dalam _list_ berdasarkan daftar buku yang ada di aplikasi BookBuffet. Pengguna juga bisa melaporkan _progress tracking_ terhadap pembacaan buku yang sudah ditambah. Jika Pengguna sudah selesai membaca buku tersebut, maka Pengguna dapat mengklik selesai terhadap buku tersebut. Pengguna juga bisa memberikan ulasan dan _rating_ terhadap buku tersebut.

### ❗ Report Book ❗
Pengguna _role_ `User` memiliki opsi untuk me-_report_ buku agar dapat di-_remove_ dari katalog buku. Pengguna akan memilih buku yang ingin di-_report_. Lalu, Pengguna wajib memberi alasan mengapa buku tersebut harus di-_remove_. Report tersebut lalu akan di-_review_ oleh `Admin` dimana ia akan mengambil keputusan apakah buku tersebut akan di-_remove_ atau tidak. User akan menerima notifikasi mengenai _report_-nya diterima `Admin` atau tidak.

## 🗺️ Sumber Dataset Katalog Buku 🗺️

## 🎭 Role Pengguna 🎭
| Peran   | Hak Akses                                                                                       |
|---------|-------------------------------------------------------------------------------------------------|
| User    |   User dapat mengakses semua fitur berikut, tetapi harus meminta izin `Admin`:                  |
|         |   - Melaporkan suatu buku agar dihapus dari katalog.                                            |
|         |   - Menambah forum diskusi pada laman community.                                                |
|         |   - Menambahkan suatu buku ke katalog aplikasi.                                                 |
| Admin   |   - Dapat mengakses segala fitur layaknya seperti `User`.                                       |    
|         |   - Menghapus suatu buku dari katalog berdasarkan laporan yang diberi `User`.                   |
|         |   - Menambahkan suatu diskusi pada forum sesuai dengan permintaan `User` jika layak atau tidak. |
|         |   - Menambahkan suatu buku ke katalog aplikasi.                                                 |
