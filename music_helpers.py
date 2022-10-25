from urllib.request import urlopen
from unidecode import unidecode
from re import findall
from colorthief import ColorThief
from io import BytesIO
from nextcord import Color

class Music_helpers():

    def link(user_words):
        """Function returns YouTube url for first video id found in HTML code"""
        user_words = unidecode(user_words).replace(" ", "+")
        html = urlopen("https://www.youtube.com/results?search_query=" + str(user_words))
        video_ids = findall(r"watch\?v=(\S{11})", html.read().decode())
        return str("https://www.youtube.com/watch?v=" + str(video_ids[0]))
        
    def get_colour(id):
        """Function finds the most suitable embed colour from YouTube thumbnail"""
        url = f'https://img.youtube.com/vi/{id}/default.jpg'
        fd = urlopen(url)
        f = BytesIO(fd.read())
        color_thief = ColorThief(f)
        rgb = list(color_thief.get_palette(color_count=6))
        print(rgb)
        which_palette = int(len(rgb) / 2)
        colour = Color.from_rgb(rgb[which_palette][0], rgb[which_palette][1], rgb[which_palette][2])
        return colour

    def get_link_shorts(url):
        return str("https://www.youtube.com/watch?v=" + str(url[-11:]))