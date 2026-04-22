import os
import time
import requests
import pandas as pd

os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def safe_get_json(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)

        if response.status_code != 200:
            print(f"Skipped URL (status {response.status_code}): {url}")
            return None

        if not response.text.strip():
            print(f"Skipped URL (empty response): {url}")
            return None

        try:
            return response.json()
        except Exception:
            print(f"Skipped URL (invalid JSON): {url}")
            print("First 200 chars of response:", response.text[:200])
            return None

    except Exception as e:
        print(f"Request failed for {url}: {e}")
        return None

# -----------------------------
# PULL RACE RESULTS
# -----------------------------
all_results = []

for year in range(2021, 2026):
    url = f"https://api.jolpi.ca/ergast/f1/{year}/results.json?limit=1000"
    data = safe_get_json(url)

    if data is None:
        continue

    races = data["MRData"]["RaceTable"]["Races"]

    for race in races:
        season = race["season"]
        round_num = race["round"]
        race_name = race["raceName"]
        circuit_id = race["Circuit"]["circuitId"]
        circuit_name = race["Circuit"]["circuitName"]
        race_date = race["date"]

        for result in race["Results"]:
            row = {
                "season": season,
                "round": round_num,
                "race_name": race_name,
                "circuit_id": circuit_id,
                "circuit_name": circuit_name,
                "race_date": race_date,
                "driver_id": result["Driver"]["driverId"],
                "driver_code": result["Driver"].get("code", ""),
                "given_name": result["Driver"]["givenName"],
                "family_name": result["Driver"]["familyName"],
                "constructor_id": result["Constructor"]["constructorId"],
                "constructor_name": result["Constructor"]["name"],
                "grid": result["grid"],
                "position": result.get("position", ""),
                "points": result["points"],
                "status": result["status"]
            }
            all_results.append(row)

results_df = pd.DataFrame(all_results)
results_df.to_csv("data/raw/results_2021_2025.csv", index=False)

print("Created: data/raw/results_2021_2025.csv")
print(results_df.shape)

# -----------------------------
# PULL QUALIFYING RESULTS
# -----------------------------
all_qualifying = []

for year in range(2021, 2026):
    url = f"https://api.jolpi.ca/ergast/f1/{year}/qualifying.json?limit=1000"
    data = safe_get_json(url)

    if data is None:
        continue

    races = data["MRData"]["RaceTable"]["Races"]

    for race in races:
        season = race["season"]
        round_num = race["round"]
        race_name = race["raceName"]
        circuit_id = race["Circuit"]["circuitId"]
        circuit_name = race["Circuit"]["circuitName"]
        race_date = race["date"]

        for qual in race["QualifyingResults"]:
            row = {
                "season": season,
                "round": round_num,
                "race_name": race_name,
                "circuit_id": circuit_id,
                "circuit_name": circuit_name,
                "race_date": race_date,
                "driver_id": qual["Driver"]["driverId"],
                "driver_code": qual["Driver"].get("code", ""),
                "given_name": qual["Driver"]["givenName"],
                "family_name": qual["Driver"]["familyName"],
                "constructor_id": qual["Constructor"]["constructorId"],
                "constructor_name": qual["Constructor"]["name"],
                "qualifying_position": qual.get("position", ""),
                "q1": qual.get("Q1", ""),
                "q2": qual.get("Q2", ""),
                "q3": qual.get("Q3", "")
            }
            all_qualifying.append(row)

qualifying_df = pd.DataFrame(all_qualifying)
qualifying_df.to_csv("data/raw/qualifying_2021_2025.csv", index=False)

print("Created: data/raw/qualifying_2021_2025.csv")
print(qualifying_df.shape)

# -----------------------------
# PULL DRIVER STANDINGS
# -----------------------------
all_driver_standings = []

for year in range(2021, 2026):
    for round_num in range(1, 26):
        url = f"https://api.jolpi.ca/ergast/f1/{year}/{round_num}/driverStandings.json?limit=1000"
        data = safe_get_json(url)

        if data is None:
            time.sleep(0.25)
            continue

        standings_lists = data["MRData"]["StandingsTable"].get("StandingsLists", [])

        if not standings_lists:
            time.sleep(0.25)
            continue

        standings_round = standings_lists[0]["round"]

        for standing in standings_lists[0]["DriverStandings"]:
            constructors = standing.get("Constructors", [])
            constructor_id = constructors[0]["constructorId"] if constructors else ""
            constructor_name = constructors[0]["name"] if constructors else ""

            row = {
                "season": year,
                "round": standings_round,
                "driver_id": standing["Driver"]["driverId"],
                "driver_code": standing["Driver"].get("code", ""),
                "given_name": standing["Driver"]["givenName"],
                "family_name": standing["Driver"]["familyName"],
                "driver_standing_position": standing.get("position", ""),
                "driver_standing_points": standing.get("points", ""),
                "driver_standing_wins": standing.get("wins", ""),
                "constructor_id": constructor_id,
                "constructor_name": constructor_name
            }
            all_driver_standings.append(row)

        time.sleep(0.25)

driver_standings_df = pd.DataFrame(all_driver_standings)
driver_standings_df.to_csv("data/raw/driver_standings_2021_2025.csv", index=False)

print("Created: data/raw/driver_standings_2021_2025.csv")
print(driver_standings_df.shape)

# -----------------------------
# PULL CONSTRUCTOR STANDINGS
# -----------------------------
all_constructor_standings = []

for year in range(2021, 2026):
    for round_num in range(1, 26):
        url = f"https://api.jolpi.ca/ergast/f1/{year}/{round_num}/constructorStandings.json?limit=1000"
        data = safe_get_json(url)

        if data is None:
            time.sleep(0.25)
            continue

        standings_lists = data["MRData"]["StandingsTable"].get("StandingsLists", [])

        if not standings_lists:
            time.sleep(0.25)
            continue

        standings_round = standings_lists[0]["round"]

        for standing in standings_lists[0]["ConstructorStandings"]:
            row = {
                "season": year,
                "round": standings_round,
                "constructor_id": standing["Constructor"]["constructorId"],
                "constructor_name": standing["Constructor"]["name"],
                "constructor_standing_position": standing.get("position", ""),
                "constructor_standing_points": standing.get("points", ""),
                "constructor_standing_wins": standing.get("wins", "")
            }
            all_constructor_standings.append(row)

        time.sleep(0.25)

constructor_standings_df = pd.DataFrame(all_constructor_standings)
constructor_standings_df.to_csv("data/raw/constructor_standings_2021_2025.csv", index=False)

print("Created: data/raw/constructor_standings_2021_2025.csv")
print(constructor_standings_df.shape)