from googletrans import Translator


def name_translator(word):
    translator = Translator()
    word = translator.translate(word, dest="ru").text
    return word
