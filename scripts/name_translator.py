"""
Utility script, that helps to translate the celestial bodies' names from french
(hence the source database the data is acquired from is french) to russian
"""

from googletrans import Translator


def name_translator(word):
    translator = Translator()
    word = translator.translate(word, dest="ru").text
    return word
