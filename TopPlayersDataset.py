import csv
import requests
import time
from datetime import datetime

# number of players
def get_games_played(username, year, month):
    url = f"https://api.chess.com/pub/player/{username}/games/{year}/{month}"
    print(f"Fetching games for {username} for {month}/{year}...")
    print(f"Constructed URL: {url}")
    
    for attempt in range(5):
        response = requests.get(url, headers={"User-Agent": "YourAppName/1.0 (your.email@example.com)"})
        
        if response.status_code == 200:
            data = response.json()
            games_count = len(data.get('games', []))  # Return the number of games
            print(f"Found {games_count} games for {username}.")
            return games_count
        elif response.status_code == 403:
            print(f"Access forbidden for {username}. Status code: 403")
            return 0
        elif response.status_code == 429:
            wait_time = 2 ** attempt  # Exponential backoff
            print(f"Rate limit exceeded. Waiting for {wait_time} seconds before retrying...")
            time.sleep(wait_time)
        elif response.status_code == 404:
            print(f"User '{username}' not found or URL is malformed. Status code: 404")
            return 0
        elif response.status_code == 410:
            print(f"No data available for {username}. Status code: 410")
            return 0
        else:
            print(f"Failed to fetch games for {username}. Status code: {response.status_code}")
            return 0

    print(f"Max retries reached for {username}. Returning 0 games.")
    return 0


def read_existing_usernames(club_games_file):
    existing_usernames = set()
    with open(club_games_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            existing_usernames.add(row['white_username'])
            existing_usernames.add(row['black_username'])
    return existing_usernames

def main():
    input_file = 'TopPlayers.csv'
    output_file = 'TopPlayers_with_games.csv'
    club_games_file = 'club_games_data.csv'

    
    now = datetime.now()
    last_month = now.month - 1 if now.month > 1 else 12
    last_year = now.year if now.month > 1 else now.year - 1
    print(f"Processing data for last month: {last_month}/{last_year}")


    existing_usernames = read_existing_usernames(club_games_file)


    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['games_played_last_month']
        rows = []

    
        for row in reader:
            username = row['profilelink'].split('/')[-1].strip()
            print(f"Processing username: '{username}'")
            
            if username in existing_usernames:
                games_played = get_games_played(username, last_year, last_month)
            else:
                print(f"User '{username}' not found in club_games_data. Adding with 0 games.")
                games_played = 0
            
            row['games_played_last_month'] = games_played
            rows.append(row)


            time.sleep(1)

    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Data has been written to {output_file}.")

if __name__ == "__main__":
    main()
