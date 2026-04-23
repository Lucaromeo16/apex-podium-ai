import pandas as pd

result_files = [
    "data/raw/results_2016_2018.csv",
    "data/raw/results_2019_2021.csv",
    "data/raw/results_2022_2023.csv",
    "data/raw/results_2024_2025.csv",
    "data/raw/results_2026_2026.csv",
]

quali_files = [
    "data/raw/qualifying_2016_2018.csv",
    "data/raw/qualifying_2019_2021.csv",
    "data/raw/qualifying_2022_2023.csv",
    "data/raw/qualifying_2024_2025.csv",
    "data/raw/qualifying_2026_2026.csv",
]

df_results = pd.concat([pd.read_csv(f) for f in result_files], ignore_index=True)
df_quali = pd.concat([pd.read_csv(f) for f in quali_files], ignore_index=True)

df_results = df_results.drop_duplicates()
df_quali = df_quali.drop_duplicates()

df_results.to_csv("data/raw/results_2016_2026.csv", index=False)
df_quali.to_csv("data/raw/qualifying_2016_2026.csv", index=False)

print("Combined results shape:", df_results.shape)
print("Combined qualifying shape:", df_quali.shape)

print("\nResults rounds by season:")
print(df_results.groupby("season")["round"].nunique().sort_index())

print("\nQualifying rounds by season:")
print(df_quali.groupby("season")["round"].nunique().sort_index())