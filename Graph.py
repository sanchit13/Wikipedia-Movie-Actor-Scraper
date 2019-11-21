import json


class ActorNode:
    def __init__(self, name, totalGross, age, movies):
        self.name = name
        self.age = age
        self.totalGross = totalGross
        self.movies = movies

    def toJson(self):
        data = {}
        data["name"] = self.name
        data["age"] = self.age
        data["total_gross"] = self.totalGross
        data["movies"] = self.movies
        return data

    def getActorName(self):
        return self.name

    def getAge(self):
        return self.age

    def getGross(self):
        return self.totalGross

    def getMovies(self):
        return self.movies

    def setAge(self, age):
        self.age = age

    def setGross(self, gross):
        self.totalGross = gross


class MovieNode:
    def __init__(self, name, wikiPage, boxOffice, year, actors):
        self.name = name
        self.wikiPage = wikiPage
        self.boxOffice = boxOffice
        self.year = year
        self.actors = actors

    def toJson(self):
        data = {}
        data["name"] = self.name
        data["wiki_page"] = self.wikiPage
        data["year"] = self.year
        data["box_office"] = self.boxOffice
        data["actors"] = self.actors
        return data

    def getActors(self):
        return self.actors

    def getBoxOffice(self):
        return self.boxOffice

    def getYear(self):
        return self.year

    def getMovieName(self):
        return self.name

    def getUrl(self):
        return self.wikiPage

    def setBoxOffice(self, gross):
        self.boxOffice = gross

    def setYear(self, year):
        self.year = year


class Edge:
    def __init__(self, actor, movie, weight):
        self.actor = actor
        self.movie = movie
        self.weight = weight

    def getMovieNode(self):
        return self.movie

    def getActorNode(self):
        return self.actor

    def getWeight(self):
        return self.weight


class Graph:
    def __init__(self, fileName):
        self.aNodes = {}
        self.mNodes = {}
        self.edges = {}
        with open(fileName, "r") as jsonFile:
            data = json.load(jsonFile)
            actors = data["Actors"]
            movies = data["Movies"]
        for actor in actors:
            self.aNodes[actor["name"]] = ActorNode(
                actor["name"], actor["total_gross"], actor["age"], actor["movies"]
            )
        for movie in movies:
            self.mNodes[movie["name"]] = MovieNode(
                movie["name"],
                movie["wiki_page"],
                movie["box_office"],
                movie["year"],
                movie["actors"],
            )
            sumOfAllActorsAges = 0
            if movie["actors"]:
                for actor in movie["actors"]:
                    if actor not in self.aNodes:
                        continue
                    aNode = self.aNodes[actor]
                    sumOfAllActorsAges += aNode.getAge()
                for actor in movie["actors"]:
                    if actor not in self.aNodes:
                        continue
                    aNode = self.aNodes[actor]
                    actorsAge = aNode.getAge()
                    weight = (actorsAge / sumOfAllActorsAges) * movie["box_office"]
                    edge = Edge(aNode, self.mNodes[movie["name"]], weight)
                    if aNode.getActorName() not in self.edges:
                        self.edges[aNode.getActorName()] = [edge]
                    else:
                        self.edges[aNode.getActorName()] = self.edges[
                            aNode.getActorName()
                        ] + [edge]

    def getMovieGross(self, movieName):
        mNode = self.mNodes[movieName]
        if mNode != None:
            return mNode.getBoxOffice()
        return "Movie doesn't exist in Graph"

    def getActorsInMovie(self, movieName):
        mNode = self.mNodes[movieName]
        if mNode != None:
            return mNode.getActors()
        return "Movie doesn't exist in Graph"

    def getMoviesForActor(self, actorName):
        aNode = self.aNodes[actorName]
        if aNode != None:
            return aNode.getMovies()

    def saveToJson(self):
        data = {}
        actors = []
        movies = []
        for actorName, aNode in self.aNodes.items():
            actors.append(aNode.toJson())
        for movieName, mNode in self.mNodes.items():
            movies.append(mNode.toJson())
        data["Actors"] = actors
        data["Movies"] = movies
        with open("data.json", "w") as output:
            json.dump(data, output)

    def getHighestWeightedActors(self):
        res = []
        for actorName, aNode in self.aNodes.items():
            if actorName not in self.edges:
                continue
            edges = self.edges[actorName]
            sum = 0
            for edge in edges:
                sum += edge.getWeight()
            res.append((actorName, sum))
        return sorted(res, key=lambda tup: tup[1], reverse=True)[0:10]

    def getMoviesFromYear(self, year):
        res = []
        for movieName, mNode in self.mNodes.items():
            if mNode.getYear() == year:
                res.append(movieName)
        return res

    def getActorsFromYear(self, year):
        res = []
        for actorName, aNode in self.aNodes.items():
            if aNode.getYear() == year:
                res.append(actorName)
        return res

    def getActors(self):
        res = []
        for actorName, aNode in self.aNodes.items():
            res.append(aNode.toJson())
        return res
        
    
    def getMovies(self):
        res = []
        for movieName, mNode in self.mNodes.items():
            res.append(mNode.toJson())
        return res


    def getNumActors(self):
        return len(self.aNodes.items())

    def getNumMovies(self):
        return len(self.mNodes.items())

    def getActor(self, actorName):
        if actorName in self.aNodes:
            return (self.aNodes[actorName]).toJson()
        return None

    def getMovie(self, movieName):
        if movieName in self.mNodes:
            return (self.mNodes[movieName]).toJson()
        return None

    def getMnode(self, movieName):
        if movieName in self.mNodes:
            return (self.mNodes[movieName])
        return None
        
    def createNewActor(self, name, age, totalGross, movies):
        if name in self.aNodes:
            return "Actor Already Exists"
        else:
            self.aNodes[name] = ActorNode(name, totalGross, age, movies)
            self.saveToJson()
            return "Actor Created"

    def createNewMovie(self, name, year, box_office, wiki_page, actors):
        if name in self.mNodes:
            return "Movie Already Exists"
        else:
            self.mNodes[name] = MovieNode(name, wiki_page, box_office, year, actors)
            self.saveToJson()
            return "Movie Created"

    def deleteMovieByName(self, movieName):
        if movieName in self.mNodes:
            del self.mNodes[movieName]
            self.saveToJson()
            return "Movie Deleted!"
        else:
            return "Movie not found!"

    def deleteActorByName(self, actorName):
        if actorName in self.aNodes:
            del self.aNodes[actorName]
            self.saveToJson()
            return "Actor Deleted!"
        else:
            return "Actor not found!"

    def updateActor(self, actorName, age, totalGross):
        if actorName in self.aNodes:
            aNode = self.aNodes[actorName]
            if age != None:
                aNode.setAge(age)
            if totalGross != None:
                aNode.setGross(totalGross)
            self.saveToJson()
            return "Successfully Updated!"
        else:
            return "Actor not Found!"

    def updateMovie(self, movieName, boxOffice, year):
        if movieName in self.mNodes:
            mNode = self.mNodes[movieName]
            if boxOffice != None:
                mNode.setBoxOffice(boxOffice)
            if year != None:
                mNode.setYear(year)
            self.saveToJson()
            return "Successfully Updated!"
        else:
            return "Movie not Found!"

    def getActorsByFilter(self, name, age, totalGross):
        res = []
        for actorName, aNode in self.aNodes.items():
            if actorName == name or str(aNode.getAge()) == str(age) or str(aNode.getGross()) == str(totalGross):
                res.append(aNode.toJson())
        return res
    
    def getMoviesByFilter(self, name, wikiPage, boxOffice, year):
        res = []
        for movieName, mNode in self.mNodes.items():
            if movieName == name or mNode.getUrl() == wikiPage or str(mNode.getBoxOffice()) == str(boxOffice) or str(mNode.getYear()) == str(year):
                res.append(mNode.toJson())
        return res