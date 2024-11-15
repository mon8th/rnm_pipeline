import pandas as pd
import requests
import json
import sqlite3


# Extracting Data from the API
def get_all_RnM_data():
    baseurl = "https://rickandmortyapi.com/api/"
    endpoints = ["character", "location", "episode"]
    all_data = {}
    for endpoint in endpoints:
        data_list = []
        page = 1  # Start w 1
        while True:
            response = requests.get(f"{baseurl}{endpoint}?page={page}")
            if response.status_code != 200:
                break
            response_data = response.json()
            data_list.extend(response_data["results"])
            if not response_data["info"]["next"]:
                break  # No more pages
            page += 1
        all_data[endpoint] = data_list
    return all_data


# Transforming Data
# Clean raw data
def clean_data(raw_data):
    cleaned_data = {"characters": [], "locations": [], "episodes": []}
    location_dict = {}
    episode_dict = {}

    # Locations
    for location in raw_data.get("location", []):
        location_id = location["id"]
        location_dict[location["url"]] = location_id
        cleaned_data["locations"].append(
            {
                "id": location_id,
                "name": location["name"],
                "type": location.get("type", "Unknown"),
                "dimension": location.get("dimension", "Unknown"),
                "residents": [r.split("/")[-1] for r in location.get("residents", [])],
            }
        )

    # Episodes
    for ep in raw_data.get("episode", []):
        episode_id = ep["id"]
        episode_dict[ep["url"]] = episode_id
        cleaned_data["episodes"].append(
            {
                "id": episode_id,
                "name": ep["name"],
                "air_date": ep["air_date"],
                "episode_code": ep["episode"],
                "characters": [c.split("/")[-1] for c in ep.get("characters", [])],
            }
        )

    # Characters
    for character in raw_data.get("character", []):
        cleaned_data["characters"].append(
            {
                "id": character["id"],
                "name": character["name"],
                "status": character.get("status", "Unknown"),
                "species": character.get("species", "Unknown"),
                "gender": character.get("gender", "Unknown"),
                "origin": {
                    "name": character["origin"]["name"],
                    "url": location_dict.get(character["origin"]["url"], None),
                },
                "location": {
                    "name": character["location"]["name"],
                    "url": location_dict.get(character["location"]["url"], None),
                },
                "image": character["image"],
                "episodes": [
                    episode_dict.get(e, None) for e in character.get("episode", [])
                ],
            }
        )

    return cleaned_data


# Combine data
def combine_data(cleaned_data):
    combined_data = []
    episodes_dict = {ep["id"]: ep for ep in cleaned_data["episodes"]}
    locations_dict = {loc["id"]: loc for loc in cleaned_data["locations"]}

    # Combine data
    for char in cleaned_data["characters"]:
        episodes = [episodes_dict.get(ep_id, {}) for ep_id in char["episodes"]]
        location = locations_dict.get(char["origin"]["url"], {})

        for ep in episodes:
            if ep:
                combined_data.append(
                    {
                        "character_id": char["id"],
                        "character_name": char["name"],
                        "character_status": char["status"],
                        "character_species": char["species"],
                        "episode_name": ep.get("name", "Unknown"),
                        "episode_code": ep.get("episode_code", "Unknown"),
                        "episode_air_date": ep.get("air_date", "Unknown"),
                        "dimension": location.get("dimension", "Unknown"),
                    }
                )

    return combined_data


# Loading to Sqlite
def insert_to_database(combined_data):
    conn = sqlite3.connect("files/rnm.db")
    c = conn.cursor()

    # Create the table if ot exists
    c.execute(
        """CREATE TABLE IF NOT EXISTS characters_episodes (
            character_id INTEGER,
            character_name TEXT,
            character_status TEXT, 
            character_species TEXT,
            episode_name TEXT,
            episode_code TEXT,
            episode_air_date TEXT,
            dimension TEXT
        )"""
    )
    print(f"Inserting {len(combined_data)} rows into the database...")

    for row in combined_data:
        c.execute(
            """INSERT INTO characters_episodes 
            (character_id, character_name, character_status, character_species, episode_name, episode_code, episode_air_date, dimension)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (row["character_id"], row["character_name"], row["character_status"], row["character_species"], 
             row["episode_name"], row["episode_code"], row["episode_air_date"], row["dimension"])
        )

    conn.commit()
    conn.close()

    
# Main Pipeline
raw_data = get_all_RnM_data()
with open("files/raw_data.json", "w") as file:
    json.dump(raw_data, file)

cleaned_data = clean_data(raw_data)
with open("files/cleaned_data.json", "w") as file:
    json.dump(cleaned_data, file)

combined_data = combine_data(cleaned_data)
df = pd.DataFrame(combined_data)
df.to_csv("files/combined_data.csv", index=False)

insert_to_database(combined_data)