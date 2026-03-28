# Load the uploaded disaster dataset (once) and do quick sanity checks
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

csv_path = './cleaned_disaster_data.csv'

disaster_df = pd.read_csv(csv_path, encoding='ascii')

print(disaster_df.head())
print(disaster_df.shape)
print(disaster_df.isna().sum())


# Create requested visuals and top-5 table using the already-loaded disaster_df
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style='whitegrid')

df = disaster_df.copy()

# Ensure numeric
for col_name in ['year', 'deaths', 'affected', 'magnitude']:
    if col_name in df.columns:
        df[col_name] = pd.to_numeric(df[col_name], errors='coerce')

# 1) Bar chart: total deaths by disaster type (overall)
by_type_deaths = (
    df.groupby('disaster_type', dropna=False)['deaths']
      .sum()
      .sort_values(ascending=False)
      .reset_index()
)

plt.figure(figsize=(10, 5))
sns.barplot(data=by_type_deaths, x='disaster_type', y='deaths', color='#4C78A8')
plt.title('Total deaths by disaster type (all countries/years in file)')
plt.xlabel('Disaster type')
plt.ylabel('Total deaths')
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.show()

print(by_type_deaths)

# 2) Trend 2000–2023: total deaths per year (overall), fill missing years with 0
trend_df = (
    df[(df['year'] >= 2000) & (df['year'] <= 2023)]
      .groupby('year')['deaths']
      .sum()
      .reindex(range(2000, 2024), fill_value=0)
      .reset_index()
)
trend_df.columns = ['year', 'deaths']

plt.figure(figsize=(11, 4.8))
sns.lineplot(data=trend_df, x='year', y='deaths', marker='o', color='#F58518')
plt.title('Total deaths per year (2000–2023, all countries in file)')
plt.xlabel('Year')
plt.ylabel('Total deaths')
plt.tight_layout()
plt.show()

print(trend_df.head(10))

# 3) Top 5 deadliest disasters in India (row-level events) within 2000–2023 (assumption)
india_top5 = (
    df[(df['country'] == 'India') & (df['year'] >= 2000) & (df['year'] <= 2023)]
      .sort_values('deaths', ascending=False)
      .head(5)
      .loc[:, ['country', 'year', 'disaster_type', 'deaths', 'affected', 'magnitude']]
      .reset_index(drop=True)
)

print(india_top5)

# Helpful viz for top 5
if len(india_top5) > 0:
    india_top5_plot = india_top5.copy()
    india_top5_plot['label'] = india_top5_plot['year'].astype(int).astype(str) + ' ' + india_top5_plot['disaster_type'].astype(str)

    plt.figure(figsize=(10, 4.8))
    sns.barplot(data=india_top5_plot, y='label', x='deaths', palette='Reds_r')
    plt.title('Top 5 deadliest disasters in India (2000–2023)')
    plt.xlabel('Deaths')
    plt.ylabel('')
    plt.tight_layout()
    plt.show()


    