import streamlit as st
import pandas as pd


def display_data_collection():
    text = """
    # Data Collection
    Tahap ini melakukan scraping dan crawling data komentar Instagram dari akun [@dkksemarang](https://www.instagram.com/dkksemarang/).

    ### Tools dan code untuk crawling
    Tools yang digunakan untuk melakukan pengambilan data menggunakan library
    ```
    selenium
    instascrape
    ```
    Code untuk crawling dapat dilihat pada folder [scraper]()

    ### Proses data collection
    Proses crawling dilakukan dengan beberapa tahap:

    1. Crawling daftar URL post instagram dari @dkksemarang menggunakan script `get_post_dkk.py`
    """
    st.markdown(text, unsafe_allow_html=True)
    st.markdown(f'<div style="position: relative; padding-bottom: 56.25%; height: 0;"><iframe src="https://www.loom.com/embed/63a97d262dd74f1bbee945c3d791309e" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"> </iframe></div>', unsafe_allow_html=True)
    st.markdown(f'<br>', unsafe_allow_html=True)

    text = """
    2. Lakukan batch URL post instagram
    ```
    python batch_url_posts.py
    ```

    3. Crawling semua komentar yang terdapat pada masing-masing URL post instagram @dkksemarang menggunakan script `get_comments.py`
    """
    st.markdown(text, unsafe_allow_html=True)
    st.markdown(f'<div style="position: relative; padding-bottom: 56.25%; height: 0;"><iframe src="https://www.loom.com/embed/56cec350df5c421cbd932164cac74a15" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>', unsafe_allow_html=True)
    st.markdown(f'<br>', unsafe_allow_html=True)
    
    st.markdown("### Hasil crawling", unsafe_allow_html=True)
    df_raw = pd.read_csv('../data/data_raw_masked.csv')
    min_date_raw = pd.to_datetime(df_raw['datetime'].min())
    max_date_raw = pd.to_datetime(df_raw['datetime'].max())

    st.markdown(
        f'- Jumlah data: {df_raw.shape[0]} baris', unsafe_allow_html=True)
    st.markdown(
        f'- Data columns: `{", ".join(list(df_raw))}`', unsafe_allow_html=True)
    st.markdown(
        f'- Range date: `{min_date_raw.strftime("%d %b %Y")}` to `{max_date_raw.strftime("%d %b %Y")}`')
    st.markdown(f'- Data preview')
    st.dataframe(df_raw.head())