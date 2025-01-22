from googletrans import Translator as GTranslator


class CustomTranslator:
    def __init__(self):
        self.translator = GTranslator()

    def translateToEnglish(self, text: str) -> str:
        """
        param text: Input sentence to translate.
        returns: Translated sentence
        """
        result = self.translator.translate(text, src="ja")
        return result.text

    def translateToJapanese(self, text: str) -> str:
        result = self.translator.translate(text, dest="ja", src="en")
        return result.text
    
    def translate(self, text: str) -> tuple[str, tuple[str, str]]:
        # TODO: Have this auto-detect language and 
        lang = self.translator.detect(text).lang
        if lang == "en":
            translation = self.translateToJapanese(text)
        elif lang == "ja":
            translation = self.translateToEnglish(text)
        else:
            return None
        return translation, lang