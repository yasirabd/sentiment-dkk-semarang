# Panduan Menambahkan Projectku

## Mempersiapkan environment project
1. Instalasi library `virtualenv` menggunakan `pip`.
    ```
    python -m pip install virtualenv
    ```
2. Buat environment pada folder tujuan Anda dan beri nama folder `env`
    ```
    python -m virtualenv <nama folder> --python=python3.8
    ```

    Misalkan disini membuat folder `env`.
    ```
    E:\DSI\research>python -m virtualenv env --python=python3.8
    ```
    Secara otomatis akan terbentuk folder `env`.

3. Aktifkan environment dengan perintah berikut (windows).
    ```
    E:\DSI\research>env\scripts\activate
    (env) E:\DSI\research>
    ```
4. Environment sudah siap digunakan.

##  Mengunduh repository dan persiapan project
1. Lakukan `Fork` pada repository dengan menekan button yang terdapat pada halaman repository. Setelah dilakukan, hasilnya akan membuat kopian repository di dalam koleksi repository Anda.
2. Lakukan `clone` dari repository Anda ke local disk, dan tambahkan base repository sebagai `remote`.
    ```
    git clone https://github.com/<username GitHub>/sentiment-dkk-semarang
    cd sentiment-dkk-semarang
    git remote add upstream https://github.com/yasirabd/sentiment-dkk-semarang
    ```
3. <b>Jangan lupa aktifkan environment</b>, terus lakukan instalasi requirements.
    ```
    pip install -r requirements.txt
    ```
4. Persiapan environment dan repository sudah siap.

## Menambahkan project Anda
1. Buat `branch` terlebih dahulu dengan nama project yang akan dimasukkan. 
    ```
    git fetch upstream
    git rebase upstream/master
    git checkout -b add-svm-model-tuned
    ```
> <b>Jangan lakukan develop</b> di `master` branch.
2. Masukkan projectmu ke dalam folder terkait. Misalkan disini Saya memasukkan model SVM dengan nama `tfidf_svc_tuned.joblib` ke dalam folder `models`. Anda juga bisa melakukan coding disini.
3. Jika sudah selesai saat development, mari kita lakukan langkah berikutnya.

## Melakukan Pull Request
1. Tambahkan/`add` seluruh project yang sudah dikerjakan dan lakukan `commit`.
    ```
    git add .
    git commit
    ```
    Yang perlu diperhatikan, sebaiknya melakukan sync dengan repository original secara berkala supaya tidak terjadi bentrokan code.
    * Jika belum melakukan `push` pada `branch`, kamu bisa melakukan `rebase` pada `upstream/master`.
        ```
        git fetch upstream
        git rebase upstream/master
        ```
    * Jika kamu sudah melakukan `push` pada `branch`, <b>jangan</b> `rebase` tetapi lakukan `merge`.
2. Lakukan `push` perubahan yang dilakukan.
    ```
    git push -u origin <nama branch>
    ```
    Misalkan
    ```
    git push -u origin add-svm-model-tuned
    ```
3. Setelah dirasa cukup, pergi ke halaman repository GitHub Anda. Terus tekan `Pull Request` untuk mengirim projectmu ke main repository.

<b>Selamat kamu sudah selesai menambahkan projectmu! 🤗</b>
