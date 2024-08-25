import altair as alt
import pandas as pd
import streamlit as st

from tennis123.analysis import calculate_match_win_rate, sort_matches_by_start_time
from tennis123.scrape.match import get_matches

st.title("Tennis Match Outcomes")

player_name = st.text_input("Enter player name:", "xffxff")
matches = get_matches(player_name)

# Sort matches by start time
matches = sort_matches_by_start_time(matches)

if player_name:
    match_win_rate, total_matches = calculate_match_win_rate(
        player_name, matches, return_total=True
    )

    st.text(
        f"Match win rate for {player_name} is {match_win_rate:.2f}% over {total_matches} matches."
    )

    outcomes = {"Match Number": list(range(1, len(matches) + 1)), "Outcome": []}
    for match in matches:
        if match.winner == player_name:
            outcomes["Outcome"].append(1)
        else:
            outcomes["Outcome"].append(0)

    # Convert the outcomes dictionary to a DataFrame for Streamlit charts
    df_outcomes = pd.DataFrame(outcomes)

    # Allow users to configure the window size
    window_size = st.number_input(
        "Choose window size for moving average of win rate:", min_value=1, value=10
    )

    df_outcomes["Win Rate Moving Average"] = (
        df_outcomes["Outcome"].rolling(window=window_size).mean()
    )

    # Add a column to distinguish between points and moving average
    df_outcomes["Type"] = "Outcome"
    df_moving_avg = df_outcomes.copy()
    df_moving_avg["Type"] = "Win Rate Moving Average"

    # Concatenate the two dataframes
    df_combined = pd.concat([df_outcomes, df_moving_avg])

    # Scatter plot for outcomes
    scatter_chart = (
        alt.Chart(df_combined[df_combined["Type"] == "Outcome"])
        .mark_circle(size=60)
        .encode(
            x="Match Number",
            y="Outcome",
            color=alt.value("blue"),  # Specific color for outcome points
            shape=alt.ShapeValue("circle"),  # Specific shape for outcome points
        )
    )

    # Line chart for moving average
    line_chart = (
        alt.Chart(df_combined[df_combined["Type"] == "Win Rate Moving Average"])
        .mark_line(color="orange")
        .encode(
            x="Match Number",
            y="Win Rate Moving Average",
            color=alt.value("orange"),  # Specific color for moving average line
        )
    )

    # Combine the scatter and line chart
    combined_chart = alt.layer(scatter_chart, line_chart).properties(
        title=f"Outcomes and {window_size}-Match Moving Average of Win Rate"
    )

    # Display the combined chart
    st.altair_chart(combined_chart, use_container_width=True)
