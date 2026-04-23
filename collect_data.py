import os
import sys
import time
import requests
import pandas as pd

os.makedirs("data/raw", exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

MAX_ROUNDS = 26
SLEEP_SECONDS = 1.2


def safe_get_json(url):
    max_retries = 5

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=20)

            if response.status_code == 200:
                if not response.text.strip():
                    return None
                return response.json()

            if response.status_code == 429:
                wait_time = 2 * attempt
                print(f"429 hit -> retrying in {wait_time}s: {url}")
                time.sleep(wait_time)
                continue

            print(f"Skipped URL ({response.status_code}): {url}")
            return None

        except Exception as e:
            print(f"Request failed: {url} -> {e}")
            time.sleep(2 * attempt)

    print(f"FAILED after retries: {url}")
    return None


def collect_results(start_year, end_year):
    all_results = []

    for year in range(start_year, end_year + 1):
        print(f"\nPulling results for {year}...")
        rounds_found = 0

        for round_num in range(1, MAX_ROUNDS + 1):
            url = f"https://api.jolpi.ca/ergast/f1/{year}/{round_num}/results.json"
            data = safe_get_json(url)
            time.sleep(SLEEP_SECONDS)

            if data is None:
                continue

            races = data.get("MRData", {}).get("RaceTable", {}).get("Races", [])
            if not races:
                continue

            rounds_found += 1

            for race in races:
                season = race["season"]
                rnd = race["round"]
                race_name = race["raceName"]
                circuit_id = race["Circuit"]["circuitId"]
                circuit_name = race["Circuit"]["circuitName"]
                race_date = race["date"]

                for result in race.get("Results", []):
                    all_results.append({
                        "season": season,
                        "round": rnd,
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
                        "grid": result.get("grid"),
                        "position": result.get("position"),
                        "points": result.get("points"),
                        "status": result.get("status"),
                    })

        print(f"Rounds found for {year}: {rounds_found}")

    results_df = pd.DataFrame(all_results)
    results_path = f"data/raw/results_{start_year}_{end_year}.csv"
    results_df.to_csv(results_path, index=False)

    print(f"\nCreated: {results_path}")
    print("Results shape:", results_df.shape)

    if not results_df.empty:
        print("\nUnique races per season (results):")
        print(results_df.groupby("season")["round"].nunique().sort_index())


def collect_qualifying(start_year, end_year):
    all_qualifying = []

    for year in range(start_year, end_year + 1):
        print(f"\nPulling qualifying for {year}...")
        rounds_found = 0

        for round_num in range(1, MAX_ROUNDS + 1):
            url = f"https://api.jolpi.ca/ergast/f1/{year}/{round_num}/qualifying.json"
            data = safe_get_json(url)
            time.sleep(SLEEP_SECONDS)

            if data is None:
                continue

            races = data.get("MRData", {}).get("RaceTable", {}).get("Races", [])
            if not races:
                continue

            rounds_found += 1

            for race in races:
                season = race["season"]
                rnd = race["round"]

                for qual in race.get("QualifyingResults", []):
                    all_qualifying.append({
                        "season": season,
                        "round": rnd,
                        "driver_id": qual["Driver"]["driverId"],
                        "qualifying_position": qual.get("position"),
                        "q1": qual.get("Q1", ""),
                        "q2": qual.get("Q2", ""),
                        "q3": qual.get("Q3", ""),
                    })

        print(f"Rounds found for {year}: {rounds_found}")

    qualifying_df = pd.DataFrame(all_qualifying)
    qualifying_path = f"data/raw/qualifying_{start_year}_{end_year}.csv"
    qualifying_df.to_csv(qualifying_path, index=False)

    print(f"\nCreated: {qualifying_path}")
    print("Qualifying shape:", qualifying_df.shape)

    if not qualifying_df.empty:
        print("\nUnique races per season (qualifying):")
        print(qualifying_df.groupby("season")["round"].nunique().sort_index())


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 collect_data.py <start_year> <end_year>")
        sys.exit(1)

    start_year = int(sys.argv[1])
    end_year = int(sys.argv[2])

    collect_results(start_year, end_year)
    collect_qualifying(start_year, end_year)