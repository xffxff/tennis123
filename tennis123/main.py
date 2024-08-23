from datetime import datetime
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.tennis123.net"
MATCH_URL = f"{BASE_URL}/member/match92575_Singles_r30"

class Match:
    def __init__(self, players, score, winner, info, start_time):
        self.players = players
        self.score = score
        self.winner = winner
        self.info = info
        self.start_time = start_time

    def __str__(self):
        return f"match: {self.players}, score: {self.score}, winner: {self.winner}, info: {self.info}, start time: {self.start_time}"
    
class Tournament:
    def __init__(self):
        self.matches = []

    def add_match(self, match):
        self.matches.append(match)

    def __iter__(self):
        return iter(self.matches)

    def __len__(self):
        return len(self.matches)

    def display_matches(self):
        for match in self.matches:
            print(match)

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
    main_soup = get_soup(MATCH_URL)
    match_links = extract_match_links(main_soup)

    for match_url in match_links:
        print(f"Getting match details from {match_url}")
        match_soup = get_soup(match_url)
        match_data = extract_match_data(match_soup)
        for match in match_data:
            tournament.add_match(match)
    
    tournament.display_matches()

if __name__ == "__main__":
    main()