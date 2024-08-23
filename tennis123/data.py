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