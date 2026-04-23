import pandas as pd

results_files = [
    "data/raw/results_2016_2018.csv",
    "data/raw/results_2019_2021.csv",
    "data/raw/results_2022_2023.csv",
    "data/raw/results_2024_2025.csv",
    "data/raw/results_2026_2026.csv",
]

qualifying_files = [
    "data/raw/qualifying_2016_2018.csv",
    "data/raw/qualifying_2019_2021.csv",
    "data/raw/qualifying_2022_2023.csv",
    "data/raw/qualifying_2024_2025.csv",
    "data/raw/qualifying_2026_2026.csv",
]

results_df = pd.concat([pd.read_csv(f) for f in results_files], ignore_index=True)
qualifying_df = pd.concat([pd.read_csv(f) for f in qualifying_files], ignore_index=True)

results_df = results_df.drop_duplicates()
qualifying_df = qualifying_df.drop_duplicates()

results_df.to_csv("data/raw/results_2016_2026.csv", index=False)
qualifying_df.to_csv("data/raw/qualifying_2016_2026.csv", index=False)

print("Created: data/raw/results_2016_2026.csv", results_df.shape)
print("Created: data/raw/qualifying_2016_2026.csv", qualifying_df.shape)

print("\nResults rounds by season:")
print(results_df.groupby("season")["round"].nunique().sort_index())

print("\nQualifying rounds by season:")
print(qualifying_df.groupby("season")["round"].nunique().sort_index())