import csv

class JapaneseData:
    def __init__(self):
        self.core6000 = {}
        self.__load_core_6000__()

    def __load_core_6000__(self):
        with open("./data/japanese/core6000.csv", mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader)
            for row in reader:
                key = row[0]
                self.core6000[key] = {headers[i]: row[i] for i in range(1, len(headers))}

jp = JapaneseData()

print(jp.core6000[str(0)])