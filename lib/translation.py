from googletrans import Translator as GTranslator


class CustomTranslator:
    def __init__(self):
        self.translator = GTranslator()

    def translateToEnglish(self, text: str) -> str:
        """
        param text: Input Jpanese sentence to translate.
        returns: Translated sentence in Englsih.
        """
        result = self.translator.translate(text, src="ja")
        return result.text

    def translateToJapanese(self, text: str) -> str:
        result = self.translator.translate(text, dest="ja", src="en")
        return result.text
    
    def translate(self, text: str) -> tuple[str, tuple[str, str]]:
        """
        param text: Input sentence to be auto-detected and translated.

        returns: Translated sentence in opposite language. None if input language isn't JA or EN.
        """
        lang = self.translator.detect(text).lang
        if lang == "en":
            translation = self.translateToJapanese(text)
        elif lang == "ja":
            translation = self.translateToEnglish(text)
        else:
            return None
        return translation, lang