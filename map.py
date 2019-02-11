#!/usr/bin/python
# -*- coding: utf-8 -*-
import folium
from tqdm import tqdm
import doctest
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


def dict_maker(film, dic, year, user_year, location):
    """
    Forms a dictionary with use of given data
    (str, str, int, int, str) -> dict
    >>> dict1 = {}
    >>> dict_maker("Alo-alo", dict1, 1900, 1900, "Montenegro")
    {'Alo-alo': 'Montenegro'}
    """

    if film not in dic:
        if year == user_year:
            dic[film] = location
    return dic


def read_file(path):
    """
    Reads information from file and returns three
    dictionaries with name of the film and location where the film was shot
    in every dictionary: with the year that user inputed, ten years before
    user's year and tweny years ago before the user's year.
    () -> tuple(dict, dict, dict)
    """

    file = open(path, 'r', errors='ignore', encoding='utf-8')
    data = file.readlines()[14:]
    dict1 = {}
    dict2 = {}

    # for films made 10 years ago

    dict3 = {}

    # for films made 20 years ago

    for el in data:
        if el.strip().endswith(')'):
            el = el.strip().split('\t')[:-1]
        else:
            el = el.strip().split('\t')
        location = ','.join(el[-1].split(',')[-3:])

        try:
            index1 = el[0].index(')')
            index2 = el[0].index('(')
            film = (el[0])[:index2]
            year = int((el[0])[index2 + 1:index1])
            user_year10 = user_year - 10
            user_year20 = user_year - 20
        except:
            pass

        dict_maker(film, dict1, year, user_year, location)
        dict_maker(film, dict2, year, user_year10, location)
        dict_maker(film, dict3, year, user_year20, location)

    return (dict1, dict2, dict3)


def coordinates(dict_tuple):
    """
    Writes the html file with the map
    (dict, dict, dict) -> None
    """

    dict1 = dict_tuple[0]
    dict2 = dict_tuple[1]
    dict3 = dict_tuple[2]
    (num_films1, num_films2, num_films3) = (len(dict1), len(dict2),
            len(dict3))

    # counting numbers of films in each year

    map = folium.Map()

    # creates map

    geolocator = Nominatim(user_agent='todo', timeout=6)
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    fg_films1 = \
        folium.FeatureGroup(name='Films shot in year {}, summary: {}'.format(str(user_year),
                            num_films1))
    fg_films2 = \
        folium.FeatureGroup(name='Films shot in year {}, summary: {}'.format(str(user_year
                            - 10), num_films2))
    fg_films3 = \
        folium.FeatureGroup(name='Films shot in year {}, summary: {}'.format(str(user_year
                            - 20), num_films3))

    for (film, loc) in tqdm(dict1.items()):
        try:
            location = geolocator.geocode(loc)
            mark = [location.latitude, location.longitude]
            fg_films1.add_child(folium.Marker(location=mark, popup=film
                                + ', location: ' + loc,
                                icon=folium.Icon(color='red',
                                icon='cloud')))
        except:
            print('This location no longer exist or\
 is written not in a right way')
            print(loc)

    for (film, loc) in tqdm(dict2.items()):
        try:
            location = geolocator.geocode(loc)
            mark = [location.latitude, location.longitude]
            fg_films2.add_child(folium.Marker(location=mark, popup=film
                                + ', location: ' + loc,
                                icon=folium.Icon(color='blue',
                                icon='cloud')))
        except:
            print('This location no longer exist or\
 is written not in a right way')
            print(loc)

    for (film, loc) in tqdm(dict3.items()):
        try:
            location = geolocator.geocode(loc)
            mark = [location.latitude, location.longitude]
            fg_films3.add_child(folium.Marker(location=mark, popup=film
                                + ', location: ' + loc,
                                icon=folium.Icon(color='black',
                                icon='cloud')))
        except:
            print('This location no longer exist or\
 is written not in a right way')
            print(loc)

    fg_area = folium.FeatureGroup(name='Area')
    fg_area.add_child(folium.GeoJson(data=open('world.json', 'r',
                      encoding='utf-8-sig').read(),
                      style_function=lambda x: {'fillColor': ('yellow'
                       if x['properties']['AREA'] < 50000 else ('green'
                       if 100000 <= x['properties']['AREA']
                      < 150000 else ('orange' if 150000
                      <= x['properties']['AREA'] < 200000 else 'red'
                      )))}))

    map.add_child(fg_films1)
    map.add_child(fg_films2)
    map.add_child(fg_films3)
    map.add_child(fg_area)
    map.add_child(folium.LayerControl())
    map.save('Map_Todo2.html')


if __name__ == '__main__':
    doctest.testmod()
    user_year = \
        int(input("Please enter a year films of which\
 you want to see on the map, please note that old locations\
 can no longer exist and not appear on the map: "
            ))
    coordinates(read_file('locations.list'))
