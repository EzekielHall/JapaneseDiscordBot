'''
Utility script to extract the .mp3 files from the anki deck
Creates a directory called 'media' with all the mp3 a JSON file which maps each anki card by ID to its associated sound file(s)
'''
import json, os, sqlite3, re, zipfile

apkg_file_path = "./Japanese_Core_2000_2k_-_Sorted_w_Audio.apkg"

# Unzip .apkg file as a .zip file
with zipfile.ZipFile(apkg_file_path, 'r') as zip_archive:
    zip_archive.extractall("./media")

# Query 'collection.anki2' sqlite database to find mapping between audio file name and the Core 2k ID
sqlite_db_path = "./media/collection.anki2"

# returns a list of tuples where:
#   tuple[1] = Core 2k Index (starting at 1)
#   tuple[0] = anki card contents
rows = sqlite3.connect(sqlite_db_path).execute("SELECT flds, sfld FROM notes").fetchall()

# Write mapping to JSON file
id_to_mp3_files_mapping = {row[1] - 1: re.findall(r"(?<=sound:)\w+\.mp3", row[0]) for row in rows}
with open("./media/mapping.json", 'w') as json_file:
    json.dump(id_to_mp3_files_mapping, json_file, indent=4)

# Rename audio files according to JSON data contained in 'media' file
with open("./media/media", 'r') as json_file:
    media_file_mapping = json.load(json_file)
    for file_name_in_archive, mp3_file_name in media_file_mapping.items():
        os.rename(f"./media/{file_name_in_archive}", f"./media/{mp3_file_name}")

# Clean up unnecessary files
for file_name in os.listdir("./media"):
    if not file_name.endswith(".mp3") and not file_name.endswith(".json"):
        os.unlink(f"./media/{file_name}")
