from bs4 import BeautifulSoup
import logging
import json
import time
import requests
import re

BASE_URL = "https://en.wikipedia.org"
movieLinks = []
actorLinks = []
jsonData = {}
movieJsonData = []
actorJsonData = []
actors = set()
movies = set()
orderScrapedMovie = 1
orderScrapedActor = 1


def scrapeMoviesAndAssociatedActors():
    global orderScrapedMovie
    global actorLinks
    global movieLinks
    for movieLink in movieLinks:
        if (orderScrapedMovie) > 250:
            break
        response = requests.get(movieLink, timeout=5)
        soup = BeautifulSoup(response.content, "html.parser")
        movieData = soup.find("table", {"class": "infobox vevent"})
        if movieData == None:
            logging.error("Couldn't Parse Movie Data")
            continue
        if movieData.find("tbody").find("th", {"class": "summary"}) == None:
            logging.error("Couldn't Parse Movie Data")
            continue
        movieTitle = (
            movieData.find("tbody").find("th", {"class": "summary"}).text.strip()
        )
        if movieTitle in movies:
            continue
        movies.add(movieTitle)
        text = "Scraping Movie - " + movieTitle
        c1 = time.time()
        logging.info(text)
        movieGross = "Couldn't parse value"
        movieActorsHrefs = []
        relDate = "Couldn't parse value"
        movieGrossText = (
            soup.find("table", {"class": "infobox vevent"})
            .find("tbody")
            .find("th", text="Box office")
        )
        if movieGrossText != None:
            movieGrossText = movieGrossText.nextSibling.text
            if movieGrossText.find("[") > 0:
                movieGrossText = movieGrossText[0 : movieGrossText.find("[")]
                movieGrossText = movieGrossText.replace("\xa0", " ")
            firstIndexOfNum = re.search("\d", movieGrossText)
            if firstIndexOfNum:
                firstIndexOfNum = firstIndexOfNum.start()
            if "million" in movieGrossText:
                movieGross = (
                    float(
                        movieGrossText[
                            firstIndexOfNum : movieGrossText.index("million")
                        ].replace(",", "")
                    )
                    * 1000000
                )
            elif "billion" in movieGrossText:
                movieGross = (
                    float(
                        movieGrossText[
                            firstIndexOfNum : movieGrossText.index("billion")
                        ].replace(",", "")
                    )
                    * 1000000000
                )
            else:
                movieGrossText = movieGrossText.split(" ", 1)[0]
                movieGross = float(movieGrossText[firstIndexOfNum:].replace(",", ""))
        print(movieGross)
        starring = (
            soup.find("table", {"class": "infobox vevent"})
            .find("tbody")
            .find("th", text="Starring")
        )
        if starring != None:
            movieActorsHrefs = starring.nextSibling.find_all("a")
        releaseDateTableHeader = (
            soup.find("table", {"class": "infobox vevent"})
            .find("tbody")
            .find("th", text="Release date")
        )
        if releaseDateTableHeader != None:
            releaseDateText = releaseDateTableHeader.nextSibling
            if releaseDateText.find("span", {"class": "bday"}) != None:
                relDate = releaseDateText.find("span", {"class": "bday"}).text[0:4]
            else:
                relDate = releaseDateText.text[-4:].strip()
        movieActors = [actor.get("title") for actor in movieActorsHrefs]
        movieActorLinks = [BASE_URL + actor.get("href") for actor in movieActorsHrefs]
        if (
            movieGross == "Couldn't parse value"
            or relDate == "Couldn't parse value"
            or len(movieActors) == 0
        ):
            continue

        movieData = {
            "Name": movieTitle,
            "Order Scraped": orderScrapedMovie,
            "URL": movieLink,
            "Year Released": relDate,
            "Grossed": movieGross,
            "Starring": movieActors,
        }
        movieJsonData.append(movieData)
        c2 = time.time()
        diff = c2 - c1
        duration = f"Scraping for {movieTitle} took " + str(diff) + "s"
        # logging.info(duration)
        orderScrapedMovie += 1
        if len(actorLinks) < 150:
            actorLinks += movieActorLinks
    movieLinks.clear()


def scrapeActors():
    global orderScrapedActor
    global actorLinks
    global movieLinks
    for actorLink in actorLinks:
        if (orderScrapedActor) > 250:
            break
        response = requests.get(actorLink, timeout=5)
        soup = BeautifulSoup(response.content, "html.parser")
        actorData = soup.find("table", {"class": "infobox biography vcard"})
        if actorData == None:
            logging.error("Couldn't parse data for an actor")
            continue
        actorData = actorData.find("tbody")
        actorName = actorData.find("div", {"class": "fn"}).text.strip()
        if actorName in actors:
            continue
        actors.add(actorName)
        text = "Scraping Actor - " + actorName
        logging.info(text)
        ageSpan = actorData.find("th", text="Born").nextSibling.find(
            "span", {"class": "noprint ForceAgeToShow"}
        )
        deathSpan = actorData.find("th", text="Died")
        age = 0
        if ageSpan != None:
            age = ageSpan.text[-3:-1]
        elif deathSpan != None:
            age = deathSpan.nextSibling.text
            ageLoc = age.find("aged")
            age = age[ageLoc + 4 : ageLoc + 7].strip()
        if age == 0:
            logging.error("Couldn't parse data for an actor")
            continue
        actorData = {"Name": actorName, "Age": age, "Order Scraped": orderScrapedActor}
        orderScrapedActor += 1
        actorJsonData.append(actorData)
        if len(movieLinks) >= 250:
            continue
        titleFind = actorName + " " + "filmography"
        filmographyPageExists = soup.find("a", {"title": titleFind})
        films = []
        if filmographyPageExists != None:
            filmsUrl = filmographyPageExists.get("href")
            filmsPageResponse = requests.get(BASE_URL + filmsUrl, timeout=5)
            filmsSoup = BeautifulSoup(filmsPageResponse.content, "html.parser")
            filmsTable = filmsSoup.find_all("table")[0].find("tbody")
            rows = filmsTable.find_all("tr")
            for row in rows:
                if row.find("a") != None:
                    films.append(BASE_URL + row.find("a").get("href"))
        movieLinks += films
    actorLinks.clear()


# if __name__ == '__main__':
#     # Set Logger
#     logging.getLogger().setLevel(logging.INFO)
#     logging.info("Getting films from Morgan Freemans Filmography")
#     # Start from Morgan Freeman's Page and get movies
#     startingLink = "https://en.wikipedia.org/wiki/Morgan_Freeman"
#     response = requests.get(startingLink, timeout=5)
#     initialMovieParse = BeautifulSoup(response.content, 'html.parser')
#     initialFilms = initialMovieParse.find("div", {"class" : "div-col columns column-width"}).find_all("a")
#     for film in initialFilms:
#         movieLinks.append(BASE_URL + film.get("href"))
#     # Keep scraping until we hit a minimum
#     while orderScrapedMovie < 250:
#         scrapeMoviesAndAssociatedActors()
#         scrapeActors()
#     logging.info("Scraping Done - Saving to output")
#     jsonData["Actors"] = actorJsonData
#     jsonData["Movies"] = movieJsonData
#     with open('json.txt', 'w') as outfile:
#         json.dump(jsonData, outfile)
