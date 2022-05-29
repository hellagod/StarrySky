"""
the file is meant for prior import, initialization and easier fetch of
objects from the ephem library, that allow real-time astronomy data computation
"""

import ephem

ephem_bodies_list = [ephem.Sun(), ephem.Moon(),
                     ephem.Mercury(), ephem.Venus(),
                     "placeholder", ephem.Mars(),
                     ephem.Jupiter(), ephem.Saturn(),
                     ephem.Uranus(), ephem.Neptune()]
