import requests
import json
from bs4 import BeautifulSoup

class DuolingoScraper:
    def __init__(self, username: str):
        self.username = username

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        }

        if not self.__check_if_valid_user__():
            raise ConnectionAbortedError("No user with that name found.")
        if not self.__get_user_information__():
            raise ConnectionAbortedError("Some kind of error idk")
    
    def __check_if_valid_user__(self) -> bool:
        url = f"https://www.duolingo.com/profile/{self.username}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            og_image = soup.find("meta", property="og:image")
            if og_image:
                self.user_id = og_image["content"].replace("https://simg-ssl.duolingo.com/ssr-avatars/","").split("/")[0]
                return True
            else:
                return False
        else:
            return False
    
    def __get_user_information__(self):
        url = f"https://www.duolingo.com/2017-06-30/users/{self.user_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            self.user_data = response.json()
            with open(f'./data/duoUsers/{self.username}.json', 'w') as json_file:
                json.dump(self.user_data, json_file, indent=4)
            return True
        else:
            return False
