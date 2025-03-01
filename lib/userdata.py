import json
import discord
import os

from lib.myLogging import log

class UserDataHandler:
    def __init__(self):
        self.filename = "./data/userdata.json" # ./data/ because the bot is ran from the root project dir
        self.fields = {
            "username": "",    # Stores the user's name
            "nickname": None,  # Stores a nickname if the user has one
            "translations": 0, # Stores amount of times they've translated
            "admin": False     # Stores if they have admin perms
        }

        self.data = self.__load_userdata__()
    
    def __load_userdata__(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                _data = json.load(file)
                log("Userdata successfully loaded.")
                return _data
        except (FileNotFoundError, json.JSONDecodeError) as e:
            if isinstance(e, FileNotFoundError):
                os.makedirs(os.path.dirname(self.filename), exist_ok=True)
                with open(self.filename, "w", encoding="utf-8") as file:
                    json.dump({}, file)
                log("No user data found. New data file created.")
                return {}
            elif isinstance(e, json.JSONDecodeError):
                log("Critical error reading user data.")
                with open(self.filename, "r") as file:
                    _data = file.read()
                    with open("./data/damagedData.json", "w", encoding="utf-8") as backup:
                        backup.write(_data)
                        backup.close()
                    file.close()
                return {}

    def _save_user_data(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)
            log("Dumped data to userdata.")
    
    def _ensure_user_exist(self, user: discord.User):
        if not str(user.id) in self.data:
            self.data[str(user.id)] = self.fields
    
    def incrementTranslationCount(self, user: discord.User):
        self._ensure_user_exist(user)

        self.data[str(user.id)]["translations"] += 1

        self._save_user_data()
        log(f"User {user.name} updated successfully.")
    
    def getUser(self, user: discord.user):
        self._ensure_user_exist(user)
        return self.data[str(user.id)]