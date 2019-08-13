from bs4 import BeautifulSoup
import requests
import csv
import re
from bom_scraper import file_util
import logging
import time

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def bom_download_html():
    current_url = (
        "http://www.boxofficemojo.com/movies/alphabetical.htm?letter=NUM&p=.html"
    )  # starting point for search, can be any letter
    movie_links = []  # initialize as an empty list

    response = requests.get(current_url)

    soup = BeautifulSoup(
        response.content
    )  # generate list of links for the letter indices
    letters = soup.findAll("a", href=re.compile("letter="))
    letter_index = []  # intialize as an empty list
    for t in letters:
        letter_index.append("http://www.boxofficemojo.com" + t["href"])

    for i in [1]:  # range(0,27): #loop through all letter indices for movies
        current_url = letter_index[i]
        response = requests.get(current_url)
        soup = BeautifulSoup(response.content)
        navbar = soup.find("div", "alpha-nav-holder")
        pages = navbar.findAll("a", href=re.compile("alphabetical"))
        page_list = []  # page_list is reset for each letter index

        for t in pages:
            page_list.append("http://www.boxofficemojo.com" + t["href"])

        movietable = soup.find("div", {"id": "main"})
        movies = movietable.findAll("a", href=re.compile("id="))
        for t in movies:
            movie_links.append("http://www.boxofficemojo.com" + t["href"])

        if pages != None:  # this only runs if there is a 2nd page for this letter
            i = 0  # page list starts at 2 (consequence of page layout)
            while i < len(page_list):  # loop over multiple pages for each letter index
                current_url = page_list[i]
                response = requests.get(current_url)
                soup = BeautifulSoup(response.content)
                movietable = soup.find("div", {"id": "main"})
                movies = movietable.findAll("a", href=re.compile("id="))
                for t in movies:
                    movie_links.append("http://www.boxofficemojo.com" + t["href"])
                i += 1

    for url in movie_links:
        response = requests.get(url)
        filename = url.split("=")[-1]
        with open(f"htm/{filename}", "wb") as fp:
            fp.write(response.content)
        time.sleep(10.0)


def main():
    bom_download_html()
