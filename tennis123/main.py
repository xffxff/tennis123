import argparse

from tennis123 import analysis
from tennis123.scrape.match import get_matches

BASE_URL = "https://www.tennis123.net"


def main(player_name, last_n_matches):
    matches = get_matches(player_name)

    match_win_rate, total_matches = analysis.calculate_match_win_rate(
        player_name, matches, return_total=True
    )
    print(
        f"Match win rate for {player_name} is {match_win_rate:.2f}% over {total_matches} matches."
    )
    game_win_rate, total_games = analysis.calculate_game_win_rate(
        player_name, matches, return_total=True
    )
    print(
        f"Game win rate for {player_name} is {game_win_rate:.2f}% over {total_games} games."
    )

    if last_n_matches:
        last_n_match_win_rate = analysis.calculate_match_win_rate(
            player_name, matches, last_n_matches, return_total=False
        )
        print(
            f"Match win rate for {player_name} in the last {last_n_matches} matches is {last_n_match_win_rate:.2f}%."
        )

        last_n_match_game_win_rate, total_games = analysis.calculate_game_win_rate(
            player_name, matches, last_n_matches, return_total=True
        )
        print(
            f"Game win rate for {player_name} in the last {last_n_matches} matches is {last_n_match_game_win_rate:.2f}% over {total_games} games."
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tennis match analysis tool.")
    parser.add_argument(
        "player_name", type=str, help="The name of the player to analyze."
    )
    parser.add_argument(
        "--last-n-matches",
        default=None,
        type=int,
        help="The number of last matches to consider for analysis.",
    )
    args = parser.parse_args()
    main(args.player_name, args.last_n_matches)
