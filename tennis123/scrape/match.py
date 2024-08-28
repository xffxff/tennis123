import json
import os
from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup

from tennis123.data import Match, MatchType
from tennis123.scrape.user import get_user_id

BASE_URL = "https://www.tennis123.net"


def save_matches_to_file(matches: List[Match], filename):
    try:
        with open(filename, "w") as file:
            json_matches = [
                {
                    "players": match.players,
                    "score": match.score,
                    "winner": match.winner,
                    "match_type": match.match_type.value,
                    "start_time": match.start_time,
                }
                for match in matches
            ]
            json.dump(json_matches, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving matches to file: {e}")
        os.remove(filename)


def load_matches_from_file(filename):
    with open(filename, "r") as file:
        json_matches = json.load(file)
        matches = [
            Match(
                match["players"],
                match["score"],
                match["winner"],
                MatchType(match["match_type"]),
                match["start_time"],
            )
            for match in json_matches
        ]
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
    match_links = soup.find_all("a", class_="pull-right")
    return [f"{BASE_URL}{link.get('href')}" for link in match_links if link.get("href")]


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
    target_div = soup.select_one(".row:nth-child(3) .col-xs-6:nth-child(1)")
    if target_div:
        # Extract the text within the strong tag inside the target div
        start_time_element = target_div.find("strong")
        if start_time_element:
            time_str = start_time_element.get_text(strip=True)
            return convert_to_iso(time_str)
    return None


def _get_match_type(s) -> MatchType:
    if "小组赛" in s:
        return MatchType.GROUP_STAGE
    elif s == "1/4决赛":
        return MatchType.QUARTER_FINAL
    elif s == "半决赛":
        return MatchType.SEMI_FINAL
    elif s == "决赛":
        return MatchType.FINAL
    else:
        return None


def extract_match_data(soup, player_name):
    """Extracts match data from a match soup object."""
    start_time = extract_start_time(soup)

    rows = soup.find_all("tr", attrs={"data-objid": True})
    match_data = []

    for row in rows:
        tds = row.find_all("td")
        if len(tds) >= 5:
            players = tds[0].get_text(strip=True).replace("VS", " VS ")
            if player_name not in players:
                continue
            score = tds[1].get_text(strip=True)
            winner = tds[2].get_text(strip=True)
            match_type = _get_match_type(tds[4].get_text(strip=True))

            match_data.append(Match(players, score, winner, match_type, start_time))

    return match_data


def get_matches(player_name, level="30"):
    user_id = get_user_id(player_name)
    match_url = f"{BASE_URL}/member/match{user_id}_Singles_r{level}"

    cache_data_file = f"{player_name}_{level}_matches.json"
    if os.path.exists(cache_data_file):
        print("Loading matches from local file...")
        matches = load_matches_from_file(cache_data_file)
    else:
        print("Scraping matches from web...")
        main_soup = get_soup(match_url)
        match_links = extract_match_links(main_soup)

        matches = []
        for match_url in match_links:
            print(f"Getting match details from {match_url}")
            match_soup = get_soup(match_url)
            match_data = extract_match_data(match_soup, player_name)
            for match in match_data:
                matches.append(match)

        save_matches_to_file(matches, cache_data_file)
    return matches
