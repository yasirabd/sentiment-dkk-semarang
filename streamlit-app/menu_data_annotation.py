import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image


def display_data_annotation():
    text = '''
    # Data Annotation
    Tahap ini melakukan anotasi label data menjadi `neutral`, `positive`, dan `negative` dari data yang didapatkan pada proses crawling.
    '''
    st.markdown(text, unsafe_allow_html=True)
    st.info("Note: data yang dilakukan anotasi hanya pada rentang waktu awal kasus Covid-19 di Semarang yaitu tanggal `3 Maret 2020` hingga seterusnya")
    
    text = '''
    Sehingga setelah difilter berdasarkan rentang waktu, didapatkan data sebanyak `9959 data`.

    ### Metode pelabelan
    Pelabelan dilakukan oleh semua anggota team dengan masing-masing anggota melakukan anotasi sebanyak kurang lebih `1991 data`.

    Untuk panduan pelabelan `neutral`, `positive`, dan `negative` mengacu pada metode/aturan berikut:
    - Positive
        * Terdapat _keyword_ yang bermakna positif, seperti: ucapan syukur, doa, kata-kata semangat.
        * Terdapat emoticon yang memiliki konteks positif, seperti: 🥰, 😄, 🙏.
        * Komentar apapun yang memiliki konteks positif.
    - Negative
        * Terdapat _keyword_ yang bermakna negatif, seperti: kecewa, sedih, kekesalan.
        * Terdapat emoticon yang memiliki konteks negatif, seperti: 😢, 😭, 😡.
        * Komentar apapun yang memiliki konteks negatif, seperti: sindiran, ketidakpuasan dengan kebijakan, keluhan.
    - Neutral
        * Tidak bisa masuk kategori positive atau negative.
        * Komentar yang bersifat pertanyaan misalnya ingin mengetahui suatu informasi.

    ### Tools pelabelan
    Pelabelan menggunakan open source annotation tool `doccano`.
    '''
    st.markdown(text, unsafe_allow_html=True)

    st.warning("Doccano yang digunakan versi 1.2.4 karena yang bisa berjalan pada windows")
    doccano = Image.open('../images/doccano.png')
    st.image(doccano, caption='', width=300)
    st.markdown("Proses melakukan anotasi label menggunakan `doccano` seperti video di bawah.")
    st.markdown(f'<div style="position: relative; padding-bottom: 56.25%; height: 0;"><iframe src="https://www.loom.com/embed/55e2689eee9f4855951959e9bcf02696" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>', unsafe_allow_html=True)
    st.markdown(f'<br>', unsafe_allow_html=True)
    
    text = '''
    ### Hasil pelabelan
    Berikut hasil pelabelan yang dilakukan.
    '''
    st.markdown(text, unsafe_allow_html=True)

    df_label_composition = pd.DataFrame([['neutral', 3658], ['positive', 2832], [
                                        'negative', 3469]], columns=['sentiment', 'frequency'])
    col1, col2 = st.columns(2)
    with col1:
        st.table(df_label_composition)

        # create pie chart
        fig_pie = px.pie(
            df_label_composition,
            values='frequency',
            names='sentiment',
            color='sentiment',
            color_discrete_map={'neutral': '#636EFA', 'positive': '#00CC96', 'negative': '#EF553B'})
        st.plotly_chart(fig_pie)