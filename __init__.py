"""
the file is meant for prior import, initialization and easier fetch of data
"""

import ephem
import wikipedia

"""
ephem_bodies_list gets and stores objects from the ephem library, 
that allow real-time astronomy data computation
"""

ephem_bodies_list = [ephem.Sun(), ephem.Moon(),
                     ephem.Mercury(), ephem.Venus(),
                     "placeholder", ephem.Mars(),
                     ephem.Jupiter(), ephem.Saturn(),
                     ephem.Uranus(), ephem.Neptune()]

"""
wiki_queries_dict executes several queries to wikipedia in order to 
get necessary info for all the bodies prior to the app's launch
"""

wikipedia.set_lang("ru")
wiki_queries_dict = {
    'soleil': wikipedia.summary("Солнце (астр.)"),
    'lune': wikipedia.summary("Луна (спутник)"),
    'mercure': wikipedia.summary("Меркурий (планета)"),
    'venus': wikipedia.summary("Венера (планета)"),
    'terre': wikipedia.summary("Земля (планета)"),
    'mars': wikipedia.summary("Марс (планета)"),
    'jupiter': wikipedia.summary("Юпитер (планета)"),
    'saturne': wikipedia.summary("Сатурн (планета)"),
    'uranus': wikipedia.summary("Уран (планета)"),
    'neptune': wikipedia.summary("Нептун (планета)"),
}
