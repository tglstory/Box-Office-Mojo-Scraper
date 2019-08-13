from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv
import re
import bom_metadata
import logging
import time

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


current_url = (
    "http://www.boxofficemojo.com/movies/alphabetical.htm?letter=NUM&p=.html"
)  # starting point for search, can be any letter
movie_links = []  # initialize as an empty list


soup = BeautifulSoup(
    urlopen(current_url).read()
)  # generate list of links for the letter indices
letters = soup.findAll("a", href=re.compile("letter="))
letter_index = []  # intialize as an empty list
for t in letters:
    letter_index.append("http://www.boxofficemojo.com" + t["href"])

for i in [1]:  # range(0,27): #loop through all letter indices for movies
    current_url = letter_index[i]
    soup = BeautifulSoup(urlopen(current_url).read())
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
            soup = BeautifulSoup(urlopen(current_url).read())
            movietable = soup.find("div", {"id": "main"})
            movies = movietable.findAll("a", href=re.compile("id="))
            for t in movies:
                movie_links.append("http://www.boxofficemojo.com" + t["href"])
            i += 1


with open("movie_data.csv", "w") as f:
    fieldnames = (
        "title",
        "director1",
        "director2",
        "domestic",
        "distributor",
        "release",
        "genre",
        "genres",
        "franchises",
        "runtime",
        "rating",
        "budget",
        "actor1",
        "actor2",
        "actor3",
        "actor4",
        "actor5",
        "actor6",
        "producer1",
        "producer2",
        "producer3",
        "producer4",
        "producer5",
        "producer6",
        "writer1",
        "writer2",
        "composer1",
        "composer2",
        "domestic",
        "foreign",
        "worldwide",
        "limited_release_date",
        "wide_release_date",
        "limited_opening",
        "wide_opening",
        "widest_release",
        "close_date",
        "in_release",
    )  # can add foreign release dates/boxoffice, review data, award data, trope data from other sites eventually
    output = csv.writer(f, delimiter=",")
    output.writerow(fieldnames)

    for url in movie_links:
        if (
            "elizabeth" in url and "elizabethtown" not in url
        ):  # fixes an annoying encoding error in an inelagent way
            url = "http://www.boxofficemojo.com/movies/?id=elizabeth%A0.htm"
        if "simpleplan" in url:
            url = "http://www.boxofficemojo.com/movies/?id=simpleplan%A0.htm"
        logging.info(f"Now processing {url}")
        time.sleep(1.0)
        current_url = url
        directors = soup.findAll("a", href=re.compile("Director&id"))
        director_list = []
        for t in directors:
            director_list.append(t.encode_contents())
        for i in range(0, 2):
            if i >= len(director_list):
                director_list.append("N/A")  # fill rest of list
        director1 = director_list[0]
        director2 = director_list[1]

        writers = soup.findAll("a", href=re.compile("Writer&id"))
        writer_list = []
        for t in writers:
            writer_list.append(t.encode_contents())
        for i in range(0, 2):
            if i >= len(writer_list):
                writer_list.append("N/A")
        writer1 = writer_list[0]
        writer2 = writer_list[1]

        composers = soup.findAll("a", href=re.compile("Composer&id"))
        composer_list = []
        for t in composers:
            composer_list.append(t.encode_contents())
        for i in range(0, 2):
            if i >= len(composer_list):
                composer_list.append("N/A")
        composer1 = composer_list[0]
        composer2 = composer_list[1]

        actors = soup.findAll("a", href=re.compile("Actor&id"))
        actor_list = []
        for t in actors:
            actor_list.append(t.encode_contents())
        for i in range(0, 6):
            if i >= len(actor_list):
                actor_list.append("N/A")
        actor1 = actor_list[0]
        actor2 = actor_list[1]
        actor3 = actor_list[2]
        actor4 = actor_list[3]
        actor5 = actor_list[4]
        actor6 = actor_list[5]

        producers = soup.findAll("a", href=re.compile("Producer&id"))
        producer_list = []
        for t in producers:
            producer_list.append(t.encode_contents())
        for i in range(0, 6):
            if i >= len(producer_list):
                producer_list.append("N/A")
        producer1 = producer_list[0]
        producer2 = producer_list[1]
        producer3 = producer_list[2]
        producer4 = producer_list[3]
        producer5 = producer_list[4]
        producer6 = producer_list[5]

        soup = BeautifulSoup(urlopen(current_url).read())

        all_bs = soup.findAll("b")
        b_list = (
            []
        )  # lots of the information we want is in bold, and appears in the same order on each page
        for t in all_bs:
            if "Domestic Lifetime" not in str(
                t.encode_contents()
            ):  # want to ignore the lifetime box office
                b_list.append(str(t.encode_contents()))
        if len(b_list) >= 10:  # avoids bad entries with no box office data
            if (
                "$" in b_list[2] or "n/a" in b_list[9]
            ):  # avoid movies w/o box office data, or unadjustable box office data, if not caught above
                if "n/a" in b_list[9]:  # has a foreign release only, order is shifted
                    title = str(b_list[1])
                    domestic = "N/A"
                    if "N/A" not in b_list[2]:
                        distributor = str(b_list[2].split(">")[1].split("<")[0])
                    else:
                        distributor = str(b_list[2])
                    if (
                        len(b_list[3].split(">")) > 3
                    ):  # sometimes the release date is not in a hyperlink
                        release = str(b_list[3].split(">")[2].split("<")[0])
                    else:
                        release = str(b_list[3].split(">")[1].split("<")[0])
                    genre = str(b_list[4])
                    runtime = str(b_list[5])
                    rating = str(b_list[6])
                    budget = str(b_list[7])
                    worldwide = str(b_list[12])
                else:  # has a domestic release
                    title = str(b_list[1])
                    domestic = str(b_list[2])
                    if "n/a" not in b_list[3]:
                        distributor = str(b_list[3].split(">")[1].split("<")[0])
                    else:
                        distributor = str(b_list[3])
                    if (
                        len(b_list[4].split(">")) > 3
                    ):  # sometimes the release date is not in a hyperlink
                        release = str(b_list[4].split(">")[2].split("<")[0])
                    else:
                        release = str(b_list[4].split(">")[1].split("<")[0])
                    genre = str(b_list[5])
                    runtime = str(b_list[6])
                    rating = str(b_list[7])
                    budget = str(b_list[8])
                    if (
                        len(b_list) == 11 or "%" not in b_list[11]
                    ):  # this means it only has a domestic release
                        worldwide = "N/A"
                    else:
                        worldwide = str(b_list[13])
                franchises = ""
                genres = ""
                limited_release_date = ""
                wide_release_date = ""
                limited_opening = ""
                wide_opening = ""
                widest_release = ""
                close_date = ""
                in_release = ""
                domestic = ""
                foreign = ""
                worldwide = ""
                all_mp_box = soup.findAll("div", {"class": "mp_box"})
                for mp_box in all_mp_box:
                    descriptor = mp_box.find("div").text
                    if descriptor == "Genres":
                        genres_div = mp_box
                        genres = ",".join(
                            list(map(lambda x: x.text, genres_div.findAll("a")))
                        )
                    elif descriptor == "Franchises":
                        franchises_div = mp_box
                        franchises = ",".join(
                            list(map(lambda x: x.text, franchises_div.findAll("a")))
                        )
                    elif descriptor == "Total Lifetime Grosses":
                        domestic, foreign, worldwide = bom_metadata.process_grosses(
                            mp_box
                        )
                    elif descriptor == "Domestic Summary":
                        limited_release_date, wide_release_date, limited_opening, wide_opening, widest_release, close_date, in_release = bom_metadata.process_summary(
                            mp_box
                        )
            output.writerow(
                [
                    title,
                    director1,
                    director2,
                    domestic,
                    distributor,
                    release,
                    genre,
                    genres,
                    franchises,
                    runtime,
                    rating,
                    budget,
                    actor1,
                    actor2,
                    actor3,
                    actor4,
                    actor5,
                    actor6,
                    producer1,
                    producer2,
                    producer3,
                    producer4,
                    producer5,
                    producer6,
                    writer1,
                    writer2,
                    composer1,
                    composer2,
                    domestic,
                    foreign,
                    worldwide,
                    limited_release_date,
                    wide_release_date,
                    limited_opening,
                    wide_opening,
                    widest_release,
                    close_date,
                    in_release,
                ]
            )

print("Done writing file")
