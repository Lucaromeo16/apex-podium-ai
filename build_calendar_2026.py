import os
import pandas as pd

os.makedirs("data/processed", exist_ok=True)

calendar_rows = [
    {"season": 2026, "round": 1, "race_name": "Australian Grand Prix", "circuit_id": "albert_park", "race_date": "2026-03-08", "race_status": "completed"},
    {"season": 2026, "round": 2, "race_name": "Chinese Grand Prix", "circuit_id": "shanghai", "race_date": "2026-03-15", "race_status": "completed"},
    {"season": 2026, "round": 3, "race_name": "Japanese Grand Prix", "circuit_id": "suzuka", "race_date": "2026-03-29", "race_status": "completed"},
    {"season": 2026, "round": 4, "race_name": "Miami Grand Prix", "circuit_id": "miami", "race_date": "2026-05-03", "race_status": "upcoming"},
    {"season": 2026, "round": 5, "race_name": "Canadian Grand Prix", "circuit_id": "villeneuve", "race_date": "2026-05-24", "race_status": "upcoming"},
    {"season": 2026, "round": 6, "race_name": "Monaco Grand Prix", "circuit_id": "monaco", "race_date": "2026-06-07", "race_status": "upcoming"},
    {"season": 2026, "round": 7, "race_name": "Spanish Grand Prix", "circuit_id": "catalunya", "race_date": "2026-06-14", "race_status": "upcoming"},
    {"season": 2026, "round": 8, "race_name": "Austrian Grand Prix", "circuit_id": "red_bull_ring", "race_date": "2026-06-28", "race_status": "upcoming"},
    {"season": 2026, "round": 9, "race_name": "British Grand Prix", "circuit_id": "silverstone", "race_date": "2026-07-05", "race_status": "upcoming"},
    {"season": 2026, "round": 10, "race_name": "Belgian Grand Prix", "circuit_id": "spa", "race_date": "2026-07-19", "race_status": "upcoming"},
    {"season": 2026, "round": 11, "race_name": "Hungarian Grand Prix", "circuit_id": "hungaroring", "race_date": "2026-07-26", "race_status": "upcoming"},
    {"season": 2026, "round": 12, "race_name": "Dutch Grand Prix", "circuit_id": "zandvoort", "race_date": "2026-08-23", "race_status": "upcoming"},
    {"season": 2026, "round": 13, "race_name": "Italian Grand Prix", "circuit_id": "monza", "race_date": "2026-09-06", "race_status": "upcoming"},
    {"season": 2026, "round": 14, "race_name": "Madrid Grand Prix", "circuit_id": "madrid", "race_date": "2026-09-13", "race_status": "upcoming"},
    {"season": 2026, "round": 15, "race_name": "Azerbaijan Grand Prix", "circuit_id": "baku", "race_date": "2026-09-27", "race_status": "upcoming"},
    {"season": 2026, "round": 16, "race_name": "Singapore Grand Prix", "circuit_id": "marina_bay", "race_date": "2026-10-11", "race_status": "upcoming"},
    {"season": 2026, "round": 17, "race_name": "United States Grand Prix", "circuit_id": "americas", "race_date": "2026-10-25", "race_status": "upcoming"},
    {"season": 2026, "round": 18, "race_name": "Mexico City Grand Prix", "circuit_id": "rodriguez", "race_date": "2026-11-01", "race_status": "upcoming"},
    {"season": 2026, "round": 19, "race_name": "Sao Paulo Grand Prix", "circuit_id": "interlagos", "race_date": "2026-11-08", "race_status": "upcoming"},
    {"season": 2026, "round": 20, "race_name": "Las Vegas Grand Prix", "circuit_id": "las_vegas", "race_date": "2026-11-21", "race_status": "upcoming"},
    {"season": 2026, "round": 21, "race_name": "Qatar Grand Prix", "circuit_id": "losail", "race_date": "2026-11-29", "race_status": "upcoming"},
    {"season": 2026, "round": 22, "race_name": "Abu Dhabi Grand Prix", "circuit_id": "yas_marina", "race_date": "2026-12-06", "race_status": "upcoming"},
    {"season": 2026, "round": 98, "race_name": "Bahrain Grand Prix", "circuit_id": "bahrain", "race_date": "2026-04-12", "race_status": "canceled"},
    {"season": 2026, "round": 99, "race_name": "Saudi Arabian Grand Prix", "circuit_id": "jeddah", "race_date": "2026-04-19", "race_status": "canceled"},
]

calendar_df = pd.DataFrame(calendar_rows)
calendar_df["race_date"] = pd.to_datetime(calendar_df["race_date"])

calendar_df.to_csv("data/processed/calendar_2026.csv", index=False)

print("Created: data/processed/calendar_2026.csv")
print(calendar_df[["race_status"]].value_counts())
print(calendar_df.sort_values(["race_status", "round"]).head(30))