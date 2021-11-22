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

    st.markdown("### Data development")
    st.markdown(
        f"Shape dari data development: {data.shape[0]} baris, {data.shape[1]} kolom")
    st.dataframe(data)

    st.markdown("### Distribusi tiap sentiment")
    temp = data['label'].value_counts().reset_index()
    temp = temp.rename(columns={'index': 'label', 'label': 'count'})
    fig_bar = px.bar(temp,
                     x='label',
                     y='count',
                     color='label',
                     title='Histogram sentiment',
                     category_orders=dict(
                         label=['neutral', 'positive', 'negative']),
                     color_discrete_map={'neutral': '#636EFA', 'positive': '#00CC96', 'negative': '#EF553B'})
    st.plotly_chart(fig_bar)

    # funnel chart
    fig_funnel = px.funnel_area(names=temp['label'],
                                values=temp['count'],
                                title='Funnel-Chart of Sentiment Distribution',
                                color_discrete_map={'neutral': '#636EFA', 'positive': '#00CC96', 'negative': '#EF553B'})
    st.plotly_chart(fig_funnel)

    '''
    ### Wordcloud sentiment
    Data development dilakukan untuk text dilakukan *cleaning* terlebih dahulu. Proses *cleaning* lebih detail dapat dilihat pada menu `Data Preprocessing`.
    '''
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
    sentiment_counter = pd.read_csv('../data/sentiment_counter.csv')
    max_datetime = data['datetime'].max()
    sentiment_counter = sentiment_counter[sentiment_counter['date']
                                          <= max_datetime]

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

    st.markdown(
        "### COVID-19 Positive Active Cases vs Sentiment (Neutral, Positive, Negative)")
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
        width=900,
        height=400,
        margin=dict(t=20, l=70, r=70, b=70)
    )
    # Set x-axis, y-axis title
    # fig.update_xaxes(title_text="date")
    fig.update_yaxes(title_text="Number of Sentiments",
                     secondary_y=True, rangemode='tozero')
    fig.update_yaxes(title_text="Number of Cases",
                     secondary_y=False, rangemode='tozero')
    st.plotly_chart(fig)

    st.markdown("### COVID-19 Cases, Recovery, and Deaths Monthly")
    df_coronas['Tanggal'] = pd.to_datetime(df_coronas['Tanggal'])
    coronas_by_month = df_coronas.groupby(pd.Grouper(
        key='Tanggal', freq='M')).sum().reset_index()
    temp = coronas_by_month.copy()
    fig = go.Figure(data=[
        go.Bar(name='Deaths', x=temp['Tanggal'],
               y=temp['NEW DEATH'], marker_color='#ff0000'),
        go.Bar(name='Recovered Cases',
               x=temp['Tanggal'], y=temp['NEW RECOVERED'], marker_color='#2bad57'),
        go.Bar(name='Confirmed Cases', x=temp['Tanggal'], y=temp['POSITIVE ACTIVE'], marker_color='#326ac7')])
    fig.update_layout(barmode='stack')
    fig.update_traces(textposition='inside')
    # fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_layout(plot_bgcolor='rgb(275, 270, 273)',
                      template='presentation',
                      width=900,
                      height=400,
                      margin=dict(t=20, l=70, r=70, b=70))
    fig.update_yaxes(title_text="Number of Cases")
    st.plotly_chart(fig)

    st.markdown("### Sentiment Neutral vs Positive vs Negative by Monthly")
    sentiment_counter['date'] = pd.to_datetime(sentiment_counter['date'])
    sentiment_counter_monthly = sentiment_counter.groupby(
        pd.Grouper(key='date', freq='M')).sum().reset_index()
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

    st.markdown(
        "### COVID-19 Positive Active Cases vs Sentiment (Neutral, Positive, Negative) by Monthly")
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
        width=900,
        height=400,
        margin=dict(t=20, l=70, r=70, b=70)
    )
    # Set y-axes titles
    fig.update_yaxes(title_text="Number of Sentiments",
                     secondary_y=True, rangemode='tozero')
    fig.update_yaxes(title_text="Number of Cases",
                     secondary_y=False, rangemode='tozero')
    st.plotly_chart(fig)