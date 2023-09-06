import os
import pandas as pd

CURRENT_DIRECTORY = os.getcwd()
AWARDS_SUBPATH = "/assets/rcc_award_detail.csv"
FACULTY_SUBPATH = "/assets/rcc_faculty.csv"

awards_data = pd.read_csv(f"{CURRENT_DIRECTORY}{AWARDS_SUBPATH}")
faculty_data = pd.read_csv(f"{CURRENT_DIRECTORY}{FACULTY_SUBPATH}")

grouped_awards_data = (
    awards_data[["Award Title", "PI Name", "Awarded Total"]]
    .groupby(["Award Title", "PI Name"], as_index=False)["Awarded Total"]
    .sum()
)

grouped_awards_data[["last_name", "first_name"]] = grouped_awards_data[
    "PI Name"
].str.split(",", expand=True)

new_list = faculty_data.merge(
    grouped_awards_data[["Award Title", "Awarded Total", "first_name", "last_name"]],
    on=["first_name", "last_name"],
    how="outer",
)
print(new_list)
