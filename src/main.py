import os
import pandas as pd

CURRENT_DIRECTORY = os.getcwd()
AWARDS_SUBPATH = "/assets/rcc_award_detail.csv"
FACULTY_SUBPATH = "/assets/rcc_faculty.csv"

# Reading the CSV files.
awards_data = pd.read_csv(f"{CURRENT_DIRECTORY}{AWARDS_SUBPATH}")
faculty_data = pd.read_csv(f"{CURRENT_DIRECTORY}{FACULTY_SUBPATH}")

# Finding the sum of awarded total, group by the title and PI name.
grouped_awards_data = (
    awards_data[["Award Title", "PI Name", "Awarded Total"]]
    .groupby(["Award Title", "PI Name"], as_index=False)["Awarded Total"]
    .sum()
)

# Splitting the PI Name field into first and last name.
grouped_awards_data[["last_name", "first_name"]] = grouped_awards_data[
    "PI Name"
].str.split(",", expand=True)

# Merging the two CSV files.
merged_result = faculty_data.merge(
    grouped_awards_data[["Award Title", "Awarded Total", "first_name", "last_name"]],
    on=["first_name", "last_name"],
    # By using left outer join, all the faculty names will be there even if
    # there is no matching award details. Unmatched awards data is not kept.
    # To preserve that use "outer" join.
    how="left",
)

# Saving the results in a CSV file to view it easily.
merged_result.to_csv("result.csv", index=False)
# Sending to STDOUT.
print(merged_result)
