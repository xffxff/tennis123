import altair as alt
import pandas as pd
import streamlit as st

from tennis123.analysis import (
    calculate_match_win_rate,
    count_game_wins_and_losses,
    filter_out_walkovers,
    sort_matches_by_start_time,
)
from tennis123.scrape.match import get_matches


def display_title():
    st.title("Tennis Match Outcomes")


def get_player_name():
    return st.text_input("Enter player name:", "xffxff")


def fetch_and_prepare_matches(player_name):
    matches = get_matches(player_name)
    matches = filter_out_walkovers(matches)
    return sort_matches_by_start_time(matches)


def calculate_statistics(player_name, matches):
    outcomes = {"Match Number": list(range(1, len(matches) + 1)), "Outcome": []}
    net_win_losses = {
        "Match Number": list(range(1, len(matches) + 1)),
        "Net Win-Loss": [],
    }

    for match in matches:
        outcomes["Outcome"].append(1 if match.winner == player_name else 0)
        game_wins, game_losses = count_game_wins_and_losses([match], player_name)
        net_win_losses["Net Win-Loss"].append(game_wins - game_losses)

    return pd.DataFrame(outcomes), pd.DataFrame(net_win_losses)


def configure_window_size():
    return st.number_input(
        "Choose window size for moving average of win rate:", min_value=1, value=10
    )


def prepare_outcomes_data(df_outcomes, window_size):
    df_outcomes["Win Rate Moving Average"] = (
        df_outcomes["Outcome"].rolling(window=window_size).mean()
    )
    df_outcomes["Type"] = "Outcome"
    df_moving_avg = df_outcomes.copy()
    df_moving_avg["Type"] = "Win Rate Moving Average"
    return pd.concat([df_outcomes, df_moving_avg])


def plot_combined_chart(df_combined, window_size):
    scatter_chart = (
        alt.Chart(df_combined[df_combined["Type"] == "Outcome"])
        .mark_circle(size=60)
        .encode(
            x="Match Number",
            y="Outcome",
            color=alt.value("blue"),
            shape=alt.ShapeValue("circle"),
        )
    )
    line_chart = (
        alt.Chart(df_combined[df_combined["Type"] == "Win Rate Moving Average"])
        .mark_line(color="orange")
        .encode(
            x="Match Number",
            y="Win Rate Moving Average",
            color=alt.value("orange"),
        )
    )
    combined_chart = alt.layer(scatter_chart, line_chart).properties(
        title=f"Outcomes and {window_size}-Match Moving Average of Win Rate"
    )
    st.altair_chart(combined_chart, use_container_width=True)


def plot_net_win_loss_chart(df_net_win_loss, window_size):
    net_win_loss_scatter_chart = (
        alt.Chart(df_net_win_loss)
        .mark_circle(size=60, color="green")
        .encode(x="Match Number", y="Net Win-Loss")
        .properties(title="Net Win-Loss for Each Match")
    )
    net_win_loss_line_chart = (
        alt.Chart(df_net_win_loss)
        .mark_line(color="red")
        .encode(x="Match Number", y="Net Win-Loss Moving Average")
    )
    net_win_loss_combined_chart = alt.layer(
        net_win_loss_scatter_chart, net_win_loss_line_chart
    ).properties(title=f"Net Win-Loss and {window_size}-Match Moving Average")
    st.altair_chart(net_win_loss_combined_chart, use_container_width=True)


def main():
    display_title()
    player_name = get_player_name()

    if player_name:
        matches = fetch_and_prepare_matches(player_name)
        df_outcomes, df_net_win_loss = calculate_statistics(player_name, matches)

        window_size = configure_window_size()
        df_combined = prepare_outcomes_data(df_outcomes, window_size)

        st.subheader("Match Win Rate")

        match_win_rate, total_matches = calculate_match_win_rate(
            player_name, matches, return_total=True
        )
        st.text(
            f"Match win rate for {player_name} is {match_win_rate:.2f}% over {total_matches} matches."
        )

        plot_combined_chart(df_combined, window_size)

        df_net_win_loss["Net Win-Loss Moving Average"] = (
            df_net_win_loss["Net Win-Loss"].rolling(window=window_size).mean()
        )

        st.subheader("Net Win-Loss")

        plot_net_win_loss_chart(df_net_win_loss, window_size)


if __name__ == "__main__":
    main()
