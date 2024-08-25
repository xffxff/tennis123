from enum import Enum


class MatchType(Enum):
    GROUP_STAGE = 1
    QUARTER_FINAL = 2
    SEMI_FINAL = 3
    FINAL = 4


class Match:
    def __init__(self, players, score, winner, match_type, start_time):
        self.players = players
        self.score = score
        self.winner = winner
        self.match_type = match_type
        self.start_time = start_time

    def __str__(self):
        return f"match: {self.players}, score: {self.score}, winner: {self.winner}, match type: {self.match_type}, start time: {self.start_time}"
