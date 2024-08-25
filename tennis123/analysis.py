import re
from typing import List

from tennis123.data import Match


def count_game_wins_and_losses(matches: List[Match], player_name):
    wins = 0
    losses = 0

    for match in matches:
        if player_name in match.players:
            player1, player2 = match.players.split(" VS ")
            # Use regex to remove any parentheses and content within them
            cleaned_score = re.sub(r"\(.*?\)", "", match.score)

            # Split the score by '-'
            scores = cleaned_score.split("-")

            if player_name == player1:
                scores = cleaned_score.split("-")
                wins += int(scores[0])  # Wins by player1
                losses += int(scores[1])  # Losses by player1
            elif player_name == player2:
                scores = cleaned_score.split("-")
                wins += int(scores[1])  # Wins by player2
                losses += int(scores[0])
    return wins, losses


def count_match_wins_and_losses(matches: List[Match], player_name):
    wins = 0
    losses = 0

    for match in matches:
        if player_name in match.players:
            if match.winner == player_name:
                wins += 1
            else:
                losses += 1
    return wins, losses


def _win_rate(wins, losses):
    if wins + losses == 0:
        return 0
    return wins / (wins + losses) * 100


def sort_matches_by_start_time(matches, reverse=False):
    return sorted(
        matches,
        key=lambda match: (match.start_time, match.match_type.value),
        reverse=reverse,
    )


def calculate_match_win_rate(
    player_name, matches: List[Match], last_n_matches=None, return_total=False
):
    matches = sort_matches_by_start_time(matches)

    if last_n_matches:
        matches = matches[-last_n_matches:]

    wins, losses = count_match_wins_and_losses(matches, player_name)
    if return_total:
        return _win_rate(wins, losses), wins + losses
    return _win_rate(wins, losses)


def calculate_game_win_rate(
    player_name, matches: List[Match], last_n_matches=None, return_total=False
):
    matches = sort_matches_by_start_time(matches)

    if last_n_matches:
        matches = matches[-last_n_matches:]

    wins, losses = count_game_wins_and_losses(matches, player_name)
    if return_total:
        return _win_rate(wins, losses), wins + losses
    return _win_rate(wins, losses)
