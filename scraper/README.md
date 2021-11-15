# Scraper
Tools untuk melakukan scraping komentar instagram DKK Semarang

# How to use
1. Pastikan library ini sudah terinstall
    ```
    selenium
    instascrape
    webdriver-manager
    ```
2. Jalankan script `get_post_dkk.py` untuk mendapatkan list URL instagram post dari account DKK Semarang. 
    > Sebelumnya pastikan sudah menambahkan `INSTAGRAM_SESSIONID` pada `.env` dengan langkah [berikut](http://valvepress.com/how-to-get-instagram-session-cookie/).
    ```
    python get_post_dkk.py
    ```
    > Anda harus melakukan login secara manual dalam prosesnya

    Hasil dari script ini adalah text file `instagram_posts.txt` yang berisi daftar URL post instagram dari DKK Semarang.
3. Jalankan script `batch_url_posts.py` untuk melakukan batch dari daftar URL post instagram. Tujuannya adalah untuk membagi proses menjadi bagian kecil dan menangani jika Instagram melakukan blokir scraper kita setidaknya kita sudah menyimpan beberapa data komentar Instagram.
    ```
    python batch_url_posts.py
    ```

    Hasil dari script ini adalah folder `batch` yang berisi text files hasil batching.

4. Jalankan script `get_comments.py` untuk mendapatkan semua komentar dari tiap URL post Instagram yang terdapat pada folder batch.
    > Sebelumnya pastikan sudah menambahkan `INSTAGRAM_USERNAME` dan `USERNAME_PASSWORD` pada `.env`.

    Pada kode ini masih manual untuk *scraping* tiap batch text file. Jadi atur nilai variable `n_batch = n`, dengan `n` adalah batch yang ingin diambil komentarnya. Misalkan `n_batch = 0`.
    ```
    python get_comments.py
    ```
    Hasilnya adalah csv file dari komentar tiap batch yang terdapat pada folder `batch_csv`.