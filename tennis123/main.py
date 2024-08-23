from datetime import datetime
import requests
from bs4 import BeautifulSoup
import json
import os
from tennis123.data import Match, Tournament
from tennis123 import analysis

BASE_URL = "https://www.tennis123.net"
MATCH_URL = f"{BASE_URL}/member/match92575_Singles_r30"
DATA_FILE = "matches.json"


def save_matches_to_file(matches, filename):
    with open(filename, 'w') as file:
        json_matches = [
            {
                "players": match.players,
                "score": match.score,
                "winner": match.winner,
                "info": match.info,
                "start_time": match.start_time
            }
        for match in matches]
        json.dump(json_matches, file)


def load_matches_from_file(filename):
    with open(filename, 'r') as file:
        json_matches = json.load(file)
        matches = [
            Match(
                match["players"],
                match["score"],
                match["winner"],
                match["info"],
                match["start_time"]
            )
            for match in json_matches]
    return matches

def get_soup(url):
    """Fetches the URL and returns a BeautifulSoup object."""
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, "html.parser")
    else:
        response.raise_for_status()

def extract_match_links(soup):
    """Extracts match links from the soup object."""
    match_links = soup.find_all('a', class_='pull-right')
    return [f"{BASE_URL}{link.get('href')}" for link in match_links if link.get('href')]

def convert_to_iso(datetime_str):
    """Converts the extracted datetime string to ISO 8601 format."""
    # The format of the extracted datetime string
    format_str = "%Y年%m月%d号 %H:%M"
    # Parse the string into a datetime object
    try:
        dt = datetime.strptime(datetime_str, format_str)
        # Return the datetime in ISO 8601 format
        return dt.isoformat()
    except ValueError as e:
        print(f"Error parsing datetime string: {e}")
        return None

def extract_start_time(soup):
    target_div = soup.select_one('.row:nth-child(3) .col-xs-6:nth-child(1)')
    if target_div:
        # Extract the text within the strong tag inside the target div
        start_time_element = target_div.find('strong')
        if start_time_element:
            time_str = start_time_element.get_text(strip=True)
            return convert_to_iso(time_str)
    return None

def extract_match_data(soup):
    """Extracts match data from a match soup object."""
    start_time = extract_start_time(soup)

    rows = soup.find_all('tr', attrs={'data-objid': True})
    match_data = []

    for row in rows:
        tds = row.find_all('td')
        if len(tds) >= 5:
            players = tds[0].get_text(strip=True).replace('VS', ' VS ')
            score = tds[1].get_text(strip=True)
            winner = tds[2].get_text(strip=True)
            group_info = tds[4].get_text(strip=True)
            
            match_data.append(Match(players, score, winner, group_info, start_time))
    
    return match_data

def main():
    tournament = Tournament()

    if os.path.exists(DATA_FILE):
        print("Loading matches from local file...")
        tournament.matches = load_matches_from_file(DATA_FILE)
    else:
        print("Scraping matches from web...")
        main_soup = get_soup(MATCH_URL)
        match_links = extract_match_links(main_soup)

        for match_url in match_links:
            print(f"Getting match details from {match_url}")
            match_soup = get_soup(match_url)
            match_data = extract_match_data(match_soup)
            for match in match_data:
                tournament.add_match(match)

        save_matches_to_file(tournament.matches, DATA_FILE)
    
    tournament.display_matches()

    player_name = "xffxff"
    match_win_rate = analysis.calculate_match_win_rate(player_name, tournament)
    game_win_rate = analysis.calculate_game_win_rate(player_name, tournament)
    print(f"Match win rate for {player_name}: {match_win_rate:.2f}%")
    print(f"Game win rate for {player_name}: {game_win_rate:.2f}%")

if __name__ == "__main__":
    main()