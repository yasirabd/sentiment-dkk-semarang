import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from collections import Counter


def display_eda():
    text = '''
    # Exploratory Data Analysis (EDA)
    Data yang dilakukan eksplorasi adalah tipe data `data development` yang akan digunakan untuk membentuk model sentiment analysis.
    '''
    st.markdown(text, unsafe_allow_html=True)

    df = pd.read_csv("../data/data_complete_masked.csv")
    data = df[df.data_type == 'development']
    temp = data.copy()
    temp['datetime'] = pd.to_datetime(temp['datetime'])

    st.markdown("### Data development")
    st.markdown(f"Shape dari data development: {data.shape[0]} baris, {data.shape[1]} kolom")
    st.markdown(f'Rentang waktu: `{temp["datetime"].min().strftime("%d %b %Y")}` sampai `{temp["datetime"].max().strftime("%d %b %Y")}`')
    st.dataframe(data)

    st.markdown("Keterangan untuk tiap kolom data:")
    text = """
    | Column      | Keterangan                                                                                                                                                                                                                                                                                                                                                                              |
    |-------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | `text`      | Komentar-komentar dari user Instagram                                                                                                                                                                                                                                                                                                                                                   |
    | `label`     | Sentiment label berupa `neutral`, `positive`, dan `negative`                                                                                                                                                                                                                                                                                                                            |
    | `username`  | Username Instagram (sudah dilakukan masking untuk menjaga kerahasiaan user)                                                                                                                                                                                                                                                                                                             |
    | `likes`     | Jumlah like dari komentar                                                                                                                                                                                                                                                                                                                                                               |
    | `datetime`  | Tanggal dari komentar dibuat                                                                                                                                                                                                                                                                                                                                                            |
    | `data_type` | Tipe data dibedakan menjadi: <br>- data `development` adalah data komentar yang digunakan untuk membuat model dengan rentang waktu `3 Mar 2021` - `7 Jul 2021` dengan `label` dari hasil anotasi. <br>- data `inference` adalah data komentar yang diambil dari `8 Jul 2021` - `14 Nov 2021` dengan `label` didapatkan dari prediksi model terbaik yang dilatih menggunakan data `development`. |
    """
    st.markdown(text, unsafe_allow_html=True)
    st.markdown(f"<br>", unsafe_allow_html=True)
    st.info("Data yang digunakan EDA dibawah semuanya sudah dilakukan preprocessing. Untuk detail proses preprocessing dapat dilihat pada menu Data Preprocessing.")

    st.markdown("### Distribusi tiap sentiment")
    st.markdown("Kita lihat distribusi sentiment dari data development menggunakan histogram.")
    temp = data['label'].value_counts().reset_index()
    temp = temp.rename(columns={'index': 'label', 'label': 'count'})
    fig_bar = px.bar(temp,
                     x='label',
                     y='count',
                     color='label',
                     title='Histogram sentiment',
                     category_orders=dict(label=['neutral', 'positive', 'negative']),
                     color_discrete_map={'neutral': '#636EFA', 'positive': '#00CC96', 'negative': '#EF553B'})
    st.plotly_chart(fig_bar)

    # funnel chart
    st.markdown("Untuk visualisasi lebih baik, kita buat Funnel-Chart untuk mengetahui persentase dari tiap sentimen.")
    fig_funnel = px.funnel_area(names=temp['label'],
                                values=temp['count'],
                                title='Funnel-Chart of Sentiment Distribution',
                                color_discrete_map={'neutral': '#636EFA', 'positive': '#00CC96', 'negative': '#EF553B'})
    st.plotly_chart(fig_funnel)
    text = """
    Perbandingan persentase data untuk sentiment `neutral` : `positive` : `negative` = 36.7% : 28.4% : 34.8%. Meskipun jumlah data 
    untuk masing-masing kelas tidak sebanding atau mengalami `imbalance data`, tetapi rentang perbandingan tersebut 
    tidak terlalu signifikan. Sehingga untuk persiapan data sebelum pelatihan model tidak diterapkan metode tertentu.
    """
    st.markdown(text, unsafe_allow_html=True)

    text = '''
    ### Word Cloud Sentiment
    Data development dilakukan untuk text dilakukan *cleaning* terlebih dahulu. Proses *cleaning* lebih detail dapat dilihat pada menu `Data Preprocessing`.
    '''
    st.markdown(text, unsafe_allow_html=True)

    # load preprocessed data
    data = pd.read_csv('../data/data_complete_masked_preprocessed.csv')
    data = data[data.data_type == 'development']
    # slice comments
    neutral = data[data['label'] == 'neutral']
    positive = data[data['label'] == 'positive']
    negative = data[data['label'] == 'negative']

    comment_words_neu = ''
    comment_words_pos = ''
    comment_words_neg = ''

    # iterate
    for val in neutral['text']:
        # typecaste each val to string
        val = str(val)
        tokens = val.split()
        for i in range(len(tokens)):
            tokens[i] = re.sub(r'[^\x00-\x7F]+', ' ', tokens[i])
            tokens[i] = tokens[i].strip()
        comment_words_neu += " ".join(tokens)+" "
    for val in positive['text']:
        # typecaste each val to string
        val = str(val)
        tokens = val.split()
        for i in range(len(tokens)):
            tokens[i] = re.sub(r'[^\x00-\x7F]+', ' ', tokens[i])
            tokens[i] = tokens[i].strip()
        comment_words_pos += " ".join(tokens)+" "
    for val in negative['text']:
        # typecaste each val to string
        val = str(val)
        tokens = val.split()
        for i in range(len(tokens)):
            tokens[i] = re.sub(r'[^\x00-\x7F]+', ' ', tokens[i])
            tokens[i] = tokens[i].strip()
        comment_words_neg += " ".join(tokens)+" "

    st.markdown("#### Sentiment Neutral")
    text = """
    Kata-kata seperti `vaksin`, `semarang`, `usia`, `mohon`, `kota` muncul terbanyak untuk sentiment neutral.
    Hal ini karena banyaknya komentar-komentar yang bertanya informasi vaksin yang tersedia di kota Semarang.
    """
    st.markdown(text, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        n_words_neu = st.slider("Set the number of words in Word Cloud",
                                min_value=50, max_value=200, step=10, key="neutral")
        wc_neutral = WordCloud(colormap='Blues', mode='RGBA', max_words=n_words_neu,
                               background_color='white', width=1000, height=500)
        wc_neutral.generate(comment_words_neu)
        fig = plt.figure(figsize=(15, 5))
        plt.imshow(wc_neutral, interpolation='bilinear')
        plt.axis("off")
        plt.tight_layout()
        st.pyplot(fig)
    with col2:
        top = Counter(comment_words_neu.split()).most_common(10)
        temp = pd.DataFrame(top, columns=['word', 'count'])
        temp = temp.sort_values(by='count', ascending=True)
        fig_tree_neu = px.treemap(
            temp, path=['word'], values='count', title='Top 10 Most Common Words')
        fig_tree_neu.update_layout(margin=dict(t=30, l=0, r=50, b=50))
        st.plotly_chart(fig_tree_neu)

    st.markdown("#### Sentiment Positive")
    text = """
    Kata-kata seperti `tangan_berdoa`, `semoga`, `ayo`, `alhamdulillah`, `semangat` muncul terbanyak untuk sentiment positive.
    Hal ini terjadi karena terdapat penurunan kasus COVID-19 di kota Semarang sehingga masyarakat Semarang memberikan komentar
    positive. Untuk kata `tangan_berdoa` merupakan hasil konversi emoticon 🙏 setelah melalui proses text preprocessing.
    """
    st.markdown(text, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        n_words_pos = st.slider("Set the number of words in Word Cloud",
                                min_value=50, max_value=200, step=10, key="positive")
        wc_positive = WordCloud(colormap='Greens', mode='RGBA', max_words=n_words_pos,
                                background_color='white', width=1000, height=500)
        wc_positive.generate(comment_words_pos)
        fig = plt.figure(figsize=(15, 5))
        plt.imshow(wc_positive, interpolation='bilinear')
        plt.title('Wordcloud Sentiment Positive')
        plt.axis("off")
        plt.tight_layout()
        st.pyplot(fig)
    with col2:
        top = Counter(comment_words_pos.split()).most_common(10)
        temp = pd.DataFrame(top, columns=['word', 'count'])
        temp = temp.sort_values(by='count', ascending=True)
        fig_tree_pos = px.treemap(
            temp, path=['word'], values='count', title='Top 10 Most Common Words')
        fig_tree_pos.update_layout(margin=dict(t=30, l=0, r=50, b=50))
        st.plotly_chart(fig_tree_pos)

    st.markdown("#### Sentiment Negative")
    text = """
    Kata-kata seperti `wajah_menangis_keras`, `wajah_menangis`, `covid`, `data`, `pakai`, `masker`, `positif` muncul 
    terbanyak untuk sentiment negative. Hal ini terjadi terjadi kenaikan kasus positif COVID-19 di kota Semarang. 
    Menariknya disini juga muncul kata-kata `data`, `pakai`, `masker` menunjukkan keraguan masyarakat terhadap 
    kebenaran data kasus positif yang naik sekaligus mengetahui bahwa kenaikan tersebut karena terdapat masyarakat 
    tidak memakai masker di lingkungannya.
    """
    st.markdown(text, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        n_words_neg = st.slider("Set the number of words in Word Cloud",
                                min_value=50, max_value=200, step=10, key="negative")
        wc_negative = WordCloud(colormap='Reds', mode='RGBA', max_words=n_words_neg,
                                background_color='white', width=1000, height=500)
        wc_negative.generate(comment_words_neg)
        fig = plt.figure(figsize=(15, 5))
        plt.imshow(wc_negative, interpolation='bilinear')
        plt.title('Wordcloud Sentiment Negative')
        plt.axis("off")
        plt.tight_layout()
        st.pyplot(fig)
    with col2:
        top = Counter(comment_words_neg.split()).most_common(10)
        temp = pd.DataFrame(top, columns=['word', 'count'])
        temp = temp.sort_values(by='count', ascending=True)
        fig_tree_neg = px.treemap(
            temp, path=['word'], values='count', title='Top 10 Most Common Words')
        fig_tree_neg.update_layout(margin=dict(t=30, l=0, r=50, b=50))
        st.plotly_chart(fig_tree_neg)

    st.markdown("### Sentiment Neutral vs Positive vs Negative")
    text = """
    Kita lihat perbandingan jumlah masing-masing sentimen tiap harinya pada data `development`. Jika kita perhatikan
    jumlah komentar meningkat pada bulan Juni-Juli 2021. Hal ini dikarenakan kenaikan kasus COVID-19 yang terjadi di Semarang.
    Kita perlu melihat perbandingan kasus positif aktif COVID-19 terhadap jumlah tiap sentimen.
    """
    st.markdown(text, unsafe_allow_html=True)

    sentiment_counter = pd.read_csv('../data/sentiment_counter.csv')
    max_datetime = data['datetime'].max()
    sentiment_counter = sentiment_counter[sentiment_counter['date'] <= max_datetime]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sentiment_counter['date'], y=sentiment_counter['neutral'],
                             mode='lines+markers', marker_color='#636EFA', name='Neutral'))
    fig.add_trace(go.Scatter(x=sentiment_counter['date'], y=sentiment_counter['positive'],
                             mode='lines+markers', marker_color='#00CC96', name='Positive'))
    fig.add_trace(go.Scatter(x=sentiment_counter['date'], y=sentiment_counter['negative'],
                             mode='lines+markers', marker_color='#EF553B', name='Negative'))
    fig.update_layout(template='presentation',
                      plot_bgcolor='rgb(275, 270, 273)',
                      width=900,
                      height=400,
                      margin=dict(t=20, l=70, r=0, b=70))
    # Set x-axes and y-axes titles
    fig.update_yaxes(title_text="Number of Sentiments")
    fig.update_xaxes(title_text="Date")
    st.plotly_chart(fig)

    st.markdown("### COVID-19 Cases, Recovery, and Deaths in Semarang")
    text = """
    Kasus COVID-19 di Semarang terdapat 3 puncak yaitu `July 2020`, `January 2021`, dan `July 2021`. Jumlah kematian
    akan meningkat jika semakin banyak masyarakat Semarang yang terjangkit virus COVID-19.
    """
    st.markdown(text, unsafe_allow_html=True)
    df_coronas = pd.read_csv('../data/data_corona_semarang_14112021.csv')
    df_coronas = df_coronas[df_coronas['Tanggal'] <= max_datetime]

    fig = go.Figure(data=[
        go.Bar(name='Deaths', x=df_coronas['Tanggal'],
               y=df_coronas['NEW DEATH'], marker_color='#ff0000'),
        go.Bar(name='Recovered Cases', x=df_coronas['Tanggal'],
               y=df_coronas['NEW RECOVERED'], marker_color='#2bad57'),
        go.Bar(name='Confirmed Cases', x=df_coronas['Tanggal'], y=df_coronas['POSITIVE ACTIVE'], marker_color='#326ac7')])
    fig.update_layout(barmode='stack')
    fig.update_traces(textposition='inside')
    fig.update_layout(plot_bgcolor='rgb(275, 270, 273)',
                      template='presentation', width=900,
                      height=400,
                      margin=dict(t=20, l=70, r=0, b=70))
    fig.update_yaxes(title_text="Number of Cases")
    st.plotly_chart(fig)

    st.markdown("### COVID-19 Positive Active Cases vs Sentiment (Neutral, Positive, Negative)")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=df_coronas['Tanggal'], y=df_coronas['POSITIVE ACTIVE'],
                         name='Positive Active', marker_color='rgba(255, 161, 90, 0.8)',
                         marker_line_width=0),
                  secondary_y=False)
    fig.add_trace(go.Scatter(x=sentiment_counter['date'], y=sentiment_counter['neutral'],
                             mode='lines+markers', marker_color='#636EFA', name='Sentiment Neutral'),
                  secondary_y=True)
    fig.add_trace(go.Scatter(x=sentiment_counter['date'], y=sentiment_counter['positive'],
                             mode='lines+markers', marker_color='#00CC96', name='Sentiment Positive'),
                  secondary_y=True)
    fig.add_trace(go.Scatter(x=sentiment_counter['date'], y=sentiment_counter['negative'],
                             mode='lines+markers', marker_color='#EF553B', name='Sentiment Negative'),
                  secondary_y=True)
    # Add figure title
    fig.update_layout(
        template='presentation',
        plot_bgcolor='rgb(275, 270, 273)',
        width=1100,
        height=400,
        margin=dict(t=20, l=70, r=70, b=20)
    )
    # Set x-axis, y-axis title
    fig.update_yaxes(title_text="Number of Sentiments", secondary_y=True, rangemode='tozero')
    fig.update_yaxes(title_text="Number of Cases", secondary_y=False, rangemode='tozero')
    st.plotly_chart(fig)
    text = """
    Terdapat beberapa insight yang dapat kita ketahui:
    - Jumlah komentar semakin meningkat jika kasus COVID-19 meningkat.
    - Jika terjadi kenaikan kasus, jumlah sentimen `negative` akan semakin banyak dibandingkan dengan sentimen `positive`.
    - Sebaliknya jika terjadi penurunan kasus, jumlah sentimen `positive` akan semakin banyak dibandingkan dengan sentimen `negative`.
    - Pada bulan Juni-July 2021, sentimen `neutral` semakin banyak karena banyaknya komentar pertanyaan terkait info vaksinasi. Selain itu
    vaksinasi sudah dibuka oleh pemerintah kota Semarang untuk masyarakat umum.
    """
    st.markdown(text, unsafe_allow_html=True)

    st.markdown("### COVID-19 Cases, Recovery, and Deaths Monthly")
    st.markdown("Kita coba lihat data dengan timeframe bulanan.")
    df_coronas['Tanggal'] = pd.to_datetime(df_coronas['Tanggal'])
    coronas_by_month = df_coronas.groupby(pd.Grouper(key='Tanggal', freq='M')).sum().reset_index()
    temp = coronas_by_month.copy()

    fig = go.Figure(data=[
        go.Bar(name='Deaths', x=temp['Tanggal'],
               y=temp['NEW DEATH'], marker_color='#ff0000'),
        go.Bar(name='Recovered Cases',
               x=temp['Tanggal'], y=temp['NEW RECOVERED'], marker_color='#2bad57'),
        go.Bar(name='Confirmed Cases', x=temp['Tanggal'], y=temp['POSITIVE ACTIVE'], marker_color='#326ac7')])
    fig.update_layout(barmode='stack')
    fig.update_traces(textposition='inside')
    fig.update_layout(plot_bgcolor='rgb(275, 270, 273)',
                      template='presentation',
                      width=900,
                      height=400,
                      margin=dict(t=20, l=70, r=70, b=70))
    fig.update_yaxes(title_text="Number of Cases")
    st.plotly_chart(fig)

    st.markdown("### Sentiment Neutral vs Positive vs Negative by Monthly")
    st.markdown("Kita lihat juga jumlah sentiment dalam timeframe bulanan.")
    sentiment_counter['date'] = pd.to_datetime(sentiment_counter['date'])
    sentiment_counter_monthly = sentiment_counter.groupby(pd.Grouper(key='date', freq='M')).sum().reset_index()
    temp = sentiment_counter_monthly.copy()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=temp['date'], y=temp['neutral'],
                             mode='lines+markers', marker_color='#636EFA', name='Neutral'))
    fig.add_trace(go.Scatter(x=temp['date'], y=temp['positive'],
                             mode='lines+markers', marker_color='#00CC96', name='Positive'))
    fig.add_trace(go.Scatter(x=temp['date'], y=temp['negative'],
                             mode='lines+markers', marker_color='#EF553B', name='Negative'))
    fig.update_layout(
        template='presentation',
        plot_bgcolor='rgb(275, 270, 273)',
        width=900,
        height=400,
        margin=dict(t=20, l=70, r=70, b=70)
    )
    # Set x-axes and y-axes titles
    fig.update_yaxes(title_text="Number of Sentiments")
    st.plotly_chart(fig)

    st.markdown("### COVID-19 Positive Active Cases vs Sentiment (Neutral, Positive, Negative) by Monthly")
    st.markdown("Insight yang dihasilkan dari timeframe bulanan sama dengan yang harian.")
    temp1 = coronas_by_month.copy()
    temp2 = sentiment_counter_monthly.copy()

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=temp1['Tanggal'], y=temp1['POSITIVE ACTIVE'],
                         name='Positive Active',
                         marker_color='rgba(255, 161, 90, 0.8)',
                         marker_line_width=0),
                  secondary_y=False)
    fig.add_trace(go.Scatter(x=temp2['date'], y=temp2['neutral'],
                             mode='lines+markers', marker_color='#636EFA', name='Sentiment Neutral'),
                  secondary_y=True)
    fig.add_trace(go.Scatter(x=temp2['date'], y=temp2['positive'],
                             mode='lines+markers', marker_color='#00CC96', name='Sentiment Positive'),
                  secondary_y=True)
    fig.add_trace(go.Scatter(x=temp2['date'], y=temp2['negative'],
                             mode='lines+markers', marker_color='#EF553B', name='Sentiment Negative'),
                  secondary_y=True)
    fig.update_layout(
        template='presentation',
        plot_bgcolor='rgb(275, 270, 273)',
        width=1100,
        height=400,
        margin=dict(t=20, l=70, r=70, b=70)
    )
    # Set y-axes titles
    fig.update_yaxes(title_text="Number of Sentiments", secondary_y=True, rangemode='tozero')
    fig.update_yaxes(title_text="Number of Cases", secondary_y=False, rangemode='tozero')
    st.plotly_chart(fig)