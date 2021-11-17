import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from collections import Counter


st.set_page_config(layout="wide")

# menu sidebar
list_menu = ['Home', 'Data Collection', 'Data Annotation', 'Exploratory Data Analysis', 'Data Preprocessing', 'Modeling', 'Evaluation', 'Deployment']
menu_choice = st.sidebar.selectbox("Select a menu", list_menu)

### MENU: HOME ###
if menu_choice == 'Home':
    st.markdown(f'<h1 style="font-weight:bolder;font-size:40px;color:black;text-align:center;">Sentiment Analysis Komentar Instagram</h1>', unsafe_allow_html=True)
    st.markdown(f'<h3 style="font-weight:normal;font-size:18px;color:gray;text-align:center;">Study Case: Dinas Kesehatan Kota Semarang (@dkksemarang)</h1>', unsafe_allow_html=True)

    # read dataset
    df_comments = pd.read_csv('../data/data_complete_visualization.csv')
    df_coronas = pd.read_csv('../data/data_corona_semarang_14112021.csv')
    df_sentiment_counter = pd.read_csv('../data/sentiment_counter.csv')
    
    # convert data types
    df_comments['datetime'] = pd.to_datetime(df_comments['datetime'])
    df_coronas['Tanggal'] = pd.to_datetime(df_coronas['Tanggal'])
    df_sentiment_counter['date'] = pd.to_datetime(df_sentiment_counter['date'])
    df_sentiment_counter['neutral'] = pd.to_numeric(df_sentiment_counter['neutral'])
    df_sentiment_counter['positive'] = pd.to_numeric(df_sentiment_counter['positive'])
    df_sentiment_counter['negative'] = pd.to_numeric(df_sentiment_counter['negative'])

    # select chart type
    chart_type = st.radio("Choose your chart type:", ['All ', 'Filter'])
    
    if chart_type == 'Filter':
        comments = df_comments.copy()
        coronas = df_coronas.copy()
        sentiment_counter = df_sentiment_counter.copy()

        # create 2 columns
        col1, col2 = st.columns(2)

        # Filter by data type
        with col1:
            selected_data = st.selectbox('Select data type', ["Data for Development", "Data for Inference"])

            if selected_data == "Data for Development":
                comments = comments[comments.data_type == 'development']
            elif selected_data == "Data for Inference":
                comments = comments[comments.data_type == 'inference']

            max_month = comments['datetime'].max().month
            max_year = comments['datetime'].max().year
            min_month = comments['datetime'].min().month
            min_year = comments['datetime'].min().year
            min_datetime = comments['datetime'].min()
            max_datetime = comments['datetime'].max()

        with col2:
            mode_chart = st.radio("Select your chart mode:", ['All', 'Filter by Month'])

        if mode_chart == 'Filter by Month':
            selected_time = st.slider(
                "Select month",
                min_value=datetime(min_year, min_month, 1),
                max_value=datetime(max_year, max_month, 1),
                format="MMM YYYY")

            st.caption('__*Filtered by ' + selected_data + ' in ' + selected_time.strftime('%b-%Y') + '*__')

            filter_month = selected_time.month
            filter_year = selected_time.year

            coronas_filter = coronas[(coronas['Tanggal'].dt.month == filter_month) & (
                coronas['Tanggal'].dt.year == filter_year)]
            sentiment_counter_filter = sentiment_counter[(sentiment_counter['date'].dt.month == filter_month) & (
                sentiment_counter['date'].dt.year == filter_year)]
            comments = comments[(comments['datetime'].dt.month == filter_month) & (
                comments['datetime'].dt.year == filter_year)]

        elif mode_chart == 'All':
            coronas_filter = coronas[(coronas['Tanggal'] >= min_datetime) & (coronas['Tanggal'] <= max_datetime)]
            sentiment_counter_filter = sentiment_counter[(sentiment_counter['date'] >= min_datetime) & (sentiment_counter['date'] <= max_datetime)]
            st.caption('__*Filtered by ' + selected_data + ' from ' + min_datetime.strftime(
                "%d %b %Y") + ' to ' + max_datetime.strftime("%d %b %Y") + '*__')

    else:
        comments = df_comments.copy()
        coronas = df_coronas.copy()
        sentiment_counter = df_sentiment_counter.copy()

        coronas_filter = coronas.copy()
        sentiment_counter_filter = sentiment_counter.copy()

    # make plot
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(x=coronas_filter['Tanggal'], y=coronas_filter['POSITIVE ACTIVE'],
                         name='Positive Active',
                         marker_color='rgba(0,0,250, 0.3)',
                         marker_line_width=0),
                  secondary_y=False)

    fig.add_trace(go.Scatter(x=sentiment_counter_filter['date'], y=sentiment_counter_filter['neutral'],
                             mode='lines+markers', marker_color='deepskyblue', name='Sentiment Neutral'),
                  secondary_y=True)
    fig.add_trace(go.Scatter(x=sentiment_counter_filter['date'], y=sentiment_counter_filter['positive'],
                             mode='lines+markers', marker_color='seagreen', name='Sentiment Positive'),
                  secondary_y=True)
    fig.add_trace(go.Scatter(x=sentiment_counter_filter['date'], y=sentiment_counter_filter['negative'],
                             mode='lines+markers', marker_color='orangered', name='Sentiment Negative'),
                  secondary_y=True)

    # Add figure title
    fig.update_layout(
        title_text="COVID-19 Positive Active Cases vs Sentiment (Neutral, Positive, Negative)",
        template='presentation',
        plot_bgcolor='rgb(275, 270, 273)'
    )

    # Set x-axis title
    # fig.update_xaxes(title_text="date")

    # Set y-axes titles
    fig.update_yaxes(title_text="Number of Sentiments",
                     secondary_y=True, rangemode='tozero')
    fig.update_yaxes(title_text="Number of Cases",
                     secondary_y=False, rangemode='tozero')

    # margin legend
    # fig.update_layout(margin=dict(r=25))
    st.plotly_chart(fig, use_container_width=True)


    # WORD CLOUD

    # filter data for each sentiment
    neutral = comments[comments.label == "neutral"]
    positive = comments[comments.label == "positive"]
    negative = comments[comments.label == "negative"]

    # create slider for the number of words
    n_words = st.slider("Set the number of words in Word Cloud", min_value=50, max_value=200, step=10)

    # create 3 columns
    col1, col2, col3 = st.columns(3)

    # neutral
    with col1:
        texts = ''
        for val in neutral['text']:
            val = str(val)
            tokens = val.split()
            for i in range(len(tokens)):
                tokens[i] =  re.sub(r'[^\x00-\x7F]+',' ', tokens[i])
                tokens[i] = tokens[i].strip()
            texts += " ".join(tokens)+" "
        wc = WordCloud(
            colormap="Blues",
            mode="RGBA",
            max_words=n_words,
            background_color="white",
            collocations=False,
            width=400, height=400,
        )
        wc.generate(texts)

        st.markdown("#### Sentiment Neutral", unsafe_allow_html=False)
        # plot
        fig = plt.figure(figsize=(20, 8), dpi=80)
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        plt.tight_layout()
        st.pyplot(fig)

        # top 10 words 
        top10 = Counter(texts.split()).most_common(10)
        df_top10 = pd.DataFrame(top10, columns=['word','freq'])
        df_top10 = df_top10.sort_values(by='freq', ascending=True)

        # plot
        fig_bar = px.bar(df_top10, x="freq", y="word",
                         orientation='h', height=400, width=350)
        fig_bar.update_layout(title_text='Top 10 words sentiment neutral',
                        plot_bgcolor='rgb(275, 270, 273)')
        fig_bar.update_traces(marker_color='lightblue')

        # Set x-axes and y-axes titles
        fig_bar.update_yaxes(title_text="")
        fig_bar.update_xaxes(title_text="frequency")
        st.plotly_chart(fig_bar)

    # positive
    with col2:
        texts = ''
        for val in positive['text']:
            val = str(val)
            tokens = val.split()
            for i in range(len(tokens)):
                tokens[i] =  re.sub(r'[^\x00-\x7F]+',' ', tokens[i])
                tokens[i] = tokens[i].strip()
            texts += " ".join(tokens)+" "
        wc = WordCloud(
            colormap="Greens",
            mode="RGBA",
            max_words=n_words,
            background_color="white",
            collocations=False,
            width=400, height=400,
        )
        wc.generate(texts)

        st.markdown("#### Sentiment Positive", unsafe_allow_html=False)
        # plot
        fig = plt.figure(figsize=(20, 8), dpi=80)
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        plt.tight_layout()
        st.pyplot(fig)

        # top 10 words
        top10 = Counter(texts.split()).most_common(10)
        df_top10 = pd.DataFrame(top10, columns=['word', 'freq'])
        df_top10 = df_top10.sort_values(by='freq', ascending=True)

        # plot
        fig_bar = px.bar(df_top10, x="freq", y="word",
                         orientation='h', height=400, width=350)
        fig_bar.update_layout(title_text='Top 10 words sentiment positive',
                              plot_bgcolor='rgb(275, 270, 273)')
        fig_bar.update_traces(marker_color='lightgreen')

        # Set x-axes and y-axes titles
        fig_bar.update_yaxes(title_text="")
        fig_bar.update_xaxes(title_text="frequency")
        st.plotly_chart(fig_bar)
    # negative
    with col3:
        texts = ''
        for val in negative['text']:
            val = str(val)
            tokens = val.split()
            for i in range(len(tokens)):
                tokens[i] =  re.sub(r'[^\x00-\x7F]+',' ', tokens[i])
                tokens[i] = tokens[i].strip()
            texts += " ".join(tokens)+" "
        wc = WordCloud(
            colormap="Reds",
            mode="RGBA",
            max_words=n_words,
            background_color="white",
            collocations=False,
            width=400, height=400,
        )
        wc.generate(texts)

        st.markdown("#### Sentiment Negative", unsafe_allow_html=False)
        # plot
        fig = plt.figure(figsize=(20, 8), dpi=80)
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        plt.tight_layout()
        st.pyplot(fig)

        # top 10 words
        top10 = Counter(texts.split()).most_common(10)
        df_top10 = pd.DataFrame(top10, columns=['word', 'freq'])
        df_top10 = df_top10.sort_values(by='freq', ascending=True)

        # plot
        fig_bar = px.bar(df_top10, x="freq", y="word",
                         orientation='h', height=400, width=350)
        fig_bar.update_layout(title_text='Top 10 words sentiment negative',
                              plot_bgcolor='rgb(275, 270, 273)')
        fig_bar.update_traces(marker_color='red')

        # Set x-axes and y-axes titles
        fig_bar.update_yaxes(title_text="")
        fig_bar.update_xaxes(title_text="frequency")
        st.plotly_chart(fig_bar)

### MENU: DATA COLLECTION ###
if menu_choice == 'Data Collection':
    """
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
    st.markdown(f'<div style="position: relative; padding-bottom: 56.25%; height: 0;"><iframe src="https://www.loom.com/embed/63a97d262dd74f1bbee945c3d791309e" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"> </iframe></div>', unsafe_allow_html=True)
    st.markdown(f'<br>', unsafe_allow_html=True)
    """
    2. Lakukan batch URL post instagram
    ```
    python batch_url_posts.py
    ```

    3. Crawling semua komentar yang terdapat pada masing-masing URL post instagram @dkksemarang menggunakan script `get_comments.py`
    """
    st.markdown(f'<div style="position: relative; padding-bottom: 56.25%; height: 0;"><iframe src="https://www.loom.com/embed/56cec350df5c421cbd932164cac74a15" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>', unsafe_allow_html=True)
    st.markdown(f'<br>', unsafe_allow_html=True)
    """
    ### Hasil crawling
    """
    df_raw = pd.read_csv('../data/data_raw_masked.csv')
    min_date_raw = pd.to_datetime(df_raw['datetime'].min())
    max_date_raw = pd.to_datetime(df_raw['datetime'].max())
    
    st.markdown(f'- Jumlah data: {df_raw.shape[0]} baris', unsafe_allow_html=True)
    st.markdown(f'- Data columns: `{", ".join(list(df_raw))}`', unsafe_allow_html=True)
    st.markdown(f'- Range date: `{min_date_raw.strftime("%d %b %Y")}` to `{max_date_raw.strftime("%d %b %Y")}`')
    st.markdown(f'- Data preview')
    st.dataframe(df_raw.head())