#import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import re

#part 1: Data Loading and Initial Exploration

# Step 1: Load the metadata.csv file
file_path = 'metadata.csv'  # Example: './data/metadata.csv'
df = pd.read_csv(file_path, low_memory=False)

# Step 2: Preview the data
print("\n🔍 First 5 rows of the dataset:")
print(df.head())

print("\n📐 DataFrame dimensions:")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

print("\n🔤 Data types of each column:")
print(df.dtypes)

# Step 3: Check for missing values in important columns
important_columns = ['title', 'abstract', 'authors', 'publish_time', 'journal']
print("\n❓ Missing values in important columns:")
print(df[important_columns].isnull().sum())

# Step 4: Basic statistics for numerical columns
print("\n📊 Descriptive statistics for numerical columns:")
print(df.describe())

#part 2: Data Cleaning and preparation

# Step 1: Identify columns with many missing values
missing_summary = df.isnull().sum().sort_values(ascending=False)
print("\n🚨 Columns with most missing values:")
print(missing_summary.head(10))

# Step 2: Decide how to handle missing values
# Drop columns with more than 80% missing values
threshold = 0.8 * len(df)
df_cleaned = df.dropna(thresh=threshold, axis=1)

# Drop rows missing critical metadata
critical_columns = ['title', 'abstract', 'publish_time']
df_cleaned = df_cleaned.dropna(subset=critical_columns)

#  Fill missing 'journal' with 'Unknown'
if 'journal' in df_cleaned.columns:
    df_cleaned['journal'] = df_cleaned['journal'].fillna('Unknown')

# Step 3: Convert publish_time to datetime format
df_cleaned['publish_time'] = pd.to_datetime(df_cleaned['publish_time'], errors='coerce')

# Step 4: Extract year from publish_time
df_cleaned['publish_year'] = df_cleaned['publish_time'].dt.year

# Step 5: Create new column: abstract word count
df_cleaned['abstract_word_count'] = df_cleaned['abstract'].apply(lambda x: len(str(x).split()))

# Final check
print("\n✅ Cleaned DataFrame preview:")
print(df_cleaned.head())

print("\n📊 Summary of new columns:")
print(df_cleaned[['publish_year', 'abstract_word_count']].describe())


#part 3 data analysis and visualization
# Load cleaned dataset
df = pd.read_csv('metadata_cleaned.csv', parse_dates=['publish_time'])

# Set plot style
sns.set(style='whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)

# -------------------------------
# 🔢 1. Count papers by publication year
# -------------------------------
df['publish_year'] = df['publish_time'].dt.year
year_counts = df['publish_year'].value_counts().sort_index()

# -------------------------------
# 🏛️ 2. Identify top journals
# -------------------------------
top_journals = df['journal'].value_counts().head(10)

# -------------------------------
# 🧠 3. Most frequent words in titles
# -------------------------------
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

title_words = df['title'].dropna().apply(clean_text).str.split()
flat_words = [word for sublist in title_words for word in sublist if len(word) > 3]
word_freq = Counter(flat_words)
top_words = dict(word_freq.most_common(20))

# -------------------------------
# 📈 4. Plot publications over time
# -------------------------------
plt.figure()
year_counts.plot(kind='line', marker='o', color='teal')
plt.title('📈 Number of Publications Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Papers')
plt.tight_layout()
plt.show()

# -------------------------------
# 📊 5. Bar chart of top journals
# -------------------------------
plt.figure()
top_journals.plot(kind='bar', color='coral')
plt.title('🏛️ Top Publishing Journals')
plt.xlabel('Journal')
plt.ylabel('Number of Papers')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# -------------------------------
# ☁️ 6. Word cloud of paper titles
# -------------------------------
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)

plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('☁️ Word Cloud of Paper Titles')
plt.tight_layout()
plt.show()

# -------------------------------
# 🧪 7. Distribution of paper counts by source
# -------------------------------
if 'source_x' in df.columns:
    source_counts = df['source_x'].value_counts().head(10)
    plt.figure()
    source_counts.plot(kind='bar', color='slateblue')
    plt.title('🧪 Paper Counts by Source')
    plt.xlabel('Source')
    plt.ylabel('Number of Papers')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
else:
    print("⚠️ Column 'source_x' not found in dataset.")
