import streamlit as st
from PIL import Image
import pandas as pd


def display_feature_extraction():
    text = """
    # Feature Extraction
    Tahap ini melakukan ekstraksi fitur dari data teks. Fitur tersebut yang akan menjadi input model machine learning.
    Model machine learning sendiri hanya bisa menerima input fitur dengan tipe data numeric (angka). Maka, data kita
    yang berupa teks harus direpresentasikan menjadi angka.

    Terdapat dua metode yang digunakan, yaitu

    ### TF-IDF
    Term Frequency - Inverse Document Frequency (TF-IDF) adalah metode pengukuran statistik yang menhitung seberapa
    relevan suatu kata pada suatu dokumen dalam kumpulan dokumen. Terdapat dua metriks penting:
    - Term frequency (`tf`): menunjukkan banyak kemunculan suatu kata dalam suatu dokumen.
    - Inverse document frequency (`idf`): menunjukkan *inverse document frequency* dari kata pada kumpulan dokumen.

    ##### Term Frequency
    `tf` menghitung kemunculan suatu kata dalam suatu dokumen. Formula untuk menghitung `tf` dapat dituliskan:
    """
    st.markdown(text, unsafe_allow_html=True)
    latext = r"""
    $$ 
    tf(t,d) = \frac {count \ of \ t \ in \ d}{number \ of \ words \ in \ d}
    $$
    """
    st.markdown(latext, unsafe_allow_html=True)
    text = """
    dimana
    - `t` adalah kata
    - `d` adalah dokumen

    ##### Inverse Document Frequency
    `idf` adalah *inverse document frequency* dari kata dalam kumpulan dokumen. Artinya, menunjukkan seberapa sering
    atau jarang suatu kata muncul pada seluruh dokumen. Semakin nilai mendekati 0, menunjukkan semakin sering munculnya
    kata tersebut. Begitu juga sebaliknya. 

    Metrik ini dapat dihitung dengan total dokumen dibagi dengan jumlah dokumen yang mengandung suatu kata tersebut. Kemudian
    dihitung logaritma dari hasilnya. Formula `idf` dapat dituliskan:

    """
    st.markdown(text, unsafe_allow_html=True)
    latext = r"""
    $$ 
    idf(t,D) = log \big(\frac{N}{df(t) + 1} \big)
    $$

    dimana
    $$
    df(t) = \lvert {d ∈ D: t ∈ d} \rvert
    $$
    """
    st.markdown(latext, unsafe_allow_html=True)
    text = """
    dengan
    - `N` adalah jumlah total dokumen dalam korpus
    - `D` adalah kumpulan dokumen d
    - `df(t)` adalah banyaknya jumlah dokumen yang mengandung kata *t*
    - `+ 1` untuk menghindari pembagian terhadap 0

    Maka formula `tfidf` dapat dituliskan:
    """
    st.markdown(text, unsafe_allow_html=True)  
    latext = r"""
    $$ 
    tfidf(t,d,D) = tf(t,d) * idf(t,D)
    $$
    """
    st.markdown(latext, unsafe_allow_html=True)
    text="""
    ##### Contoh tf-idf
    Berikut ini adalah langkah-langkah yang dilakukan pada `tf-idf`.
    
    **Pertama, hitung `tf`**

    Untuk mendapatkan `tf`, kita buat *Vocabulary* yaitu kumpulan kata-kata unique. Kemudian
    hitung *frequency* tiap kata pada masing-masing dokumen.
    """
    st.markdown(text, unsafe_allow_html=True)
    img = Image.open('../images/TF-IDF part 1.png')
    st.image(img, caption='Hitung frequency')
    img = Image.open('../images/TF-IDF part 2.png')
    st.image(img, caption='Hitung term frequency')
    
    text = """
    **Kedua, hitung `idf`**

    Contoh untuk `idf(ayo)`, dengan jumlah document `N = 2` dan kata `ayo` hanya
    muncul pada doc 1, maka `df(ayo) = 1`.

    Sehingga `idf(ayo) = log(N/df(ayo) = log(2/1) = 0.3`.
    """
    st.markdown(text, unsafe_allow_html=True)
    st.info("Formula `idf` yang digunakan pada contoh tanpa menggunakan `+ 1`, karena menggunakan data contoh yang berukuran kecil")
    img = Image.open('../images/TF-IDF part 3.png')
    st.image(img, caption='Hitung inverse document frequency')

    text = """
    **Terakhir, hitung `tf-idf`**

    Didapatkan dengan mengalikan `tf` dengan `idf`.
    """
    st.markdown(text, unsafe_allow_html=True)
    img = Image.open('../images/TF-IDF part 4.png')
    st.image(img, caption='Hitung TF-IDF')

    text = """
    ### Word2Vec
    Word2Vec mengubah setiap kata menjadi sebuah *vector*. Pada tahap ini kita menggunakan [*pre-trained word vectors* Indonesia](https://fasttext.cc/docs/en/crawl-vectors.html) 
    dari Fasttext. Dataset yang digunakan untuk membentuk *word vectors* bersumber dari [Common Crawl](https://commoncrawl.org/) dan [Wikipedia](https://www.wikipedia.org/) 
    berbahasa Indonesia. Model tersebut dilatih menggunakan Continous Bag of Words (CBOW) dengan *weight-position*, 
    ukuran dimensi 300, karakter n-gram dengan panjang 5, *window size* 5 dan 10 negatif.

    ##### Word vectors Fast Text Indonesia
    Berikut ini adalah deskripsi *pre-trained word vectors* Indonesia yang digunakan:

    | Property    | Value           |
    |-------------|-----------------|
    | File name   | cc.id.300.bin   |
    | Model size  | 4.2 GB          |
    | Vocab size  | 2.000.000 words |

    Berdasarkan ukuran vocabulary pada model, maka terdapat 2 juta kata vector pada model. Sebagai contoh untuk vector kata `makan`.
    ```python
    word2vec['makan']
    ```
    ```
    array([ 7.65823573e-02, -5.22948839e-02, -7.58241490e-02,  7.79563114e-02,
        4.24031261e-03, -3.52708995e-02, -5.65536432e-02,  7.04095978e-03,
        1.35103157e-02, -7.67766833e-02, -3.09904497e-02, -8.63214862e-03,
       -2.52841637e-02,  3.53445597e-02, -3.19182128e-02,  6.22232519e-02,
        5.86843677e-02,  1.55164115e-02,  1.05511762e-01, -1.88412555e-02,
       -3.83044779e-02,  1.27268853e-02,  1.51229920e-02,  7.48559758e-02,
        2.16742977e-02,  7.62321204e-02, -4.09204029e-02, -1.07316859e-02,
        1.14914417e-01,  7.60577060e-03,  1.06626213e-01, -1.34900212e-04,
        3.02968435e-02,  1.32901426e-02,  1.08709838e-02,  4.38845344e-02,
       -3.91090661e-02,  1.73634011e-03,  1.87462941e-02, -5.98455220e-03,
       -5.01004979e-02, -6.89068437e-02, -2.74596065e-02,  7.06195012e-02,
        2.78385803e-02, -2.58003250e-02, -5.25348783e-02,  1.44458888e-03,
        1.08640194e-02, -8.10575932e-02, -5.24356700e-02,  3.64395753e-02,
        2.87113432e-02, -1.52273923e-01, -4.57562357e-02, -6.49298821e-03,
        3.21065746e-02,  3.73334736e-02, -2.79761665e-02,  2.25719810e-02,
        5.19546904e-02,  5.48765212e-02, -2.02274621e-02,  7.49710575e-03,
       -2.92404369e-02,  3.65215838e-02,  2.71895938e-02, -5.96923567e-03,
        7.12356269e-02,  2.12637894e-03, -4.29165550e-03,  2.74326000e-02,
        1.10751092e-01,  3.49476002e-02,  3.99067812e-02, -3.97722423e-02,
       -8.04219544e-02, -3.68497483e-02, -2.94326432e-02,  7.24084824e-02,
       -8.96963701e-02, -3.56668234e-02, -3.81345749e-02, -2.64855772e-02,
        3.42096314e-02,  3.47739607e-02, -8.56922418e-02, -8.63250121e-02,
        1.29129570e-02,  4.69886288e-02, -4.00665291e-02,  1.25692844e-01,
       -2.39724703e-02, -4.68557663e-02, -7.15523064e-02, -1.12096816e-01,
       -1.12486985e-02,  1.85788749e-03, -1.50960088e-02,  6.74999040e-03,
       -4.24261903e-03, -1.58168562e-03,  4.03643288e-02,  1.98662616e-02,
        1.19036838e-01,  4.22454216e-02,  7.10317791e-02, -5.07033430e-04,
       -1.86485536e-02, -3.72926034e-02, -1.71194766e-02, -1.14467390e-01,
       -4.94581833e-03,  3.40595879e-02, -1.13615133e-02, -6.83007538e-02,
       -1.08073931e-02,  1.88419148e-02, -2.86318343e-02,  6.01747334e-02,
       -1.16462205e-02,  2.41732970e-02,  9.55546461e-03, -4.11423109e-02,
        5.47121046e-04, -5.76864667e-02,  1.33765573e-02, -5.61839603e-02,
       -8.67253914e-02,  1.49397869e-02,  3.06868404e-02,  3.60826366e-02,
        8.17225426e-02, -8.77092127e-03,  8.06602910e-02, -2.58788280e-02,
       -9.42394324e-03,  1.17068160e-02,  3.17073241e-02,  2.13548727e-02,
        1.14122391e-01, -1.57536894e-01,  2.72010546e-02,  2.55819894e-02,
        2.01501977e-02, -4.66570631e-02,  2.07931884e-02,  3.61044109e-02,
        4.28777859e-02, -4.75179479e-02,  6.40087575e-02, -4.64810506e-02,
       -7.79459625e-02, -1.05593791e-02,  1.13269992e-01, -3.91777791e-02,
        1.85047835e-02, -3.34535725e-03, -5.59984744e-02,  4.78161052e-02,
        6.61986917e-02, -7.51348585e-03,  4.46088724e-02, -2.18404457e-02,
        7.58041441e-03,  9.12467204e-03,  8.17106068e-02,  2.57199891e-02,
        6.26780689e-02,  5.60221896e-02,  4.71344404e-02,  4.77840379e-02,
        1.87761560e-02, -5.24602085e-02,  1.78369023e-02,  4.62170243e-02,
        7.93902427e-02, -6.64993525e-02, -3.18350680e-02,  8.61232355e-02,
        9.25639942e-02,  4.19104956e-02,  1.40621811e-02,  1.57663934e-02,
        5.73305367e-03,  7.08800554e-02,  8.10448229e-02, -2.90589835e-02,
       -6.42868411e-03, -7.76229752e-03,  1.20480340e-02,  2.93171592e-02,
        2.98335440e-02,  2.20943857e-02, -4.79331315e-02,  2.75380798e-02,
        6.56596571e-02,  2.76083648e-02, -9.59931687e-03,  1.37705579e-02,
        2.58285683e-02,  4.68399376e-02, -5.52027440e-03, -7.17512816e-02,
        1.39557812e-02,  1.13948230e-02,  3.09192343e-03,  1.75549779e-02,
       -3.73916328e-02,  1.55867022e-02, -5.05810007e-02, -1.21239526e-02,
       -2.36558802e-02,  3.27059589e-02,  3.04684453e-02,  1.20062679e-02,
        7.36553296e-02, -1.59782860e-02, -1.84271932e-02,  5.77097461e-02,
        1.29483566e-02, -3.49723548e-03, -1.40901087e-02,  4.93866950e-03,
        1.69356912e-03, -3.17962393e-02, -5.40170446e-02,  1.31113548e-02,
        5.40774129e-02, -2.67037023e-02,  7.19963610e-02,  3.24626528e-02,
        5.53710274e-02,  4.23886999e-02, -7.07782507e-02, -2.91333161e-02,
       -4.35674004e-02, -3.41600552e-03, -8.35765451e-02,  5.95176630e-02,
        2.49241237e-02, -5.62551152e-03,  5.25752222e-03, -1.29735887e-01,
       -7.51086250e-02, -1.78651195e-02,  4.14344575e-03,  6.01351038e-02,
       -3.18846144e-02,  2.40726452e-02, -1.64101645e-02, -5.59301823e-02,
        3.82546382e-03,  1.09482184e-03, -2.14715451e-02,  5.95197938e-02,
        2.23850608e-02,  4.52589989e-03,  4.68008444e-02,  1.17081050e-02,
       -4.75475714e-02,  1.80556308e-02, -4.14063297e-02, -1.98237710e-02,
       -4.77769412e-02, -4.87884544e-02,  5.97444503e-03,  6.24524876e-02,
        7.63270073e-03,  1.51174637e-02,  5.85723016e-03, -3.70063782e-02,
       -7.11303130e-02, -1.15408547e-01, -9.79476571e-02,  8.20836052e-02,
       -1.13318458e-01,  3.19620296e-02, -1.23315513e-01,  1.58719551e-02,
       -5.08308038e-02,  1.34078627e-02,  9.41347405e-02, -1.52928054e-01,
       -1.60345417e-02, -1.01086805e-02,  1.21061755e-02,  2.42803693e-02,
       -5.11977300e-02, -2.96257902e-03, -1.13348281e-02,  1.49072437e-02,
       -1.55614018e-02, -2.31607258e-02,  2.93966755e-02,  1.83843244e-02,
       -7.78319836e-02, -6.59285635e-02, -4.89819981e-02,  9.20532942e-02],
      dtype=float32)
    ```

    ##### Contoh ekstraksi fitur word2vec
    Berikut ini adalah langkah-langkah yang dilakukan.

    **Pertama, ubah tiap `word` menjadi `vector`**

    Jika diperhatikan kata `covid` pada dokumen 1 dan dokumen 2 memiliki vector yang sama.
    """
    st.markdown(text, unsafe_allow_html=True)
    img = Image.open('../images/Word2Vec part 1.png')
    st.image(img, caption='Ubah word jadi vector')

    text = """
    **Kedua, susun `vector` dan tambah *zero padding***

    Jika kita perhatikan jumlah kata pada tiap dokumen berbeda. Dokumen 1 memiliki jumlah kata 4, sedangkan 
    dokumen 2 memiliki jumlah kata 3. Kita harus membuat ukuran fitur sama semua untuk jumlah kata. Maka kita 
    definisikan `MAX_LEN = 50` untuk menyamakan jumlah *vector* kata pada tiap dokumen.
    """
    st.markdown(text, unsafe_allow_html=True)
    st.info("Untuk demonstrasi menggunakan `MAX_LEN = 4`")
    img = Image.open('../images/Word2Vec part 2.png')
    st.image(img, caption='Tambah zero padding')

    st.error("Untuk model dari `scikit-learn` seperti `SVM` dan `Naive Bayes` hanya bisa menerima fitur input 2-dimensi")
    text = """
    Dikarenakan model dari `scikit-learn` hanya bisa menerima fitur input 2-dimensi, maka kita hitung `average` dari vector tiap dokumen.
    """
    st.markdown(text, unsafe_allow_html=True)
    st.info("Tidak dilakukan penambahan `zero padding`.")
    img = Image.open('../images/Word2Vec part 3.png')
    st.image(img, caption='Feature extraction 2-dimensi')