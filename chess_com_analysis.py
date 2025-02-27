import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = 'club_games_data.csv'
data = pd.read_csv(file_path)

data['white_rating'] = pd.to_numeric(data['white_rating'], errors='coerce')
data['black_rating'] = pd.to_numeric(data['black_rating'], errors='coerce')

# Summary statistics
white_elo_stats = data['white_rating'].describe()
black_elo_stats = data['black_rating'].describe()
white_elo_mode = data['white_rating'].mode()[0]
black_elo_mode = data['black_rating'].mode()[0]

print("Chess.com White Elo Ratings Summary Statistics:")
print(white_elo_stats)
print(f"Mode: {white_elo_mode}\n")
print("Chess.com Black Elo Ratings Summary Statistics:")
print(black_elo_stats)
print(f"Mode: {black_elo_mode}\n")

# Game counts
white_counts = data['white_username'].value_counts()
black_counts = data['black_username'].value_counts()
game_counts = white_counts.add(black_counts, fill_value=0)

# Top 10 Players by Game Count
plt.figure(figsize=(12, 6))
game_counts.sort_values(ascending=False).head(10).plot(kind='bar', color='skyblue')
plt.title('Top 10 Chess.com Players by Game Count')
plt.xlabel('Players')
plt.ylabel('Number of Games')
plt.xticks(rotation=45)
plt.show()

# Elo Ratings Distribution
plt.figure(figsize=(12, 6))
sns.histplot(data['white_rating'].dropna(), bins=30, kde=True, color='blue', label='White Players', alpha=0.5)
sns.histplot(data['black_rating'].dropna(), bins=30, kde=True, color='orange', label='Black Players', alpha=0.5)
plt.title('Elo Ratings Distribution for Chess.com Players')
plt.xlabel('Elo Rating')
plt.ylabel('Count')
plt.legend()
plt.show()

# Game Types Distribution
game_type_counts = data['time_class'].value_counts()
selected_game_types = ['blitz', 'rapid', 'bullet']  # Exclude 'daily'
filtered_game_type_counts = game_type_counts[game_type_counts.index.isin(selected_game_types)]
other_count = game_type_counts[~game_type_counts.index.isin(selected_game_types)].sum()
filtered_game_type_counts['Other'] = other_count

plt.figure(figsize=(8, 8))
filtered_game_type_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
plt.title('Distribution of Game Types (Chess.com)')
plt.ylabel('')
plt.show()

# Total Games Over Time
data['UTCDate'] = pd.to_datetime(data['UTCDate'])
games_over_time = data.groupby(data['UTCDate'].dt.date).size()

plt.figure(figsize=(12, 6))
games_over_time.plot(kind='line', marker='o', color='orange')
plt.title('Number of Games Played Over Time (Chess.com)')
plt.xlabel('Date')
plt.ylabel('Number of Games')
plt.xticks(rotation=45)
plt.show()

# Top N Players by Game Count
top_n = game_counts.sort_values(ascending=False).head(10)
print("Top 10 Chess.com Players by Game Count:")
print(top_n)
