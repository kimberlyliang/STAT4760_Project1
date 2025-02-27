import pandas as pd

file_path = "games_metadata_profile_2024_01.csv"
print(f"Loading data from {file_path}...")
df = pd.read_csv(file_path)
print("Data loaded successfully.")

white_column = "White"
black_column = "Black"
elo_white_column = "WhiteElo"
elo_black_column = "BlackElo"

print("Counting games played by each user...")
user_game_counts = pd.concat([df[white_column], df[black_column]]).value_counts().reset_index()
user_game_counts.columns = ["username", "game_count"]

user_game_counts["elo"] = 0

print("Calculating Elo ratings...")
for index, row in user_game_counts.iterrows():
    username = row["username"]
    
    white_elo = df.loc[df[white_column] == username, elo_white_column].mean()
    black_elo = df.loc[df[black_column] == username, elo_black_column].mean()
    
    if pd.notna(white_elo) and pd.notna(black_elo):
        user_game_counts.at[index, "elo"] = round((white_elo + black_elo) / 2)
    elif pd.notna(white_elo):
        user_game_counts.at[index, "elo"] = white_elo
    elif pd.notna(black_elo):
        user_game_counts.at[index, "elo"] = black_elo
    else:
        user_game_counts.at[index, "elo"] = 0

output_path = "lichess_game_counts.csv"
user_game_counts.to_csv(output_path, index=False)
print(f"Statistics saved to {output_path}.")

print("Here are the first few rows of the user statistics:")
print(user_game_counts.head())
