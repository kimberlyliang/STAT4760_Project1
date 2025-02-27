import pandas as pd


file_path = 'club_games_data.csv'
data = pd.read_csv(file_path)

data['white_rating'] = pd.to_numeric(data['white_rating'], errors='coerce')
data['black_rating'] = pd.to_numeric(data['black_rating'], errors='coerce')


white_players = data[['white_username', 'white_rating']].rename(columns={'white_username': 'username', 'white_rating': 'rating'})
black_players = data[['black_username', 'black_rating']].rename(columns={'black_username': 'username', 'black_rating': 'rating'})

all_players = pd.concat([white_players, black_players])
all_players = all_players.drop_duplicates()
top_players = all_players.sort_values(by='rating', ascending=False)

unique_player_count = top_players['username'].nunique()
print(f"Total unique players: {unique_player_count}")


top_players = top_players.head(1500)

# sum stats
top_players_stats = top_players.groupby('username').agg({
    'rating': ['mean', 'std', 'min', 'max', 'count']
}).reset_index()

top_players_stats.columns = ['username', 'mean_rating', 'std_dev_rating', 'min_rating', 'max_rating', 'game_count']

output_path = 'chess_com_top_100_players_statistics.csv'
top_players_stats.to_csv(output_path, index=False)

print("Top 100 Rated Players and Their Statistics:")
print(top_players_stats)
