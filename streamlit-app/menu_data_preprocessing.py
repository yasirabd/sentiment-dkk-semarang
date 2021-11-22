import streamlit as st


def display_data_preprocessing():
    text = """
    # Data Preprocessing
    Data teks yang bersumber dari sosial media sering masih kotor. Kotor yang dimaksud disini adalah banyak kata-kata yang 
    tidak sesuai dengan kaidah bahasa Indonesia yang benar. Selain itu, seringkali juga terdapat kata-kata bahasa gaul (slang), 
    singkatan kata, duplikasi huruf pada kata, salah penulisan tidak disengaja (typo), tanda baca berlebih, dan pemakaian emoji.
    

    Oleh karena itu, sebelum data teks menjadi *feature input* model machine learning, harus dilakukan preprocessing terlebih dahulu. 
    Proses text processing yang dilakukan adalah:

    ### Step 1: Cleansing text
    Tahap ini membersihkan teks secara umum, meliputi:
    - *Case folding*, mengubah menjadi huruf kecil
    - *Remove punctuation*, menghapus tanda baca
    - *Replace newline*, mengganti *newline* dengan spasi
    - *Remove digit*, menghapus angka
    - *Remove extra space*, menghapus spasi berlebih

    Berikut ini adalah proses yang terjadi.

    Sebelum dilakukan `cleansing text`:
    ```
    Makasih infonya.....ayo jgn lengah......tetap smangat... pandemi belom usai...

    ...tetap ikuti protokol kesehatan dengan baik....🙏🙏🙏
    ```

    Setelah dilakukan `cleansing text`:
    ```
    makasih infonya ayo jgn lengah tetap smangat pandemi belom usai tetap ikuti protokol kesehatan 
    dengan baik 🙏🙏🙏
    ```

    ### Step 2: Convert emojis
    Tahap ini melakukan konversi emoticon menjadi teks. Kamus tersebut dapat diakses pada [Kaggle Emoji to Text Indonesia](https://www.kaggle.com/yasirabd/emoji-to-text-indonesia).

    Berikut ini adalah proses yang terjadi.

    Sebelum dilakukan `convert emojis`:
    ```
    makasih infonya ayo jgn lengah tetap smangat pandemi belom usai tetap ikuti protokol kesehatan 
    dengan baik 🙏🙏🙏
    ```

    Setelah dilakukan `convert emojis`:
    ```
    makasih infonya ayo jgn lengah tetap smangat pandemi belom usai tetap ikuti protokol kesehatan 
    dengan baik tangan_berdoa tangan_berdoa tangan_berdoa
    ```

    ### Step 3: Normalize text
    Tahap ini mengubah kata tidak baku / kata alay menjadi kata baku. Referensi kamus alay yang digunakan:
    - [Kamus bahasa alay oleh Rama Prakoso](https://raw.githubusercontent.com/ramaprakoso/analisis-sentimen/master/kamus/kbba.txt)
    - [Kamus alay oleh Nikmatun Aliyah Salsabila](https://raw.githubusercontent.com/nasalsabila/kamus-alay/master/colloquial-indonesian-lexicon.csv)

    Berikut ini adalah proses yang terjadi.

    Sebelum dilakukan `normalize text`:
    ```
    makasih infonya ayo jgn lengah tetap smangat pandemi belom usai tetap ikuti protokol kesehatan 
    dengan baik tangan_berdoa tangan_berdoa tangan_berdoa
    ```

    Setelah dilakukan `normalize text`:
    ```
    terima kasih infonya ayo jangan lengah tetap semangat pandemi belum usai tetap ikuti protokol 
    kesehatan dengan baik tangan_berdoa tangan_berdoa tangan_berdoa
    ```

    ### Step 4: Remove stopwords
    Tahap ini menghapus kata-kata yang termasuk *stop words*. *Stop words* adalah kata-kata yang tidak
    memiliki makna atau arti jika dia berdiri sendiri. Misalnya: apa, kenapa, saya, yang.

    Daftar *stop words* yang digunakan gabungan dari beberapa referensi, yaitu:
    - [Stop words oleh Rama Prakoso](https://raw.githubusercontent.com/ramaprakoso/analisis-sentimen/master/kamus/stopword.txt)
    - [Stop words oleh Yasir Utomo](https://raw.githubusercontent.com/yasirutomo/python-sentianalysis-id/master/data/feature_list/stopwordsID.txt)
    - [Stop words oleh FPMIPA](https://raw.githubusercontent.com/onlyphantom/elangdev/master/elang/word2vec/utils/stopwords-list/fpmipa-stopwords.txt)
    - [Stop words oleh Sastrawi](https://raw.githubusercontent.com/onlyphantom/elangdev/master/elang/word2vec/utils/stopwords-list/sastrawi-stopwords.txt)
    - [Stop words oleh Ali Akbar S](https://raw.githubusercontent.com/onlyphantom/elangdev/master/elang/word2vec/utils/stopwords-list/aliakbars-bilp.txt)
    - [Stop words oleh Pebahasa](https://raw.githubusercontent.com/onlyphantom/elangdev/master/elang/word2vec/utils/stopwords-list/pebbie-pebahasa.txt)
    - [Stop words oleh Elangdev](https://raw.githubusercontent.com/onlyphantom/elangdev/master/elang/word2vec/utils/stopwords-id.txt)
    - Stop words oleh NLTK
    - Tambahan *stop words*: `admin`, `mimin`, `min`, `minkes`, `kalo`, `nya`, `username` 
    
    Berikut ini adalah proses yang terjadi.

    Sebelum dilakukan `remove stopwords`:
    ```
    terima kasih infonya ayo jangan lengah tetap semangat pandemi belum usai tetap ikuti protokol 
    kesehatan dengan baik tangan_berdoa tangan_berdoa tangan_berdoa
    ```

    Setelah dilakukan `remove stopwords`:
    ```
    terima kasih infonya ayo lengah semangat pandemi ikuti protokol kesehatan tangan_berdoa 
    tangan_berdoa tangan_berdoa
    ```

    ### Step 5: Tokenization
    Tahap ini merubah kalimat menjadi token-token kata. Proses pemisahan menjadi token kata berdasarkan spasi.

    Sebelum dilakukan `tokenization`:
    ```
    terima kasih infonya ayo lengah semangat pandemi ikuti protokol kesehatan tangan_berdoa 
    tangan_berdoa tangan_berdoa
    ```

    Setelah dilakukan `tokenization`:
    ```python
    [terima, kasih, infonya, ayo, lengah, semangat, pandemi, ikuti, protokol, kesehatan, 
    tangan_berdoa, tangan_berdoa, tangan_berdoa]
    ```
    """
    st.markdown(text, unsafe_allow_html=True)