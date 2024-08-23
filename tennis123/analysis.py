import re
from tennis123.data import Tournament

def count_game_wins_and_losses(tournament: Tournament, player_name):
    wins = 0
    losses = 0

    for match in tournament.matches:
        if player_name in match.players:
            player1, player2 = match.players.split(' VS ')
            # Use regex to remove any parentheses and content within them
            cleaned_score = re.sub(r'\(.*?\)', '', match.score)
            
            # Split the score by '-'
            scores = cleaned_score.split('-')

            if player_name == player1:
                scores = cleaned_score.split('-')
                wins += int(scores[0])  # Wins by player1
                losses += int(scores[1])  # Losses by player1
            elif player_name == player2:
                scores = cleaned_score.split('-')
                wins += int(scores[1])  # Wins by player2
                losses += int(scores[0])
    return wins, losses

def count_match_wins_and_losses(tournament: Tournament, player_name):
    wins = 0
    losses = 0

    for match in tournament.matches:
        if player_name in match.players:
            if match.winner == player_name:
                wins += 1
            else:
                losses += 1
    return wins, losses

def calculate_match_win_rate(player_name, tournament):
    wins, losses = count_match_wins_and_losses(tournament, player_name)
    if wins + losses == 0:
        return 0
    return wins / (wins + losses) * 100

def calculate_game_win_rate(player_name, tournament):
    wins, losses = count_game_wins_and_losses(tournament, player_name)
    if wins + losses == 0:
        return 0
    return wins / (wins + losses) * 100