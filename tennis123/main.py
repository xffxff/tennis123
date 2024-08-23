import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.tennis123.net"
MATCH_URL = f"{BASE_URL}/member/match92575_Singles_r30"

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

def extract_match_data(soup):
    """Extracts match data from a match soup object."""
    rows = soup.find_all('tr', attrs={'data-objid': True})
    match_data = []

    for row in rows:
        tds = row.find_all('td')
        if len(tds) >= 5:
            players = tds[0].get_text(strip=True).replace('VS', ' VS ')
            score = tds[1].get_text(strip=True)
            winner = tds[2].get_text(strip=True)
            group_info = tds[4].get_text(strip=True)
            
            match_data.append({
                "players": players,
                "score": score,
                "winner": winner,
                "group_info": group_info
            })
    
    return match_data

def print_match_data(match_data):
    """Prints match data in a readable format."""
    for data in match_data:
        print(f"比赛: {data['players']}, 比分: {data['score']}, 胜者: {data['winner']}, 信息: {data['group_info']}")

def main():
    main_soup = get_soup(MATCH_URL)
    match_links = extract_match_links(main_soup)

    for match_url in match_links:
        print(f"Getting match details from {match_url}")
        match_soup = get_soup(match_url)
        match_data = extract_match_data(match_soup)
        print_match_data(match_data)

if __name__ == "__main__":
    main()
