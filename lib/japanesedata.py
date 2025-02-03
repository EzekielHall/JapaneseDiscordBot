import csv

class JapaneseData:
    def __init__(self):
        self.words: Word = []
        self.grammar: Grammar = []
        self._core6000_dict = {}
        self._frequency_dict = {}
        self._grammar_dict = {}
        self._literature_dict = {}
        self.__load_core_6000__()
        self.__load_frequency__()
        self.__load_grammar__()
        self.__load_literature__()
        self.__create_word_bank__()
        # self.__create_frequency_bank__()
        self.__create_grammar_bank__()
        # self.__create_literature_bank__()

    def __load_core_6000__(self):
        with open("./data/japanese/core6000.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            headers = next(reader)
            for row in reader:
                key = row[0]
                self._core6000_dict[key] = {headers[i]: row[i] for i in range(1, len(headers))}
    
    def __load_frequency__(self):
        with open("./data/japanese/frequency.csv","r", encoding="utf-8") as file:
            reader = csv.reader(file)
            headers = next(reader)
            for row in reader:
                key = row[0]
                self._frequency_dict[key] = {headers[i]: row[i] for i in range(1, len(headers))}

    def __load_grammar__(self):
        with open("./data/japanese/grammar.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            headers = next(reader)
            for row in reader:
                key = row[0]
                self._grammar_dict[key] = {headers[i]: row[i] for i in range(1, len(headers))}

    def __load_literature__(self):
        with open("./data/japanese/literature.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            headers = next(reader)
            for row in reader:
                key = row[0]
                self._literature_dict[key] = {headers[i]: row[i] for i in range(1, len(headers))}

    def __create_word_bank__(self):
        word_dicts = [self._core6000_dict[i] for i in self._core6000_dict]
        for word in word_dicts:
            self.words.append(Word(word))
        self._core6000_dict.clear()
        
    def __create_grammar_bank__(self):
        grammar_dicts = [self._grammar_dict[i] for i in self._grammar_dict]
        for grammar in grammar_dicts:
            self.grammar.append(Grammar(grammar))
        self._grammar_dict.clear()

class Word:
    def __init__(self, data: dict):
        self._data = data
        self.word: str = ""
        self.kana: str = ""
        self.meaning: str = ""
        self.partOfSpeech: str = ""
        self.japaneseExample: str = ""
        self.englishExample: str = ""
        self.jishoLink: str = ""
        self.__create_properties__()
    
    def __create_properties__(self):
        self.word = self._data["Word"]
        self.kana = self._data["Kana"]
        self.meaning = self._data["Meaning"]
        self.partOfSpeech = self._data["Part of Speech"]
        self.japaneseExample = self._data["Example JP"]
        self.englishExample = self._data["Example EN"]
        self.jishoLink = self._data["Jisho Link"]

class Grammar:
    def __init__(self, data: dict):
        self._data = data
        self._parent_link = "https://core6000.neocities.org/dojg/"
        self.word: str = ""
        self.romaji: str = ""
        self.meaning: str = ""
        self.pageLink: str = ""
        self.explanation: str = ""
        self.exampleSentences: str = ""
        self.__create_properties__()
    
    def __create_properties__(self):
        self.word = self._data["Word"]
        self.romaji = "".join([i for i in self._data["Romaji"] if not i.isdigit()])
        self.meaning = self._data["Meaning"].replace(".", ". ")
        self.pageLink = self._parent_link + self._data["Page Link"]
        self._detailedInfo = eval(self._data["Detailed Info"])
        self.explanation = self._detailedInfo["Explanation"].replace("Spoiler English example sentences","").replace(".", ". ")
        self.exampleSentences = self._detailedInfo["Example Sentences"]         # Sentence struct: [("jp1","en1"),("jp2","en2")]
        self.imageNoteLink = self._detailedInfo["Image Notes"]
