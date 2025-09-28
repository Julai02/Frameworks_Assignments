# cord19_streamlit_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import re

# Load cleaned data
@st.cache_data
def load_data():
    df = pd.read_csv('metadata_cleaned.csv', parse_dates=['publish_time'])
    df['publish_year'] = df['publish_time'].dt.year
    return df

df = load_data()

# 🎯 App Title and Description
st.title("CORD-19 Data Explorer")
st.markdown("Explore trends in COVID-19 research papers using the CORD-19 metadata.")

# 📅 Year Range Slider
min_year, max_year = int(df['publish_year'].min()), int(df['publish_year'].max())
year_range = st.slider("Select publication year range", min_year, max_year, (2020, 2021))

# 📊 Journal Dropdown
journals = df['journal'].dropna().unique()
selected_journal = st.selectbox("Filter by journal", options=['All'] + sorted(journals.tolist()))

# 🔍 Filtered Data
filtered_df = df[df['publish_year'].between(year_range[0], year_range[1])]
if selected_journal != 'All':
    filtered_df = filtered_df[filtered_df['journal'] == selected_journal]

# 📋 Show Sample Data
st.subheader("📋 Sample of Filtered Data")
st.dataframe(filtered_df[['title', 'journal', 'publish_time']].head(10))

# 📈 Publications Over Time
st.subheader("📈 Publications Over Time")
pubs_by_year = filtered_df['publish_year'].value_counts().sort_index()
fig1, ax1 = plt.subplots()
sns.lineplot(x=pubs_by_year.index, y=pubs_by_year.values, marker='o', ax=ax1)
ax1.set_xlabel("Year")
ax1.set_ylabel("Number of Papers")
st.pyplot(fig1)

# 🏛️ Top Journals
st.subheader("🏛️ Top Journals")
top_journals = filtered_df['journal'].value_counts().head(10)
fig2, ax2 = plt.subplots()
sns.barplot(x=top_journals.values, y=top_journals.index, ax=ax2)
ax2.set_xlabel("Number of Papers")
ax2.set_ylabel("Journal")
st.pyplot(fig2)

# ☁️ Word Cloud of Titles
st.subheader("☁️ Word Cloud of Paper Titles")
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

title_words = filtered_df['title'].dropna().apply(clean_text).str.split()
flat_words = [word for sublist in title_words for word in sublist if len(word) > 3]
word_freq = Counter(flat_words)
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)

fig3, ax3 = plt.subplots(figsize=(10, 5))
ax3.imshow(wordcloud, interpolation='bilinear')
ax3.axis('off')
st.pyplot(fig3)

# 🧪 Source Distribution
if 'source_x' in filtered_df.columns:
    st.subheader("🧪 Paper Counts by Source")
    source_counts = filtered_df['source_x'].value_counts().head(10)
    fig4, ax4 = plt.subplots()
    sns.barplot(x=source_counts.values, y=source_counts.index, ax=ax4)
    ax4.set_xlabel("Number of Papers")
    ax4.set_ylabel("Source")
    st.pyplot(fig4)
